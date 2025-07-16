# Gemini Collaboration Guide for pynntt

This document outlines the conventions and practices for using Gemini to co-develop the `pynntt` project.

## Project Overview

Pynntt is a Python project for network theory analysis. It uses a custom descriptor language to define and analyze RLC networks.

## Development Workflow

1.  **Parsing:** The core of the project is the `parse_descriptor` function in `src/pynntt/networks.py`. Any changes to the descriptor grammar in `doc/descriptor_grammar.md` must be reflected in the parser.
2.  **Evaluation:** The `eval_impedance` function evaluates the AST produced by the parser. New network elements or structures will require extending this function.
3.  **Testing:** All new features or bug fixes must be accompanied by `pytest` tests in the `tests/` directory. Use the existing tests in `tests/test_networks.py` as a template.

## Coding Style

*   **Formatting:** Adhere to the `snake_case` convention for all Python code. Use a single space around all operators and inside parentheses and brackets.
*   **Imports:** Use `import sympy as sp`.
*   **Docstrings:** Use simple, single-line docstrings for functions where the purpose is clear from the name.

## Commands

*   **Run tests:** `pytest tests/`
