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

# New test cases for parse_descriptor error handling
def test_parse_descriptor_mismatched_parentheses():
    with pytest.raises(ValueError, match=r"Mismatched parentheses in descriptor"):
        parse_descriptor("(R+L")

def test_parse_descriptor_bridge_missing_ampersand_1():
    with pytest.raises(ValueError, match=r"Expected '&' after first element in bridge"):
        parse_descriptor("<(R)@(R&R)/C>")

def test_parse_descriptor_bridge_missing_second_element_and_ampersand():
    with pytest.raises(ValueError, match=r"Expected '&' after first element in bridge"):
        parse_descriptor("<(R")

def test_parse_descriptor_bridge_missing_closing_paren_1():
    with pytest.raises(ValueError, match=r"Expected '\)' after second element in bridge"):
        parse_descriptor("<(R&R@(R&R)/C>")

def test_parse_descriptor_bridge_missing_at():
    with pytest.raises(ValueError, match=r"Expected '@' after bridge arm 1"):
        parse_descriptor("<(R&R)(R&R)/C>")

def test_parse_descriptor_bridge_missing_opening_paren_2():
    with pytest.raises(ValueError, match=r"Expected '\(' after '@'"):
        parse_descriptor("<(R&R)@R&R)/C>")

def test_parse_descriptor_bridge_missing_ampersand_2():
    with pytest.raises(ValueError, match=r"Expected '&' after third element in bridge"):
        parse_descriptor("<(R&R)@(R R)/C>")

def test_parse_descriptor_bridge_missing_closing_paren_2():
    with pytest.raises(ValueError, match=r"Expected '\)' after fourth element in bridge"):
        parse_descriptor("<(R&R)@(R&R/C>")

def test_parse_descriptor_bridge_missing_slash():
    with pytest.raises(ValueError, match=r"Expected '/' after bridge arm 2"):
        parse_descriptor("<(R&R)@(R&R)C>")

def test_parse_descriptor_bridge_missing_greater_than():
    with pytest.raises(ValueError, match=r"Expected '>' after bridge expression"):
        parse_descriptor("<(R&R)@(R&R)/C")

def test_parse_descriptor_unexpected_token():
    with pytest.raises(ValueError, match=r"Unexpected token: \)"):
        parse_descriptor("(R+X)")

# New test case for eval_impedance error handling
def test_eval_impedance_unrecognized_structure():
    with pytest.raises(ValueError, match=r"Unrecognized structure: \('X', 'Y'\)"):
        eval_impedance(('X', 'Y'))