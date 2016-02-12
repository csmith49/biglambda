def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def one() -> "Int":
    '''1'''
    return 1

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def fst(p : "(1, 2)") -> "1":
    return p[0]

def snd(p : "(1, 2)") -> "2":
    return p[1]

def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def filt(p : "1->Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def isname(w : "String") -> "Bool":
    return w.isupper() and len(w) > 1

def get_words(w : "String") -> "[String]":
    return w.split()

def issentiment(w : "String") -> "Bool":
    return w in ["love", "hate"]

def append(x : "[1]", y : "[1]") -> "[1]":
    return x + y
