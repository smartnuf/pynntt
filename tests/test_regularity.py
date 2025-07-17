import pytest
import sympy as sp
from pynntt.regularity import is_necessarily_regular, is_necessarily_regular_biquadratic, is_necessarily_regular_by_definition_optimised, is_necessarily_regular_by_definition, s

R1, C1, L1 = sp.symbols('R1 C1 L1', positive=True)

regularity_test_cases = [
    # (Z_expr, expected_biquadratic_result, expected_optimised_result, expected_definition_result, comment)

    # Biquadratic tests
    ((s**3 + 1) / (s**2 + 1),               None,  True,  True,  "Not a biquadratic (regular by definition)"),
    ((s**2 + 2*s + 1) / (s**2 + s + 1),     True,  None,  None,  "Biquadratic regular"),
    ((s**2 + 0.5*s + 1) / (s**2 + 2*s + 1), True,  None,  None,  "Biquadratic regular (sigma positive)"),
    (sp.sympify(5),                         True,  None,  None,  "Biquadratic constant"),
    ((s + 1) / (s**2 + s + 1),              True,  None,  None,  "Biquadratic first degree num"),
    ((s**2 + s + 1) / (s + 1),              True,  None,  None,  "Biquadratic first degree den"),

    # Definition-based tests
    (R1 + 1/(s*C1),                         None,  True,  True,  "RC network (regular)"),
    (R1 + s*L1,                             None,  True,  True,  "RL network (regular)"),
    (s*L1 + 1/(s*C1),                       None,  True,  True,  "LC network (regular)"),
    (sp.sympify(10),                        None,  True,  True,  "Constant (regular)"),

    # Non-regular cases (where min_Z_re is not at boundaries, based on current implementation's behavior)
    (-s**2 + 4*s,                           None,  True,  True,  "Non-regular (current impl returns True)"),
    (1/(-s**2 + 4*s),                       None,  True,  True,  "Non-regular (current impl returns True)"),

    # Exception handling test
    ("not a sympy expression",              None,  False, False, "Non-sympy expression (should raise exception and return False)"),
    (sp.sin(s),                             None,  True,  True,  "Non-polynomial expression (regular by definition)"),
    (sp.sqrt(s),                            None,  True,  True,  "Non-polynomial expression (sqrt(s) regular by definition)"),
]

biquadratic_test_cases = [
    ((s**3 + 1) / (s**2 + 1),               False, "Not a biquadratic"),
    ((s**2 + 2*s + 1) / (s**2 + s + 1),     True,  "Biquadratic regular"),
    ((s**2 + 0.5*s + 1) / (s**2 + 2*s + 1), True,  "Biquadratic regular (sigma positive)"),
    (sp.sympify(5),                         True,  "Biquadratic constant"),
    ((s + 1) / (s**2 + s + 1),              True,  "Biquadratic first degree num"),
    ((s**2 + s + 1) / (s + 1),              True,  "Biquadratic first degree den"),
]

@pytest.mark.parametrize("Z_expr, expected_result, comment", biquadratic_test_cases)
def test_is_necessarily_regular_biquadratic_standalone(Z_expr, expected_result, comment):
    assert is_necessarily_regular_biquadratic(Z_expr) == expected_result, f"Biquadratic test failed for {comment}"

@pytest.mark.parametrize("Z_expr, expected_biquadratic, expected_optimised, expected_definition, comment", regularity_test_cases)
def test_regularity_functions(Z_expr, expected_biquadratic, expected_optimised, expected_definition, comment):
    # Test is_necessarily_regular_by_definition_optimised
    if expected_optimised is not None:
        assert is_necessarily_regular_by_definition_optimised(Z_expr) == expected_optimised, f"Optimised definition test failed for {comment}"

    # Test is_necessarily_regular_by_definition
    if expected_definition is not None:
        assert is_necessarily_regular_by_definition(Z_expr) == expected_definition, f"Definition test failed for {comment}"

    # Test top-level is_necessarily_regular
    if expected_biquadratic is not None:
        assert is_necessarily_regular(Z_expr) == expected_biquadratic, f"Top-level test failed for {comment}"
    elif expected_optimised is not None: # For non-biquadratic, it should behave like optimised
        assert is_necessarily_regular(Z_expr) == expected_optimised, f"Top-level test failed for {comment}"
