# RobotLibrary.xml

PLCopen-XML export of the open SRCI PLC library (Codesys/TwinCAT).

- Repository: https://github.com/ThorstenBrach/SRCI, library 1.5.3 (fixes F1 ... F108) plus the new
  function blocks MC_MoveDirectCamFB, MC_ReadAnalogOutputFB, MC_ReadSafeReferencePositionFB,
  MC_SafeReferencingFB (F109), and the ST fixes F110 ... F153
- Export: library 1.5.5.0, 2026-11-07, repository SRCI (`RobotLibrary.xml`)
- License: MIT
- sha256: bf5963865386ae369ee2d7d15c448cbca0e2b0ba9b326f7cc6c07484ba09bf80

Used as the single source for the generated types in `src/srci/types/_generated`
(`python -m tools.plcopen_gen`). Do not edit by hand – replace with a new export
and regenerate.
