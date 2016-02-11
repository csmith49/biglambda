def word_split(line : "String") -> "[String]":
    return line.split()

def PATTERN(word : "String") -> "Bool":
    return word in ["cat", "dog", "human"]

def p_filter(f : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(f, xs))

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def emit(x : "1") -> "[1]":
    return [x]

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def one() -> "Int":
    '''1'''
    return 1

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def plus(x : "Int", y : "Int") -> "Int":
    return x + y

def is_zero(x : "Int") -> "Bool":
    '''a0 == 0'''
    return x == 0

def length(word : "String") -> "Int":
    return len(word)
