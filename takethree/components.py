from inspect import signature, getdoc
from importlib import machinery
from . import e
from . import t
import ply.yacc as yacc
import ply.lex as lex

BASE_TYPES = []
CONSTRUCTED_EXPR = {}

tokens = ["BASE", "VAR", "QUANT",
            "COMMA", "TO", "OPEN",
            "CLOSE", "DOT", "OPENLIST",
            "CLOSELIST"]

t_ignore = ' \t'
t_BASE = r'[A-Z][a-z]*'
t_VAR = r'[0-9]+'
t_QUANT = r'@'
t_COMMA = r','
t_TO = r'->'
t_OPEN = r'\('
t_CLOSE = r'\)'
t_DOT = r'\.'
t_OPENLIST = r'\['
t_CLOSELIST = r'\]'

def t_error(te):
    print("Illegal character '{}'".format(te.value[0]))
    te.lexer.skip(1)

type_lexer = lex.lex()

def p_type(p):
    '''type : mono
            | poly'''
    p[0] = p[1]

def p_poly(p):
    '''poly : QUANT varlist DOT mono'''
    p[0] = t.Scheme(p[2], p[4])

def p_varlist(p):
    '''varlist : var
               | var COMMA varlist'''
    if len(p) is 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    
def p_mono(p):
    '''mono : OPEN mono CLOSE
            | base
            | var
            | constructor'''
    if len(p) is 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_constructor(p):
    '''constructor : function
                   | list
                   | pair'''
    p[0] = p[1]
    
def p_function(p):
    '''function : mono TO mono'''
    p[0] = t.Func(p[1], p[3])

def p_list(p):
    '''list : OPENLIST mono CLOSELIST'''
    p[0] = t.List(p[2])
    
def p_pair(p):
    '''pair : mono COMMA mono'''
    p[0] = t.Pair(p[1], p[3])

def p_base(p):
    '''base : BASE'''
    if p[1] not in BASE_TYPES:
        BASE_TYPES.append(p[1])
    p[0] = t.Base(p[1])
    
def p_var(p):
    '''var : VAR'''
    p[0] = t.Var(int(p[1]))

PARSER = yacc.yacc(tabmodule='typetab')

def parse_type(string):
    return PARSER.parse(string, lexer=type_lexer)

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
    if rules is None:
        return signature, None, module
    from . import norm
    normalizer = norm.generate_normalizer(rules)
    setattr(generate_resources, "output", (signature, normalizer, module))
    return signature, normalizer, module
