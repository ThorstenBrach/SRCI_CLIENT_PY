# Example: the SRCI profile "Core" in Python

[`core_profile_demo.py`](core_profile_demo.py) executes **every function of the profile "Core"**
(SRCI profile V1.5.9, table 5-2) one after the other and prints what the robot controller answers.
This document explains the library concepts the demo uses and walks through each function
with the relevant code excerpt.

- [1. Installation](#1-installation)
- [2. How the library works](#2-how-the-library-works)
- [3. Running the demo](#3-running-the-demo)
- [4. The Core functions step by step](#4-the-core-functions-step-by-step)
- [5. Patterns for your own program](#5-patterns-for-your-own-program)
- [6. Troubleshooting](#6-troubleshooting)

## 1. Installation

The package is called `srci-client` and is imported as `srci`. It needs Python ≥ 3.12 and has
no dependencies.

```bash
pip install srci_client-<version>-py3-none-any.whl   # the wheel from dist/ (python -m build)
# or, from a clone of the repository:
pip install -e .
```

```python
import srci
print(srci.__version__, srci.SRCI_PROFILE_VERSION)  # e.g. 0.1.0.dev0 1.5.9
```

## 2. How the library works

### PLC function blocks in Python

The package is a 1:1 port of the SRCI PLC library for Codesys/TwinCAT. Every function block
(`MC_…FB`) has the same name, the same inputs and outputs and behaves the same way as in the PLC:

| Kind | Start | Result | Examples |
|---|---|---|---|
| **Execute** blocks | rising edge of `Execute` | `Done` / `Error` + `ErrorID` / `CommandAborted`, values in `OutCmd` | `MC_GroupResetFB`, `MC_MoveAxesAbsoluteFB`, `MC_ReadToolDataFB` |
| **Enable** blocks | `Enable = True` | `Enabled` (or `Valid`), runs until `Enable = False` | `MC_EnableRobotFB`, `MC_GroupJogFB`, `MC_ReadActualPositionCyclicFB` |

Command parameters are in `ParCmd`, results in `OutCmd` – exactly the structures of the PLC
library and of the specification:

```python
from srci.fb import MC_MoveAxesAbsoluteFB

move = MC_MoveAxesAbsoluteFB()
move.ParCmd.JointPosition.J1 = 45.0  # degrees
move.ParCmd.VelocityRate = 50.0  # % of the reference velocity (-1.0 = default)
```

All blocks can be imported from `srci.fb`; all data types and enums from `srci.types`.

### Cycles and telegrams

SRCI is cyclic: in every cycle (e.g. 10 ms) the client sends one telegram to the robot controller
(RC) and receives one. `MC_RobotTaskFB` builds and parses the telegrams; the command blocks
register their commands with it. In a PLC all of them are called once per cycle – in Python the
same happens in a **`RobotProgram`**:

```
cycle n:  command blocks (in the order they were added)  ->  MC_RobotTaskFB  ->  telegram to the RC
                                                                        <-  telegram of the RC
```

`RobotProgram` holds the RobotTask, its configuration (`config`, a `RobotTaskParCfg`), the user
data arrays (tools, frames, loads, work areas, SW limits, dynamics, logs) and the list of command
blocks.

### Transport

How the telegram reaches the robot is the job of a *transport*:

| Transport | Use |
|---|---|
| `srci.transport.TcpTransport(host, port, send_size, recv_size)` | real robot: a PLC acts as gateway between TCP and PROFINET (see the main README) |
| `srci.sim.sdk.sdk_transport(sim, …)` | SRCI SDK simulator in-process (tests, this demo) |
| `srci.transport.LoopbackTransport(handler, …)` | your own simulation / unit tests |

The telegram lengths (`send_size`, `recv_size`) must match the configuration of the robot /
gateway (here 256 bytes each).

### `SrciClient`: sequential scripts

A robot program in Python is usually written sequentially ("reset, enable, move, wait"). But the
RobotTask needs a cycle at least every *LifeSignTimeOut* (50 ms), also while the script waits.
**`SrciClient`** therefore runs the program like a PLC task: cyclically in a background thread
(`srci-runner`), which starts with the first call of the script (after the configuration) and
stops with `close()` / the end of the `with` block. The script only sets inputs and waits for
outputs – a plain `time.sleep()` does not interrupt the communication:

| Method | Does |
|---|---|
| `wait_initialized()` | waits until the RobotTask is initialized (commands enabled) |
| `execute(block)` | Execute block: rising edge, waits for `Done`, resets `Execute` and removes the block; raises `CommandError` on `Error`/abort, `WaitTimeoutError` after the timeout (`Execute` is reset as well – the command may still run on the RC) |
| `start(block)` / `wait_done(block)` | the same in two steps (e.g. to start several motions) |
| `enable(block)` / `disable(block)` | Enable block: sets `Enable`, waits for `Enabled`/`Valid` (or back); `disable` removes the block |
| `add(block, **inputs)`, `set(block, **inputs)`, `remove(block)` | add a block / set several inputs together / remove it |
| `run(n)`, `idle(seconds)`, `run_until(condition)` | wait for n cycles / a time / a condition |

The helpers change inputs between two cycles (in the cycle thread) and take the results from one
cycle, so they are always consistent. Outputs can be read at any time, a single input of an
active block (e.g. a jog key) may be set directly.

`SrciClient(..., background=False)` (default with `realtime=False` or an own `clock`) runs the
cycles in the calling thread and only while the script waits in a helper – deterministic for
tests and simulations (`--fast`); there pauses must use `client.idle()`.

## 3. Running the demo

```bash
cd examples/core_profile

# real robot behind the PLC gateway (THE ROBOT MOVES - check the positions in the code first!)
python core_profile_demo.py --gateway 192.168.0.10:5000

# SRCI SDK simulator in-process / behind a local TCP gateway
python core_profile_demo.py --sdk
python core_profile_demo.py --sdk-tcp

# options: --fast (simulator: do not wait for the cycle time), --debug (log every telegram)
```

The SDK simulator is not part of the package (the SDK is licensed); it is used when it was built
locally (`SRCI_SDK_SIM_LIB`). The demo is also a test: `tests/sdk/test_example_core_profile.py`
runs it against the SDK simulator (in-process and over TCP with `--fast`, and in-process in real
time with the background cycle).

Output (shortened):

```
=== RobotTask - initialization ============================================
  Initialized                  True
  TelegramState                INITIALIZED
  SRCI version RC              1.5
=== RobotTask - robot data, configuration, messages =======================
  RCManufacturer               SRCI_PY SimRobot
  InterpreterCycleTime [ms]    10
  HighestToolIndex             19
...
=== GroupInterrupt, GroupJog, ReturnToPrimary, GroupContinue ==============
  interrupted                  primary sequence paused
  MotionActive while jogging   True
  ReturnToPrimary.Progress [%] 100.0
  interrupted move             finished after GroupContinue
...
all Core functions executed
```

## 4. The Core functions step by step

The 33 functions of table 5-2 and where the demo uses them:

| # | Function | Block | Demo function |
|---:|---|---|---|
| 1 | RobotTask | `MC_RobotTaskFB` (in `RobotProgram`) | `create_client`, `demo_robot_task` |
| 2 | ReadRobotData | inside the RobotTask (`AxesGroup.State.RobotData`) | `demo_robot_data_configuration_messages` |
| 3 | EnableRobot | `MC_EnableRobotFB` | `demo_group_reset_and_enable` |
| 4 | GroupReset | `MC_GroupResetFB` | `demo_group_reset_and_enable` |
| 5 | ReadActualPosition | `MC_ReadActualPositionFB` | `demo_read_actual_position` |
| 6 | ReadActualPositionCyclic | `MC_ReadActualPositionCyclicFB` | `demo_read_actual_position_cyclic` |
| 7 | ExchangeConfiguration | inside the RobotTask (`AxesGroup.State.ConfigurationData`) | `demo_robot_data_configuration_messages` |
| 8 | SetSequence | `MC_SetSequenceFB` | `demo_set_sequence` |
| 9 | ChangeSpeedOverride | `MC_ChangeSpeedOverrideFB` | `demo_change_speed_override` |
| 10 | ReadMessages | inside the RobotTask (output `MessageLog`) | `demo_robot_data_configuration_messages` |
| 11–12 | CreateServerLog, ReadServerLog | – (not in the PLC library yet) | `demo_logs` |
| 13–14 | CreateClientLog, ReadClientLog | system log of the library | `demo_logs` |
| 15–16 | Read/WriteRobotReferenceDynamics | `MC_Read…`/`MC_WriteRobotReferenceDynamicsFB` | `demo_limits_and_dynamics` |
| 17–18 | Write/ReadRobotDefaultDynamics | `MC_Write…`/`MC_ReadRobotDefaultDynamicsFB` | `demo_limits_and_dynamics` |
| 19–24 | Write/Read Frame, Tool, LoadData | `MC_Write…`/`MC_Read{Frame,Tool,Load}DataFB` | `demo_tool_frame_load` |
| 25 | ReadRobotSWLimits | `MC_ReadRobotSWLimitsFB` | `demo_limits_and_dynamics` |
| 26 | GroupJog | `MC_GroupJogFB` | `demo_interrupt_jog_return_continue` |
| 27 | MoveLinearAbsolute | `MC_MoveLinearAbsoluteFB` | `demo_moves` |
| 28 | MoveDirectAbsolute | `MC_MoveDirectAbsoluteFB` | `demo_moves` |
| 29 | MoveAxesAbsolute | `MC_MoveAxesAbsoluteFB` | `demo_moves` |
| 30 | GroupStop | `MC_GroupStopFB` | `demo_group_stop` |
| 31 | GroupInterrupt | `MC_GroupInterruptFB` | `demo_interrupt_jog_return_continue` |
| 32 | GroupContinue | `MC_GroupContinueFB` | `demo_interrupt_jog_return_continue` |
| 33 | ReturnToPrimary | `MC_ReturnToPrimaryFB` | `demo_interrupt_jog_return_continue` |

### 4.1 RobotTask – connect and initialize

The client creates the `RobotProgram` (with `MC_RobotTaskFB`) for the transport. Everything that
the RobotTask negotiates with the RC during the initialization is configured before the first
cycle – here the cyclic position data needed by `ReadActualPositionCyclic`:

```python
client = SrciClient(transport)  # RobotProgram with MC_RobotTaskFB
cfg = client.program.config  # RobotTaskParCfg
cfg.Rob.OptionalCyclic.UseJointPosition = True  # cyclic joint position RC -> PLC
cfg.Rob.OptionalCyclic.UseCartesianPosition = True  # cyclic Cartesian position RC -> PLC
cfg.Rob.Parameter.MessageLevel = MessageLevel.WARNING

client.wait_initialized(timeout=10.0)
rt = client.program.robot_task  # outputs of MC_RobotTaskFB
print(rt.Initialized, client.program.axes_group.Cyclic.RobToPlc.TelegramState.name)
```

The RobotTask runs the start-up handshake (telegram state `READY_FOR_INITIALIZATION` →
`INITIALIZE` → `INITIALIZED`), reads the robot data, exchanges the configuration and starts
`ReadMessages` internally. After that `AxesGroup.State.CMDsEnabled` is TRUE and commands can be
sent. The RobotTask also supervises the life sign and reports lost communication
(`rt.Error`, `rt.ErrorID`).

Optional: synchronisation of tools, frames, loads … between PLC and RC
(`cfg.Plc.Parameter.SynchronizationModes`) – then the user data arrays of the program
(`client.program.tools`, `.frames`, …) are kept equal to the RC and `rt.Synchronized` becomes TRUE.

### 4.2 Robot data, configuration and messages – inside the RobotTask

`ReadRobotData`, `ExchangeConfiguration` and `ReadMessages` are executed by the RobotTask itself:
the first two during the initialization, `ReadMessages` permanently. They are **not** called by
the user program; their results are available in the axes group and in the outputs of the
RobotTask:

```python
ag = client.program.axes_group
robot = ag.State.RobotData  # ReadRobotData
print(robot.RCManufacturer, robot.RCFirmwareVersion, robot.InterpreterCycleTime)
if robot.RCSupportedFunctions.MoveLinearAbsolute: ...

config = ag.State.ConfigurationData  # ExchangeConfiguration
print(config.HighestToolIndex, config.HighestFrameIndex, config.HighestLoadIndex)

for m in client.program.message_log:  # RobotTask output MessageLog (RC + command messages)
    if m.MessageCode:
        print(m.Severity.name, m.MessageText)
```

What the RobotTask sends is configured before the first cycle, e.g. the message level of the RC
messages: `cfg.Rob.Parameter.MessageLevel = MessageLevel.WARNING`.

### 4.3 GroupReset and EnableRobot

`GroupReset` acknowledges errors of the axes group; `EnableRobot` switches the drives on and keeps
them on while `Enable` is TRUE:

```python
client.execute(MC_GroupResetFB())
enable = client.enable(MC_EnableRobotFB())  # enable.Enabled == True: robot has power
...
client.disable(enable)  # at the end: drives off
```

### 4.4 ChangeSpeedOverride

```python
ov = MC_ChangeSpeedOverrideFB()
ov.ParCmd.Override = 50.0  # % of the programmed velocity, applies to all motions
client.execute(ov)
```

### 4.5 ReadActualPosition and ReadActualPositionCyclic

`ReadActualPosition` is a command (one answer per `Execute`); `ReadActualPositionCyclic` reads
the positions the RC sends in **every** telegram (configured in 4.1) – no command, no delay:

```python
rp = client.execute(MC_ReadActualPositionFB())
print(rp.OutCmd.ActualJointPosition.J1, rp.OutCmd.ActualCartesianPosition.X)

cyc = MC_ReadActualPositionCyclicFB()
cyc.ParCmd.ReadJointPosition = True
cyc.ParCmd.ReadCartesianPosition = True  # in the coordinate system ParCmd.ToolNo / FrameNo
client.enable(cyc)
# from now on cyc.OutCmd.JointPosition / CartesianPosition follow the robot in every cycle
```

`OutCmd.CoordinateSystem` is the tool/frame of the returned position,
`OutCmd.CurrentCoordinateSystem` the tool/frame the robot currently uses (finding F59: the PLC
library mixed them up – fixed in Python).

### 4.6 Tool, frame and load data

Tool, frame and load 0 are fixed on the RC (flange, world, no load); the user data start at
index 1. A tool refers to its load (`LoadNo` ≥ 1):

```python
wt = MC_WriteToolDataFB()
wt.ParCmd.ToolNo = 1
wt.ParCmd.ToolData.Z = 150.0  # TCP 150 mm in front of the flange
wt.ParCmd.ToolData.LoadNo = 1
client.execute(wt)

rt = MC_ReadToolDataFB()
rt.ParCmd.ToolNo = 1
client.execute(rt)
print(rt.OutCmd.ToolData.Z)
```

Frames (`MC_WriteFrameDataFB`/`MC_ReadFrameDataFB`, `FrameNo`, `FrameData.X…Rz`) and loads
(`MC_WriteLoadDataFB`/`MC_ReadLoadDataFB`, `LoadNo`, `LoadData.Mass`, center of mass `X…Z`,
inertia `Ix…Iz`) work the same way.

### 4.7 SW limits and dynamics

```python
sw = client.execute(MC_ReadRobotSWLimitsFB())
print(sw.OutCmd.LimitValues.J1LowerLimit, sw.OutCmd.LimitValues.J1UpperLimit)

rd = client.execute(MC_ReadRobotDefaultDynamicsFB())
wd = MC_WriteRobotDefaultDynamicsFB()
copy_into(wd.ParCmd.DynamicValues, rd.OutCmd.DynamicValues)  # keep all other values
wd.ParCmd.DynamicValues.VelocityRate = 50.0
client.execute(wd)
```

The *default dynamics* are used by every motion whose rates are −1.0 (the default of all
`VelocityRate`, `AccelerationRate`, `DecelerationRate`, `JerkRate` inputs); the *reference
dynamics* (`MC_Read/WriteRobotReferenceDynamicsFB`) are the 100 % values the rates refer to.

### 4.8 Motions

All motions are Execute blocks. By default (`AbortingMode = BUFFER`) a new motion waits for the
running one; `ABORT` replaces it.

```python
move = MC_MoveAxesAbsoluteFB()  # PTP in joint coordinates
move.ParCmd.JointPosition.J1 = 45.0
client.execute(move)  # returns when the robot is there

md = MC_MoveDirectAbsoluteFB()  # PTP to a Cartesian position
md.ParCmd.Position.X, md.ParCmd.Position.Y, md.ParCmd.Position.Z = 30.0, 10.0, 20.0
md.ParCmd.ToolNo = 1
client.execute(md)

first, second = MC_MoveLinearAbsoluteFB(), MC_MoveLinearAbsoluteFB()  # linear motions
...  # positions, ToolNo, VelocityRate
client.start(first)
client.start(second)  # buffered: second.CommandBuffered == True
client.wait_done(first)
client.wait_done(second)
```

### 4.9 Interrupt, jog, return, continue

`GroupInterrupt` pauses the *primary sequence* (the programmed motions). While it is paused the
*secondary sequence* may move the robot, e.g. jogging. `ReturnToPrimary` moves back to the
position where the primary sequence was left, `GroupContinue` resumes it:

```python
mv = client.start(move_axes(60.0))
client.idle(0.3)
client.execute(MC_GroupInterruptFB())

jog = MC_GroupJogFB()
jog.ParCmd.Mode = JogMode.JOG_AXES
jog.ParCmd.Override = 50
client.enable(jog)
jog.ParCmd.Control.Y_J2_Pos = True  # like holding the "J2 +" key
client.idle(0.3)
jog.ParCmd.Control.Y_J2_Pos = False
client.disable(jog)

rtp = MC_ReturnToPrimaryFB()
rtp.ParCmd.ToolNo = TOOL  # tool of the interrupted motion
client.add(rtp, Enable=True)
client.run_until(lambda: rtp.Done or rtp.Error)
client.disable(rtp)

client.execute(MC_GroupContinueFB())
client.wait_done(mv)  # the interrupted motion finishes
```

### 4.10 GroupStop

Stops the robot and aborts all motions (`CommandAborted` of the running and the buffered blocks):

```python
mv = client.start(move_axes(-60.0))
client.idle(0.3)
client.execute(MC_GroupStopFB())
client.run_until(lambda: mv.CommandAborted)
client.wait_done(mv, check=False)  # resets Execute and removes the aborted block
```

### 4.11 SetSequence

Switches the active sequence (primary / secondary) explicitly:

```python
seq = MC_SetSequenceFB()
seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
client.execute(seq)
seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
client.execute(seq)
```

Motions are assigned to a sequence with their input `SequenceFlag`.

### 4.12 Logs

- **Client log** (CreateClientLog/ReadClientLog): every block writes its log entries into the
  system log of the axes group – `client.program.system_log` (ring buffer, newest first) and,
  if set, an external logger. `srci.logging_bridge.PythonLogger` forwards them to Python
  `logging` (`--debug` in the demo):

  ```python
  client.program.external_logger = PythonLogger()  # loggers "srci.plc" and "srci.rc"
  client.program.log_level = Severity.DEBUG
  ```

- **Server log** (CreateServerLog/ReadServerLog): not implemented in the PLC library yet
  (`MC_CreateServerLog_ToDo`, `MC_ReadServerLog` are empty).
- **Messages** of the RC and of the commands: RobotTask output `MessageLog`
  (`client.program.message_log`).

## 5. Patterns for your own program

**Sequential script** (like the demo):

```python
import srci
from srci.api import SrciClient
from srci.fb import MC_EnableRobotFB, MC_GroupResetFB, MC_MoveAxesAbsoluteFB
from srci.transport import TcpTransport

with SrciClient(TcpTransport("192.168.0.10", 5000, 256, 256)) as client:
    client.wait_initialized()
    client.execute(MC_GroupResetFB())
    enable = client.enable(MC_EnableRobotFB())
    move = MC_MoveAxesAbsoluteFB()
    move.ParCmd.JointPosition.J1 = 30.0
    client.execute(move)
    client.disable(enable)
```

**Own cycle loop** without `SrciClient` (e.g. a long running program with an own state
machine; other threads interact through `runner.call`):

```python
from srci.api import RobotProgram
from srci.runtime import Runner

program = RobotProgram(256, 256)
move = program.add(MC_MoveAxesAbsoluteFB())
with Runner(transport, program, cycle_time=0.01) as runner:  # runs until the with block ends
    runner.call(lambda: setattr(move, "Execute", True))  # set inputs in the cycle thread
    ...
```

**Without any transport**: `program.step(robot_in_data) -> robot_out_data` executes one cycle; the
bytes can be exchanged with any fieldbus stack.

**Library parameters** (array sizes, like the library parameters in Codesys) are set before the
first block is created: `srci.configure(TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)`.

## 6. Troubleshooting

| Symptom | Cause |
|---|---|
| `WaitTimeoutError` in `wait_initialized` | no answer of the RC: gateway address/port, telegram lengths of both sides, robot in the right mode |
| `CommandError … ErrorID 16#80A2` (and `rt.Error`) | RobotTask lost the initialization (e.g. life sign timeout – no cycles for > 50 ms, e.g. `time.sleep()` with `background=False`, or an overloaded computer – see `client.runner.monitor`) |
| `CommandError … ErrorID 16#8xxx` | error of the RC, see spec table 7-1 (e.g. `16#8D17` invalid load number, `16#8E03` invalid dynamics) |
| motion does not start | robot not enabled, primary sequence interrupted (→ `GroupContinue`), override 0 |
| `ReturnToPrimary` fails with `16#8C22…8C27` | tool/frame/load differ from the interrupted motion – use the same `ToolNo`/`FrameNo` |

The messages in the RobotTask output `MessageLog` and the system log (`--debug`) usually tell the reason.
