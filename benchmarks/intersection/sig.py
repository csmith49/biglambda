def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def get_elem(x : "Int", r : "Row") -> "String":
    return r[x]

def zero() -> "Int":
    return 0

def succ(x : "Int") -> "Int":
    return x + 1

def db(rs : "(String, [Row])") -> "String":
    return rs[0]

def rows(rs : "(String, [Row])") -> "[Row]":
    return rs[1]

def append(xs : "[1]", ys : "[1]") -> "[1]":
    return xs + ys

def filter_unique(xs : "[(String, [String])]" ) -> "[String]":
    return list([k for k, v in xs if len(set(v)) > 1])
