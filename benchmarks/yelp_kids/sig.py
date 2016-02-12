def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def filt(p : "1->Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def one() -> "Int":
    '''1'''
    return 1

def append(x : "[1]", y : "[1]") -> "[1]":
    return x + y

def city(r : "Review") -> "String":
    return r[0]

def state(r : "Review") -> "String":
    return r[1]

def review(r : "Review") -> "String":
    return r[2]

def rev_count(r : "Review") -> "Int":
    return r[3]

def hasAttr(r : "Review", a : "Attr") -> "Bool":
    try:
        if r[-1][a]:
            return True
        else:
            return False
    except:
        return False

def goodForKids() -> "Attr":
    return "Good for Kids"

def length(xs : "[1]") -> "Int":
    return len(xs)


def bool_to_int(b : "Bool") -> "Int":
    '''z3.If(a0, 1, 0)'''
    if b:
        return 1
    else:
        return 0
