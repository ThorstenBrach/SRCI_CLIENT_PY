# Porting rules ST ↔ Python

Goal: a change in the PLC library (Structured Text) can be found and applied in
Python quickly – and vice versa.

Since M6 the function blocks and functions are **transpiled** from the PLCopen XML
export of the PLC library (`third_party/robotlibrary/RobotLibrary.xml`). Only a few
parts are hand written (see below). A change in the PLC library therefore reaches
Python by exporting the XML and regenerating:

```bash
python -m tools.plcopen_gen          # types:  src/srci/types/_generated
python -m tools.st2py                # FBs/functions: src/srci/fb, functions, interfaces
python -m tools.st2py --check        # CI: fail if generated code is out of date
```

Never edit generated files (header "Generated from the PLC library ... DO NOT EDIT").

## What the transpiler produces

1. **Same names.** Function block → class of the same name; `VAR_INPUT`/`VAR_OUTPUT`/
   `VAR` → attributes; `METHOD` → method; `PROPERTY` → Python property. Method and
   function parameters are keyword arguments with the ST names.
2. **Same step chains.** `CASE step OF` → `match` with the *same* step numbers.
   Comments of the ST code are kept, the line structure follows the ST code.
3. **Same file cut.** One module per POU with the folder structure of the library:
   `POUs/Read/MC_ReadToolData/MC_ReadToolDataFB` → `srci.fb.Read.MC_ReadToolData.MC_ReadToolDataFB`,
   `Functions/...` → `srci.functions...`. Each module names its ST source.
4. **IEC semantics.** Structures and arrays are copied on assignment
   (`copy_into`), integers wrap around (`wrap`), `/` and `MOD` truncate like ST,
   `AND`/`OR` evaluate both operands when a call is involved, `VAR_INPUT` structures
   are copies, `REFERENCE TO` set once with `REF=` becomes an alias, pointers and the
   memory functions (`ADR`, `SysDepMemCpy/Cmp/Set`) work on a byte image with the PLC
   layout (`pack_mode 1`, little endian). Runtime: `srci.iec.rt`, `srci.iec.conv`.
5. **Initialisation like Codesys.** All variables of the class hierarchy first, then
   `FB_init` of every class, base first (`srci.iec.fb.FunctionBlock`).
6. **Library parameters** (`RobotLibraryParameter`, e.g. `TOOL_MAX`) are set with
   `srci.configure(...)` before the first function block is created; array sizes that
   depend on them follow the configured values.

## Deviations from the ST code

All deviations are listed in `tools/st2py/config.py` and `docs/ST_FINDINGS.md`:

* **Source patches** (`SourcePatch`): small textual corrections of the ST source before
  transpiling, each with the finding id. A patch fails when its text no longer occurs in
  the ST code (e.g. after the fix was made in the PLC library) and must then be removed.
* **Appended statements** (`BodyAppend`): ST text appended to a method, e.g.
  `CheckAddParameter := TRUE;` for the function blocks of finding F28.
* **Hand written methods** (`Mixin`): the telegram coding of `MC_RobotTaskFB`
  (`CreateSendPayload*`, `ParseRecvPayload*`, `Calculate*`) with ST-FIX F1, F2, F5 lives in
  `MC_RobotTaskFB_Telegram.py` and is used instead of the transpiled methods.
* **Hand written POUs**: the send/receive buffers (`RobotLibrarySendData*FB`,
  `RobotLibraryRecvData*FB`, `RobotLibraryCommandDataFB`, `RobotLibraryResponseDataFB`),
  `Functions/Common` and `Functions/Convert/Misc|DT` (they are fast and carry the ST-FIX
  F3, F6, F9, F10, F22). Their modules start with
  `# ST-Source: <path>  sha256: <hash>` per unit;
  `python -m tools.st_drift <path to RobotLibrary/Library>` lists units whose ST source
  changed since porting.

Where the ST code contradicts the specification (or the SDK), Python follows the
specification, marks the place with `ST-FIX <id>` and the finding is listed in
`docs/ST_FINDINGS.md` so that it can be fixed in the PLC library as well. Findings that
change behaviour but have no clear fix are *not* patched – the tests document them
(`xfail` with the finding id).

## Payload check against the specification

`python -m tools.payload_check [FB ...]` records the `Add*`/`Get*` calls of every function block
and compares them with the payload tables of the specification (offset, size, REAL/signed/
unsigned, string field length, payload length). `tests/unit/fb/test_payload_spec.py` fails for
new deviations and for fixed ones that are still listed as known; it also checks the command
type of every function block.

The commands the SDK implements are additionally compared with the SDK structures
(`tests/sdk/test_payload_sdk.py`): the harness fills the `CMD`/`RSP` structure with a byte pattern
and converts it like the SDK, the reversed multi-byte fields give the exact SDK layout.

## Logging

The generated code keeps every log call of the ST code (`CreateLogMessage*`, the
telegram logs of `MC_RobotTaskFB`, ACR entries, …). As in the PLC the entries go into the
ring buffer `AxesGroup.MessageLog.SystemLogs` (output `SystemLog` of the RobotTask) and,
filtered by `LogLevel`, to an external logger. `srci.logging_bridge.PythonLogger` is an
external logger for Python `logging` (loggers `srci.plc` and `srci.rc`); transport and
runtime log to `srci.transport` / `srci.runtime`.
