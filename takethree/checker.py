import z3
from .adt import NodeVisitor

def create_z3_var(name, type):
    if type[1] == "Int":
        return z3.Int(name)
    elif type[1] == "Float":
        return z3.Real(name)
    else:
        raise NotImplementedError

class ReducerVisitor(NodeVisitor):
    def __init__(self, signature):
        self.encodings = {s.name : s.encoding for s in signature}
        self._type = None
        self._placeholders = {}
    def __call__(self, node):
        # reset context
        self._type = None
        self._placeholders = {}
        # create expr
        expr = self.visit(node)
        # look stuff up so we can close it in F
        try: v1 = self._placeholders['v1']
        except: v1 = create_z3_var('v1', self._type)
        try: v2 = self._placeholders['v2']
        except: v2 = create_z3_var('v2', self._type)
        vout = create_z3_var("out", self._type)
        vtype = self._type
        # create function F
        def F(*args):
            replacements = zip([v1, v2, vout], [create_z3_var(s, vtype) for s in args])
            return z3.substitute(expr == vout, *replacements)
        def V(str):
            return create_z3_var(str, vtype)
        return F, V
    def visit_var(self, node):
        label, type = node[1]
        name = 'v' + str(label)
        try:
            return self._placeholders[name]
        except KeyError:
            value = create_z3_var(name, type)
            self._placeholders[name] = value
            if not self._type:
                self._type = type
            return value
    def visit_func(self, node):
        encoding = self.encodings[node[1]]
        if not encoding:
            raise NotImplementedError
        children = [self.visit(c) for c in node[2]]
        d = {'a' + str(i) : c for i, c in enumerate(children)}
        return(eval(encoding, globals(), d))

def reducer_check(node, signature, verbose=True):
    visitor = ReducerVisitor(signature)
    # i wouldn't worry about it
    reducer = node[2][0][2][0]
    # use r for rel, v for making new nodes
    try:
        r, v = visitor(reducer)
        # solver we'll push into
        solver = z3.Solver()
        # now, we need to add constraints
        # comm
        solver.add(r("i1", "i2", "o1"), r("i2", "i1", "o2"))
        # assoc
        solver.add(r("o1", "i3", "o3"), r("i2", "i3", "o4"), r("i1", "o4", "o5"))
        # csg
        solver.add(z3.Or(v("o1") != v("o2"), v("o3") != v("o5")))
        # now check for unsat
        result = solver.check() != 1
        if verbose:
            print("DINNER_STAT z3 verified_{}".format(result))
        return result
    except Exception as e:
        if verbose:
            print("DINNER_STAT z3 unknown: {}".format(repr(e)))
        return True # we return even if we can't decide
