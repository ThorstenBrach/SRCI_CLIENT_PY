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
 - Repository renamed to SRCI_CLIENT_PY (distribution `srci-client`, package `srci`)
 - `RobotProgram`: the configuration of the RobotTask is `ParCfg` (keyword and attribute), the
   name of the input of `MC_RobotTaskFB` in the PLC library (was `config`)
 - ST patches follow the ST coding rules: THEN on its own line, a log entry behind every
   `SetError`

### Fixed
 - ST-FIX F59 … F75 (specification audit): FB outputs, two telegram sequences, RI errors,
   parameter checks, messages
 - ST-FIX F76: `MC_GroupResetFB` no longer resets the FastStop half byte. After GroupStop and
   GroupReset the RC kept the sequence interrupted, so no further motion ran (found on the JAKA
   MiniCobo and with SRCI_PY_HMI)
 - ST fixes compile in TwinCAT: duplicate `CmdType.SoftSwitchTCP` (C0142), explicit conversions
   instead of implicit narrowing (C0032, F60/F74), enum aliases for literals hidden by inputs
   (F35, F51)
 - `tools.sdk_custom_report` accepts a CUSTOM block that keeps the original SDK code as a comment
   (BEGIN opens the comment, END closes it)

### Tested with
 - JAKA MiniCobo (controller 1.7.1, SRCI 1.1, profile Core) behind the TwinCAT PLC gateway.
   Linear moves need TurnMode FREE and ConfigMode SAME or FREE; the only accepted blending mode
   is MAX_CORNER_DEVIATION (linear and joint moves). The RC sends no LifeSign for about 200 ms
   after a rejected command, so a LifeSign timeout of 500 ms is used
