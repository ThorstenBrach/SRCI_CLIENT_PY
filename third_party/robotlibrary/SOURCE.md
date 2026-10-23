# RobotLibrary.xml

PLCopen-XML export of the open SRCI PLC library (Codesys/TwinCAT).

- Repository: https://github.com/ThorstenBrach/SRCI, library 1.5.2 (fixes F1 ... F107) plus the new
  function blocks MC_CreateServerLogFB / MC_ReadServerLogFB (F108, not yet committed in the library)
- Export: TwinCAT PLC Control 3.5.13.21, 2026-10-23, folder `Library` of the project
  SRCI_PLC_TEST_SUITE (`build.py --library source`); `RobotLibraryParameter.TOOL/FRAME/LOAD_MAX` = 20
  (was 16), like the SDK simulator
- License: MIT
- sha256: 91dd909c0ed9802d2a560dfd80fbd8180f9b430b986e86a694e2404f59e6af90

Used as the single source for the generated types in `src/srci/types/_generated`
(`python -m tools.plcopen_gen`). Do not edit by hand – replace with a new export
and regenerate.
