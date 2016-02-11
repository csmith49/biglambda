def smap(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def ssum(xs : "[Int]") -> "Int":
    total = 0
    for i in xs:
        total += i
    return total

def smin(x : "Int", y : "Int") -> "Int":
    '''z3.If(a0 > a1, a1, a0)'''
    return min(x, y)

def smax(x : "Int", y : "Int") -> "Int":
    '''z3.If(a0 > a1, a0, a1)'''
    return max(x, y)

def splus(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def zero() -> "Int":
    '''0'''
    return 0

def inc(x : "Int") -> "Int":
    '''a0 + 1'''
    return x + 1

def li(x : "1") -> "[1]":
    return [x]

def cons(x : "1", xs : "[1]") -> "[1]":
    return [x] + xs
