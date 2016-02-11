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
    return [(k, [q for p, q in pairs if p == k]) for k in used]

class FilledSketch(object):
    def __init__(self, m, r, a = None, f = False, k = False):
        self._m = m
        self._r = r
        self._a = a
        self._flattened = f
        self._keyed = k
    def __call__(self, li, writer):
        return self._execute(li, writer)
    def __repr__(self):
        output = "filled sketch: {n}\n    mapper: {m}\n    reducer: {r}\n    flags: {f}"
        return output.format(n='test', 
                m=repr(self._m), 
                r=repr(self._r), 
                f=repr( (self._a, self._flattened, self._keyed) ))
    def _execute(self, li, writer):
        m = writer(self._m)
        r = uncurry(writer(self._r))
        a = writer(self._a) if self._a else lambda s: s
        # first map
        mapped = list(map(m, li))
        # flatten if we need
        if self._flattened:
            mapped = list(flatten(mapped))
        # if we have keys, shuffle correctly
        if self._keyed:
            reduced = []
            for k, v in collect(mapped):
                reduced.append( (k, reduce(r, v)) )
        else:
            reduced = reduce(r, mapped)
        # apply if needed - defaults to id
        return a(reduced)
    def csg_check(self, li, writer):
        m = writer(self._m)
        r = uncurry(writer(self._r))
        old_value = None
        mapped = map(m, li)
        if self._flattened:
            mapped = flatten(mapped)
        for permuted in itertools.permutations(mapped):
            if self._keyed:
                reduced = []
                for k, v in collect(permuted):
                    reduced.append( (k, reduce(r, v)) )
            else:
                reduced = reduce(r, permuted)
            if isinstance(reduced, list):
                return sorted(reduced)
            if old_value and (reduced != old_value):
                return False
            else:
                old_value = reduced
        return True

class Sketch(object):
    def __init__(self, types, flatten = False, applier = False):
        # flags for sketch kind
        self.flattened = flatten
        self.applied = applier
        self.keyed = len(types) >= 3
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
            mappings['final'] = "[({}, {})]".format(types[2], mappings['red'])
        else:
            mappings['inter'] = mappings['red']
            mappings['final'] = mappings['red']
        # now, check for flattening stuff
        if self.flattened:
            mappings['inter'] = "[{}]".format(mappings['inter'])
        # now set requirements
        self.reqs = [s.format(**mappings) for s in self.reqs]
    def consume(self, gen):
        for e in gen:
            m, r = e[0], e[1]
            a = e[2] if len(e) > 2 else None
            yield FilledSketch(m, r, a, self.flattened, self.keyed)

def gen_requirements(types, flatten = False, applier = False):
    f = flatten
    a = applier
    k = len(types) >= 3

    i_t, o_t = types[0], types[1]
    reqs = ["{input} -> {inter}", "{red} -> {red} -> {red}"]
    mappings = {'input': i_t, 'output': o_t}

    if a:
        reqs.append("{final} -> {output}")
        mappings['red'] = '1'
    else:
        mappings['red'] = o_t

    if k:
        mappings['inter'] = "({}, {})".format(types[2], mappings['red'])
        mappings['final'] = "[({}, {})]".format(types[2], mappings['red'])
    else:
        mappings['inter'] = mappings['red']
        mappings['final'] = mappings['red']
    # now, check for flattening stuff
    if f:
        mappings['inter'] = "[{}]".format(mappings['inter'])
    # now set requirements
    return [(f, a, k)] + [s.format(**mappings) for s in reqs]
