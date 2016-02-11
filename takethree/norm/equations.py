from itertools import product
from .meta import UnifyError, Substitution, Meta, constructor, unify
from .ordering import Order, GroundedOrder
from .. import e
from .. import t
from .. import cache

class Condition:
    def __init__(self, predicates):
        # predicates are pairs [domain, allowed]
        def tuplify(obj):
            if isinstance(obj, list):
                return tuple(obj)
            if isinstance(obj, tuple):
                return obj
            else:
                return obj
        self.predicates = set((tuplify(d), tuplify(a)) for d, a in predicates)
    def ground_domain(self, sub):
        output = []
        try:
            domain, allowed = zip(*self.predicates)
        except ValueError:
            return self.predicates
        for symbol in domain:
            cons = sub.lookup(Meta(symbol))
            if cons:
                output.append(cons.value)
            else:
                output.append(symbol)
        return zip(output, allowed)
    def check(self, sub):
        grounded = self.ground_domain(sub)
        return all(v in a for v, a in grounded)
    def combine(self, other):
        return Condition(self.predicates.union(other.predicates))._collapse()
    def _collapse(self):
        output = {}
        for d, a in self.predicates:
            try:
                output[d] = tuple(set(output[d]).intersection(set(a)))
            except KeyError:
                output[d] = a
        return Condition(set(output.items()))
    def update_domain(self, sub):
        return Condition(self.ground_domain(sub))._collapse()
    def possible(self):
        for d, a in self.predicates:
            if len(a) == 0:
                return False
        return True
    def __repr__(self):
        output = []
        for d, a in self.predicates:
            output.append(str(d) + u"\u220A" + str(a))
        return ", ".join(output)
    def __eq__(self, other):
        return self.predicates == other.predicates

def normalize(expr, m_base = 0, c_base = 0):
    sub = Substitution()
    m_count, c_count = 0, 0
    for flat in e.linearize(expr):
        kind, value, n_arity, bindings = flat
        if kind == "meta" and not (kind, value) in sub.triples.keys():
            if kind == "meta" and n_arity == 0:
                sub = sub.add(Meta(value), constructor(Meta("c_" + str(c_count + c_base))))
                c_count += 1
            if kind == "meta" and n_arity != 0:
                sub = sub.add(Meta(value), constructor(Meta("F_" + str(m_count + m_base)), n_arity))
                m_count += 1
    return sub, m_count + m_base, c_count + c_base

def match_rule(expr, rule, sub = None):
    if sub is None:
        sub = Substitution()
    pattern = sub.visit(rule)
    if (pattern.kind == expr.kind) and (pattern.value == expr.value):
        for (s1, s2) in zip(expr.children, pattern.children):
            sub = match_rule(s1, s2, sub)
        return sub
    if pattern.kind == "meta" and pattern.arity == 0:
        return sub.add(pattern, expr)
    if pattern.kind == "meta" and (pattern.arity == expr.arity):
        sub = sub.add(pattern, constructor(expr, expr.arity))
        for (s1, s2) in zip(expr.children, pattern.children):
            sub = match_rule(s1, s2, sub)
        return sub
    raise UnifyError(expr, rule) 

class Equation:
    def __init__(self, cond, left, right, mc = 0, cc = 0):
        s, self.m_count, self.c_count = normalize(e.Func("pair", left, right), mc, cc)
        self.left, self.right = s.visit(left), s.visit(right)
        self.condition = cond.update_domain(s)
    def fresh_wrt(self, expr):
        if isinstance(expr, Equation):
            return Equation(self.condition, self.left, self.right, expr.m_count, expr.c_count)
        else:
            s, m, c = normalize(expr, 0, 0)
            return Equation(self.condition, self.left, self.right, m, c)
    def apply(self, expr, order):
        for eq in self.fresh_wrt(expr).orient(order):
            for p in expr.positions:
                try:
                    sub = match_rule(expr[p], eq.left)
                    new_expr = expr._substitute(p, sub.visit(eq.right))
                    if order(expr, new_expr) == Order.GT and self.condition.check(sub):
                        return new_expr
                except UnifyError:
                    pass
        return None
    def orient(self, order):
        if order(self.left, self.right) != Order.LT:
            yield self
        if order(self.right, self.left) != Order.LT:
            eq = Equation(self.condition, self.left, self.right)
            eq.condition, eq.left, eq.right = self.condition, self.right, self.left
            eq.m_count, eq.c_count = self.m_count, self.c_count
            yield eq
    def istrivial(self):
        return (self.left == self.right) and self.condition.possible()
    def __repr__(self):
        return repr(self.condition) + " : " + repr(self.left) + " == " + repr(self.right)
    def __eq__(self, other):
        if self.condition == other.condition:
            if self.left == other.left and self.right == other.right:
                return True
            elif self.left == other.right and self.right == other.left:
                return True
        return False

def cp_inner(e1, e2, order):
    pairs = []
    e2 = e2.fresh_wrt(e1)
    for p in e1.left.positions:
        if (e1.left[p].kind == "meta" and e1.left[p].arity == 0):
            continue
        try:
            sub = unify(e1.left[p], e2.left)
            base = sub.visit(e1.left)
            if order(sub.visit(e1.left), sub.visit(e1.right)) not in [Order.EQ, Order.LT]:
                if order(sub.visit(e2.left), sub.visit(e2.right)) not in [Order.EQ, Order.LT]:
                    new_cond = e1.condition.combine(e2.condition).update_domain(sub)
                    new_l = sub.visit(e1.left._substitute(p, e2.right))
                    new_r = sub.visit(e1.right)
                    pairs.append(Equation(new_cond, new_l, new_r))
        except UnifyError:
            pass
    return pairs

def critical_pairs(e1, e2, order):
    pairs = []
    for a, b in product(e1.orient(order), e2.orient(order)):
        pairs += cp_inner(a, b, order)
        pairs += cp_inner(b, a, order)
    return pairs

norm_format_string = '''Number of equations: {num}
Ordering: {order}
Equations:
> {eq}'''

class Normalizer:
    def __init__(self, equations, order):
        self.equations, self.order_functional = equations, order
    def reduce(self, expr):
        if isinstance(expr, Equation):
            l = self.reduce_expr(expr.left)
            r = self.reduce_expr(expr.right)
            return Equation(expr.condition, l, r)
        else:
            return self.reduce_expr(expr)
    def reduce_expr(self, expr, order = None):
        if order is None:
            order = self.order_functional()
        else:
            order = self.order_functional(order)
        output, done = expr, False
        while not done:
            for eq in self.equations:
                new_expr = eq.apply(output, order)
                if new_expr:
                    output = new_expr
                    break
            else:
                done = True
        return output
    def isnormal(self, expr):
        for eq in self.equations:
            new_expr = eq.apply(expr, self.order_functional())
            if new_expr:
                return False
        return True
    def __repr__(self):
        return norm_format_string.format(
                num=len(self.equations),
                order=self.order_functional.__name__,
                eq="\n> ".join(repr(e) for e in self.equations))
    def ground_joinable(self, l, r):
        # all structural - does not take conditions into account
        if l == r:
            return True
        for eq in self.equations:
            pair = e.Func("pair", l, r)
            pair2 = e.Func("pair", r, l)
            for rule in eq.orient(self.order_functional()):
                rule_pair = e.Func("pair", rule.left, rule.right)
                try:
                    sub = match_rule(pair, rule_pair)
                    return True
                except UnifyError:
                    pass
                try:
                    sub = match_rule(pair2, rule_pair)
                    return True
                except UnifyError:
                    pass
        for ord in GroundedOrder.generate(e.Func("pair", l, r)):
            if self.reduce_expr(l, ord) != self.reduce_expr(r, ord):
                break
        else:
            return True
        if (l.value == r.value) and (l.arity == r.arity):
            return all(self.ground_joinable(lc, rc) for lc, rc in zip(l.children, r.children))
        return False
