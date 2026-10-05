# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.sim.control
#  Author:      Thorsten Brach
#  Date:        2026-10-04
#
#  Description:
#    Control channel of the SDK server: a PLC test (TcUnit) sets up and checks the
#    simulated robot controller over a second TCP port.
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""Control channel of the SDK server (``python -m srci.sim.server --control-port 5001``).

The Python tests call the simulator directly (``sim.set_move_cycles(20)``, ``sim.joints``); a
PLC test cannot. The control channel offers the same functions over a second TCP port as a
line protocol, so the TcUnit tests of the PLC library (SRCI_PLC_TEST) can do what the Python
tests do: one request line, one answer line, ASCII, terminated with LF (CR is ignored).

Answer: ``OK [value]`` or ``ERR <reason>``. Numbers can be written as ``123``, ``16#7B`` or
``0x7B``. Commands (case-insensitive)::

    PING                          OK SRCI-SDK-CONTROL <protocol version>
    RESET                         new simulator (restart of the RC), tampering off, log mark 0
    MOVE_CYCLES <n>               duration of a motion [cycles]
    FAIL_ENABLE <0|1>             EnableRobot fails
    MOTION_ERROR <code>           motion error (0: none)
    COMMAND_ERROR <type> <code>   commands of <type> answered with <code> (0: normal)
    RESPONSE <type> <field> <v>   response value of a command the SDK does not implement
    CLEAR_RESPONSES               all response values back to 0
    ALL_FUNCTIONS <0|1>           ReadRobotData: all functions or those of the original SDK
    JOINTS <j1> [<j2> ...]        joint position (up to 12 values, the others 0)
    GET <item>                    ENABLED, OVERRIDE, JOINTS, JOINT <1..12>, RI_STATE,
                                  POWER_STATE, SEQUENCE_STATE, OPERATION_MODE, MOVING,
                                  ERROR_PENDING, CYCLES, SDK_VERSION, CONNECTIONS, TELEGRAMS,
                                  LIFESIGN_GAPS, LIFESIGN_REPEATS
    LAST <type> <field>           field of the last command of <type> as the SDK decoded it
    MARK                          start of the log window (COUNT_COMMANDS, LOG_CONTAINS)
    COUNT_COMMANDS <type>         commands of <type> the SDK accepted since MARK
    LOG_CONTAINS <text>           1 if a log message of the SDK since MARK contains <text>
    MAX_SEVERITY                  highest severity of the log messages since MARK (0: none)
    TAMPER FREEZE                 answer RC -> PLC frozen (the last answer is repeated)
    TAMPER KEEP_ACK <start>       acknowledge of the sequence at <start> kept, no response
    TAMPER SET <index> <value>    byte of the answer RC -> PLC overwritten
    TAMPER XOR <index> <mask>     byte of the answer RC -> PLC inverted with <mask>
    TAMPER REQ_SET <index> <v>    byte of the telegram PLC -> RC overwritten before the SDK
    TAMPER OFF                    no tampering

The commands work on the simulator of the current connection; ``RESET`` and a new PLC
connection start a new one.
"""

from __future__ import annotations

import contextlib
import socket
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from srci.sim.server import SdkServer

__all__ = ["PROTOCOL_VERSION", "SdkControlServer", "Tamper", "parse_number"]

PROTOCOL_VERSION = 1
MAX_LINE = 1024


def parse_number(text: str) -> int:
    """``123``, ``-5``, ``16#7B``, ``0x7B`` -> int."""
    t = text.strip().replace("_", "")
    sign = -1 if t.startswith("-") else 1
    t = t.lstrip("+-")
    if t.upper().startswith("16#"):
        return sign * int(t[3:], 16)
    return sign * int(t, 0)


@dataclass
class Tamper:
    """Modifications of the telegrams between the PLC and the SDK (fault injection)."""

    freeze: bool = False
    frozen: bytes | None = None
    keep_ack: int | None = None  # start address of the sequence RC -> PLC
    kept_ack: bytes | None = None
    answer_set: dict[int, int] = field(default_factory=dict)
    answer_xor: dict[int, int] = field(default_factory=dict)
    request_set: dict[int, int] = field(default_factory=dict)

    @property
    def active(self) -> bool:
        return bool(
            self.freeze or self.keep_ack is not None or self.answer_set or self.answer_xor or self.request_set
        )

    def request(self, telegram: bytes) -> bytes:
        if not self.request_set:
            return telegram
        data = bytearray(telegram)
        for index, value in self.request_set.items():
            if index < len(data):
                data[index] = value & 0xFF
        return bytes(data)

    def answer(self, answer: bytes) -> bytes:
        if self.freeze:
            if self.frozen is None:
                self.frozen = answer
            return self.frozen
        data = bytearray(answer)
        if self.keep_ack is not None:
            start = self.keep_ack
            if self.kept_ack is None:
                self.kept_ack = bytes(data[start : start + 2])
            data[start : start + 4] = self.kept_ack + b"\x00\x00"
        for index, value in self.answer_set.items():
            if index < len(data):
                data[index] = value & 0xFF
        for index, mask in self.answer_xor.items():
            if index < len(data):
                data[index] ^= mask & 0xFF
        return bytes(data)


class ControlError(Exception):
    """Invalid request of the control channel (answered with ``ERR``)."""


class SdkControlServer:
    """Threaded TCP server of the control channel (one client at a time, a new one replaces it)."""

    def __init__(self, server: SdkServer, host: str = "127.0.0.1", port: int = 5001) -> None:
        self.server = server
        self.requests = 0
        self.errors: list[str] = []
        self._listener = socket.create_server((host, port), reuse_port=False)
        self._listener.settimeout(0.05)
        self.address: tuple[str, int] = self._listener.getsockname()[:2]
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="SdkControlServer", daemon=True)
        self._commands: dict[str, Callable[[list[str]], str]] = {
            "PING": lambda a: f"SRCI-SDK-CONTROL {PROTOCOL_VERSION}",
            "RESET": self._reset,
            "MOVE_CYCLES": lambda a: self._sim_call("set_move_cycles", self._int(a, 0)),
            "FAIL_ENABLE": lambda a: self._sim_call("set_fail_enable", bool(self._int(a, 0))),
            "MOTION_ERROR": lambda a: self._sim_call("set_motion_error", self._int(a, 0)),
            "COMMAND_ERROR": lambda a: self._sim_call("set_command_error", self._int(a, 0), self._int(a, 1)),
            "RESPONSE": self._response,
            "CLEAR_RESPONSES": lambda a: self._sim_call("clear_responses"),
            "ALL_FUNCTIONS": lambda a: self._sim_call("set_all_functions_supported", bool(self._int(a, 0))),
            "JOINTS": self._joints,
            "GET": self._get,
            "LAST": self._last,
            "MARK": self._mark,
            "COUNT_COMMANDS": self._count_commands,
            "LOG_CONTAINS": self._log_contains,
            "MAX_SEVERITY": self._max_severity,
            "TAMPER": self._tamper,
        }

    # ------------------------------------------------------------------ lifecycle

    @property
    def port(self) -> int:
        return self.address[1]

    def start(self) -> SdkControlServer:
        self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2.0)
        with contextlib.suppress(OSError):
            self._listener.close()

    # ------------------------------------------------------------------ server

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                conn, _ = self._listener.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            conn.settimeout(0.05)
            try:
                self._serve(conn)
            except OSError as exc:
                self.errors.append(str(exc))
            finally:
                with contextlib.suppress(OSError):
                    conn.close()

    def _serve(self, conn: socket.socket) -> None:
        buffer = b""
        while not self._stop.is_set():
            try:
                chunk = conn.recv(256)
            except TimeoutError:
                continue
            if not chunk:
                return
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                answer = self.handle(line.decode("latin-1"))
                conn.sendall(answer.encode("latin-1") + b"\n")
            if len(buffer) > MAX_LINE:
                conn.sendall(b"ERR line too long\n")
                buffer = b""

    # ------------------------------------------------------------------ requests

    def handle(self, line: str) -> str:
        """Answer to one request line (``OK ...`` / ``ERR ...``)."""
        self.requests += 1
        words = line.replace("\r", "").replace("\x00", "").split()
        if not words:
            return "ERR empty request"
        command = self._commands.get(words[0].upper())
        if command is None:
            return f"ERR unknown command {words[0]}"
        try:
            with self.server.lock:
                value = command(words[1:])
        except (ControlError, ValueError, IndexError, RuntimeError) as exc:
            return f"ERR {exc}"
        return f"OK {value}".rstrip()

    @staticmethod
    def _int(args: list[str], index: int) -> int:
        if index >= len(args):
            raise ControlError(f"argument {index + 1} missing")
        return parse_number(args[index])

    def _sim_call(self, name: str, *args: object) -> str:
        getattr(self.server.sim, name)(*args)
        return ""

    def _reset(self, args: list[str]) -> str:
        self.server.restart()
        return ""

    def _response(self, args: list[str]) -> str:
        if len(args) < 3:
            raise ControlError("RESPONSE <type> <field> <value>")
        self.server.sim.set_response(self._int(args, 0), {args[1]: " ".join(args[2:])})
        return ""

    def _joints(self, args: list[str]) -> str:
        if not 1 <= len(args) <= 12:
            raise ControlError("JOINTS needs 1..12 values")
        values = [float(a) for a in args] + [0.0] * (12 - len(args))
        self.server.sim.joints = values
        return ""

    def _get(self, args: list[str]) -> str:
        if not args:
            raise ControlError("GET <item>")
        sim, srv = self.server.sim, self.server
        item = args[0].upper()
        if item == "JOINT":
            return _number(sim.joints[self._int(args, 1) - 1])
        states = sim.states
        values: dict[str, Callable[[], object]] = {
            "ENABLED": lambda: int(sim.enabled),
            "OVERRIDE": lambda: _number(sim.override),
            "JOINTS": lambda: ",".join(_number(j) for j in sim.joints),
            "RI_STATE": lambda: states.ri_state,
            "POWER_STATE": lambda: states.ra_power_state,
            "SEQUENCE_STATE": lambda: states.ra_sequence_state,
            "OPERATION_MODE": lambda: states.operation_mode,
            "MOVING": lambda: int(states.is_moving),
            "ERROR_PENDING": lambda: int(states.error_pending),
            "CYCLES": lambda: sim.cycles,
            "SDK_VERSION": lambda: sim.sdk_version,
            "CONNECTIONS": lambda: srv.connections,
            "TELEGRAMS": lambda: srv.telegrams,
            "LIFESIGN_GAPS": lambda: srv.number_gaps,
            "LIFESIGN_REPEATS": lambda: srv.number_repeats,
        }
        if item not in values:
            raise ControlError(f"unknown item {args[0]}")
        return str(values[item]())

    def _last(self, args: list[str]) -> str:
        if len(args) < 2:
            raise ControlError("LAST <type> <field>")
        fields = self.server.sim.last_command(self._int(args, 0))
        if fields is None:
            raise ControlError("no command received")
        if args[1] not in fields:
            raise ControlError(f"no field {args[1]}")
        return fields[args[1]]

    def _mark(self, args: list[str]) -> str:
        self.server.log_mark = len(self.server.sim.logs)
        return ""

    def _logs(self) -> list[str]:
        return [log.text for log in self.server.sim.logs[self.server.log_mark :]]

    def _count_commands(self, args: list[str]) -> str:
        cmd_type = self._int(args, 0)
        # the same rule as tests/sdk/test_methodology.py: commands() - accepted by the SDK
        key = f"({cmd_type}), cmdID"
        return str(sum(1 for text in self._logs() if key in text and "EMPTY -> BUFFERED" in text))

    def _log_contains(self, args: list[str]) -> str:
        if not args:
            raise ControlError("LOG_CONTAINS <text>")
        text = " ".join(args)
        return str(int(any(text in log for log in self._logs())))

    def _max_severity(self, args: list[str]) -> str:
        logs = self.server.sim.logs[self.server.log_mark :]
        return str(max((log.severity for log in logs), default=0))

    def _tamper(self, args: list[str]) -> str:
        if not args:
            raise ControlError("TAMPER <FREEZE|KEEP_ACK|SET|XOR|REQ_SET|OFF>")
        tamper = self.server.tamper
        mode = args[0].upper()
        if mode == "OFF":
            self.server.tamper = Tamper()
        elif mode == "FREEZE":
            tamper.freeze, tamper.frozen = True, None
        elif mode == "KEEP_ACK":
            tamper.keep_ack, tamper.kept_ack = self._int(args, 1), None
        elif mode == "SET":
            tamper.answer_set[self._int(args, 1)] = self._int(args, 2)
        elif mode == "XOR":
            tamper.answer_xor[self._int(args, 1)] = self._int(args, 2)
        elif mode == "REQ_SET":
            tamper.request_set[self._int(args, 1)] = self._int(args, 2)
        else:
            raise ControlError(f"unknown tamper mode {args[0]}")
        return ""


def _number(value: float) -> str:
    """REAL as text without exponent (the PLC converts with STRING_TO_REAL)."""
    text = f"{value:.6f}".rstrip("0")
    return text + "0" if text.endswith(".") else text
