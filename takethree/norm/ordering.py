from enum import Enum
from itertools import combinations, combinations_with_replacement
from .meta import Meta

Order = Enum("Order", "LT EQ GT INC")

class OrderFunctional:
    def __init__(self, base = None):
        if base is None:
            self.base = default_base
        else:
            self.base = base
    def __call__(self, a, b):
        return self.base(a, b)
    def __repr__(self):
        return self.__name__ + "(" + self.base.__name__ + ")"

class Lexicographic(OrderFunctional):
    def __call__(self, a, b):
        for x, y in zip(a, b):
            ord = self.base(x, y)
            if ord != Order.EQ:
                return ord
        return Order.EQ

class LPO(OrderFunctional):
    def _inner(self, a, b):
        if self.base(a, b) == Order.GT:
            if all(self(a, c) == Order.GT for c in b.children):
                return True
        elif self.base(a, b) == Order.EQ:
            if Lexicographic(self)(a.children, b.children) == Order.GT:
                return True
        elif any(self(c, b) in [Order.GT, Order.EQ] for c in a.children):
            return True
        else:
            return False

    def __call__(self, a, b):
        return Order.INC
        first, second = self.ge(a,b), self.ge(b,a)
        if first and second:
            return Order.EQ
        elif first:
            return Order.GT
        elif second:
            return Order.LT
        else:
            return Order.INC

    def ge(self, a, b):
        if (b.kind == "meta") and (b.arity == 0):
            return (a == b) or (b.value in a._values_from_kind("meta"))
        elif (a.kind == "meta") and (a.arity == 0):
            return False
        else:
            if all(map(lambda s: not self.ge(s, b), a.children)):
                order = self.base(a, b)
                if order == Order.GT:
                    return all(map(lambda t: self(a, t) == Order.GT, b.children))
                elif order == Order.EQ:
                    return Lexicographic(self)(a.children, b.children) in [Order.EQ, Order.GT]
                else:
                    return False
            else:
                return True

def str_repr(expr):
    return expr.kind + ":" + str(expr.value)

def default_base(e1, e2):
    a, b = str_repr(e1), str_repr(e2)
    if a == b:
        return Order.EQ
    if "meta" in a or "meta" in b:
        return Order.INC
    if a < b:
        return Order.LT
    if a > b:
        return Order.GT

class GroundedOrder:
    def __init__(self, meta_dict):
        self.meta_dict = meta_dict
    def _lookup(self, str_a, str_b):
        try:
            return self.meta_dict[(str_a, str_b)]
        except KeyError:
            pass
        try:
            ord = self.meta_dict[(str_b, str_a)]
            if ord == Order.LT: return Order.GT
            if ord == Order.GT: return Order.LT
            return ord
        except KeyError:
            pass
        return None
    def __call__(self, a, b):
        ord = self._lookup(str_repr(a), str_repr(b))
        if ord:
            return ord
        else:
            return default_base(a, b)
    @staticmethod
    def generate(expr):
        metas = set("meta:" + str(val) for val in expr._values_from_kind("meta"))
        num_of_pairs = len(metas) * (len(metas) - 1) // 2
        for possible in combinations_with_replacement([Order.LT, Order.GT, Order.EQ], num_of_pairs):
            meta_dict = {k:v for k, v in zip(combinations(metas, 2), possible)}
            yield GroundedOrder(meta_dict)
