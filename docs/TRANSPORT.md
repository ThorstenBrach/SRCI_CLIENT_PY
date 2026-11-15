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

- tested against a local asyncua server;
- **tested on 2026-10-18 with a JAKA MiniCobo**: TwinCAT PLC as OPC UA bridge
  (`ns=4;s=GVL_Bridge.RobotOutData` written, `ns=4;s=GVL_Bridge.RobotInData` read, both `Byte[256]`)
  -> PROFINET -> robot; connected and moved with SRCI_PY_HMI, LifeSign timeout 500 ms, no timeouts;
- **tested on 2026-11-14 with a Staubli CS9 in the SRS emulator** (uniVALpi 1.3.4, SRCI 1.3, OPC UA
  server of the controller, one node per byte, profile `staubli_cs9`): RobotTask initialized, robot
  data and read commands; about 15 ms per exchange (2 x 256 nodes). The RC needs
  `WaitAtBlendingZone = TRUE` in ExchangeConfiguration (else 16#8E21).

```python
from srci.transport import OpcUaTransport

transport = OpcUaTransport(
    "opc.tcp://192.168.0.254:4840",  # endpoint
    "ns=2;s=SRCI.PlcToRob",  # out_node: PLC->RC telegram, written
    "ns=2;s=SRCI.RobToPlc",  # in_node:  RC->PLC telegram, read
    256,
    256,  # send_size, recv_size
    timeout=1.0,  # per request
    username=None,
    password=None,  # optional; anonymous without
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

### Node layouts and configuration files

A direction (`out_node` / `in_node`) is either **one node** with the whole telegram (PLC bridge) or
**one node per byte**: a list of `send_size` / `recv_size` NodeIds. That is how robot controllers
publish their PROFINET I/O on OPC UA, e.g. a Staubli CS9 (`...:%IB0`, `...:%IB8` ... one `Byte` node
per telegram byte). Per byte:

| Item | Definition |
|---|---|
| Exchange | all nodes of a direction in **one Write** / **one Read** request; split only if the server publishes a smaller `MaxNodesPerRead/Write` (OperationLimits) or `max_nodes_per_call` is set |
| Data type | every node a number (`Byte`, `(U)Int16/32/64`, `Float`, `Double` ...), one byte each; arrays and other types are rejected on connect |
| Write access | checked on connect (`UserAccessLevel`): a node the session may not write gives `TransportConnectError` ("not writable for an anonymous session") instead of an error in the first cycle |
| `write_changed_only` | optional: write only the bytes that changed since the last cycle (fewer nodes per request; after a (re)connect all bytes once). Off by default |
| `consistency_byte` | optional, PLC->RC: the nodes are not written at the same instant, so an RC that takes a snapshot may see half old, half new bytes. With `consistency_byte = n` byte n is written invalid first (a value neither old nor new), then all other bytes, then byte n with its new value - a snapshot in between fails the RC's check. Staubli CS9: byte 255 (uniVALpi processes a telegram only if it equals the LifeSign in byte 1) |

The layout of a robot is kept in a **configuration file** (TOML), so nobody has to link hundreds of
nodes by hand. `{bit}` (= 8 * byte number) and `{index}` (byte number, from `first`) in `nodes`
expand to one NodeId per byte:

```toml
name = "Staubli CS9 uniVALpi"
endpoint = "opc.tcp://192.168.2.117:853/Staubli"
username = "maintenance"
password_env = "SRCI_OPCUA_PASSWORD"   # the password is not stored in the file
cycle_ms = 20                          # recommendations for the application (HMI)
lifesign_timeout_ms = 1000

[plc_to_rc]                            # written by the client
nodes = "ns=1;s=Robot:Inputs/Outputs:J207J208-SiemensTRL_256:%IB{bit}"
size = 256

[rc_to_plc]                            # read by the client
nodes = "ns=1;s=Robot:Inputs/Outputs:J207J208-SiemensTRL_256:%QB{bit}"
size = 256
```

```python
from srci.transport import OpcUaTransport, opcua_profiles

transport = OpcUaTransport.from_config("my_robot.toml", password="...")  # own file
transport = OpcUaTransport.from_profile("staubli_cs9", password="...")  # shipped file
print(opcua_profiles())  # ['srci_bridge_twincat', 'staubli_cs9']
```

Keys: `endpoint`, `[plc_to_rc]` and `[rc_to_plc]` with `nodes` (NodeId, template or list) and `size`
(optional `first`, in `[plc_to_rc]` also `consistency_byte`) are required; optional `name`, `description`, `username`, `password_env`,
`password` (avoid), `security`, `timeout`, `check_lengths`, `write_changed_only`,
`max_nodes_per_call`, `cycle_ms`, `lifesign_timeout_ms`. Unknown keys are kept in `config.extra`.
Arguments of `from_config` override the file. Shipped files (`src/srci/transport/opcua_profiles`):

| Profile | Layout |
|---|---|
| `srci_bridge_twincat` | TwinCAT bridge, `GVL_Bridge.RobotOutData` / `RobotInData`, `Byte[256]` each |
| `staubli_cs9` | Staubli CS9 with uniVALpi (SRCI 1.3, profile Core), board `J207J208-SiemensTRL_256`: 256 + 256 `Byte` nodes. Reading works anonymously, writing needs a user with `writeAccess` (`maintenance`); the server offers security None only (password in clear text). The VAL 3 application `run_uniVALpi` must be running |

`srci.transport.opcua.browse(endpoint)` lists the variables of a server (NodeId, path, data type,
length, writable, `telegram_candidate`) - used by the connection configurator of the HMI.

`srci.sim.opcua.OpcUaRcSimulator(handler, send, recv)` is the counterpart for tests and demos: an
asyncua server with the nodes `SRCI.PlcToRob` / `SRCI.RobToPlc` that runs its own cycle (10 ms) like a
robot controller and answers with `handler` (your own simulation of the robot controller).
With `per_byte=True` it has one node per byte (`SRCI.PlcToRob.%IB<8n>` / `SRCI.RobToPlc.%QB<8n>`) like
a robot controller; `sim.config()` gives the matching configuration.

Notes for robot controllers:

- Writing usually needs a logged-in user; anonymous sessions are often read only.
- Controllers whose OPC UA server publishes only scalar `num`/`bool`/`string` variables cannot carry
  a telegram; number **arrays** (`Double[]`) work since the data type is detected.
- Some controllers offer SRCI also over a TCP socket of their own; whether that protocol matches
  the raw telegram exchange of `TcpTransport` has to be checked per manufacturer.

## Other transports

- `LoopbackTransport(handler, …)` - in-process, e.g. with your own simulation of the robot controller.
- `FaultInjectingTransport(inner, FaultPlan(...))` - deterministic faults for tests
  (timeout, lost request, disconnect, bit flip, stale answer, protocol violation).
- `srci.sim.gateway.PlcGatewaySimulator` - TCP server that behaves like the gateway PLC
  (for tests: the telegrams are answered by a `handler`).
