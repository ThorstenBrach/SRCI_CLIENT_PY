# Porting rules ST ↔ Python

Goal: a change in the PLC library (Structured Text) can be found and applied in
Python quickly – and vice versa.

1. **Same names.** Function block → class of the same name; `VAR_INPUT`/`VAR_OUTPUT`
   → attributes with the same names; `METHOD` → method with the same name.
   Enum and structure names are identical (they are generated, see below).
2. **Same step chains.** `CASE step OF` → `match` with the *same* step numbers.
   Error, warning and info ids are identical.
3. **Same file cut.** One Python module per ST POU; the folder structure follows
   `RobotLibrary/Library/POUs/...` (snake_case package names).
4. **Back reference.** Every ported module starts with
   `# ST-Source: <path relative to RobotLibrary/Library>  sha256: <hash>`.
   `python -m tools.st_drift <path to RobotLibrary/Library>` lists modules whose ST
   source changed since porting.
5. **`REFERENCE TO` / `VAR_IN_OUT`** are mapped to object references or small state
   objects – never to local copies of ints (a local `int` cannot be written back).
6. **Allowed deviations.** Duplication that only exists for ST syntax reasons
   (e.g. the seven data synchronisation step chains) may be implemented generically,
   keeping the step numbers and documenting the mapping to the ST code.

## Generated types

`src/srci/types/_generated` is generated from
`third_party/robotlibrary/RobotLibrary.xml` (PLCopen XML export of the PLC library):

```bash
python -m tools.plcopen_gen          # regenerate
python -m tools.plcopen_gen --check  # CI: fail if generated code is out of date
```

Never edit generated files by hand.
