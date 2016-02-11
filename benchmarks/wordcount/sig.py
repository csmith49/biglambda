'''
reference implementation:
    map: l.map(l.pair(Var1, one), split(Var1))
    reduce: l.l.plus(Var1, Var2)
'''

def split(x : "String") -> "[String]":
    return x.split(" ")

def m(f : "1 -> 2", l : "[1]") -> "[2]":
    return list(map(f, l))

def pair(x : "1", y: "2") -> "(1, 2)":
    return (x, y)

def one() -> "Int":
    '''1'''
    return 1

def plus(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

