def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def f_add(x : "Float", y : "Float") -> "Float":
    '''a0 + a1'''
    return x + y

def time(r : "Record") -> "Int":
    return r[0]

def watts(r : "Record") -> "Int":
    return r[1]

def bpm(r : "Record") -> "Int":
    return r[2]

def speed(r : "Record") -> "Float":
    return r[3]

def roundToTen(x : "Int") -> "Int":
    import math
    return int(math.ceil(x / 1000.0)) * 1000

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def fst(p : "(1, 2)") -> "1":
    return p[0]

def snd(p : "(1, 2)") -> "2":
    return p[1]

def filt(p : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def emit(x : "1") -> "[1]":
    return [x]

def mult(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x * y

def toReal(x : "Int") -> "Float":
    return x

def pmax(x : "Int", y : "Int") -> "Int":
    '''z3.If(a0 > a1, a0, a1)'''
    return max(x, y)

def pmin(x : "Int", y : "Int") -> "Int":
    '''z3.If(a0 > a1, a1, a0)'''
    return min(x, y)

def ceiling(x : "Float") -> "Int":
    import math
    return math.ceil(x)

def one() -> "Int":
    '''1'''
    return 1
