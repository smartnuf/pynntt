# Evaluation Semantics

ASTs are interpreted to compute different network properties.

## Impedance Evaluation
- Series: `Z1 + Z2`
- Parallel: `1 / (1/Z1 + 1/Z2)`
- Bridge: Uses known formula:
  ```
  Zin = (za*zb*zc + za*zb*zd + za*zc*zd + zb*zc*zd + (za+zb)(zc+zd)ze)
        / ((za+zc)(zb+zd) + (za+zb+zc+zd)ze)
  ```

## Regularity
- Evaluates impedance Z(jω), tests if real parts of Z and 1/Z have minima at 0 or ∞
- If so, the function is *not* regular

## Canonical Form
- Expanded and collected rational Z(s) = N(s)/D(s)
- Uses `sympy.expand`, `collect(..., evaluate=False)`, and custom formatting

## Schematic Rendering
- Optional: Drawn using `schemdraw` if requested