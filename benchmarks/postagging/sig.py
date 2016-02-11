def word_split(line : "String") -> "[String]":
    return line.split()

def tag(word : "String") -> "Tag":
    if word in ["cat", "dog", "human"]:
        return "Noun"
    elif word in ["sleep", "eat", "play"]:
        return "Verb"
    elif word in ["fluffy", "small", "loud"]:
        return "Adjective"
    else:
        return "Huh?"

def one() -> "Int":
    '''1'''
    return 1

def plus(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

