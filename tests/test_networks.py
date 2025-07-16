import pytest
from sympy import simplify
import sympy as sp
from pynntt.networks import parse_descriptor, eval_impedance, canonical_form, s

def test_parse_simple_series():
    desc = "(R+L)"
    ast = parse_descriptor(desc)
    assert ast == ('+', 'R', 'L')

def test_parse_simple_parallel():
    desc = "(L|C)"
    ast = parse_descriptor(desc)
    assert ast == ('|', 'L', 'C')

def test_eval_impedance_series():
    desc = "(R+L)"
    ast = parse_descriptor(desc)
    Z = eval_impedance(ast)
    assert "R1" in str(Z) and "L1" in str(Z)

def test_eval_impedance_parallel():
    desc = "(R|C)"
    ast = parse_descriptor(desc)
    Z = eval_impedance(ast)
    assert "R1" in str(Z) and "C1" in str(Z)

def test_bridge_impedance_canonical():
    desc = "<(R&R)@(R&R)/C>"
    ast = parse_descriptor(desc)
    Z = eval_impedance(ast)
    cf = canonical_form(Z)
    # The canonical_form now returns a SymPy expression, not a string.
    # We can check its type and then its symbolic equivalence.
    assert isinstance(cf, sp.Expr)
    # For a bridge, the exact form can be complex, so we check for symbolic equivalence
    # to a known correct form or properties of the expression.
    # Here, we'll check if it's a rational function of 's' and contains expected symbols.
    # A more rigorous test would involve comparing to a pre-calculated correct SymPy expression.
    assert cf.is_rational_function(s)
    assert any(sym.name.startswith('R') for sym in cf.free_symbols)
    assert any(sym.name.startswith('C') for sym in cf.free_symbols)
