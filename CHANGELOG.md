# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
The version follows the SRCI profile: 1.5.x is the client for the profile V1.5 (specification
V1.5.9); the last digit counts the releases of the client.

## [1.5.2] - unreleased

First release in this repository (the earlier releases were published from the development
repository).

### Added
- OPC UA transport for robot controllers that publish their PROFINET I/O byte by byte (e.g. Staubli
  CS9): `OpcUaTransport` also takes a list of NodeIds for `out_node` / `in_node`, one node per byte;
  all nodes of a direction go in one Write and one Read request, `write_changed_only` writes only the
  changed bytes, `consistency_byte` writes a check byte invalid first and valid last.
- Configuration files (TOML) for the OPC UA transport: `OpcUaTransport.from_config` / `from_profile`,
  `load_opcua_config`, `opcua_profiles` (endpoint, user, node layout, recommended cycle time and
  LifeSign timeout). Shipped: `srci_bridge_twincat`, `staubli_cs9`.
- `OpcUaRcSimulator(per_byte=True)` and `config()`.

### Changed
- SafeReferencing sends a reserved byte after `ToolNo`, as robot controllers based on the SRCI SDK
  expect it; `MaximumDistance` starts at byte 14. The telegram table of the specification (6-838) has
  no reserved byte - the deviation is reported to PI.
- ReadSafeReferencePosition reads the external axes E1..E6 directly after J6, as the robot controller
  sends them (before they were read 20 bytes too late). `ReadSafeReferencePositionRecvData` has no
  field `CartesianPositionExt` any more.

## [1.5.1] - 2026-11-14

Generated from the PLC library 1.5.6.0.

### Changed (behaviour - please check your programs)
- Start values from the parameter tables of the specification: ChangeSpeedOverride and GroupJog
  `Override` 10 % (was 5 %); ReadFrameData / ReadToolData / ReadLoadData number 1 (was 0);
  ReadActualPositionCyclic `ReadCartesianPosition` and `ReadJointPosition` TRUE (set the flag of a
  cyclic area you did not configure to FALSE, otherwise the block reports 16#0008);
  `RobotWorkAreaData.AreaType` BOX; spline `BlendingParameter` [10, 0]; superimposed
  Acceleration/Deceleration/JerkDiffRate -1 (= RC default); SetTriggerLimit `Data_1/Data_2` 999999;
  ForceControl `TargetValue` -99999.9999; BrakeTest J1..J6 active; CollisionDetection
  `ActivateMonitoring` TRUE and `Sensitivity` 100; Approach/Depart/PickPlace `VelocityCoefficient`
  1.0, PickPlaceDirect `ReductionRate` 100.
- WriteRobotDefaultDynamics / WriteRobotReferenceDynamics: an untouched ParCmd has all values -1
  (= do not change).
- ReadActualTCPVelocity refuses the trigger processing modes; MoveTime above 65.535 s is an error;
  WriteWorkArea runs parallel only; SetTriggerLimit refuses TriggerMode INVALID.
- TriggerCondition `START_POSITION_TCP_VELOCIT_ABSOLUTE` renamed to
  `START_POSITION_TCP_VELOCITY_ABSOLUTE`.
- ActivateConveyorTracking `ConveyorNo` / `ConnectionMode` are USINT.
- `MoveAxesAbsoluteParCmd.ConfigMode` removed (not in the specification, never sent).
- `RobotLibraryErrorIdEnum`: `ERR_LIFESIGN_TIMEOUT_0x8005` (16#8004) is now
  `ERR_LIFESIGN_TIMEOUT_0x8004`, `ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8_0x80A8` is now
  `ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8`.
- A write of the start-up synchronization refused by the RC is a warning and the start-up goes on.

### Fixed
- No false lifesign timeout 16#80A5 after a short disable of the RobotTask.
- Several fixes of error codes, outputs and parameter checks (AxesGroup change, SyncToConveyor,
  SoftSwitchTcp, CallSubprogram ReturnData, ReturnToPrimary, RCInterpreterVersion with the new output
  `RCInterpreterVersionNumber`, LogLevel, synchronizing flags, CollisionDetection,
  RedefineTrackingPos); new constant `RobotLibraryConstants.CYCLIC_SUB_PROGRAM_DATA_MAX`.

## [1.5.0] - 2026-11-10

First release: Python client of the SRCI interface (specification V1.5.9), generated from the PLC
library 1.5.5.0.

- All function blocks, data types and functions of the SRCI PLC library, kept identical to it.
- `srci.api.RobotProgram` (RobotTask + user data + function blocks) and `srci.api.SrciClient`
  (sequential scripts; the program runs cyclically in a background thread like a PLC task),
  `srci.runtime.Runner`.
- Transports: TCP/IP to a PLC gateway (lockstep, reconnect), loopback, fault injection, OPC UA
  (optional extra `srci-client[opcua]`).
- Examples: quickstart, every function of the profile Core, JAKA MiniCobo.
