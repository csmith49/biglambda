def factor(x : "Int") -> "[Int]":
    output = []
    for i in range(1, x + 1):
        if divides(i, x):
            if isPrime(i):
                output.append(i)
    return output

def divides(x : "Int", y : "Int") -> "Bool":
    return y % x == 0

def isPrime(x : "Int") -> "Bool":
    if x == 1:
        return False
    for i in range(2, x):
        if divides(i, x):
            return False
    return True

def plus(x : "Int", y : "Int") -> "Int":
    return x + y

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def one() -> "Int":
    return 1

def emit(x : "1") -> "[1]":
    return [x]

def div(x : "Int", y : "Int") -> "Float":
    return x / y

def round(x : "Float") -> "Int":
    return int(x)

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))
