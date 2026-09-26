# SRCI for Python

Python client for the **Standard Robot Command Interface (SRCI)**, profile V1.5.9.

This is a port of the open SRCI PLC library for Codesys/TwinCAT
([ThorstenBrach/SRCI](https://github.com/ThorstenBrach/SRCI)). Function blocks,
methods, step numbers and error ids mirror the PLC library 1:1, so that fixes
can be ported between both implementations (see [docs/PORTING.md](docs/PORTING.md)).

> Status: rewrite in progress (branch `rewrite`). The previous experimental port
> is preserved on branch `legacy` / tag `legacy-v0`.

## Installation

```bash
pip install srci_client-<version>-py3-none-any.whl   # wheel built with "python -m build"
pip install -e .                                     # or from a clone of the repository
```

The wheel can also be built without any build dependency: `python -m tools.build_dist`
(writes `dist/`). Python ≥ 3.12, no runtime dependencies.

## Quick start

```python
from srci.api import SrciClient
from srci.fb import MC_EnableRobotFB, MC_GroupResetFB, MC_MoveAxesAbsoluteFB
from srci.transport import TcpTransport

with SrciClient(TcpTransport("192.168.0.10", 5000, 256, 256)) as client:
    client.wait_initialized()  # MC_RobotTaskFB: handshake with the RC
    client.execute(MC_GroupResetFB())
    enable = client.enable(MC_EnableRobotFB())
    move = MC_MoveAxesAbsoluteFB()
    move.ParCmd.JointPosition.J1 = 30.0
    client.execute(move)  # returns when the robot is there
    client.disable(enable)
```

* `srci.fb` – all function blocks of the PLC library (`MC_…FB`, same inputs/outputs as in the PLC)
* `srci.types` – all data types and enums
* `srci.api.RobotProgram` – RobotTask + user data + command blocks (one "PLC program"),
  `srci.api.SrciClient` – runs it from a sequential script, `srci.runtime.Runner` – cyclic in a thread

**Example:** [examples/core_profile](examples/core_profile) executes every function of the profile
"Core" and explains the library step by step ([README](examples/core_profile/README.md)).

## How the port is made

The data types, function blocks and functions are **generated** from the PLCopen XML
export of the PLC library (`third_party/robotlibrary/RobotLibrary.xml`): a small
ST → Python transpiler (`tools/st2py`) keeps names, step chains and comments of the
ST code. Only the telegram coding and the send/receive buffers are hand written.
Deviations (bug fixes) are documented in `tools/st2py/config.py` and
[docs/ST_FINDINGS.md](docs/ST_FINDINGS.md).

Library parameters (like the library parameters of a Codesys project) are set before
the first function block is created:

```python
import srci

srci.configure(TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
```

## How it talks to the robot

SRCI is transported over PROFINET. A PLC acts as gateway: it exchanges the
PROFINET process data with the robot controller and forwards the raw SRCI
byte array to Python over TCP/IP.

```
Python (srci)  --TCP, raw telegram-->  PLC gateway  --PROFINET-->  Robot controller
               <--one reply per request--
```

* Python is the cycle master: it sends one telegram per cycle, the PLC answers
  each received telegram with exactly one telegram (lockstep).
* No extra framing: telegram lengths are fixed by configuration on both sides.
* The transport is exchangeable (`srci.transport.Transport`); the library core can
  also be used without any transport (`cycle(in_bytes) -> out_bytes`).

## Development

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows  (Linux: source .venv/bin/activate)
pip install -e ".[dev]"

pytest                        # tests
ruff check . && ruff format --check .
mypy
python -m tools.plcopen_gen   # regenerate types from third_party/robotlibrary/RobotLibrary.xml
python -m tools.st2py         # regenerate function blocks and functions
```

### SDK in the loop

The SRCI SDK (robot controller side) is licensed and therefore **not** part of this
repository. It is built locally together with a simulated robot (`srci_py_harness`
in the private SDK folder) into `srci_sdk_sim.dll/.so`, which the tests load with
`ctypes`. Default location: `../SRCI SDK/srci_py_harness/bin/`, or set
`SRCI_SDK_SIM_LIB` / `SRCI_SDK_DIR`.

```bash
pytest -m sdk      # SDK in the loop tests (skipped if the library is missing)
pytest -m tcp      # tests with local TCP sockets
```

In CI the job `sdk` checks the SDK out of a private repository, builds it and runs these tests
without showing anything of the SDK in the logs – see [docs/CI_SDK.md](docs/CI_SDK.md).

### Test cases and test report

Every test has a unique, stable ID (`tests/testcases.json`); all test cases are listed and
described in [docs/TestCases.md](docs/TestCases.md), known deviations of the PLC library in
[docs/ST_FINDINGS.md](docs/ST_FINDINGS.md).

```bash
pytest --tc-report build/test-report    # TestReport.md + TestReport.html (quality evidence)
python -m tools.test_report update      # assign IDs to new tests
python -m tools.test_report catalog     # regenerate docs/TestCases.md
```

## License

MIT – see [LICENSE](LICENSE).

The developed software is based on the SRCI technology of "PROFIBUS and PROFINET
International" (PI), but it is not an official publication of PI.
This project is provided without any guarantee. Any use is at the user's own risk.
