# RobotLibrary.xml

PLCopen-XML export of the open SRCI PLC library (Codesys/TwinCAT).

- Repository: https://github.com/ThorstenBrach/SRCI, library 1.5.3 (fixes F1 ... F108) plus the new
  function blocks MC_MoveDirectCamFB, MC_ReadAnalogOutputFB, MC_ReadSafeReferencePositionFB,
  MC_SafeReferencingFB (F109), and the ST fixes F110 ... F154
- Export: library 1.5.5.0, 2026-11-10 from the XAE Shell (PLCopen 3.5.13), repository SRCI (`RobotLibrary.xml`)
- License: MIT
- sha256: f5f292ace154abd6366a78c1d03e7e5a81f38d4a0dd1773122be2ef5db74a45f

Used as the single source for the generated types in `src/srci/types/_generated`
(`python -m tools.plcopen_gen`). Do not edit by hand – replace with a new export
and regenerate.
