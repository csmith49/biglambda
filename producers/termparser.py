from . import kbo
import ply.yacc as yacc
import ply.lex as lex

tokens = ["BASE", "VAR", "COMMA", "TO", "OPEN", "CLOSE", "EQ"]

t_ignore = ' \t'
t_BASE = r'[a-z]+'
t_VAR = r'[0-9]+'
t_COMMA = r','
t_TO = r'->'
t_OPEN = r'\('
t_CLOSE = r'\)'
t_EQ = r'=='

def t_error(te):
	te.lexer.skip(1)

term_lexer = lex.lex()

def p_pair(p):
	'''pair : term TO term
			| term EQ term'''
	p[0] = (p[1], p[3])

def p_leaf(p):
	'''leaf : base
			| var'''
	p[0] = p[1]

def p_term(p):
	'''term : leaf
			| BASE OPEN termlist CLOSE'''
	if len(p) is 2:
		p[0] = p[1]
	else:
		p[0] = kbo.Func(p[1], *p[3])

def p_termlist(p):
	'''termlist : term
				| term COMMA termlist'''
	if len(p) is 2:
		p[0] = (p[1], )
	else:
		p[0] = tuple([p[1]] + list(p[3]))

def p_base(p):
	'''base : BASE'''
	p[0] = kbo.Func(p[1])

def p_var(p):
	'''var : VAR'''
	p[0] = kbo.Var(int(p[1]))

PARSER = yacc.yacc(tabmodule='termtab')

def parse_term(string):
	return PARSER.parse(string, lexer=term_lexer)