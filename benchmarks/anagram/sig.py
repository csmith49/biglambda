def word_split(words : "String") -> "[String]":
    return words.split()

def word_sorted(word : "String") -> "String":
    return "".join(list(sorted(word)))

def one() -> "Int":
    '''1'''
    return 1

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def emit(x : "1") -> "[1]":
    return [x]

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def cons(x : "1", xs : "[1]") -> "[1]":
    return [x] + xs

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

