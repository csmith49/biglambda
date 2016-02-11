def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def emit(x : "1") -> "[1]":
    return [x]

def length(xs : "[1]") -> "Int":
    return len(xs)

def isZero(x : "Int") -> "Bool":
    '''a0 == 0'''
    return x == 0

def remove(f : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(f, xs))

def PATTERN(s : "String") -> "Bool":
    return len(s) == 6 and "DATE" in s

def extract(p : "String -> Bool", s : "String") -> "[String]":
    l = len(s)
    subs = [s[i : j] for i in range(l) for j in range(i + 1, l + 1)]
    return list(filter(p, subs))

def concat(xs : "[String]") -> "String":
    return "".join(xs)
