from ..adt import NodeVisitor
from .. import e
from .. import t

#########################################################################
## ReprWrapper                                                         ##
#########################################################################

import functools
class reprwrapper(object):
    def __init__(self, repr, func, value):
        self._repr = repr
        self._func = func
        self.value = value
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)
    def __repr__(self):
        return self._repr(self._func)

def withrepr(reprfun, value):
    def _wrap(func):
        return reprwrapper(reprfun, func, value)
    return _wrap

#########################################################################
## Metaterm construction                                               ##
#########################################################################

class Meta(e.Expr):
    def __new__(cls, label, *args):
        return super().__new__(cls, "meta", label, tuple(args))
    def __repr__(self):
        kids = [repr(c) for c in self.children]
        if kids:
            return self.value + "(" + ", ".join(kids) + ")"
        else:
            return self.value

class Hole(e.Expr):
    def __new__(cls, label):
        return super().__new__(cls, "hole", label, ())
    def __repr__(self):
        return "*"

def constructor(node, arity = 0):
    if arity is 0:
        @withrepr(lambda s: repr(node), node.value)
        def cons_constant(*args):
            return node
        return cons_constant
    else:
        c = node._replace(args=tuple(Hole(i) for i in range(arity)))
        @withrepr(lambda s: repr(c), node.value)
        def cons_meta(*args):
            return c._replace(args=args)
        return cons_meta

class Substitution(NodeVisitor):
    def __init__(self, triples = None):
        if triples and isinstance(triples, (list, zip, tuple)):
            self.triples = {(k, v) : t for k, v, t in triples}
        elif triples and isinstance(triples, dict):
            self.triples = triples
        else:
            self.triples = {}
    def add(self, l, r):
        if isinstance(r, e.Expr):
            r = constructor(r)
        new_triple = dict(self.triples)
        new_triple.update({(l.kind, l.value) : r})
        return Substitution(new_triple)
    def lookup(self, node):
        kind, value = node.kind, node.value
        try:
            return self.triples[(kind, value)]
        except KeyError:
            return None
    def visit_meta(self, node):
        kids = [self.visit(c) for c in node.children]
        cons = self.lookup(node)
        if cons:
            return cons(*kids)
        else:
            return node._replace(args=tuple(kids))
    def visit_hole(self, node):
        cons = self.lookup(node)
        if cons:
            return cons()
        else:
            return node
    def generic_visit(self, node):
        kids = [self.visit(c) for c in node.children]
        if kids:
            return node._replace(args=tuple(kids))
        else:
            return node
    def __repr__(self):
        return repr(list(str(k[1]) + " -> " + repr(v) for k, v in self.triples.items()))

#########################################################################
## Unification, et. al                                                 ##
#########################################################################

class UnifyError(Exception):
    def __init__(self, l, r):
        self.message = "Cannot unify {} and {}".format(repr(l), repr(r))
    def __repr__(self):
        return self.message

def unify(e1, e2, sub = None):
    if sub is None:
        sub = Substitution()
    l, r = sub.visit(e1), sub.visit(e2)
    # identity case - limits addition of trivial subs
    if (l.kind == r.kind) and (l.value == r.value):
        for (s1, s2) in zip(l.children, r.children):
            sub = unify(s1, s2, sub)
        return sub
    # l is meta-variable with 0 arity
    if l.kind == "meta" and l.arity == 0:
        if l.value in r._values_from_kind("meta"):
            raise UnifyError(l, r)
        return sub.add(l, r)
    # r is meta with 0 arity, just switch
    if r.kind == "meta" and r.arity == 0:
        return unify(r, l, sub)
    # higher-arity meta case for l
    if l.kind == "meta" and (l.arity == r.arity):
        sub = sub.add(l, constructor(r, r.arity))
        for (s1, s2) in zip(l.children, r.children):
            sub = unify(s1, s2, sub)
        return sub
    # high-arity meta for r, just switch
    if r.kind == "second" and (r.arity == l.arity):
        return unify(r, l, sub)
    # fall-through case of failure
    raise UnifyError(l, r)
