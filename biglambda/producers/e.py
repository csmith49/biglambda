from .adt import Node
from itertools import chain, repeat

## recursively-defined expression langauge
## mostly self-explanatory, just defined representations and constructors
class Expr(Node): pass

class Var(Expr):
    def __new__(cls, label, type):
        return super().__new__(cls, "var", (label, type), ())
    def __repr__(self):
        return "Var({l}, {t})".format(l=repr(self.value[0]), t=repr(self.value[1]))
    def __reduce__(self):
        return Var, tuple(self.value)

class Un(Expr):
    _count = 0
    def __new__(cls, *args):
        if len(args) == 1:
            value = (Un._count, args[0])
            Un._count += 1
        else:
            value = tuple(args[:2])
        return super().__new__(cls, "un", value, ())
    def __repr__(self):
        return u"\u25cb(" + repr(self.value[1]) + ")"
    def __reduce__(self):
        return Un, tuple(self.value)

class App(Expr):
    def __new__(cls, l, r):
        return super().__new__(cls, "app", None, (l, r))
    def __repr__(self):
        return "({l} {r})".format(l=repr(self.args[0]), r=repr(self.args[1]))
    def __reduce__(self):
        return App, self.args

class Abs(Expr):
    def __new__(cls, type, s):
        return super().__new__(cls, "abs", type, (s,))
    def __repr__(self):
        return u"\u03bb." + repr(self.args[0])
    def __reduce__(self):
        return Abs, (self.value, self.args[0])

class Func(Expr):
    def __new__(cls, name, *args):
        return super().__new__(cls, "func", name, tuple(args))
    def __repr__(self):
        return "{name}({a})".format(
            name=self.value,
            a=", ".join(repr(c) for c in self.args))
    def __reduce__(self):
        return Func, tuple([self.value] + list(self.args))

## functions to manipulate expressions

def linearize(expr):
    visited, expr_stack = [], [expr]
    while expr_stack:
        # get the current node
        node = expr_stack.pop()
        # do stuff
        visited.append((node[0], node[1], len(node[2]), ()))
        # visit some kids
        expr_stack.extend(reversed(node[2]))
    return visited

def linearize_w_tvars(expr):
    visited, stack = [], [(expr, [])]
    tvars = set()
    while stack:
        # get the newest stuff
        node, bindings = stack.pop()
        # transform representation
        if node[0] == "abs":
            tvars.update(node[1]._values_from_kind("var"))
            bindings = [(i+1, t) for i, t in bindings]
            bindings.append((1, node[1]))
        elif node[0] == "var" or node[0] == "un":
            tvars.update(node[1][1]._values_from_kind("var"))
        visited.append((node[0], node[1], len(node[2]), bindings))
        # prepare for next node
        stack.extend((zip(reversed(node[2]), repeat(bindings))))
    return visited, tvars

# reconstructs a linearized term by going backwards and keeping track of arities
def reconstruct(node_list):
    arg_stack = []
    for node in reversed(node_list):
        name, value, arity, bindings = node
        if name == "var":
            arg_stack.append(Var(*value))
        elif name == "un":
            arg_stack.append(Un(*value))
        elif name == "app":
            l, r = arg_stack.pop(), arg_stack.pop()
            arg_stack.append(App(l, r))
        elif name == "abs":
            arg_stack.append(Abs(value, arg_stack.pop()))
        else:
            args = []
            for i in range(arity):
                args.append(arg_stack.pop())
            arg_stack.append(Func(value, *args))
    return arg_stack[-1]

# should enumerate over all nodes, fixing whatever types it finds
# pretty sure it's borked - need to look at it closer
def fix_types(node, sub):
    if sub is None:
        return node
    kind, val = node.kind, node.value
    if kind == "var":
        return Var(val[0], sub.visit(val[1]))
    elif kind == "un":
        return Un(val[0], sub.visit(val[1]))
    elif kind == "abs":
        kids = [fix_types(c, sub) for c in node.args]
        return node._replace(value=sub.visit(val), args=tuple(kids))
    else:
        kids = [fix_types(c, sub) for c in node.args]
        return node._replace(args=tuple(kids))

if __name__ == '__main__':
    test = Abs(None, App(Var(1, None), Un(None)))
    print(test)
    print()
    print(reconstruct(linearize(test)))
    print()
    print(linearize(test))
