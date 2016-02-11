from .adt import Node, NodeVisitor

## defining our recursive type language

class Type(Node): pass

class Var(Type):
    _count = 0
    def __new__(cls, *args):
        if len(args) > 0:
            value = args[0]
        else:
            value = Var._count
            Var._count += 1
        return super().__new__(cls, "var", value, ())
    def __repr__(self):
        return repr(self.value)
    def __reduce__(self):
        return Var, (self.value,)

class Base(Type):
    def __new__(cls, name):
        return super().__new__(cls, "base", name, ())
    def __repr__(self):
        return self.value 
    def __reduce__(self):
        return Base, (self.value,)

class Func(Type):
    def __new__(cls, l, r):
        return super().__new__(cls, "func", None, (l, r))
    def __repr__(self):
        return u"{l}\u2192{r}".format(
            l=repr(self.args[0]),
            r=repr(self.args[1]))
    def __reduce__(self):
        return Func, tuple(self.args)

class List(Type):
    def __new__(cls, s):
        return super().__new__(cls, "list", None, (s,))
    def __repr__(self):
        return "[" + repr(self.args[0]) + "]"
    def __reduce__(self):
        return List, (self.args[0], )

class Pair(Type):
    def __new__(cls, l, r):
        return super().__new__(cls, "pair", None, (l, r))
    def __repr__(self):
        return "({l}, {r})".format(
            l=repr(self.args[0]),
            r=repr(self.args[1]))
    def __reduce__(self):
        return Pair, tuple(self.args)

class Scheme(Type):
    def __new__(cls, bound, sub):
        return super().__new__(cls, "scheme", bound, (sub,))
    def __repr__(self):
        return u"\u2200{quantified}.{sub}".format(
            quantified=",".join(repr(b) for b in self.value),
            sub=repr(self.args[0]))

## functions for manipulating types

class TypeSubstitution:
    def __init__(self, sub = None):
        if sub is None:
            self._sub = {}
        else:
            self._sub = sub
    def __call__(self, node):
        return self.visit(node)
    def extend(self, var, term):
        #self._sub[var.value] = term
        output = dict(self._sub)
        output[var.value] = term
        return TypeSubstitution(output)
    def visit(self, node):
        if node[0] == "var":
            try:
                return self._sub[node[1]]
            except KeyError:
                return node
        else:
            return node._replace(args=list(map(self.visit, node[2])))
    def __repr__(self):
        return repr(self._sub)

class UnifyError(Exception):
    pass

def unify(t1, t2, sub = None):
    if sub is None:
        sub = TypeSubstitution()
    l, r = sub.visit(t1), sub.visit(t2)
    if (l.kind == r.kind) and (l.arity == r.arity) and (l.value == r.value):
        for p, q in zip(l.children, r.children):
            sub = unify(p, q, sub)
        return sub
    elif l.kind == "var":
        if l.value in r._values_from_kind("var"):
            raise UnifyError
        else:
            return sub.extend(l, r)
    elif r.kind == "var":
        return unify(r, l, sub)
    else:
        raise UnifyError

def match(t1, t2, sub = None):
    if sub is None:
        sub = TypeSubstitution()
    t, rule = sub.visit(t1), sub.visit(t2)
    if (t.kind == rule.kind) and (t.arity == rule.arity) and (t.value == rule.value):
        for p, q in zip(t.children, rule.children):
            sub = match(p, q, sub)
        return sub
    elif rule.kind == "var":
        if rule.value in t._values_from_kind("var"):
            raise UnifyError
        else:
            return sub.extend(rule, t)
    else:
        raise UnifyError


def fresh_wrt(expr, s):
    vals = expr._values_from_kind("var")
    fresh_list, base = [], 0
    while len(fresh_list) != len(vals):
        if base not in s:
            fresh_list.append(base)
        base += 1
    fresh_vars = [Var(i) for i in fresh_list]
    return TypeSubstitution({k : v for k, v in zip(vals, fresh_vars)})

if __name__ == '__main__':
    test = Func(List(Pair(Base("int"), Var(1))), Var(1))
    print(test)
    s = TypeSubstitution({1 : List(Base("str"))})
    print(s.visit(test))
