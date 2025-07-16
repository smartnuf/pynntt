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
    Use a single space around all operators and inside parentheses and 
    brackets.
*   **Imports:** Use `import sympy as sp`.
*   **Docstrings:** Use simple, single-line docstrings for functions where 
    the purpose is clear from the name.

## Commands

*   **Run tests:** `pytest tests/`
