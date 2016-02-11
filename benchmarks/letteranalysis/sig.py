def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def word_split(line : "String") -> "[String]":
    return line.split()

def to_chars(word : "String") -> "[String]":
    return list(word)

def pair(x : "1", y : "2") -> "(1, 2)":
    return x, y

def one() -> "Int":
    '''1'''
    return 1

def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def lower(s : "String") -> "String":
    return s.lower()
