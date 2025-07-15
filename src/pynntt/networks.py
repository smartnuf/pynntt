"""
networks.py — Core logic for parsing, AST evaluation, impedance computation, and canonicalization
"""

import sympy as sp
import re

ELEMENTS = ['R', 'L', 'C']
s = sp.Symbol('s')


def is_atomic(expr):
    return isinstance(expr, str) and expr in ELEMENTS


def combine_series(Z1, Z2):
    return Z1 + Z2


def combine_parallel(Z1, Z2):
    return 1 / (1 / Z1 + 1 / Z2)


def eval_impedance(expr):
    counter = {'R': 0, 'L': 0, 'C': 0}

    def make_symbol(label):
        counter[label] += 1
        return sp.Symbol(f"{label}{counter[label]}", positive=True)

    def eval_recursive(e):
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
                za_expr, zb_expr = args[0][1], args[0][2]
                zc_expr, zd_expr = args[1][1], args[1][2]
                ze_expr = args[2]

                za = eval_recursive(za_expr)
                zb = eval_recursive(zb_expr)
                zc = eval_recursive(zc_expr)
                zd = eval_recursive(zd_expr)
                ze = eval_recursive(ze_expr)

                num = (za * zb * zc + za * zb * zd + za * zc * zd +
                       zb * zc * zd + (za + zb) * (zc + zd) * ze)
                den = (za + zc) * (zb + zd) + (za + zb + zc + zd) * ze
                return num / den

        raise ValueError(f"Unrecognized structure: {e}")

    return eval_recursive(expr)


def parse_descriptor(s):
    s = s.strip()
    tokens = re.findall(r'[RLC()]|[+|/<>@&]', s)

    def parse_expr(tokens):
        def parse_primary():
            tok = tokens.pop(0)
            if tok == '(': e = parse_expr(tokens); assert tokens.pop(0) == ')'; return e
            elif tok == '<':
                assert tokens.pop(0) == '('; a = parse_expr(tokens); assert tokens.pop(0) == '&'; b = parse_expr(tokens)
                assert tokens.pop(0) == ')'; assert tokens.pop(0) == '@'; assert tokens.pop(0) == '('; c = parse_expr(tokens)
                assert tokens.pop(0) == '&'; d = parse_expr(tokens); assert tokens.pop(0) == ')'; assert tokens.pop(0) == '/'
                e = parse_expr(tokens); assert tokens.pop(0) == '>'
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


def canonical_form(Z_expr):
    num, den = sp.fraction(sp.together(Z_expr.expand()))
    num = sp.expand(num)
    den = sp.expand(den)
    num_terms = sp.collect(num, s, evaluate=False)
    den_terms = sp.collect(den, s, evaluate=False)

    def format_terms(terms):
        formatted = []
        for power in sorted(terms, key=lambda x: -sp.degree(x, gen=s)):
            coeff = sp.simplify(terms[power])
            if power == s:
                formatted.append(f"{coeff}*s")
            elif power == s**0:
                formatted.append(str(coeff))
            else:
                formatted.append(f"{coeff}*{power}")
        return ' + '.join(formatted)

    return f"({format_terms(num_terms)}) / ({format_terms(den_terms)})"
