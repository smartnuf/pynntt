# Project Layout and Coding Standards

## Layout
- `main.py` — Descriptor parser, evaluator, canonical form
- `requirements.txt` — Dependencies
- `*.md` — Grammar, AST and semantic specifications

## Coding Conventions
- snake_case throughout (except Wolfram .wl)
- One space around operators and inside parentheses
- Minimal nesting and early return where possible

## Testing
- Golden-value tests on impedance, AST, canonical form
- Parser round-trip tests: descriptor → AST → descriptor
- Future: Use `pytest` with fixtures and parameterized tests