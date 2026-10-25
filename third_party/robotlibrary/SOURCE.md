# RobotLibrary.xml

PLCopen-XML export of the open SRCI PLC library (Codesys/TwinCAT).

- Repository: https://github.com/ThorstenBrach/SRCI, library 1.5.3 (fixes F1 ... F108) plus the new
  function blocks MC_MoveDirectCamFB, MC_ReadAnalogOutputFB, MC_ReadSafeReferencePositionFB,
  MC_SafeReferencingFB (F109, not yet committed in the library)
- Export: TwinCAT PLC Control 3.5.13.21, 2026-10-25, folder `Library` of the project
  SRCI_PLC_TEST_SUITE (`build.py --library source`); `RobotLibraryParameter.TOOL/FRAME/LOAD_MAX` = 20
  (was 16), like the SDK simulator
- License: MIT
- sha256: 2021bed3e05eb8908ada74bf8b213578036d7f8bb1c6f8d496f87e2dcec647f3

Used as the single source for the generated types in `src/srci/types/_generated`
(`python -m tools.plcopen_gen`). Do not edit by hand – replace with a new export
and regenerate.
