# Findings in the PLC library (ST)

Found while porting. Reference: SRCI profile V1.5.9 (2024-12-04) and the SRCI SDK.
The Python code marks every deviation with `ST-FIX <id>`; tests in `tests/unit` cover them.
Status "fixed in Python" means: still to be fixed in the PLC library.
How to fix them in ST (exact ST diffs, generated from the corrections): [ST_Finding_Solve_Guide.md](ST_Finding_Solve_Guide.md).

| ID | Where (ST) | Problem | Spec / SDK | Python |
|---|---|---|---|---|
| F1 | `MC_RobotTaskFB.CreateSendPayloadCyclicOptional` | Cartesian position PLC→RC: `Config` is sent as **1 byte**, but `SIZEOF(...CartesianPosition)` = 34 counts 2 bytes → all following bytes are shifted by one compared to the calculated layout | Table 5-97: Config = bytes 24–25 | fixed: 2 bytes (`config`, `0`) |
| F2 | `MC_RobotTaskFB.CreateSendPayloadCyclic`, `CalculateCyclicDataLength` | `ToolNo`/`FrameNo` are **always** sent after the header | Table 5-88 bit 1 / 5-90 and SDK (`AutoTransmitCartesianPos`): only when "Cartesian Position" RC→PLC is configured; otherwise the RC expects the sequence at byte 18 | fixed: only with `RobToPlc.CartesianPosition.Active` (confirmed with the SDK in M5) |
| F3 | `RobotLibrarySendDataBaseFB.AddTurnNumber`, `RobotLibraryRecvDataBaseFB.GetTurnNumbers` | turn numbers encoded as two's complement nibble (`SINT_TO_BYTE`, -1 → `2#1111` = -7 for the RC); decoding ignores the sign bit (`-1` = `2#1001` → 9) | 5.5.4.4, tables 5-24…5-26: sign + magnitude, bits 0..2 value, bit 3 sign (E1: bits 0..6, bit 7) | fixed |
| F4 | `MC_RobotTaskFB.ParseRecvPayload` | "delete old telegram data" compares the ACK of the *previous* telegram with `LastACK[0]` – both are always equal, the branch is dead code | – | kept as in ST (documented) |
| F5 | `MC_RobotTaskFB.ParseRecvPayloadSequence` | `_fragIdx` and `_seqPayloadPtr` are not reset for the second sequence – with two sequences the second one is parsed with a wrong fragment index/length | – | fixed: reset per sequence |
| F6 | `DwordToRaStatusWord` | inserts `CollisionDetectedEnabled` at bit 13 → `CollisionDetected`, `RestartRequested`, `Accelerating`, `Decelerating`, `ConstantVelocity` are read one bit too high | Table 5-105 and SDK: 13 CollisionDetected, 14 RestartRequested, 15 Accelerating, 16 Decelerating, 17 ConstantVelocity | fixed; `CollisionDetectedEnabled` stays FALSE |
| F7 | `RobotLibraryRecvDataBaseFB.GetDword` | no byte swap (all other getters swap; `AddDword` swaps) | SDK sends the status word as little-endian bit field, so reading it without swap is *correct* for `StatusRobotArm`; unclear for `MC_ReadMessages` (`ErrorCode`) | kept as in ST, to be checked in M7 |
| F8 | `MC_RobotTaskFB.CalculateTelegramLengthPlcToRob` | uses `SIZEOF(Footer)` = 2, the footer is 1 byte (`FOOTER_SIZE`) | Tables 5-84/5-85 | kept as in ST (conservative by one byte) |
| F9 | `ByteToAxisJointUnit` | bit 1 and bit 2 both assigned to `J2`, `J1` never set | – | fixed: J1..J6 = bits 1..6 like `ByteToAxisJointUsed` |
| F10 | `PERCENT_INT_TO_REAL` | compares an `INT` with `16#FFFF_FFFF`/`16#0000_FFFF`; depending on the implicit conversion `-1` (16#FFFF) is not recognised as "not supported" | 5.6.2 percentage encoding | intended meaning implemented: all 16 bits set → -1.0 |
| F11 | `TurnNumber` (SINT per axis) | cannot represent "-0" | 5.5.4.4 uses -0 and +0 (e.g. table 5-26) | as in ST (known limitation); raw bytes are available in the telegram |
| F12 | `MC_MeasuringInputFB.CheckParameterValid` | `SetError( ErrorID := ErrorID := ...)` – duplicated assignment in the argument list | – | source patch (single `ErrorID :=`) |
| F13 | `MC_RobotTaskFB.HandleSync` | `HandleSyncToolData` is called twice per cycle (the tool step chain runs at double speed, e.g. `Execute` set and evaluated in the same cycle) | – | fixed (source patch): single call |
| F14 | `MC_RobotTaskFB.HandleAxesGroupSystemData` | `FrameDataPtr`/`WorkAreasPtr` (and Min/Max) are set to **LoadData** (copy & paste) – frame and work area data are written into the load array | – | source patch (FrameData / WorkAreas) |
| F15 | `MC_RobotTaskFB.OnExecRun` step 1 | timeout check `(State >= ERROR_161) OR (State <= ERROR_173)` is always TRUE → `ErrorID := TelegramState` also for non-error states | – | fixed (source patch): `AND` |
| F16 | `MC_Read*FB` (tool/frame/load/SW limits/dynamics) during the synchronisation | the start-up read calls `AxesGroup.SystemData.Update*` and so **overwrites the user data with the RC data** before the comparison – with `CLIENT_TO_SERVER` the PLC data is lost and the comparison always finds equal data | 5.6.7.3: client data wins | fixed: new input `UpdateSystemData` (default TRUE) of the 7 read blocks, FALSE for the internal instances of the RobotTask; update only on `DONE` |
| F17 | `MC_RobotTaskFB.HandleAxesGroupState` | `Unified*Index := MIN(..., X_MAX, ...)` but the internal arrays are `[0..X_MAX-1]` → write/read behind `_toolData` etc. | – | source patch (`X_MAX - 1`) |
| F18 | `MC_RobotTaskFB.HandleSync*Data` | copy loops run over the user array bounds (`ToolDataMin..ToolDataMax`) on the internal arrays `[0..TOOL_MAX-1]` → out of bounds if the user array is longer than `TOOL_MAX` (Python raises `IndexError`) | – | fixed (source patch): loops limited to `X_MAX - 1` |
| F19 | `ActiveCommandRegisterFB.AddRsp` | `FOR _idx := PayloadPointer TO PayloadLength - 1` – for fragments after the first one (`PayloadPointer > 0`) nothing is copied, long responses (e.g. `ReadRobotData`, 134 bytes) are truncated | 5.6.5 fragmentation | source patch (`PayloadPointer + PayloadLength - 1`) |
| F20 | synchronisation `SERVER_TO_CLIENT` | after reading the RC data the client never writes it back, so `DataChanged` on the RC is not reset and the RC never reports `DataInSync` → RI state never "Synchronized" | 5.6.7.4.2: "RobotTask then executes internally WriteToolData to reset DataChanged"; SDK resets `DataChanged` only on write | fixed: after the read (step 21) the RC data is written back (step 30) if the RC supports the write command |
| F21 | synchronisation `CLIENT_TO_SERVER` | writes tool/frame/load **0** (flange, world, …); the RC rejects it (SDK `0x8D35` invalid tool number) → warning, sync fails | 5.5.4: index 0 is fixed (flange) | fixed: tool/frame sync starts at index 1 (loops, start index, `LIMIT(1, …)`), like `LoadData` |
| F22 | `MC_ReadMessagesFB.ParseResponsePayload` | reads the 255 byte message text at offset 20 of the 256 byte response buffer (`GetDataBlock` copies behind the buffer) | – | fixed in `GetDataBlock`: missing bytes are 0 |
| F23 | `RobotLibraryBaseEnableFB` / `MC_RobotTaskFB.Reset` | disabling the RobotTask starts the cancel of the enable FBs (`_cancel`, 5 s timeout); a new enable within this time lets the pending cancel reset `MC_ReadMessagesFB` after its first response → start-up hangs in step 3 | – | fixed: a rising edge of `Enable` ends a pending cancel/error clear; a restart while the RC is still `INITIALIZED` resets the interface (`Control := RESET`, `_restartReset`) |
| F24 | `MC_RobotTaskFB.HandleSync` | a data set enabled for synchronisation whose functions the RC does not support (e.g. work areas in the SDK) keeps `Synchronized` FALSE forever | 5.6.7.1: "…or not supported by the RC does not impact the RI state Synchronized" | fixed: `_inSync*Ok` also TRUE if the RC does not support read + write (after `Initialized`) |
| F25 | `Valid` output of `MC_ReadActualPositionFB` (and `MC_ReadActualTCPVelocity`, `MC_ReadActualForce`, `MC_ReadAnalogInput`, `MC_ReadDigitalInputs/Outputs`, `MC_ReadIntegers`, `MC_ReadReals`, `MC_ReadSystemVariable`, `MC_CallSubprogram`, `MC_ActivateConveyorTracking`, `MC_SetTriggerLimit`) | `Valid` is never set to TRUE | 6.1.5: `Valid` like `Done` (TRUE while updated in `Continuous`) | fixed: output `Valid` (F25_POUS) |
| F26 | `CheckParameterValid` of 31 FBs | `IF ProcessingMode < BUFFERED AND ProcessingMode > TRIGGER_MULTIPLE` is never TRUE | – | fixed (range check before the enum conversion) |
| F27 | `MC_ReadToolDataFB`, `MC_ReadFrameDataFB` `.ParseResponsePayload` | `DataChanged` parsed before the index (ToDo "swapped compared to V1.3") → `ToolNoReturn`/`FrameNoReturn` = DataChanged; the sync updates the wrong tool/frame | tables 6-184/6-190 (and SDK): index, then DataChanged (as `MC_ReadLoadDataFB`) | fixed (source patch) |
| F28 | `CheckAddParameter` of 32 FBs (list `F28_POUS` in `tools/st2py/config.py`) | a parameter is omitted when the bytes of `_command` **behind the payload position** are zero; this assumes payload order = structure layout. Where it differs non-zero parameters are dropped, e.g. `WriteToolData`: `ToolNo` (payload end, structure start) not sent → SDK 0x8D35; `WriteRobotSWLimits`: upper limits not sent (structure J1Lower, J1Upper, …; payload all lower, then all upper); `MC_EnableRobotFB.HoldToRun`; `E2..E6` of positions | – | fixed: `CheckAddParameter := TRUE` (complete payload); `tests/unit/tools/test_st2py_f28.py` recomputes the list |
| F29 | `MC_RobotTaskFB.OnExecRun` step 8 | `Initialized := NOT ERROR AND NOT Synchronized; Initialized := NOT Synchronized;` – the 2nd line (ToDo) overwrites the first → after an error (e.g. init lost 0x80A2) `Initialized` and `CMDsEnabled` are TRUE again, FBs stay Busy forever | – | fixed (2nd line removed): FBs end with `ERR_COMMANDS_NOT_ENABLED` |
| F30 | `MC_ReadRobotDataFB.ParseResponsePayload` | `InterpreterCycleTime` read with `GetUsint` → 0 (SDK 10 ms) | table 6-18 / SDK: UINT | fixed (source patch) |
| F31 | `MC_WriteRobotSWLimitsFB.CreateCommandPayload` | `ResetToFactoryDefaults` (byte 106) is never sent | table 6-209 | fixed (source patch) |
| F32 | responses of `GroupStop`, `ExchangeConfiguration`, `ReadRobotSWLimits`, `ReadMessages` | fields at the end are not read: `AbortedSequence`, `NumberOfServerLogs`, `DataChanged`; the message text has 150 characters, ST reads 255 (F22) | tables 6-290, 6-87, 6-203, 6-108 | fixed: fields added (`FieldAdd`) and parsed |
| F33 | payload of 24 extended/optional FBs | layout differs from the spec tables (the bilateral test also found `MC_LoadMeasurementAutomaticFB`: Position_1 complete before Position_2) (shifted by missing/additional bytes, wrong data types, off-by-one loops). List with details: `KNOWN` in `tests/unit/fb/test_payload_spec.py` | chapter 6 payload tables | fixed (source patches, spline one point per command) |
| F34 | `MC_UserLoginFB`, `MC_SwitchLanguageFB` | `AddString` writes only the actual length; the spec has fixed fields (`Password`/`Username` 50, `LanguageCode` 2) → `Username` at the wrong offset | tables 6-69, 6-76 | fixed (source patches) |
| F35 | `CmdType` enum, `MC_MoveLinearAbsoluteJFB`, `MC_SoftSwitchTcpFB` | wrong command types: MoveLinearAbsoluteJ is sent as **MoveLinearAbsolute (2103)** – the RC reads the joint target as Cartesian position; SoftSwitchTcp as ShiftPosition (7205); MoveCircularAbsolute 2109 / MoveCircularRelative 2106 | spec: MoveLinearAbsoluteJ 2109, SoftSwitchTcp 7300, MoveCircularAbsolute 2106, MoveCircularRelative 2107 | fixed (enum override in `tools/plcopen_gen/overrides.py`, source patches) |
| F36 | `MC_SearchHardStopFB`, `MC_SearchHardStopJFB` `.CheckParameterValid` | `FOR _idx := 0 TO 6` over `DetectionVector[0..5]` – reads behind the array (Python: IndexError) | – | fixed (source patch) |
| F37 | `MC_EnableRobotFB`, `MC_MoveCircularRelativeFB` `.CreateCommandPayload` | two BOOLs that are bit 0/1 of **one** byte are sent as two bytes (`HoldToRun`/`ManualStep`, `PathChoice`/`Manipulation`) → `ManualStep`/`Manipulation` land in a reserved byte (not visible in the layout check, sizes happen to fit) | tables 6-25, 6-357 | fixed (source patch) |
| F38 | `MC_ReturnToPrimaryFB.CreateCommandPayload` | `AllowDifferences` is never copied into the command → always FALSE | table 6-332 | fixed (source patch) |
| F39 | ParCmd/OutCmd of several FBs | parameters without a field in the telegram of the spec (e.g. `MovePickPlaceDirect.ReductionRate`, `MoveSuperImposed.*DiffRate`, `SetTriggerRegister.EvaluateStartCondition`, `StopSubprogram.SequenceFlag`, `OutCmd.FollowID`) – list `NOT_IN_TELEGRAM` in `tests/sdk/test_bilateral.py` | – | to be reviewed (older/newer draft or values of the PLC only) |
| F40 | `MC_UnitMeasurementFB`, `MC_SyncToConveyorFB` `.OnApplyOutCmd` | `OutCmd` is only updated in state ACTIVE – the values of a response that is DONE at once are lost | – | fixed (source patch) |
| F41 | defaults of `ParCmd` (`VelocityRate`, `AccelerationRate`, `DecelerationRate`, `JerkRate`, ...) | default `0.0` = "internal minimal" velocity/acceleration; the spec defines "<0 %: (default) use default" → a command with the default values moves with minimal dynamics or is rejected (SDK: DecelerationRate 0 → 0x8E03) | chapter 6, e.g. 6.3.2.3 | fixed: rates default -1.0 (`FieldOverride`), -1.0 → 16#FFFF |
| F42 | `MC_OpenBrakeFB` | Execute block; the spec defines OpenBrake with **Enable** (brakes stay open while Enable) | 6.x OpenBrake | fixed: `MC_OpenBrakeFB` cloned from `MC_FreeDriveFB` as enable block |
| F43 | `MC_FreeDriveFB` | output `Enabled` is never set (only `OutCmd.Enabled`) | – | fixed (source patch) |
| F44 | defaults of several blocks | no valid default: ExchangeConfiguration.LifeSignTimeOut, SetSequence.TargetSequence, SetOperationMode.OperationMode, CollisionDetection.SequenceFlag, Read/WriteLoadData.LoadNo 0, SwitchLanguage/UserLogin (empty), ForceControl, ReadAnalogInput, MoveSpline, SetTriggerRegister | Siemens test "valid CMD with the default values" | fixed: defaults (ForceControl `ErrorReaction`, MoveSpline `MoveTime`); mandatory parameters documented |
| F45 | interface of 23 blocks | inputs/outputs of the spec missing or named differently (list `KNOWN_MISSING` in `tests/unit/fb/test_interface_spec.py`, e.g. ReadActualPosition: spec Enable/ReadCartesianPosition/..., WaitTime.Time, GroupStop/SetSequence output Active) | "Associated command/response values" | fixed: outputs added (`VarAppend`) + name mapping in the interface test |
| F46 | `StopSubprogramOutCmd.OriginID`, `ReadRobotDataOutCmd.RCInterpreterVersion` | no comment | – | fixed: comments added (`FieldOverride` doc) |
| F47 | `MC_ExchangeConfigurationFB`, `MC_ReadMessagesFB`, `MC_ReadRobotDataFB` | without running RobotTask they stay Busy without error (all other blocks: error) | – | fixed (via the command timeout F53) |
| F48 | 77 blocks | an undefined `ExecMode` (e.g. 18) is neither checked by the block nor rejected by the RC | Siemens "AbortingMode is not defined" | fixed: undefined `ExecMode` → error, not sent |
| F49 | `StopSubprogram.SequenceFlag`, `MoveLinearRelative.ReferenceType`, `MovePickPlaceDirect/Linear.BlendingMode`, `WriteAnalogOutput.Unit`, `CollisionDetection.ProcessingMode/SequenceFlag` | undefined enum values are not checked | – | fixed: enum checks in `CheckParameterValid` |
| F50 | base of all Execute blocks | a falling edge of `Execute` before the end cancels the command: Execute for one cycle → nothing is sent; reset during the motion → motion runs, but `Done` is never shown | 5.5.x "Output status": the falling edge "does not stop or even influence the execution", outputs set for at least one cycle | fixed: `Execute` edge held until the command ends (`_executeIn`/`_executeHold`) |
| F51 | motion blocks: inputs `AbortingMode`, `SequenceFlag` | checked but not used: the telegram always has the ExecutionMode of the input `ExecMode` → `AbortingMode = ABORT` has no effect (the new command is buffered) | 5.6.4.5 | fixed: `ExecutionMode` from `AbortingMode`/`ProcessingMode`/`SequenceFlag` (table 5-77) |
| F52 | `MC_RobotTaskFB` receive part (`RecvData`, fragment loop) | at most `FRAGMENT_MAX + 1` = 10 fragments of a received telegram are parsed, the others are dropped with a DEBUG message only - but the telegram is acknowledged, so the RC considers them delivered → the responses are lost and the function blocks stay `Busy` forever (e.g. 16 GroupInterrupt in one cycle: the SDK sends 12 DONE fragments in one telegram, 2 are lost) | 5.6.5.3: no limit of fragments per telegram (header 8 bytes, a 256 byte telegram holds up to 27 fragments) | fixed: `FRAGMENT_MAX` = 31; overflow logged as ERROR |
| F53 | 112 function blocks, `OnExecRun` | `SetTimeout(PT := _timeoutCmd, ...)` is called, but the timer is never evaluated while waiting for the response → no error when a response never arrives (see F52) | – | fixed: command timeout |
| F54 | `MC_CreateSplineFB`, `MC_DynamicSplineFB` | loops `FOR _idx := 0 TO SPLINE_DATA_MAX` over `SplineData[1..SPLINE_DATA_MAX]` → access before the array | – | fixed (source patch): loop from 1 |
| F55 | `MC_CreateSplineFB`, `MC_DynamicSplineFB` `.CreateCommandPayload` | the positions of the spline points are never copied into the command → always 0 sent | tables of CreateSpline / DynamicSpline | fixed (source patch) |
| F56 | `MC_RobotTaskFB.HandleSeqAck` | the Seq number wraps from 254 to **0**; an Ack of 0 equals the Ack of telegrams without new data → the response of that sequence is ignored, the block hangs (after 255 sequences) | 5.6.5.3: 0 only on the first exchange | fixed (source patch): wrap to 1 (`test_sequence_number_overflow`) |
| F57 | `MC_RobotTaskFB.HandleSync*` step 10 | the local change detection compares with `IgnoreTimestamp := FALSE`, but the internal copy holds the timestamp of the RC from the start-up read → every data set counts as changed on the PLC; together with the RC "not in sync" → warning "both sides changed", no synchronisation | – | fixed (source patch): `IgnoreTimestamp := TRUE` |
| F58 | `MC_RobotTaskFB.HandleSync*` step 10 | data changed on both sides only sets the warning `WARN_*_SYNC_BOTH_SIDES_CHANGED`, also with a fixed direction (`CLIENT_TO_SERVER` / `SERVER_TO_CLIENT`) → synchronisation stops | 5.6.7.4: the direction decides | fixed (source patch): step 11 / 12 for the fixed directions, warning only for `AUTOMATIC` |

## Notes on the SRCI SDK (simulation)

Changes inside the private SDK copy are marked `SRCI_PY CUSTOM BEGIN/END` and listed in
`srci_py_harness/CUSTOM_CHANGES.md` of the SDK folder:

- **C-001** `SRCI::readRobotData` left `rcSupportedFunctions` 0, so a client never uses
  optional functions (e.g. the data synchronisation). The simulation reports the commands
  the SDK implements.
- **C-002** `SRCI::log`: a FATAL message changes the RI state while `logLock` is held; the state
  change logs again → deadlock of the SDK (e.g. `initiateEnable` fails). Fixed in the private copy,
  should be reported to the SDK maintainers.
- `validateDynamicsParameters` accepts only `DecelerationRate` "not set" (`-1.0` → 16#FFFF),
  every other value → 0x8E03.
- `WriteToolData` requires `ToolData.LoadNo` ≥ 1 (0x8D17).
- Without power a motion command stays buffered (sequence interrupted); after `EnableRobot` it
  needs `GroupContinue`.
- `RSP::ReadActualPosition` has 2 reserved bytes before the extended axes that are not in the
  spec (SDK comment: "not anymore in spec, but in Tia?") → E1..E6 of ReadActualPosition are
  shifted by 2 bytes against the spec and the PLC library.
- **C-003** all commands of the spec: the SDK implements only the core commands. The harness
  generates field tables for all 115 commands from the payload tables of the spec
  (`srci_py_harness/gen_commands.py`) and answers the other commands generically
  (`srci_py_commands.cpp`: motion through the planner of the SDK, others done at once, response
  values set by the test). Every received command is decoded with these tables
  (`SdkSimulator.last_command`) – the bilateral tests (`tests/sdk/test_bilateral.py`) compare
  every ParCmd value with it and every response value with OutCmd.
- Motion commands of the planner are only the types 2101..2298 (cam 2400..2402 are executed at once).
- After SetSequence(secondary) the secondary commands need GroupContinue; after SetSequence(primary)
  GroupContinue is rejected (0x8C02) and the interrupted primary command is not continued.
- Enable-type functions of C-003 stay ACTIVE (response bit "Enabled") until the block is disabled.
- `srci_sim_layout` (harness, not an SDK change) returns the layout of the SDK structures;
  `tests/sdk/test_payload_sdk.py` compares every payload with them.
- The SDK checks the lifesign only for a *frozen* value (same lifesign for
  `LifeSignTimeOut` ms real time), not for missing telegrams.

## Notes on the specification

- The payload tables of chapter 6 are extracted with `python -m tools.spec_tables <spec.txt>`
  (text export of the PDF, `pdftotext -layout`) into `tools/spec_tables/spec_payload_tables.json`
  (offsets, data types, parameter names only). `python -m tools.payload_check` compares every
  function block with them (test `tests/unit/fb/test_payload_spec.py`).
- Table 6-203 is captioned "WriteRobotSWLimits" but is the response of ReadRobotSWLimits;
  the response table of SetTriggerError (after 6-620) has no caption.
- Table 6-492 (MoveSuperImposedDynamic) lacks `Offset.RZ`, the byte numbers are inconsistent.
- Table 6-474 (SyncToConveyor) has `EmitterID` as USINT, all other tables SINT.
- Tables 6-224/6-229 (Read/WriteWorkArea) place `ZeroPointX` (REAL) at the odd offset 17, the
  PLC library inserts a byte before it – to be clarified.

- 5.6.6.2 states "The actual SRCI version is V1.3" (also in draft 1.5.9) while the SDK uses 1.5.
  Only the major version is checked (SDK `04_Network.cpp`). Python uses 1.5.0 (generator override).
- Tables 5-87 (ClientServer, "bytes required": Cartesian 40, Joint 30) and 5-97/5-99 (34/28 bytes)
  contradict each other. The PLC library and Python follow the detailed tables (34/28). The SDK
  does not decode optional cyclic data PLC→RC yet.
