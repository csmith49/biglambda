from inspect import signature, getdoc
from importlib import machinery
from . import e
from . import t
from .typeparser import parse_type

# component class - for dynamically loaded code objects 
class Component(object):
    def __init__(self, function):
        self._function = function
        self._signature = signature(function)
        
    @property
    def term_repr(self):
        kids = [e.Un(type) for type in self.input_types]
        return e.Func(self.name, *kids)

    @property
    def name(self):
        return self._function.__name__

    @property
    def arity(self):
        return len(self.input_types)

    @property
    def input_types(self):
        if not hasattr(self, "_inputs"):
            parameters = self._signature.parameters
            annotations = [parameters[p].annotation for p in list(parameters)]
            self._inputs = [parse_type(a) for a in annotations]
        return self._inputs

    @property
    def return_type(self):
        if not hasattr(self, "_output"):
            annotation = self._signature.return_annotation
            self._output = parse_type(annotation)
        return self._output

    @property
    def type(self):
        if not hasattr(self, "_type"):
            if self.arity == 0:
                self._type = self.return_type
            elif self.arity == 1:
                self._type = t.Func(self.input_types[0], self.return_type)
            else:
                base = self.return_type
                for i_type in reversed(self.input_types):
                    base = t.Func(i_type, base)
                self._type = base
        return self._type

    @property
    def encoding(self):
        return getdoc(self._function)

    def __str__(self):
        return str(self.type)
    
    def __repr__(self):
        return str(self)

def generate_resources(sig, rules = None):
    if hasattr(generate_resources, "output"):
        return getattr(generate_resources, "output")
    module = machinery.SourceFileLoader('signature', sig).load_module()
    signature = []
    for name in filter(lambda s: "__" not in s, dir(module)):
        signature.append(Component(getattr(module, name)))
    setattr(generate_resources, "output", (signature, module))
    return signature, module
