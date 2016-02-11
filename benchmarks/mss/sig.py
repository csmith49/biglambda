# ref solution:
# mapper: \.m(\.pair(sum(x), x), xs)
# reducer: \.\.x
# applier: \.max_val_from_key(xs)

def subsets(xs : "[1]") -> "[[1]]":
    output = []
    for i in range(len(xs)):
        for j in range(i):
            output.append(xs[j:i])
    return output

def m(f : "1->2", xs : "[1]") -> "[2]":
    return list(map(f, xs))

def pair(x : "1", y : "2") -> "(1, 2)":
    return (x, y)

def s_sum(xs : "[Int]") -> "Int":
    return sum(xs)

def max_from_keys(xs : "[(Int, 1)]") -> "1":
    return sorted(xs, key=lambda p: p[0])[-1][-1]
