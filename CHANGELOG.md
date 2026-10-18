# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added
 - Python client of the SRCI interface (specification V1.5.9): all function blocks, data types and
   functions of the SRCI PLC library, generated from the PLC library and kept identical to it
 - `srci.api.RobotProgram` (RobotTask + user data + function blocks) and `srci.api.SrciClient`
   (sequential scripts; the program runs cyclically in a background thread like a PLC task,
   `background=False` for deterministic tests), `srci.runtime.Runner` (fixed cycle in a thread)
 - Transports: TCP/IP to a PLC gateway (lockstep, reconnect), loopback, fault injection
 - OPC UA transport `OpcUaTransport` (optional extra `srci-client[opcua]`, package asyncua):
   PLC->RC telegram written to one node, RC->PLC telegram read from another, data type `ByteString`
   or a number array (`Byte[]` ... `Double[]`) detected on connect, optional user / password,
   reconnect like the TCP transport; `srci.transport.opcua.browse()` lists the variables of a
   server for configuration tools. Tested against a local asyncua server, not yet on a robot
 - `srci.sim.opcua.OpcUaRcSimulator`: OPC UA server with the telegram nodes that answers in its own
   cycle like a robot controller (handler, e.g. the SDK simulator)
 - Example `examples/core_profile`: every function of the Core profile
 - Example `examples/jaka_minicobo`: first steps with a real robot behind the TwinCAT PLC gateway
   - `info`: robot data, supported Core functions (`RCSupportedFunctions`), configuration, SW
     limits, position, messages; no motion
   - `move`: one joint by a few degrees and back
   - `blending`: probes which TurnMode / ConfigMode and BlendingModes the RC accepts
   - log file with the system log of the library and a telegram trace, diagnosis of a failed
     initialization, `--srci-version`, `--lifesign-ms`, `--sdk-tcp` dry run against the SDK
     simulator
 - Example `examples/quickstart/quickstart.py`: compact template for users in one flat script.
   It initializes, switches the robot on, moves joint and direct, drives a linear rectangle with
   blended corners and prints the time of the rectangle; `--sim` runs it against the SDK simulator
 - `srci.sim.server`: the SDK simulator behind a lockstep TCP server, for PLC tests (TwinCAT,
   Codesys). The status line shows gaps and repeats of the PLC LifeSign; `--dump` shows the
   decoded telegram headers
 - `srci.sim.control`: control channel of the SDK server (`--control-port`, default 5001) for the
   TcUnit tests of the PLC library: setup of the simulator, its state, the log window and fault
   injection on the telegrams (`RESET`, `MOVE_CYCLES`, `GET JOINT`, `LAST`, `TAMPER` ...)
 - `tools.st2py.export_xml`: writes the ST fixes back into the PLCopen XML of the PLC library.
   `--verify` regenerates everything from the fixed XML; the export refuses implicit integer
   narrowing and enum literals that an input of the same name hides
 - Two telegram sequences, RI error handling (lifesign, sequence timeout, invalid frames)
 - Tests on Linux and Windows, Python 3.12 – 3.14, including a simulated robot controller;
   test case catalog and test report
 - Release workflow: wheel and source package for tags `vX.Y.Z`, release notes from this file
 - README: teaser of the teach pendant SRCI_PY_HMI (separate repository)
 - README: quick start with `execute` and the alternative `start` + `wait_done`, table of the
   `SrciClient` calls
 - README and examples: link to the PLC side SRCI_TcpIp_Bridge (TwinCAT and CODESYS examples,
   formerly SRCI_TcpGateway)

### Changed
 - The SDK simulator (`srci.sim.sdk`), the SDK server for PLC tests (`srci.sim.server`) and its
   control channel (`srci.sim.control`) moved to the private SDK repository (package
   `srci_sdk_sim`, `srci_py_harness/python`): they only work with the licensed SDK and are not
   part of the published client. `pip install -e "<SDK>/srci_py_harness/python"`, then
   `python -m srci_sdk_sim.server ...`; without the package the SDK tests are not collected.
   `srci.sim.gateway` stays in the client.
 - Test cases and docs refer only to our own test IDs (GEN-04 …), the specification and the
   ST-FIX findings; references to third-party test templates and `docs/siemens_mapping.json`
   removed (docs/TestCases.md without the template coverage section)
 - Repository renamed to SRCI_CLIENT_PY (distribution `srci-client`, package `srci`)
 - `RobotProgram`: the configuration of the RobotTask is `ParCfg` (keyword and attribute), the
   name of the input of `MC_RobotTaskFB` in the PLC library (was `config`)
 - ST patches follow the ST coding rules: THEN on its own line, a log entry behind every
   `SetError`
 - Generated from the PLC library export of 2026-10-17, which contains all fixes F1 ... F103: the
   source patches (`tools/st2py/config.py`) and type overrides (`tools/plcopen_gen/overrides.py`)
   are removed, the generated code is functionally unchanged (only F72 and F103 differ in the
   form of the ST code); new hand written `TURN_TO_SIGN_MAGNITUDE`, `SIGN_MAGNITUDE_TO_TURN`
   (functions of the PLC library for F3); `docs/ST_Finding_Solve_Guide.md` only lists what is
   still open
 - `RobotLibraryParameter.TOOL_MAX`, `FRAME_MAX`, `LOAD_MAX`: default 20 (was 16) like the PLC
   library and the SDK simulator

### Fixed
 - CI: `tools.test_report check` no longer fails without the SDK simulator (the SDK tests are not
   collected there); docs/TestCases.md with the instance counts of the SDK tests is checked in
   the job `sdk`
 - ST-FIX F59 … F75 (specification audit): FB outputs, two telegram sequences, RI errors,
   parameter checks, messages
 - ST-FIX F76: `MC_GroupResetFB` no longer resets the FastStop half byte. After GroupStop and
   GroupReset the RC kept the sequence interrupted, so no further motion ran (found on the JAKA
   MiniCobo and with SRCI_PY_HMI)
 - ST fixes compile in TwinCAT: duplicate `CmdType.SoftSwitchTCP` (C0142), explicit conversions
   instead of implicit narrowing (C0032, F60/F74), enum aliases for literals hidden by inputs
   (F35, F51)
 - ST-FIX F81: Write/ReadToolData store the tool in the `ToolData` array of the RobotTask
   (`AxesGroupSystemDataFB.UpdateToolData`, the copy was commented out)
 - ST-FIX F82: `MC_ReadActualPositionCyclicFB` sets `ReadingJointPositionExt` (not
   `ReadingCartesianPositionExt`) for the extended joint position
 - ST-FIX F83: an action started in a sequence can be deactivated (`ProcessingMode` DEACTIVATE with
   its SequenceFlag), `MC_WaitForTriggerFB` can be deactivated at all
 - ST-FIX F84: `MC_MoveLinearCamFB` accepts `TriggerDelay` up to 65535 ms (was 255)
 - ST-FIX F85: `MC_ConfigureConveyorFB` accepts `CIRCULAR_CONVEYOR_TRACKING`
 - ST-FIX F86: `MC_ForceControlFB` accepts `ConnectionMode` `PLC_SENSOR_ALGORITHM`
 - ST-FIX F87: `MC_UserLoginFB` needs a `Username` only in `Mode` `USERNAME_AND_PASSWORD`
 - ST-FIX F88: `MC_StopSubprogramFB` accepts `TargetID` up to 65534, error `ERR_INVALID_PAR_CMD`
 - ST-FIX F89: `MC_MoveSuperImposedFB` accepts `ProcessingMode` TRIGGER_CONTINUOUS
 - ST-FIX F90: `MC_MeasuringInputFB` shows `OutCmd.MeasuringID` already while the measurement is active
 - ST-FIX F91: `MC_WriteAnalogOutputFB` rejects `Index` 0 (1..32)
 - ST-FIX F92: `MC_UnitMeasurementFB` reports an invalid `MeasuringMode` as `ERR_INVALID_PAR_CMD`
 - ST-FIX F93: synchronization NO_SYNCHRONIZATION after the start-up detects changed data (`InSync`,
   `Synchronized` FALSE) without transferring them
 - ST-FIX F94: a start-up conflict with `SyncUserInteraction` is resolved by a write / read of the user
   (the RobotTask reads the RC data again after every sync timeout)
 - ST-FIX F95: synchronization AUTOMATIC after the start-up keeps watching for changes (step 13 jumps back)
 - ST-FIX F96: every negative dynamics rate is the default (sent as 16#FFFF), not only -1
 - ST-FIX F97: `MC_WriteRobotDefaultDynamicsFB` rejects rates above 655.35 % (do not fit into the telegram)
 - ST-FIX F98: `ToolNo` / `FrameNo` / `LoadNo` outside -1..254 is a range error (16#8412 / 16#8414 / 16#8418)
 - ST-FIX F99: `MC_ReturnToPrimaryFB` rejects `TrajectoryMode` 0 (Invalid) with 16#8409 - set
   `TrajectoryMode` to `LINEAR_MOVEMENT` or `PTP_MOVEMENT`
 - ST-FIX F100: the response of a command is parsed into a cleared `_response` (109 blocks) - the RC
   leaves out trailing zero bytes, a shortened response kept the values of the previous command (e.g.
   `MC_WriteRobotReferenceDynamicsFB` wrote 777 back into the user data after a write of 0)
 - ST-FIX F101: the load count check uses `HighestLoadIndex` (was `HighestToolIndex`)
 - ST-FIX F102: the count check of tools / frames / loads / work areas runs after the initialization
   (was: before, with the RC data and configuration of the previous enable)
 - ST-FIX F103: `MC_RobotTaskFB` enabled again with one telegram sequence after two no longer writes the
   header of a 2nd sequence behind the end of the telegram (`SequenceCountSend` of the previous enable)
 - Tests `tests/sdk/test_parameter_ranges.py` (area SDK-RANGE): parameter ranges against the SDK
 - Tests `tests/sdk/test_sync.py` (area SDK-SYNC): synchronization of the user data against the SDK
 - `tools.sdk_custom_report` accepts a CUSTOM block that keeps the original SDK code as a comment
   (BEGIN opens the comment, END closes it)

### Tested with
 - JAKA MiniCobo (controller 1.7.1, SRCI 1.1, profile Core) behind the TwinCAT PLC gateway.
   Linear moves need TurnMode FREE and ConfigMode SAME or FREE; the only accepted blending mode
   is MAX_CORNER_DEVIATION (linear and joint moves). The RC sends no LifeSign for about 200 ms
   after a rejected command, so a LifeSign timeout of 500 ms is used
