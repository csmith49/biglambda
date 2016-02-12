def get_lines(e: "Email") -> "[String]":
    return e.split("\n")

def get_selector(t : "Tag") -> "String -> Bool":
    def selector(s):
        return s.startswith(t)
    return selector

def extract_line(e : "Email", t : "Tag") -> "String":
    return list(filter(lambda l: l.startswith(t), e.split("\n")))[0]

def from_tag() -> "Tag":
    return "From:"

def to_tag() -> "Tag":
    return "To:"

def extract_tagged(s: "String", t: "Tag") -> "String":
    return s.partition(t)[2].strip()

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def one() -> "Int":
    '''1'''
    return 1

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def filt(p : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def append(x : "[1]", y : "[1]") -> "[1]":
    return x + y
