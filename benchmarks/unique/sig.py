def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def emit(x : "1") -> "[1]":
    return [x]

def head(xs : "[1]") -> "1":
    try:
        return xs[0]
    except:
        return []

def s_filter(f : "1 -> Bool", x : "1") -> "[1]":
    if f(x):
        return [x]
    else:
        return []

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def contains(xs : "[1]", x : "1") -> "Bool":
    return x in xs

def gather_keys(xs : "[(1, 1)]") -> "[1]":
    return [x for x, y in xs]

def zero() -> "Int":
    return 0

def succ(x : "Int") -> "Int":
    return x + 1
