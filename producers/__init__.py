from .components import generate_resources, parse_type
from .adt import ExtendedVisitor
from . import e
from . import t
from . import mr
from .data import parse_data, parse_tags
from .expansion import generate_expander
from .easynorm import EasyNormalizer
from .checker import reducer_check
from itertools import chain
from functools import reduce
from collections import defaultdict

def node(form, dict):
    return e.Un(parse_type(form.format(**dict)))

def make_keyed(input, out, key):
    output = []
    mapping = {'i': input, 'o': out, 'k': key}
    reducer = node("{o}->{o}->{o}", mapping)
    mrk = node("{i}->({k}, {o})", mapping)
    mrke = node("{i}->[({k}, {o})]", mapping)
    output.append(e.Func("map_reduce_keyed", mrk, reducer))
    output.append(e.Func("map_reduce_keyed_emit", mrke, reducer))
    return output

def make_keyed_mapped(input, out, key):
    output = []
    mapping = {'i': input, 'o': out, 'k':key, 'v': '1'}
    reducer = node("{v}->{v}->{v}", mapping)
    mrk = node("{i}->({k}, {v})", mapping)
    mrke = node("{i}->[({k}, {v})]", mapping)
    f = node("[({k}, {v})] -> {o}", mapping)
    output.append(e.Func("map_reduce_keyed_map", mrk, reducer, f))
    output.append(e.Func("map_reduce_keyed_emit_map", mrke, reducer, f))
    return output

def make_mr(input, out):
    output = []
    mapping = {'i': input, 'o': out}
    reducer = node("{o}->{o}->{o}", mapping)
    mr = node("{i}->{o}", mapping)
    mre = node("{i}->[{o}]", mapping)
    output.append(e.Func("map_reduce", mr, reducer))
    output.append(e.Func("map_reduce_emit", mre, reducer))
    return output

def make_mapped(input, out):
    output = []
    mapping = {'i': input, 'o': out, 'v': '1'}
    reducer = node("{v}->{v}->{v}", mapping)
    mrm = node("{i}->{v}", mapping)
    mrem = node("{i}->[{v}]", mapping)
    mapper = node("{v}->{o}", mapping)
    output.append(e.Func("map_reduce_map", mrm, reducer, mapper))
    output.append(e.Func("map_reduce_emit_map", mrem, reducer, mapper))
    return output

# code for creating starting nodes
def create_start(input_str, output_str, key_str = None):
    output = []
    mapping = {'i': input_str, 'k': key_str, 'o': output_str}
    reducer = node("{o}->{o}->{o}", mapping)
    func = node("1->{o}", mapping)
    # if a key is provided, we use the keyed map-reduce forms
    if key_str:
        output += make_keyed(input_str, output_str, key_str)
        # what? keyed manipulations at the end?
        output += make_keyed_mapped(input_str, output_str, key_str)
    else:
        output += make_mr(input_str, output_str)
        # now lets get weird
        output += make_mapped(input_str, output_str)
    return output

# converts terms to executable python code
class CodeWriter(ExtendedVisitor):
    def __init__(self, module):
        self._module = module
        self._glob = module.__dict__.copy()
        self._glob.update(mr.__dict__)
    def __call__(self, node):
        return self.create(node)
    def create(self, node):
        ''' evaluates the appropriate string rep of expr in the signature module'''
        node_str = self.visit(node)
        return eval(node_str, self._glob)
    def generic_visit(self, node):
        raise RuntimeError
    def visit_app(self, node, depth=0):
        l, r = node.children
        return "{func}({args})".format(func=self.visit(l, depth),
                args=self.visit(r, depth))
    def visit_abs(self, node, depth=0):
        s, = node.children
        return "(lambda {var}: {code})".format(var="x_" + str(depth),
                code=self.visit(s, depth+1))
    def visit_un(self, node, depth=0):
        return "UN"
    def visit_var(self, node, depth=0):
        return "x_" + str(depth - node.value[0])
    def visit_func(self, node, depth=0):
        if node.value == "mapreduce":
            return "{func}({args})".format(func="lambda s: ",
                    args=", ".join(self.visit(c, depth) for c in node.children))
        return "{func}({args})".format(func=node.value,
                args=", ".join(self.visit(c, depth) for c in node.children))
        
