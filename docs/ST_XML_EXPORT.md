# Transfer of the fixes into the PLC library (PLCopen XML)

The Python port corrects the ST code of the PLC library while it reads
`third_party/robotlibrary/RobotLibrary.xml` (source patches in `tools/st2py/config.py`, type
corrections in `tools/plcopen_gen/overrides.py`). `tools.st2py.export_xml` writes exactly these
corrections back into the XML, so they can be imported into the TwinCAT / Codesys project:

```bash
python -m tools.st2py.export_xml -o RobotLibrary_fixed.xml --verify
```

* Only the corrected objects change; all others stay byte-identical (same format: UTF-8 BOM, CRLF).
* Object IDs, folders, attributes and access modifiers are kept. Methods that a cloned block
  (`PouClone`: `MC_OpenBrakeFB`, `MC_DynamicSplineFB`) takes over from its template keep the ID
  of the method with the same name, new methods get a stable new ID.
* Declarations are written as plain text (`InterfaceAsPlainText`, used by the IDE) **and** as
  structured PLCopen interface / type; the tool checks that both got the same changes.
* `--verify`: the generators read the fixed XML **without** any correction (only the hand
  written Python parts stay) and must produce the same types and function blocks as from the
  original XML with all corrections (`tests/unit/tools/test_export_xml.py`).

Not contained: fixes that exist only in hand written Python code (section *Fixes without
generated diff* of [ST_Finding_Solve_Guide.md](ST_Finding_Solve_Guide.md): F1, F2, F3, F5, F6,
F9, F10, F22, F47) – they are transferred by hand.

## Import (TwinCAT 3)

1. Branch `bugfix/st-fixes` in the PLC repository, open the library project.
2. *Project → Import PLCopenXML…* → `RobotLibrary_fixed.xml`; in the dialog replace the existing
   objects (the changed objects are listed by the tool).
3. Build – no new errors or warnings may appear.
4. Export the sources as usual (Plaincat `decode`) and commit. The diff shows the fixes, every
   change is marked with `// ST-FIX Fnn`.

## After the fixes are in the library

Export the library again to `third_party/robotlibrary/RobotLibrary.xml` and follow step 9 of the
[ST Finding Solve Guide](ST_Finding_Solve_Guide.md): every correction reports itself as
"obsolete" and is removed; the generated Python code must not change functionally.
