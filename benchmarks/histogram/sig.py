def bin(x : "Float") -> "Sign":
    if x > 0:
        return "+"
    elif x < 0:
        return "-"
    else:
        return "?"

def plus(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def fplus(x : "Float", y : "Float") -> "Float":
    '''a0 + a1'''
    return x + y

def div(x : "Float", y : "Float") -> "Float":
    '''a0 / a1'''
    return x / y

def round(x : "Float") -> "Int":
    return int(x)

def intBin(x : "Int") -> "Sign":
    return bin(x)

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def emit(x : "1") -> "[1]":
    return [x]

def one() -> "Int":
    '''1'''
    return 1

def float(x : "Int") -> "Float":
    return x / 1.0

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))
