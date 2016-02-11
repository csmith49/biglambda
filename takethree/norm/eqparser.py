from .meta import Meta
from .equations import Condition, Equation
import ply.yacc as yacc
import ply.lex as lex

tokens = ["ID", "EQ", "IN", "DEFINES",
            "COLON", "LPAREN", "RPAREN",
            "COMMA", "LBRACKET", "RBRACKET"]

t_ignore = ' \t\n'
t_ID = r'[A-Za-z]+'
t_EQ = r'=='
t_IN = r'<-'
t_DEFINES = r':='
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_error(te):
    print("Illegal character '{}'".format(te.value[0]))
    te.lexer.skip(1)

lexer = lex.lex()

#####################################################
## TIME TO PARSE
#####################################################

def p_input_sets(p):
    'start : set_descriptor'
    p[0] = p[1]

def p_input_eqs(p):
    'start : equation'
    p[0] = p[1]

## set description
def p_set_descriptor(p):
    'set_descriptor : ID DEFINES set'
    p[0] = ('set', p[1], p[3])

def p_set(p):
    'set : LBRACKET set_list RBRACKET'
    p[0] = p[2]

def p_set_list_base(p):
    'set_list : ID'
    p[0] = [p[1]]

def p_set_list_list(p):
    'set_list : ID COMMA set_list'
    p[0] = [p[1]] + p[3]
##################

## condition
def p_condition_base(p):
    'condition : ID IN ID'
    p[0] = [('cond', p[1], p[3])]

def p_condition_list(p):
    'condition : ID IN ID COMMA condition'
    p[0] = [('cond', p[1], p[3])] + p[5]
############

## term parsing
def p_arg_list_base(p):
    'arg_list : term'
    p[0] = [p[1]]

def p_arg_list_list(p):
    'arg_list : term COMMA arg_list'
    p[0] = [p[1]] + p[3]

def p_term_second_order(p):
    'term : ID LPAREN arg_list RPAREN'
    p[0] = Meta(*([p[1]] + p[3]))

def p_term_constant(p):
    'term : ID'
    p[0] = Meta(p[1])
###############

## equations
def p_equation(p):
    'equation : condition COLON term EQ term'
    p[0] = ('eq', p[1], p[3], p[5])

def p_equation_unconditional(p):
    'equation : term EQ term'
    p[0] = ('eq', [], p[1], p[3])
############

def p_error(p):
    print(p)

parser = yacc.yacc(tabmodule='eqparsing')

#####################################################
## TESTING
#####################################################

def parse_string(string):
    sets, equations = {}, []
    for line in string.split('\n'):
        result = parser.parse(line)
        if result[0] == "set":
            sets[result[1]] = result[2]
        if result[0] == "eq":
            equations.append(result)
    output = []
    for eq in equations:
        kind, conds, l, r = eq
        cond = Condition([])
        for c in conds:
            cond = cond.combine(Condition([([c[1]], sets[c[2]])]))
        output.append(Equation(cond, l, r))
    return output

def parse(file):
    sets, equations = {}, []
    with open(file, 'r') as f:
        for line in f.readlines():
            result = parser.parse(line)
            if result[0] == "set":
                sets[result[1]] = result[2]
            if result[0] == "eq":
                equations.append(result)
        output = []
        for eq in equations:
            kind, conds, l, r = eq
            cond = Condition([])
            for c in conds:
                cond = cond.combine(Condition([(c[1], sets[c[2]])]))
            output.append(Equation(cond, l, r))
    return output
