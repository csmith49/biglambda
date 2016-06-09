from enum import Enum

Order = Enum("Order", "E G N")

def lpo(x, y):
    pass

def lexMAE(x, y, xs, ys):
    if len(xs) == 0 and len(ys) == 0:
        return Order.E
    else:
        result = lpo(xs[0], ys[0])
        if result == Order.E:
            return lexMAE(x, y, xs[1:], ys[1:])
        elif result == Order.G:
            return majo(x, ys[1:])
        else:
            return alpha(xs[1:], t)

def majo(x, ys):
    if len(ys) == 0:
        return Order.G
    else:
        result = lpo(x, ys[0])
        if result == Order.G:
            return majo(x, ys[1:])
        else:
            return Order.N

def alpha(xs, y):
    # empty list, we don't know
    if len(xs) == 0:
        return Order.N
    else:
        result = lpo(xs[0], y)
        if result == Order.E or result == Order.G:
            return Order.G
        else:
            return alpha(xs[1:], y)
