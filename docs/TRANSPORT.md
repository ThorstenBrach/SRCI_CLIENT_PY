# Transport: Python ↔ PLC gateway

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

## Other transports

- `LoopbackTransport(handler, …)` - in-process, e.g. with the SDK simulator.
- `FaultInjectingTransport(inner, FaultPlan(...))` - deterministic faults for tests
  (timeout, lost request, disconnect, bit flip, stale answer, protocol violation).
- `srci.sim.gateway.PlcGatewaySimulator` - TCP server that behaves like the gateway PLC
  (used by the TCP tests and by `--sdk-tcp` of the examples, with the SDK simulator behind it).

## SDK server for PLC tests

`python -m srci.sim.server --port 5000 --length 256` runs the SDK simulator behind a TCP server
with the same protocol, so a PLC (TwinCAT, Codesys) can test the SRCI PLC library against it:
the PLC is the TCP client and the cycle master, every telegram is one cycle of the simulator
(10 ms). A new connection starts a new simulator. The status line shows gaps and repeats of the
PLC LifeSign, `--dump` the decoded telegram headers. Needs the locally built SDK library
(`SRCI_SDK_SIM_LIB`).

### Control channel

The Python tests set up and check the simulator directly (`sim.set_move_cycles(20)`,
`sim.joints`, `sim.last_command(...)`). A PLC test does the same over a second TCP port, the
control channel (`--control-port`, default 5001, `0` switches it off; `srci.sim.control`):
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
| `MARK`, `COUNT_COMMANDS <type>`, `LOG_CONTAINS <text>` | log window of the SDK |
| `TAMPER FREEZE / KEEP_ACK <start> / SET <i> <v> / XOR <i> <m> / REQ_SET <i> <v> / OFF` | fault injection on the telegrams |

The answer is `OK [value]` or `ERR <reason>`; numbers can be written as `123`, `16#7B` or `0x7B`.
The TcUnit project SRCI_PLC_TEST uses it (`SdkControlFB`).
