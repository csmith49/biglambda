from pprint import pprint
from ..adt import NodeVisitor
from itertools import product, repeat, combinations_with_replacement, combinations
from enum import Enum
from copy import deepcopy
from .ordering import GroundedOrder, LPO, default_base, Order
from .equations import Normalizer, Equation, Condition, critical_pairs
from .meta import *
from .eqparser import parse, parse_string
from . import easynorm

test_comm = parse_string("f(a, b) == f(b, a)")[0]
test_assoc = parse_string("f(f(a, b), c) == f(a, f(b, c))")[0]

def generate_normalizer(eq_file):
    equations = parse(eq_file)
    comm_eq, assoc_eq = None, None
    output = []
    for eq in equations:
        l, r = eq.left, eq.right
        cl, cr = test_comm.left, test_comm.right
        al, ar = test_assoc.left, test_assoc.right
        if (l == cl and r == cr) or (l == cr and r == cl):
            comm_eq = eq
        elif (l == al and r == ar) or (l == ar and r == al):
            assoc_eq = eq
        else:
            output.append(eq)
    if comm_eq and assoc_eq:
        extra = parse_string("f(a, f(b, c)) == f(b, f(a, c))")[0]
        extra.condition = assoc_eq.condition.combine(comm_eq.condition)
        return complete([extra, assoc_eq, comm_eq], output)
    else:
        return complete([], equations)

def complete(starting_equations, fresh_equations):
    normalizer = Normalizer(starting_equations, LPO)
    while fresh_equations:
        f = normalizer.reduce(fresh_equations.pop(0))
        if (not f.istrivial()) and f not in normalizer.equations:
            normalizer.equations.append(f)
            for eq in normalizer.equations:
                c_pairs = critical_pairs(f, eq, LPO()) + critical_pairs(eq, f, LPO())
                for cp in c_pairs:
                    if not normalizer.ground_joinable(cp.left, cp.right):
                        if cp not in fresh_equations:
                            fresh_equations.append(cp)
    return normalizer

#########################################################################
## Main (for testing)
#########################################################################

if __name__ == '__main__':
    #constructor_test = constructor(Meta("F", Meta("a"), Meta("b")), 2)
    #print(constructor_test)

    id_con = Condition(["F"], [lambda d: d[0] == "f"])
    id_left = Meta("F", Meta("F", Meta("x")))
    id_right = Meta("F", Meta("x"))
    id_eq = Equation(id_con, id_left, id_right)

    comm_con = Condition(["F"], [lambda d: d[0] in "gj"])
    comm_left = Meta("F", Meta("a"), Meta("b"))
    comm_right = Meta("F", Meta("b"), Meta("a"))
    comm_eq = Equation(comm_con, comm_left, comm_right)

    assoc_con = Condition(["F"], [lambda d: d[0] in "hj"])
    assoc_left = Meta("F", Meta("a"), Meta("F", Meta("b"), Meta("c")))
    assoc_right = Meta("F", Meta("F", Meta("a"), Meta("b")), Meta("c"))
    assoc_eq = Equation(assoc_con, assoc_left, assoc_right)

    def reduced_form(eq):
        return e.Func("pair", eq.left, eq.right)



    def complete(self):
        rf = lambda eq: e.Func("pair", eq.left, eq.right)
        self.equations, reduced, fresh = [], [], self.equations
        while fresh:
            f = self.reduce(fresh.pop(0))
            if (not f.istrivial()) and (not rf(f) in reduced):
                self.equations.append(f)
                reduced.append(rf(f))
                for eq in self.equations:
                    fresh += []




    norm = Normalizer([comm_eq, id_eq, assoc_eq], lpo)
    fresh, norm.equations = norm.equations, []
    reduced = [reduced_form(eq) for eq in norm.equations]
    reduced_cps = [reduced_form(eq) for eq in fresh]
    while fresh:
        f = norm.reduce(fresh.pop(0))
        if (not f.istrivial()) and (not reduced_form(f) in reduced):
            reduced.append(reduced_form(f))
            for eq in norm.equations:
                for cp in (critical_pairs(f, eq, lpo) + critical_pairs(eq, f, lpo)):
                    cp = norm.reduce(cp)
                    if not reduced_form(cp) in reduced_cps:
                        fresh.append(cp)
            norm.equations.append(f)
            pprint(norm.equations)
    pprint(norm.equations)
