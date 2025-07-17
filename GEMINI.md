# Gemini Collaboration Guide for pynntt

This document outlines the objectives of this project as well as the 
development workflow and coding style, conventions, and practices for 
using Gemini to co-develop the `pynntt` project.

## Project Overview

Pynntt is a Python project for network theory. It uses a custom descriptor 
language to define and analyze RLC two-pole networks. This will be extened 
to include language to support other types of elements, such as mutual 
coupling, as well as other network theoretical constructs for passive, 
active, and non-reciprocal networks.

The motivation for introducing the tools and libries in this project is to
support the developemnt of new results in network theory that will be useful
in sythesis of passive transformerless netowrks and the calibration of 
measurement systems. Beyond that we are keen that the pynntt should provide
useful facilites useful for network description, analysis, sythesis, 
visualisation. We forsee the need for pynntt to be able to : 

* **Parse two-pole descriptors into an AST**
* **Generate a two pole descriptor from a two-pole AST**
* **Estimate bounds for the size of a set two-pole** that match cirtain 
   criterea (say, f.e., all distinct two-poles constructable from a subset 
   components of given set). 
* **Enumerate a set of two-poles** (generate descriptors) that match cirtain 
   ciritera.
* **Compute the impedance of a two-pole**
* **Compute the regularity of a two-pole**
* **Compute the existance of a necessarily regular recursave decomposition** 
  of a two-pole.
* **Compute the universality of a necessarily regular recursave decomposition** 
  of a two-pole.
* **Generate two-poles using critera for intrinsically regular compositions**
* **Compute the realisability set** of a given two-pole.
* **Compute equivance of realisability sets two two-poles**.
* **Compute the dual of a two-pole**
* **Compute the frequency inverse of a two-pole**
* **Compute the orbit of a two-pole** in terms of duals, and fquencey 
   inversion.
* **Partition a set of two-poles** into equivalance classes and orbits.
* **Generate sets of two-poles** that cover a cirtain parameter space.
* **Visualse two-poles schematically**
* **Visualise the realisable parameter space of a two-pole**
* **Compute cut sets, paths and loops in two-poles**
* **Visualise cut sets, paths and loops in two-poles**
* **Compute potential for autonomy in two-poes**
* **Compute determinants and cofactors for immittance** for analysis of a 
    two-pole as an n-pole of maximum dimension.
* **Compute the 


## Development Workflow

1.  **Parsing:** The core of the project is the `parse_descriptor` function 
    in `src/pynntt/networks.py`. Any changes to the descriptor grammar in 
    `doc/descriptor_grammar.md` must be reflected in the parser.
2.  **Evaluation:** The `eval_impedance` function evaluates the AST produced 
    by the parser. New network elements or structures will require extending 
    this function.
3.  **Testing:** All new features or bug fixes must be accompanied by `pytest` 
    tests in the `tests/` directory. Use the existing tests in 
    `tests/test_networks.py` as a template.

## Coding Style

*   **Formatting:** Adhere to the `snake_case` convention for all Python code. 
    * Use a single space around all operators and inside parentheses and 
    brackets. 
    * Keep text lines to no more that 78 characters in length, where possible.
*   **Imports:** Use `import sympy as sp`.
*   **Docstrings:** Use simple, single-line docstrings for functions where 
    the purpose is clear from the name.
*   **Language:** Use English English for spelling and grammar. Avoid words like "utilize" when "use" will suffice.


## Project Management

*   **TODO List:** Refer to `TODO.md` for a comprehensive list of tasks, issues, and future enhancements for the project.

## Code Quality Tools

To ensure code quality, consistency, and correctness, the `pynntt` project uses the following tools:

*   **`black` (Code Formatter):**
    *   **Purpose:** Automatically formats Python code to conform to PEP 8 style guidelines, ensuring consistent code style across the project.
    *   **Usage:** Typically run from the command line as `black .` (to format all Python files in the current directory and subdirectories).
    *   **Integration:** Recommended for use with pre-commit hooks to automatically format code before each commit.

*   **`flake8` (Linter):**
    *   **Purpose:** Checks Python code for style guide violations (PEP 8), programming errors (e.g., unused imports, undefined variables), and code complexity.
    *   **Usage:** Typically run from the command line as `flake8 .` (to lint all Python files in the current directory and subdirectories).
    *   **Integration:** Recommended for use with pre-commit hooks and as a step in CI/CD pipelines to enforce code quality standards.

*   **`mypy` (Static Type Checker):**
    *   **Purpose:** Performs static analysis of Python code to check for type errors based on type hints. This helps catch potential bugs before runtime and improves code readability and maintainability.
    *   **Usage:** Typically run from the command line as `mypy src/pynntt/` (to type-check the `pynntt` source code).
    *   **Integration:** Recommended for use with pre-commit hooks and as a step in CI/CD pipelines to ensure type correctness.

## Commands

*   **Run code quality checks:** `python tools/run_checks.py`
    *   This script runs `black --check`, `flake8`, and `mypy` to ensure code consistency, style, and type correctness.
*   **Run tests with coverage:** `pytest --cov=src/pynntt --cov-report=term-missing --cov-report=html tests/`
    *   **Coverage Goal:** Achieved 100% statement coverage for all Python source files in `src/pynntt/`. (Note: Minor reporting discrepancies by `pytest-cov` for complex conditional lines do not indicate functional gaps.)
