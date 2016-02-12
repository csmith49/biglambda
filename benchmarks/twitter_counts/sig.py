def hashtag() -> "Re":
    return "#[\w]+"

def match(s : "String", pattern : "Re") -> "Bool":
    import re
    if re.match(pattern, s):
        return True
    else:
        return False

def find_matches(s : "String", pattern : "Re") -> "[String]":
    import re
    return re.findall(pattern, s)

def pair(x : "1", y: "2") -> "(1, 2)":
    return x, y

def zero() -> "Int":
    '''0'''
    return 0

def one() -> "Int":
    '''1'''
    return 1

def append(x : "[1]", y : "[1]") -> "[1]":
    return x + y

def split(l : "String") -> "[String]":
    return l.split()

def plus(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def perms(xs : "[1]") -> "[(1, 1)]":
    import itertools
    return list(itertools.permutations(xs, 2))

def canonical(p : "(1, 1)") -> "Bool":
    return p[0] <= p[1]

def filt(p : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def emit(x : "1") -> "[1]":
    return [x]

def fst(p: "(1, 2)") -> "1":
    return p[0]

def snd(p : "(1, 2)") -> "2":
    return p[1]
