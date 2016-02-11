def get_elem(k : "Int", r : "Row") -> "String":
    return r[k]

def zero() -> "Int":
    return 0

def succ(x : "Int") -> "Int":
    return x + 1

def is_equal(x : "String", y : "String") -> "Bool":
    return x == y

def KEY() -> "String":
    return "KEY"

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def emit(x : "1") -> "[1]":
    return [x]

def single_f(f : "1 -> Bool", x : "1") -> "[1]":
    if f(x):
        return [x]
    else:
        return []

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)
