from collections import namedtuple
from itertools import chain, product
from functools import reduce

# base class for all adts
# extends namedtuples with some helpful functions
class Node(namedtuple("_Node", "kind value args")): 
    __slots__ = ()
    def __new__(cls, kind, value, args):
        for arg in args:
            if not isinstance(arg, Node):
                raise TypeError
        self = super().__new__(cls, kind, value, tuple(args))
        return self
    
    @property
    def arity(self):
        if not self.args:
            return 0
        return len(self.args)
    @property
    def children(self):
        return self.args.__iter__()
    # this seems to be having problems, not really used in code
    @property
    def values(self):
        if not hasattr(self.value, '__iter__'):
            v = (self.value,) 
        return chain([self.kind], self.value)

    # positions are lists of indices to follow
    def at_position(self, pos):
        term = self
        for index in pos:
            term = term.args[index]
        return term
    @property
    def positions(self):     
        # start out with only a reference to ourself
        pos = [[]]
        # iterate over all children
        for i, c in enumerate(self.children):
            pos += [[i] + p for p in c.positions]
        return pos

    # just replaces the indicated position with the value
    def _substitute(self, pos, value, current = None):
        if current is None:
            current = []
        if current == pos:
            return value
        else:
            kids = []
            for i, c in enumerate(self.children):
                kids.append(c._substitute(pos, value, current + [i]))
            return self._replace(args=kids)

    # wrapper for at_position
    def __getitem__(self, key):
        if isinstance(key, (list, tuple)):
            return self.at_position(key)
        else:
            return super().__getitem__(key)

    # picks out all values on nodes of a given kind
    def _values_from_kind(self, kind):
        if self[0] == kind:
            output = [self[1]]
        else:
            output = []
        for c in self[2]:
            output += c._values_from_kind(kind)
        return output


    def __reduce__(self):
        return Node, (self[0], self[1], self[2]), self.__dict__
    def __hash__(self):
        return super().__hash__()

# Base pattern for traversing recursively defined nodes
# uses introspection to select the right method
# as close to a case statement as we can get
class NodeVisitor:
    def _find_method(self, node):
        method_name = 'visit_' + node.kind
        method = getattr(self, method_name, None)
        if method is None:
            method = self.generic_visit
        return method
    def visit(self, node):
        method = self._find_method(node)
        return method(node)
    def generic_visit(self, node):
        subs = [self.visit(c) for c in node.children]
        return node._replace(args=subs)

class ExtendedVisitor(NodeVisitor):
    def visit(self, node, *args, **kwargs):
        method = self._find_method(node)
        return method(node, *args, **kwargs)
    def generic_visit(self, node, *args, **kwargs):
        subs = [self.visit(c) for c in node.children]
        return node._replace(args=subs)
