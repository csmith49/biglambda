import itertools
from functools import reduce

def uncurry(func):
    def new_func(*args):
        result = func
        for arg in args:
            result = result(arg)
        return result
    return new_func

def flatten(lli):
    return itertools.chain.from_iterable(lli)

def collect(lk):
    used = []
    pairs = list(lk)
    for k, v in pairs:
        if k not in used:
            used.append(k)
            yield k, [q for p, q in pairs if p == k]

class Sketch(object):
    def __init__(self, types, flatten = False, applier = False):
        # have to produce the appropriate types for reqs
        # choice based on flatten and applier
        # flatten - m: input -> [inter]
        # if keyed - inter: (k, reducible)
        # if applier - a: reducible -> output
        
        # flags for sketch kind
        self.flattened = flatten
        self.applied = applier
        self.keyed = len(types) >= 3
        # writer so we can make new stuff
        # maybe

        # compute requirements
        # pull out default types
        i_t, o_t = types[0], types[1]
        self.reqs = ["{input} -> {inter}", "{red} -> {red} -> {red}"]
        mappings = {'input': i_t, 'output': o_t}

        # see if we have any free vars
        if self.applied:
            self.reqs.append("{final} -> {output}")
            mappings['red'] = '1'
        else:
            mappings['red'] = o_t
        # see if we're keyed or not
        if len(types) > 2:
            mappings['inter'] = "({}, {})".format(types[2], mappings['red'])
            mappings['final'] = "[({}, {}]".format(types[2], mappings['red'])
        else:
            mappings['inter'] = mappings['red']
            mappings['final'] = mappings['red']
        # now, check for flattening stuff
        if self.flattened:
            mappings['inter'] = "[{}]".format(mappings['inter'])
        # now set requirements
        self.reqs = [s.format(**mappings) for s in self.reqs]
    def _create(self, m, r, a = lambda s: s):
        def filled_sketch(li):
            r = uncurry(r)
            # first map over
            mapped = map(m, li)
            # if we need to flatten, do it
            if self.flattened:
                mapped = flatten(mapped)
            # if we have keys, collect by value
            if self.keyed:
                reduced = []
                for k, v in collect(mapped):
                    reduced.append( (k, reduce(r, v)) )
            # else we just reduce
            else:
                reduced = reduce(r, mapped)
            # applier defaults to id
            return a(reduced)
        return filled_sketch
    def dynamic_csg_checker(self, m, r):
        def checker(li):
            r = uncurry(r)
            old_value = None
            for p in permutations(li, len(li)):
                mapped = map(m, p)
                if self.flattened:
                    mapped = flatten(mapped)
                # now we apply and compare to some old value
                if self.keyed:
                    reduced = []
                    for k, v in collect(mapped):
                        reduced.append( (k, reduce(r, v)) )
                else:
                    reduced = reduce(r, mapped)
                if isinstance(reduced, list):
                    reduced = sorted(reduced)
                if old_value and (reduced != old_value):
                    return False
                else:
                    old_value = reduced
            return True
        return checker
