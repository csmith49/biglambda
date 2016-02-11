def word_split(words : "String") -> "[String]":
    return words.split()

def sort_word(word : "String") -> "String":
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

def filt(p : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def length(xs : "[1]") -> "Int":
    return len(xs)

def is_zero(x : "Int") -> "Bool":
    return x == 0

def concat(xs : "[String]") -> "String":
    return "".join(xs)

def round(x : "Float") -> "Int":
    return int(x)

def is_prime(x : "Int") -> "Bool":
    if x == 1:
        return False
    for i in range(2, x):
        if divides(i, x):
            return False
    return True

def divides(x : "Int", y : "Int") -> "Bool":
    return y % x == 0

def factor(x : "Int") -> "[Int]":
    output = []
    for i in range(1, x + 1):
        if divides(i, x):
            if is_prime(i):
                output.append(i)
    return output

def PATTERN(word : "String") -> "Bool":
    return word in ["cat", "dog", "human"]

def bin(x : "Float") -> "Sign":
    if x > 0:
        return "+"
    elif x < 0:
        return "-"
    else:
        return "?"

def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def to_chars(word : "String") -> "[String]":
    return list(word)

def lower(word : "String") -> "String":
    return word.lower()

def sum_list(xs : "[Int]") -> "Int":
    return sum(xs)

def binary_min(x : "Int", y : "Int") -> "Int":
    return min(x, y)

def binary_max(x : "Int", y : "Int") -> "Int":
    return max(x, y)

def POS_tag(word : "String") -> "Tag":
    if word in ["cat", "dog", "human"]:
        return "Noun"
    elif word in ["sleep", "eat", "play"]:
        return "Verb"
    elif word in ["fluffy", "small", "loud"]:
        return "Adjective"
    else:
        return "?"

def square(x : "Int") -> "Int":
    return x ** 2

def default_pair(x : "1") -> "(Int, 1)":
    return (1, x)
