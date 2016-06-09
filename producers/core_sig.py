def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def zero() -> "Int":
    '''0'''
    return 0

def one() -> "Int":
    '''1'''
    return 1

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def fst(p : "(1, 2)") -> "1":
    return p[0]

def snd(p : "(1, 2)") -> "2":
    return p[1]

def emit(x : "1") -> "[1]":
    return [x]

def core_map(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def core_filter(p : "1->Bool", xs: "[1]") -> "[1]":
    return list(filter(p, xs))

def bool_emit(p : "1->Bool", x : "1") -> "[1]":
    return [x] if p(x) else []

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def length(xs : "[1]") -> "Int":
    return len(xs)

def lower(w : "String") -> "String":
    return w.lower()

def split(w : "String") -> "[String]":
    return w.split()

def to_chars(w : "String") -> "[String]":
    return list(w)

def sorted_word(w : "String") -> "String":
    return "".join(sorted(list(w)))
