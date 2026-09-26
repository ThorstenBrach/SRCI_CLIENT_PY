# SRCI for Python

Python client for the **Standard Robot Command Interface (SRCI)**, profile V1.5.9.

This is a port of the open SRCI PLC library for Codesys/TwinCAT
([ThorstenBrach/SRCI](https://github.com/ThorstenBrach/SRCI)). Function blocks,
methods, step numbers and error ids mirror the PLC library 1:1, so that fixes
can be ported between both implementations (see [docs/PORTING.md](docs/PORTING.md)).

> Status: rewrite in progress (branch `rewrite`). The previous experimental port
> is preserved on branch `legacy` / tag `legacy-v0`.

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
```

## License

MIT – see [LICENSE](LICENSE).

The developed software is based on the SRCI technology of "PROFIBUS and PROFINET
International" (PI), but it is not an official publication of PI.
This project is provided without any guarantee. Any use is at the user's own risk.
