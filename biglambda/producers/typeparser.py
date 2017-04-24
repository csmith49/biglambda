from . import t
import ply.yacc as yacc
import ply.lex as lex

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
    p[0] = t.Base(p[1])
    
def p_var(p):
    '''var : VAR'''
    p[0] = t.Var(int(p[1]))

PARSER = yacc.yacc(tabmodule='typetab')

def parse_type(string):
    return PARSER.parse(string, lexer=type_lexer)