'''
reference implementation:
    mapper : \.pair(var(1), 1)
    reduce : \.\.splift(splus, var(1), var(2))
    map    : \.div(sum(map(fst, var(1)), sum(map(snd, var(1)))))

'''

def pair(x : "Int", y : "Int") -> "(Int, Int)":
    return (x, y)

def pplus(x : "(Int, Int)", y : "(Int, Int)") -> "(Int, Int)":
    return (x[0] + y[0], x[1] + y[1])

def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def s(xs : "[Int]") -> "Int":
    output = 0
    for x in xs:
        output += x
    return output

def div(x : "Int", y : "Int") -> "Float":
    return x / y

def one() -> "Int":
    return 1

def keys(xs : "[(1, 2)]") -> "[1]":
    return [x for x, y in xs]

def vals(xs : "[(1, 2)]") -> "[2]":
    return [y for x, y in xs]
