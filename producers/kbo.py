from .e import linearize
from .adt import Node

#------------------------------------------------------------------------------
# data types for rules
#------------------------------------------------------------------------------
class Pattern(Node): pass

class Var(Pattern):
	def __new__(cls, value):
		return super().__new__(cls, "var", value, ())
	def __reduce__(self):
		return Var, tuple(self.value)

class Func(Pattern):
	def __new__(cls, name, *args):
		return super().__new__(cls, "func", name, tuple(args))
	def __reduce__(self):
		return Func, tuple([self.value + list(self.args)])

#------------------------------------------------------------------------------
# we better be matching
#------------------------------------------------------------------------------
def match(expr, pattern):
	sub = Substitution()
	worklist = [(expr, pattern)]
	while worklist:
		e, p = worklist.pop()
		e, p = e, sub(p)
		if p[0] == "var":
			sub[p] = e
		elif e[1] == p[1]:
			worklist += list(zip(e.children, p.children))
		else:
			return None
	return sub

class Substitution(object):
	def __init__(self):
		self._dict = {}
	def __call__(self, pattern):
		if pattern[0] == "var":
			try:
				return self._dict[pattern[1]]
			except KeyError:
				return pattern
		else:
			return pattern._replace(args=tuple(self(p) for p in pattern.children))
	def __setitem__(self, key, value):
		self._dict[key[1]] = value

#------------------------------------------------------------------------------
# let's get on these rules
#------------------------------------------------------------------------------
class Rule(object):
	def __init__(self, lhs, rhs, order=None):
		self.lhs = lhs
		self.rhs = rhs
		self.order = order
	def _applies(self, expr):
		worklist = [expr]
		while worklist:
			e = worklist.pop()
			sub = match(e, self.lhs)
			if sub is not None:
				return True
			worklist += list(e.children)
		return False
	def _ordered_applies(self, expr):
		worklist = [expr]
		while worklist:
			e = worklist.pop()
			sub_l = match(e, self.lhs)
			if sub_l is not None:
				if self.order(sub_l(self.lhs), sub_l(self.rhs)):
					return True
			sub_r = match(e, self.rhs)
			if sub_r is not None:
				if self.order(sub_r(self.rhs), sub_r(self.lhs)):
					return True
			worklist += list(e.children)
		return False
	def applies(self, expr):
		if self.order is not None:
			return self._ordered_applies(expr)
		else:
			return self._applies(expr)

#------------------------------------------------------------------------------
# storing information (and computing) the kbo
#------------------------------------------------------------------------------
class Weight(object):
	def __init__(self, weights):
		self._weights = weights
	def __call__(self, term):
		if term[0] == "var":
			return term[1][0]
		elif term[0] == "un":
			return self._weights[0]
		elif term[0] == "abs" or term[0] == "app":
			out = self._weights[0] + 1
		else:
			out = self._weights[term[1]]
		for t in term.children:
			out += self(t)
		return out

class Precedence(object):
	def __init__(self, precedences):
		self._precedences = precedences
	def __call__(self, term):
		if term[0] == "abs" or term[0] == "app":
			return 0
		else:
			return self._precedences[term[1]]	

def gt_kbo(s, t, W, P):
	# check variable counts! (not yet implemented)
	if W(s) > W(t):
		return True
	elif W(s) == W(t):
		if P(s) > P(t):
			return True
		elif P(s) == P(t) and s[0] == t[0]:
			# recurse lexicographically
			for x, y in zip(s.children, t.children):
				if x == y:
					pass
				elif gt_kbo(x, y, W, P):
					return True
				else:
					break
		if t[0] == "un" and s != t:
			# have to check linearity of s (singly arity functions and t)
			for kind, value, arity, bindings in linearize(s):
				if kind == "var":
					break
				elif kind == "un":
					if value != t[1][0]:
						break
				elif kind == "app":
					break
				elif kind == "func" and arity != 1:
					break
			else:
				return True

#------------------------------------------------------------------------------
# we can also construct normalizers!
#------------------------------------------------------------------------------
class Normalizer(object):
	def __init__(self, sexpr):
		pass
	def __call__(self, expr):
		for rule in self.rules:
			if rule.applies(expr):
				return True
		return False
