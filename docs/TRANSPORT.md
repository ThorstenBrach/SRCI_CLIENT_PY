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
