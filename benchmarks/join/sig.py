# ref implementation
# mapper: \.m(\.pair(VAL(x), x), rows(x))
# reducer: \.not a clue

def db(x : "DB") -> "String":
    return x[0]

def rows(x : "DB") -> "[Row]":
    return x[1]
