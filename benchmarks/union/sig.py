def filt(p : "1 -> Bool", xs : "[1]") -> "[1]":
    return list(filter(p, xs))

def m(f : "1 -> 2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def one() -> "Int":
    '''1'''
    return 1

def add(x : "Int", y : "Int") -> "Int":
    '''a0 + a1'''
    return x + y

def append(x : "[1]", y : "[1]") -> "[1]":
    return x + y

def to_items(x : "Database") -> "[Item]":
    return x[1]

def to_name(x : "Database") -> "String":
    return x[0]

def access(x : "Item", k : "Key") -> "String":
    return x[k]

def has_val(x : "Item", k : "Key", s : "String") -> "Bool":
    return x[k] == s

def KEY() -> "Key":
    return 0

def VALUE() -> "String":
    return "K0"

def concat_db(x : "Database", y : "Database") -> "[Item]":
    return x[0] + y[0]

def emit_item(x : "1") -> "[1]":
    return [x]

# union:
# m: \.x
# r: \.\.concatenate(x, y)
#
# select:
# m: \.filt(\.equal(access(x, KEY), VALUE), to_items(x))
# r: \.\.append(x, y)
#
# cross join:
# m: \.m(\.pair(access(x, VALUE), to_items(x)))
# r: \.\.append(x, y)
#
# intersect:
# ...
# ...
# a: ...
