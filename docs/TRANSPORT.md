# Transport: Python ↔ PLC gateway / OPC UA server

```
Python (srci)  --TCP, raw telegram-->  PLC gateway  --PROFINET-->  Robot controller (RC)
               <--exactly one reply--
```

## Protocol

| Item | Definition |
|---|---|
| Roles | PLC = TCP server, Python = TCP client (one client at a time) |
| Payload | raw SRCI telegram, **no** additional header or framing |
| Lengths | fixed per direction: PLC→RC `TelegramLengthPlcToRob`, RC→PLC `TelegramLengthRobToPlc` (e.g. 256/256). Both sides must be configured identically |
| Order | lockstep: Python sends one telegram per cycle, the PLC answers each received telegram with exactly one telegram. The PLC never sends on its own |
| Cycle | defined by Python (`exchange()` per cycle). The cycle time must stay well below the LifeSign timeout of the RC |
| Integrity | provided by SRCI itself (LifeSign in header and footer, sequence ACKs) |

## Behaviour of `TcpTransport`

- `exchange(out)` sends exactly `send_size` bytes and returns exactly `recv_size` bytes.
  Answers arriving in several TCP segments are assembled.
- **Response timeout** (default 100 ms): if the answer is not complete in time, the
  connection is closed. Reason: without framing a late answer would be read as the answer
  of the next request and shift the stream. The next `exchange` reconnects and starts
  with a clean stream.
- **Lockstep check**: if more bytes than one telegram arrive, `TransportProtocolError`
  is raised and the connection is closed (can be disabled with `check_extra_bytes=False`).
- **Reconnect**: automatic on the next `exchange`, with exponential backoff after failed
  connection attempts (`ReconnectPolicy`, default 0.1 s … 2 s).
- Errors: `TransportConnectError`, `TransportTimeoutError`, `TransportClosedError`,
  `TransportProtocolError` (all derived from `TransportError`). Statistics in
  `transport.statistics` (exchanges, timeouts, reconnects, round trip times).

## Requirements for the PLC gateway FB

1. TCP server on a configurable port, accept one client; a new client replaces the old one.
2. Read exactly `TelegramLengthPlcToRob` bytes, copy them to the PROFINET output data of
   the robot, answer with the current PROFINET input data (`TelegramLengthRobToPlc` bytes).
3. Answer in the same PLC cycle if possible (the Python timeout is 100 ms by default).
4. Never send without a request.
5. When the client disconnects: stop forwarding. The RC detects the missing LifeSign
   change and leaves the initialized state - no special handling needed.

## OPC UA transport

```
Python (srci)  --OPC UA Write out_node, Read in_node-->  OPC UA server (PLC bridge or robot controller)
```

For a PLC bridge that offers the PROFINET process data of the robot on its OPC UA server, or for robot
controllers that offer the SRCI telegrams on their own OPC UA server.

Status:

- tested against a local asyncua server (`tests/opcua`);
- **tested on 2026-10-18 with a JAKA MiniCobo**: TwinCAT PLC as OPC UA bridge
  (`ns=4;s=GVL_Bridge.RobotOutData` written, `ns=4;s=GVL_Bridge.RobotInData` read, both `Byte[256]`)
  -> PROFINET -> robot; connected and moved with SRCI_PY_HMI, LifeSign timeout 500 ms, no timeouts;
- not yet tested with a robot controller that has its own OPC UA server.

```python
from srci.transport import OpcUaTransport

transport = OpcUaTransport(
    "opc.tcp://192.168.0.254:4840",     # endpoint
    "ns=2;s=SRCI.PlcToRob",             # out_node: PLC->RC telegram, written
    "ns=2;s=SRCI.RobToPlc",             # in_node:  RC->PLC telegram, read
    256, 256,                           # send_size, recv_size
    timeout=1.0,                        # per request
    username=None, password=None,       # optional; anonymous without
)
```

Installation: `pip install srci-client[opcua]` (package [asyncua](https://github.com/FreeOpcUa/opcua-asyncio),
LGPL-3.0). It is imported only when a connection is opened, `import srci.transport` works without it;
a missing asyncua gives `TransportConnectError` with the install hint.

| Item | Definition |
|---|---|
| Exchange | per cycle one **Write** of the PLC->RC telegram to `out_node`, then one **Read** of `in_node` |
| Handshake | none on the OPC UA level: request and answer are matched by the SRCI protocol (sequence ACKs, LifeSign) like on PROFINET; the RC does not have to answer within the same cycle |
| Data type | detected on connect from the current value (or the declared data type of an empty node): `ByteString` or a one dimensional array of `Byte`, `SByte`, `(U)Int16/32/64`, `Float`, `Double` - one telegram byte per element (0 ... 255). The write keeps the encoding of the node |
| Length check | on connect the current value must have `send_size` / `recv_size` bytes (an empty node is accepted; `check_lengths=False` switches it off). Every read answer must have `recv_size` bytes, else `TransportProtocolError` (the connection stays) |
| Timeout | `timeout` per request (connect, write, read); exceeded: `TransportTimeoutError`, the connection is closed |
| Errors | connection lost, bad status code: `TransportClosedError`; the next `exchange` reconnects with the `ReconnectPolicy` backoff (like TCP) |
| Security | first version without security; user / password optional, `security` takes the security string of asyncua (`"Basic256Sha256,Sign,cert.der,key.pem"`, prepared, not tested) |
| Cycle time | one write + one read are two round trips (typically 1 ... 5 ms in a LAN, more with security). Keep the cycle well below the LifeSign timeout of the RC |

`srci.transport.opcua.browse(endpoint)` lists the variables of a server (NodeId, path, data type,
length, writable, `telegram_candidate`) - used by the connection configurator of the HMI.

`srci.sim.opcua.OpcUaRcSimulator(handler, send, recv)` is the counterpart for tests and demos: an
asyncua server with the nodes `SRCI.PlcToRob` / `SRCI.RobToPlc` that runs its own cycle (10 ms) like a
robot controller and answers with `handler` - e.g. the SDK simulator
(`tests/opcua/test_opcua_sim.py`: SrciClient over OPC UA against the SDK, RobotTask initialized).

Notes for robot controllers:

- Writing usually needs a logged-in user; anonymous sessions are often read only.
- Controllers whose OPC UA server publishes only scalar `num`/`bool`/`string` variables cannot carry
  a telegram; number **arrays** (`Double[]`) work since the data type is detected.
- Some controllers offer SRCI also over a TCP socket of their own; whether that protocol matches
  the raw telegram exchange of `TcpTransport` has to be checked per manufacturer.

## Other transports

- `LoopbackTransport(handler, …)` - in-process, e.g. with the SDK simulator.
- `FaultInjectingTransport(inner, FaultPlan(...))` - deterministic faults for tests
  (timeout, lost request, disconnect, bit flip, stale answer, protocol violation).
- `srci.sim.gateway.PlcGatewaySimulator` - TCP server that behaves like the gateway PLC
  (used by the TCP tests and by `--sdk-tcp` of the examples, with the SDK simulator behind it).

## SDK server for PLC tests

`python -m srci_sdk_sim.server --port 5000 --length 256` runs the SDK simulator behind a TCP server
with the same protocol, so a PLC (TwinCAT, Codesys) can test the SRCI PLC library against it:
the PLC is the TCP client and the cycle master, every telegram is one cycle of the simulator
(10 ms). A new connection starts a new simulator. The status line shows gaps and repeats of the
PLC LifeSign, `--dump` the decoded telegram headers. The server is part of the private SDK
repository (package `srci_sdk_sim` in `srci_py_harness/python`, moved from `srci.sim` on
2026-10-09); it needs the locally built SDK library (`SRCI_SDK_SIM_LIB`).

### Control channel

The Python tests set up and check the simulator directly (`sim.set_move_cycles(20)`,
`sim.joints`, `sim.last_command(...)`). A PLC test does the same over a second TCP port, the
control channel (`--control-port`, default 5001, `0` switches it off; `srci_sdk_sim.control`):
one request line, one answer line, ASCII with LF.

| Request | Answer / effect |
|---|---|
| `PING` | `OK SRCI-SDK-CONTROL 1` |
| `RESET` | new simulator (restart of the RC), no tampering, log window from the start |
| `MOVE_CYCLES <n>`, `FAIL_ENABLE <0/1>`, `MOTION_ERROR <code>` | like `SdkSimulator.set_*` |
| `COMMAND_ERROR <type> <code>`, `RESPONSE <type> <field> <value>`, `CLEAR_RESPONSES` | answers of commands the SDK does not implement |
| `ALL_FUNCTIONS <0/1>`, `JOINTS <j1> ...` | supported functions, joint position |
| `GET ENABLED`, `GET OVERRIDE`, `GET JOINT <n>`, `GET JOINTS`, `GET RI_STATE`, ... | state of the simulator |
| `LAST <type> <field>` | field of the last command as the SDK decoded it |
| `MARK`, `COUNT_COMMANDS <type>`, `LOG_CONTAINS <text>`, `MAX_SEVERITY` | log window of the SDK |
| `TAMPER FREEZE / KEEP_ACK <start> / SET <i> <v> / XOR <i> <m> / REQ_SET <i> <v> / OFF` | fault injection on the telegrams |

The answer is `OK [value]` or `ERR <reason>`; numbers can be written as `123`, `16#7B` or `0x7B`.
The TcUnit project SRCI_PLC_TEST uses it (`SdkControlFB`).
