import sympy as sp
from typing import Any

s = sp.Symbol("s", positive=True, real=True)

def is_necessarily_regular(Z_expr: sp.Expr) -> bool:
    """
    Determines if a given impedance expression is necessarily regular.
    Currently, this defers to the biquadratic regularity test.
    """
    return is_necessarily_regular_biquadratic(Z_expr)

def is_necessarily_regular_biquadratic(Z_expr: sp.Expr) -> bool:
    """
    Tests whether a biquadratic PR function Z(s) is regular using the Morelli & Smith algebraic test.

    Args:
        Z_expr: The SymPy expression for the impedance.

    Returns:
        True if the function is necessarily regular, False otherwise.
    """
    num, den = sp.fraction(Z_expr)

    num = sp.expand(num)
    den = sp.expand(den)

    ndeg = sp.degree(num, s)
    ddeg = sp.degree(den, s)
    if max(ndeg, ddeg) > 2:
        return False  # Not a biquadratic

    # Ensure coefficients are extracted correctly, padding with zeros if necessary
    # For a biquadratic, the polynomials are of degree at most 2.
    # sp.Poly(poly, var).all_coeffs() returns coeffs from highest to lowest degree.
    # We need to ensure we have A, B, C and D, E, F for degree 2 polynomials.
    # If degree is less than 2, sp.Poly will return fewer coefficients.
    # We need to pad them to ensure A,B,C and D,E,F are always present.

    num_coeffs = sp.Poly(num, s).all_coeffs()
    den_coeffs = sp.Poly(den, s).all_coeffs()

    A, B, C = (sp.sympify(0), sp.sympify(0), sp.sympify(0))
    D, E, F = (sp.sympify(0), sp.sympify(0), sp.sympify(0))

    if len(num_coeffs) == 3: A, B, C = num_coeffs
    elif len(num_coeffs) == 2: B, C = num_coeffs
    elif len(num_coeffs) == 1: C = num_coeffs[0]

    if len(den_coeffs) == 3: D, E, F = den_coeffs
    elif len(den_coeffs) == 2: E, F = den_coeffs
    elif len(den_coeffs) == 1: F = den_coeffs[0]

    # Convert to SymPy expressions to ensure proper symbolic operations
    A, B, C = sp.sympify(A), sp.sympify(B), sp.sympify(C)
    D, E, F = sp.sympify(D), sp.sympify(E), sp.sympify(F)

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

def is_necessarily_regular_by_definition_optimised(Z_expr: sp.Expr) -> bool:
    """
    Optimized symbolic test for regularity of Z(s) based on the definition.
    Avoids full Re[Z(jω)] calculation by using ω → √w substitution.

    Args:
        Z_expr: The SymPy expression for the impedance.

    Returns:
        True if the function is necessarily regular, False otherwise.
    """
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

    def finite_min(expr: sp.Expr) -> sp.Expr | None:
        deriv = sp.simplify(sp.diff(expr, w))
        # Handle cases where derivative is constant (e.g., linear functions)
        if deriv == 0:
            return expr.subs(w, 0) # Or any point, as it's constant

        # Solve for critical points where derivative is zero
        # Use sp.numer to get the numerator of the derivative if it's a fraction
        roots = sp.solve(sp.numer(deriv), w, domain=sp.S.Reals)
        finite_roots = [r for r in roots if r.is_real and r.is_positive and r != sp.oo]

        values = [expr.subs(w, r) for r in finite_roots]
        return sp.Min(*values) if values else None

    min_Z_re = finite_min(Z_re)
    min_Y_re = finite_min(Y_re)

    # A function is regular if its real part (or its inverse's) has its minimum at 0 or infinity.
    # If there are no finite minima, then the function is regular by this criterion.
    z_reg = (min_Z_re is None) or (Z_lim_0 <= min_Z_re and Z_lim_inf <= min_Z_re)
    y_reg = (min_Y_re is None) or (Y_lim_0 <= min_Y_re and Y_lim_inf <= min_Y_re)

    return z_reg or y_reg


def is_necessarily_regular_by_definition(Z_expr: sp.Expr) -> bool:
    """
    Tests whether Z(s) is regular based on the definition (slower, more direct approach).

    Args:
        Z_expr: The SymPy expression for the impedance.

    Returns:
        True if the function is necessarily regular, False otherwise.
    """
    # Use a fresh symbol for omega to avoid conflicts with 'w' from other functions
    omega = sp.Symbol("omega", positive=True, real=True)
    j = sp.I

    Z = Z_expr.subs(s, j * omega)
    Y = 1 / Z

    Z_re = sp.re(sp.simplify(Z))
    Y_re = sp.re(sp.simplify(Y))

    try:
        Z_lim_0 = sp.limit(Z_re, omega, 0)
        Z_lim_inf = sp.limit(Z_re, omega, sp.oo)
        Y_lim_0 = sp.limit(Y_re, omega, 0)
        Y_lim_inf = sp.limit(Y_re, omega, sp.oo)
    except Exception:
        return False

    def finite_min(expr: sp.Expr) -> sp.Expr | None:
        deriv = sp.simplify(sp.diff(expr, omega))
        if deriv == 0:
            return expr.subs(omega, 0)

        roots = sp.solve(sp.numer(deriv), omega, domain=sp.S.Reals)
        finite_roots = [r for r in roots if r.is_real and r.is_positive and r != sp.oo]

        values = [expr.subs(omega, r) for r in finite_roots]
        return sp.Min(*values) if values else None

    min_Z_re = finite_min(Z_re)
    min_Y_re = finite_min(Y_re)

    z_reg = (min_Z_re is None) or (Z_lim_0 <= min_Z_re and Z_lim_inf <= min_Z_re)
    y_reg = (min_Y_re is None) or (Y_lim_0 <= min_Y_re and Y_lim_inf <= min_Y_re)

    return z_reg or y_reg
