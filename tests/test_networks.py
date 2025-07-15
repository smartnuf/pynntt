import pytest
from sympy import simplify
from pynntt.networks import parse_descriptor, eval_impedance, canonical_form

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
    assert isinstance(cf, str)
    assert "/" in cf and "*" in cf
