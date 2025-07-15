# Descriptor Grammar Specification

This grammar describes how two-terminal (1-port) passive RLC networks are encoded as symbolic descriptors. These descriptors can be parsed into abstract syntax trees (ASTs) and evaluated symbolically or visually.

## Atomic Elements
- `R`, `L`, `C` represent resistors, inductors, capacitors.

## Compositional Operators
- Series: `+`
- Parallel: `|`
- Bridge: `<(a&b)@(c&d)/e>`  
  Represents a bridge where:
  - one path from terminal to terminal is a-b
  - another path is c-d
  - e bridges between the midpoints

## Grouping
- Use `(...)` for grouping precedence.
- Bridge descriptors must be fully parenthesized:
  ```
  <(R1&R2)@(R3&R4)/R5>
  ```

## Future Extensions
- Support explicit component identifiers like `R1`, `L2`
- Allow aliases and constrained substitutions
- Support for two-port descriptors