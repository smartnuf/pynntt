# Descriptor Grammar Specification

This document defines the syntax and semantics of **network descriptor strings** used to represent two-terminal (one-port) RLC networks, and outlines proposed extensions for multiport networks.

## 1. Overview

Descriptors are symbolic expressions denoting passive circuits composed of resistors (R), inductors (L), and capacitors (C), interconnected using:

- **Series**: `+`
- **Parallel**: `|`
- **Bridge**: `</...>` notation
- **Parentheses**: `(...)` to disambiguate grouping

Each element or subnetwork is either atomic (`R`, `L`, `C`) or a compound formed by combining others via an operator. Descriptors are **fully parenthesized**, avoiding ambiguity from precedence rules.

---

## 2. Grammar (BNF)

```bnf
<descriptor> ::= <series_expr> | <bridge_expr>

<series_expr> ::= <parallel_expr> | '(' <series_expr> '+' <parallel_expr> ')'
<parallel_expr> ::= <primary_expr> | '(' <parallel_expr> '|' <primary_expr> ')'

<primary_expr> ::= 'R' | 'L' | 'C' | <bridge_expr> | '(' <series_expr> ')'

<bridge_expr> ::= '<(' <descriptor> '&' <descriptor> 
                  ')@(' <descriptor> '&' <descriptor> 
                  ')/' <descriptor> ')'
```

- `&` marks series legs of the bridge
- `@` separates the upper and lower legs
- `/` marks the bridging element

---

## 3. Operator Precedence

Precedence (high to low):

1. Atomic element (`R`, `L`, `C`)
2. Parentheses `(...)`
3. Bridge `</...>`
4. Parallel `|`
5. Series `+`

Associativity is **left-to-right**.

---

## 4. Component Identifier Allocation

In current usage, `R`, `L`, and `C` are **type-only** placeholders.

- At runtime, each occurrence is uniquely renamed (e.g., `R1`, `R2`, ...) to preserve symbolic identity and avoid accidental cancellation.
- In the future, descriptors may support **explicit identifiers** (e.g., `R1`, `L3`, `Cload`).

---

## 5. Proposed Extensions

### 5.1 Tee and Pi 3-Poles

Introduce new bracketed syntax:

#### Tee:
```text
T < left, mutual, right >
```
equivalent to:
```text
[ & <left> ] : [ / <mutual> ] : [ & <right> ]
```

#### Pi:
```text
P < left, mutual, right >
```
equivalent to:
```text
[ / <left> ] : [ & <mutual> ] : [ / <right> ]
```

- `:` denotes cascade of subnetworks
- Brackets `[...]` define roles (shunt or series)

Degenerate cases (e.g. `P < O, R, L >`) permitted using:
- `O` → open circuit (∞ impedance)
- `S` → short circuit (0 impedance)

### 5.2 Cascades

Define a cascade operator `:` to represent connection of multiport subnetworks:
```text
block1 : block2 : block3
```

Precedence: lowest (parsed right-associatively unless grouped)

---

## 6. Future Work

- Add support for symbolic assignment (e.g., `X = (R + L)`)
- Include two-port (ABCD matrix) structures
- Define grammar for network constraints and substitutions

---

## 7. Example Descriptors

| Type    | Descriptor                        | Comment                       |
|---------|-----------------------------------|-------------------------------|
| SP      | `(R + (L | C))`                   | standard series-parallel      |
| Bridge  | `<(R & L) @ (C & R) / L>`         | 5-element bridge              |
| Tee     | `T <R, L, R>`                     | symmetric RL tee              |
| Pi      | `P <C, R, C>`                     | classic CRC low-pass          |
| Cascade | `[ & R ] : [ / L ] : [ & R ]`     | tee rendered in brackets      |

---
