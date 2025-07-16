import sympy as sp

s = sp.Symbol("s", positive=True, real=True)

def is_necessarily_regular(Z_expr):
    return is_necessarily_regular_biquadratic(Z_expr)

def is_necessarily_regular_biquadratic(Z_expr):
    """Test whether Z(s) is regular using M&S algebraic test for biquadratic PR functions."""
    num, den = sp.fraction(Z_expr)

    num = sp.expand(num)
    den = sp.expand(den)

    ndeg = sp.degree(num, s)
    ddeg = sp.degree(den, s)
    if max(ndeg, ddeg) > 2:
        return False  # Not a biquadratic

    A, B, C = sp.Poly(num, s).all_coeffs()
    D, E, F = sp.Poly(den, s).all_coeffs()

    # pad to length 3
    A, B, C = [sp.sympify(c) for c in [A, B, C]]
    D, E, F = [sp.sympify(c) for c in [D, E, F]]

    sigma = B*E - (sp.sqrt(A*F) - sp.sqrt(C*D))**2
    if sigma.is_negative:
        return False

    Delta = A*F - C*D
    K = (A*F - C*D)**2 - (A*E - B*D)*(B*F - C*E)

    if K.is_nonpositive:
        return True

    Lambda1 = E*(B*F - C*E) - F*Delta
    Lambda2 = B*(A*E - B*D) - A*Delta
    Lambda3 = D*Delta - E*(A*E - B*D)
    Lambda4 = C*Delta - B*(B*F - C*E)

    cond1 = Delta.is_nonnegative and Lambda1.is_nonnegative
    cond2 = Delta.is_nonnegative and Lambda2.is_nonnegative
    cond3 = Delta.is_nonpositive and Lambda3.is_nonnegative
    cond4 = Delta.is_nonpositive and Lambda4.is_nonnegative

    return cond1 or cond2 or cond3 or cond4

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
