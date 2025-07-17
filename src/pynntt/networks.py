"""
networks.py — Core logic for parsing, AST evaluation, impedance computation, and canonicalization
"""

import sympy as sp
import re
from typing import Any
from pynntt.regularity import is_necessarily_regular

ELEMENTS = ['R', 'L', 'C']
s = sp.Symbol('s')


def is_atomic(expr: Any) -> bool:
    """
    Checks if an expression is an atomic element (R, L, or C).
    """
    return isinstance(expr, str) and expr in ELEMENTS


def combine_series(Z1: sp.Expr, Z2: sp.Expr) -> sp.Expr:
    """
    Combines two impedances in series.
    """
    return Z1 + Z2


def combine_parallel(Z1: sp.Expr, Z2: sp.Expr) -> sp.Expr:
    """
    Combines two impedances in parallel.
    """
    return 1 / (1 / Z1 + 1 / Z2)


def eval_impedance(expr: Any) -> sp.Expr:
    """
    Evaluates a network descriptor (AST) into a symbolic impedance expression.

    Args:
        expr: The network descriptor (AST).

    Returns:
        A SymPy expression representing the impedance.

    Raises:
        ValueError: If an unrecognized structure is encountered.
    """
    counter = {'R': 0, 'L': 0, 'C': 0}

    def make_symbol(label: str) -> sp.Symbol:
        counter[label] += 1
        return sp.Symbol(f"{label}{counter[label]}", positive=True)

    def eval_recursive(e: Any) -> sp.Expr:
        if is_atomic(e):
            sym = make_symbol(e)
            if e == 'R': return sym
            if e == 'L': return sym * s
            if e == 'C': return 1 / (sym * s)

        if isinstance(e, tuple):
            op, *args = e
            if op == '+':
                return combine_series(eval_recursive(args[0]), eval_recursive(args[1]))
            elif op == '|':
                return combine_parallel(eval_recursive(args[0]), eval_recursive(args[1]))
            elif op == '/':
                # Bridge network: <(Za & Zb) @ (Zc & Zd) / Ze>
                # This represents a bridge where Za, Zb, Zc, Zd are the arms and Ze is the cross-branch.
                # The formula for the impedance of a bridge network is complex and depends on the specific configuration.
                # This implementation assumes a specific bridge topology and its impedance formula.
                za_expr, zb_expr = args[0][1], args[0][2]
                zc_expr, zd_expr = args[1][1], args[1][2]
                ze_expr = args[2]

                za = eval_recursive(za_expr)
                zb = eval_recursive(zb_expr)
                zc = eval_recursive(zc_expr)
                zd = eval_recursive(zd_expr)
                ze = eval_recursive(ze_expr)

                # Impedance formula for a specific bridge configuration (e.g., Wheatstone bridge-like)
                # This formula might need to be generalized or made more robust for other bridge types.
                num = (za * zb * zc + za * zb * zd + za * zc * zd +
                       zb * zc * zd + (za + zb) * (zc + zd) * ze)
                den = (za + zc) * (zb + zd) + (za + zb + zc + zd) * ze
                return num / den

        raise ValueError(f"Unrecognized structure: {e}")

    return eval_recursive(expr)


def parse_descriptor(s: str) -> Any:
    """
    Parses a string descriptor of a network into an Abstract Syntax Tree (AST).

    Args:
        s: The string descriptor (e.g., "R+(L|C)").

    Returns:
        The AST representation of the network.

    Raises:
        ValueError: If the descriptor string is malformed or contains unexpected tokens.
    """
    s = s.strip()
    tokens = re.findall(r'[RLC()]|[+|/<>@&]', s)

    def parse_expr(tokens: list) -> Any:
        def parse_primary() -> Any:
            tok = tokens.pop(0)
            if tok == '(': 
                e = parse_expr(tokens)
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Mismatched parentheses in descriptor")
                return e
            elif tok == '<':
                if not tokens or tokens.pop(0) != '(':
                    raise ValueError("Expected '(' after '<'")
                a = parse_expr(tokens)
                if not tokens or tokens.pop(0) != '&':
                    raise ValueError("Expected '&' after first element in bridge")
                b = parse_expr(tokens)
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Expected ')' after second element in bridge")
                if not tokens or tokens.pop(0) != '@':
                    raise ValueError("Expected '@' after bridge arm 1")
                if not tokens or tokens.pop(0) != '(':
                    raise ValueError("Expected '(' after '@'")
                c = parse_expr(tokens)
                if not tokens or tokens.pop(0) != '&':
                    raise ValueError("Expected '&' after third element in bridge")
                d = parse_expr(tokens)
                if not tokens or tokens.pop(0) != ')':
                    raise ValueError("Expected ')' after fourth element in bridge")
                if not tokens or tokens.pop(0) != '/':
                    raise ValueError("Expected '/' after bridge arm 2")
                e = parse_expr(tokens)
                if not tokens or tokens.pop(0) != '>':
                    raise ValueError("Expected '>' after bridge expression")
                return ('/', ('&', a, b), ('&', c, d), e)
            elif tok in ELEMENTS: return tok
            else: raise ValueError(f"Unexpected token: {tok}")

        lhs = parse_primary()
        while tokens and tokens[0] in '+|':
            op = tokens.pop(0)
            rhs = parse_primary()
            lhs = (op, lhs, rhs)
        return lhs

    return parse_expr(tokens)


def canonical_form(Z_expr: sp.Expr) -> sp.Expr:
    """
    Converts a SymPy impedance expression into its canonical form (simplified fraction).

    Args:
        Z_expr: The SymPy expression for the impedance.

    Returns:
        A simplified SymPy expression representing the canonical form.
    """
    # Ensure the expression is expanded and combined
    Z_expanded = sp.together(Z_expr.expand())
    # Get numerator and denominator as SymPy expressions
    num, den = sp.fraction(Z_expanded)
    # Return the simplified SymPy expression
    return num / den
