from pprint import pprint
from . import e
from . import t
from itertools import chain

def generate_expander(signature, normalizer = None):
    reduced_sig = [(c.type, c.term_repr, c.return_type) for c in signature]
    def get_expansions(type, bindings, tvars):
        output = []
        if type[0] == "var":
            for sig_type, sig_repr, sig_return in reduced_sig:
                clean = t.fresh_wrt(sig_type, tvars)
                expr = e.fix_types(sig_repr, clean)
                s = t.TypeSubstitution({type[1] : clean.visit(sig_return)})
                output.append( (expr, s) )
            for i, var_type in bindings:
                clean = t.fresh_wrt(var_type, tvars)
                v = e.Var(i, clean.visit(var_type))
                s = t.TypeSubstitution({type[1] : clean.visit(var_type)})
                output.append( (v, s) )
            return output
        elif type[0] == "func":
            l, r = type[2]
            expr = e.Abs(l, e.Un(r))
            return [(expr, None)]
        else:
            for sig_type, sig_repr, sig_return in reduced_sig:
                r_sub = t.fresh_wrt(sig_return, tvars)
                try:
                    s = t.match(type, r_sub.visit(sig_return))
                    output.append( (e.fix_types(e.fix_types(sig_repr, r_sub), s), None) )
                except t.UnifyError:
                    pass
            for i, var_type in bindings:
                '''try:
                    s = t.match(var_type, type)
                    output.append( (e.Var(i, var_type), s) )
                except t.UnifyError:
                    try:
                        s = t.match(type, var_type)
                        output.append( (e.Var(i, var_type), s) )
                    except t.UnifyError:
                        pass'''
                try:
                    s = t.unify(var_type, type)
                    output.append( (e.Var(i, var_type), s) )
                except t.UnifyError:
                    pass
            return output
    def expand(expr):
        linearized, tvars = e.linearize_w_tvars(expr)
        # find tvars and first index of un
        for i, flat in enumerate(linearized):
            if flat[0] == "un":
                expansions = get_expansions(flat[1][1], flat[3], tvars)
                index = i
                break
        # none found, we're so done
        else:
            return None
        # apply each expansion
        output = []
        for e_expr, e_sub in expansions:
            new_expr = e.reconstruct(list(chain(linearized[:index], e.linearize(e_expr), linearized[index+1:])))
            if (normalizer is None) or (normalizer(new_expr)):
                if e_sub is None:
                    output.append(new_expr)
                else:
                    output.append(e.fix_types(new_expr, e_sub))
            else:
                print("NORMALIZED: " + str(new_expr))
        return output
    return expand
