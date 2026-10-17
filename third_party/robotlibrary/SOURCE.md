# RobotLibrary.xml

PLCopen-XML export of the open SRCI PLC library (Codesys/TwinCAT).

- Repository: https://github.com/ThorstenBrach/SRCI, branch `bugfix/st-fixes` (working copy, not
  yet committed) - contains the fixes F1 ... F103 of this project
- Export: TwinCAT PLC Control 3.5.13.21, 2026-10-17 (project name in the export: SRCI_PLC_TEST,
  library source copied from there; `RobotLibraryParameter.TOOL/FRAME/LOAD_MAX` = 20 of the test
  project, the generator keeps the library default 16, see `tools/plcopen_gen/overrides.py`)
- License: MIT
- sha256: 321833d31319a117c8ca26440af7f91bdb5c460d6611c197e7cbea6a0ae253c5

Used as the single source for the generated types in `src/srci/types/_generated`
(`python -m tools.plcopen_gen`). Do not edit by hand – replace with a new export
and regenerate.
