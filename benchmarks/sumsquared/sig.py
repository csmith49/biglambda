def zero() -> "Int":
    '''0'''
    return 0

def succ(x : "Int") -> "Int":
    '''a0 + 1'''
    return x + 1

def square(x : "Int") -> "Int":
    '''a0 * a0'''
    return x * x

def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def mult(x : "Int", y : "Int") -> "Int":
    '''a0 * a1'''
    return x * y

def fadd(x : "Float", y : "Float") -> "Float":
    '''a0 + a1'''
    return x + y

def div(x : "Float", y : "Float") -> "Float":
    '''a0 / a1'''
    return x / y

def cast(x : "Int") -> "Float":
    return x

def round(x : "Float") -> "Int":
    return int(x)

def singleton(x: "1") -> "[1]":
    return [x]

def default(x: "1") -> "(Int, 1)":
    return (1, x)
