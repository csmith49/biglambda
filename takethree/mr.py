import itertools
from functools import reduce

def uncurry(func):
    ''' reducers are curried functions - this fixes that '''
    def new_func(*args):
        result = func
        for arg in args:
            result = result(arg)
        return result
    return new_func

def flatten(lli):
    ''' removes one level of list nesting '''
    return itertools.chain.from_iterable(lli)

def collect(lk):
    ''' groups elements by key, turning [(k,v)] -> [(k, [v])] '''
    used = []
    pairs = list(lk)
    for k, v in pairs:
        if k not in used:
            used.append(k)
            yield k, [q for p, q in pairs if p == k]

def map_reduce(mapper: "1->2", reducer: "2->2->2") -> "[1]->2":
    bin_reducer = uncurry(reducer)
    def mr(li):
        return reduce(bin_reducer, map(mapper, li))
    return mr

def map_reduce_emit(mapper: "1->[2]", reducer: "2->2->2") -> "[1]->2":
    bin_reducer = uncurry(reducer)
    def mre(li):
        try:
            return reduce(bin_reducer, flatten(map(mapper, li)))
        except:
            return []
    return mre

def map_reduce_keyed(mapper: "1->(3, 2)", reducer: "2->2->2") -> "[1]->[(3,2)]":
    bin_reducer = uncurry(reducer)
    def mrk(li):
        return [(k, reduce(bin_reducer, v)) for k, v in collect(map(mapper, li))]
    return mrk

def map_reduce_keyed_emit(mapper: "1->[(3, 2)]", reducer: "2->2->2") -> "[1]->[(3, 2)]":
    bin_reducer = uncurry(reducer)
    def mrk(li):
        return [(k, reduce(bin_reducer, v)) for k, v in collect(flatten(map(mapper, li)))]
    return mrk

def map_reduce_keyed_map(mapper, reducer, func):
    mrk = map_reduce_keyed(mapper, reducer)
    def mrkm(li):
        return func(mrk(li))
    return mrkm

def map_reduce_keyed_emit_map(mapper, reducer, func):
    mrke = map_reduce_keyed_emit(mapper, reducer)
    def mrkem(li):
        return func(mrke(li))
    return mrkem

def map_reduce_map(mapper, reducer, func):
    mr = map_reduce(mapper, reducer)
    def mrm(li):
        return func(mr(li))
    return mrm

def map_reduce_emit_map(mapper, reducer, func):
    mre = map_reduce_emit(mapper, reducer)
    def mrem(li):
        try:
            return func(mre(li))
        except:
            return []
    return mrem
