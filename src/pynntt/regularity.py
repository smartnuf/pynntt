import sympy as sp

s = sp.Symbol("s", positive=True, real=True)


def is_necessarily_regular_by_definition_optimised(Z_expr):
    """Optimized symbolic test for regularity of Z(s): avoids full Re[Z(jω)] via ω → √w substitution."""
    w = sp.Symbol("w", positive=True, real=True)
    sqrtw = sp.sqrt(w)
    j = sp.I

    Z = Z_expr.subs(s, j * sqrtw)
    Y = 1 / Z

    Z_re = sp.re(sp.simplify(Z))
    Y_re = sp.re(sp.simplify(Y))

    try:
        Z_lim_0 = sp.limit(Z_re, w, 0)
        Z_lim_inf = sp.limit(Z_re, w, sp.oo)
        Y_lim_0 = sp.limit(Y_re, w, 0)
        Y_lim_inf = sp.limit(Y_re, w, sp.oo)
    except Exception:
        return False

    def finite_min(expr):
        deriv = sp.simplify(sp.diff(expr, w))
        roots = sp.solve(sp.numer(deriv), w, domain=sp.S.Reals)
        finite_roots = [r for r in roots if r.is_real and r.is_positive]
        values = [expr.subs(w, r) for r in finite_roots]
        return sp.Min(*values) if values else None

    min_Z_re = finite_min(Z_re)
    min_Y_re = finite_min(Y_re)

    z_reg = Z_lim_0 <= min_Z_re or Z_lim_inf <= min_Z_re if min_Z_re is not None else True
    y_reg = Y_lim_0 <= min_Y_re or Y_lim_inf <= min_Y_re if min_Y_re is not None else True

    return z_reg or y_reg


def is_necessarily_regular_by_definition(Z_expr):
    """Return True if Z(s) is regular (slow definition-based version)."""
    symbols = list(Z_expr.free_symbols - {s})
    assumptions = {sym: sym.is_positive for sym in symbols}

    Z = Z_expr
    Y = 1 / Z

    Z_re = sp.re(Z.subs(s, sp.I * sp.Symbol("w", positive=True, real=True)))
    Y_re = sp.re(Y.subs(s, sp.I * sp.Symbol("w", positive=True, real=True)))

    try:
        Z_lim_0 = sp.limit(Z_re, sp.Symbol("w"), 0)
        Z_lim_inf = sp.limit(Z_re, sp.Symbol("w"), sp.oo)
        Y_lim_0 = sp.limit(Y_re, sp.Symbol("w"), 0)
        Y_lim_inf = sp.limit(Y_re, sp.Symbol("w"), sp.oo)
    except Exception:
        return False

    def finite_min(expr):
        w = sp.Symbol("w", positive=True, real=True)
        deriv = sp.simplify(sp.diff(expr, w))
        roots = sp.solve(sp.numer(deriv), w, domain=sp.S.Reals)
        finite_roots = [r for r in roots if r.is_real and r.is_positive]
        values = [expr.subs(w, r) for r in finite_roots]
        return sp.Min(*values) if values else None

    min_Z_re = finite_min(Z_re)
    min_Y_re = finite_min(Y_re)

    z_reg = Z_lim_0 <= min_Z_re or Z_lim_inf <= min_Z_re if min_Z_re is not None else True
    y_reg = Y_lim_0 <= min_Y_re or Y_lim_inf <= min_Y_re if min_Y_re is not None else True

    return z_reg or y_reg
