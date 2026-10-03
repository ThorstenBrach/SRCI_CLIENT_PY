# Example: first steps with a JAKA MiniCobo behind a TwinCAT PLC gateway

[`minicobo.py`](minicobo.py) connects to a real robot over the PLC gateway and does two things:

- `info`: initialize and read everything that does not move the robot
- `move`: enable the robot and move **one** joint by a few degrees relative to its current
  position, then back

```
PC (Python, srci)  --TCP 192.168.2.10:5000-->  TwinCAT PLC (FB_SrciTcpGateway)  --PROFINET-->  JAKA MiniCobo (SRCI)
                   <-- 256 bytes per request --                                 <-- 256 bytes --
```

The PLC only forwards the telegrams (256 bytes in, 256 bytes out, lockstep); the whole SRCI logic
(`MC_RobotTaskFB`, commands) runs in Python. The PLC project is `SRCI_TcpGateway` (TwinCAT,
TF6310, `FB_SrciTcpGateway`).

The JAKA MiniCobo supports only the profile **Core**, so the example uses only Core functions:
the RobotTask (ReadRobotData, ExchangeConfiguration, ReadMessages), GroupReset, EnableRobot,
ChangeSpeedOverride, ReadRobotSWLimits, ReadActualPosition, MoveAxesAbsolute and GroupStop. The
synchronization of user data stays off (it would need e.g. ReadWorkArea, which is not Core).
`info` shows which Core functions the robot reports in `RCSupportedFunctions` and whether it
reports anything beyond Core.

## 1. Prerequisites

| What | Check |
|---|---|
| Python ≥ 3.12 with the `srci` package | `pip install -e .` in the SRCI_PY clone (or the wheel) |
| PLC gateway running | `GVL_Gateway.Gateway.Listening = TRUE`, port 5000 open in the Windows firewall of the PLC |
| PROFINET | the robot is an online PROFINET device of the PLC, `RobotInData`/`RobotOutData` are linked to its SRCI input/output modules (256 bytes each) |
| Robot | SRCI/PROFINET control enabled on the JAKA controller (see the JAKA documentation), no pending error, operating mode that allows external control |
| Network | the PC reaches 192.168.2.10 (`ping 192.168.2.10`) |

## 2. Dry run without robot (optional)

With the locally built SDK library (`SRCI_SDK_SIM_LIB`) the same script runs against the SRCI SDK
simulator behind a local TCP gateway – the same code path as with the robot:

```bash
python minicobo.py info --sdk-tcp
python minicobo.py move --sdk-tcp --yes
```

## 3. `info` – the robot does not move

```bash
cd examples/jaka_minicobo
python minicobo.py info                    # 192.168.2.10:5000, 256 bytes
python minicobo.py info --host 192.168.2.10 --port 5000 --length 256
```

Shows: initialization (TelegramState, SRCI version of the RC, time), robot data (manufacturer,
serial numbers, firmware, Core functions supported / missing), configuration (tool/frame/load indices), software
limits, actual position (joints and Cartesian, tool 0 / frame 0), messages of the RC and
round-trip times of the TCP connection.

## 4. `move` – THE ROBOT MOVES

```bash
python minicobo.py move                         # J6 +5 deg, override 10 %, velocity 10 %
python minicobo.py move --joint 1 --delta -3    # J1 -3 deg
```

Sequence: read SW limits and actual position → check the target against the limits →
**confirmation prompt** (skip with `--yes`) → GroupReset → EnableRobot → ChangeSpeedOverride →
MoveAxesAbsolute to the target → MoveAxesAbsolute back → EnableRobot off.

- `--delta` is limited to ±30°, `--override`/`--velocity` to 0 < x ≤ 100 %.
  `--velocity -1` uses the default dynamics of the RC (if it does not support `VelocityRate`).
- On an error or Ctrl+C during the motion the script sends **GroupStop** and disables the robot.
- Have the emergency stop of the robot within reach. SRCI is not a safety interface; Python is
  not a real-time system.

## 5. Options

| Option | Default | Meaning |
|---|---|---|
| `--host`, `--port` | 192.168.2.10, 5000 | PLC gateway |
| `--length` | 256 | telegram length per direction = PROFINET module size |
| `--srci-version` | 1.5 | SRCI version in byte 0 of the header (e.g. `1.3` = 16#23 for an RC with an older SRCI version) |
| command `blending` | – | which BlendingModes the RC accepts: every mode with a 1 mm linear / 0.5° joint move and back (`16#8E05` = not supported) |
| `--joint`, `--delta` | 6, 5.0 | joint and relative move [deg] (`move`) |
| `--override`, `--velocity` | 10, 10 | speed override / velocity rate [%] (`move`) |
| `--lifesign-ms` | 100 | LifeSign timeout of the RC (sent with ExchangeConfiguration) |
| `--timeout` | 15 | time for the initialization [s] |
| `--yes` | – | move without confirmation |
| `--log FILE` | `minicobo_<date>_<time>.log` | log file in the current folder (see 7.) |
| `--no-log` | – | no log file |
| `--trace-all` | – | log file: every telegram (default: the first 50, every change of TelegramState/Control, every 100th) |
| `--debug` | – | show the whole log on the console as well |
| `--sdk-tcp`, `--fast` | – | dry run against the SDK simulator |

## 6. Troubleshooting

| Symptom | Cause / check |
|---|---|
| `cannot connect to 192.168.2.10:5000` | PLC not in RUN, gateway `Enable`/`Listening`, firewall, IP |
| not initialized, `exchanges = 0`, `timeouts > 0` | connection accepted, but no answers: gateway `Connected`, `ErrorID`, lengths in `MAIN` |
| not initialized, `TelegramState UNDEFINED`, exchanges > 0 | the PLC answers, but `RobotInData` stays 0: PROFINET device not in data exchange, mapping of `RobotInData`, robot not in SRCI mode |
| `ERROR_163_TELEGRAM_LENGTH_MISMATCH` | `--length` ≠ PROFINET module size of the robot |
| `ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE` | SRCI version of the robot firmware ≠ 1.x |
| initialized, then lost again (LifeSign timeout) | Python cycle too slow or blocked: `MaxInterval` of the gateway, `--lifesign-ms` higher, PLC task / PROFINET cycle shorter |
| `16#8E03 … Optional parameter value not supported` | the RC does not support an optional parameter (e.g. `VelocityRate`): `--velocity -1` |
| move refused (`16#8xxx`) | the message text in the "Messages" section names the reason (mode, enable, limits) |

If the RobotTask does not initialize, the script prints a diagnosis: the step of the RobotTask,
the TelegramState and the first 18 bytes of both telegrams. `RobotInData is all 0` means the PLC
answers, but the robot sends nothing over PROFINET.

## 7. Log file

Every run writes `minicobo_<date>_<time>.log` into the current folder (path at the start and at
the end of the output):

| Logger | Content |
|---|---|
| `srci.plc` | system log of all function blocks at level DEBUG: state changes of the RobotTask, commands sent, responses, errors (the same texts as `SystemLog` in the PLC) |
| `srci.telegram` | the raw telegrams as hex (`#n PLC->RC …`, `#n RC->PLC …`): the first 50 exchanges, every change of Control/TelegramState and every 100th; `--trace-all` logs every telegram |
| `srci.transport` | connect, timeouts, reconnects |

Header bytes for reading the telegram trace: PLC→RC byte 0 SRCI version (16#25 from this
library), byte 1 LifeSign, bytes 2..5 lengths, byte 6 AxesGroupID (high nibble) / Control (low
nibble: 1 INITIALIZE, 3 RESET); RC→PLC byte 1 LifeSign (high nibble), byte 3 TelegramState
(254 READY_FOR_INITIALIZATION, 255 INITIALIZED, 161..173 errors).

## 8. VS Code: run and debug

Add a configuration to `.vscode/launch.json` of the `SRCI_PY` folder (the folder is not part of
the repository; one entry per command / target):

```json
{
  "name": "MiniCobo: info (robot, no motion)",
  "type": "debugpy",
  "request": "launch",
  "program": "${workspaceFolder}/examples/jaka_minicobo/minicobo.py",
  "args": ["info"],
  "cwd": "${workspaceFolder}/examples/jaka_minicobo",
  "console": "integratedTerminal",
  "justMyCode": false
}
```

Further entries: `"args": ["move", "--joint", "6", "--delta", "5"]` (the robot moves),
`"args": ["info", "--sdk-tcp", "--fast"]` / `["move", "--sdk-tcp", "--fast", "--yes"]` (SDK
simulator, breakpoints ok).

1. Open the folder `SRCI_PY` in VS Code, install the extension "Python" (with "Python Debugger").
2. Select the interpreter of the venv: Ctrl+Shift+P → "Python: Select Interpreter" →
   `.venv\Scripts\python.exe`.
3. Set a breakpoint (F9) and start a configuration with F5. `justMyCode` is off, so you can also
   step into the library (`src/srci`, e.g. `MC_RobotTaskFB.py`).

**Breakpoints with the real robot:** a breakpoint stops all threads, including the cycle thread
of `SrciClient`. No telegram is sent while the program stands - after the LifeSign timeout
(100 ms) the robot controller leaves the initialized state, and the TCP connection runs into its
response timeout. After continuing, the RobotTask has to initialize again (restart the script).
So: with the real robot use the log file; for stepping through the code use the configurations
"against the SDK simulator" (`--sdk-tcp --fast`: the cycles run only while the script waits, a
breakpoint does not break anything there).
