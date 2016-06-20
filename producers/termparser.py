from . import kbo
import ply.yacc as yacc
import ply.lex as lex

tokens = ["BASE", "VAR", "COMMA", "TO", "OPEN", "CLOSE", "EQ"]

t_ignore = ' \t'
t_BASE = r'[A-Z][a-z]*'
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

def p_term_base(p):
	'''term : BASE'''
	p[0] = kbo.Func(p[1], ())

def p_term_var(p):
	'''term : VAR'''
	p[0] = kbo.Var(p[1])

def p_term(p):
	'''term : base OPEN termlist CLOSE'''
	p[0] = kbo.Func(p[1], p[3])

def p_termlist(p):
	'''termlist : term
				| term COMMA termlist'''
	if len(p) is 2:
		p[0] = (p[1], )
	else:
		p[0] = tuple([p[1]] + list(p[3]))

PARSER = yacc.yacc(tabmodule='termtab')

def parse_term(string):
	return PARSER.parse(string, lexer=term_lexer)