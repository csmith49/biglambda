from .components import generate_resources, parse_type
from .adt import ExtendedVisitor
from . import e
from . import t
from .data import parse_data_types, parse_examples, parse_metric, parse_reducer_type
from .expansion import generate_expander
from .checker import reducer_check
from itertools import chain
from functools import reduce
from collections import defaultdict

# converts terms to executable python code
class CodeWriter(ExtendedVisitor):
    def __init__(self, module):
        self._module = module
        self._glob = module.__dict__.copy()
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
        return "{func}({args})".format(func=node.value,
                args=", ".join(self.visit(c, depth) for c in node.children))
