# AST Structure for Network Descriptors

Each parsed network descriptor is transformed into a Python nested tuple (AST). Examples:

- `"R"` → `"R"`
- `"R+L"` → `('+', 'R', 'L')`
- `"R|(L+C)"` → `('|', 'R', ('+', 'L', 'C'))`
- `"<(R&L)@(C&R)/L>"` → `('/', ('&', 'R', 'L'), ('&', 'C', 'R'), 'L')`

These ASTs are consumed by symbolic evaluation engines to compute:
- Impedance
- Regularity
- Canonical form
- Graphical schematic