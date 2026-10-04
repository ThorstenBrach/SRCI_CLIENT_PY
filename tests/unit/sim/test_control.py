# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.sim.test_control
#  Author:      Thorsten Brach
#  Date:        2026-10-04
#
#  Description:
#    Control channel of the SDK server (PLC tests) with a fake simulator - no SDK needed.
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

"""Control channel of the SDK server (PLC tests) with a fake simulator - no SDK needed."""

from __future__ import annotations

import socket
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

import pytest

import srci.sim.server as server_module
from srci.sim.control import Tamper, parse_number
from srci.sim.sdk import SdkLog, SdkStates
from srci.sim.server import SdkServer
from srci.transport import TcpTransport

SIZE = 64


@dataclass
class FakeSim:
    """The functions of SdkSimulator the control channel uses."""

    cycle_time_ms: int = 10
    library: Any = None
    calls: list[tuple[str, tuple[Any, ...]]] = field(default_factory=list)
    joints: list[float] = field(default_factory=lambda: [0.0] * 12)
    logs: list[SdkLog] = field(default_factory=list)
    cycles: int = 0
    enabled: bool = False
    override: float = 100.0
    sdk_version: str = "1.5.9-fake"
    on_log: Any = None
    closed: bool = False
    last: dict[int, dict[str, str]] = field(default_factory=dict)

    def exchange(self, telegram: bytes, size: int) -> bytes:
        self.cycles += 1
        return bytes([self.cycles & 0xFF]) + telegram[1:size] + bytes(max(0, size - len(telegram)))

    def close(self) -> None:
        self.closed = True

    def __getattr__(self, name: str) -> Any:
        if name.startswith("set_") or name == "clear_responses":
            return lambda *args: self.calls.append((name, args))
        raise AttributeError(name)

    def last_command(self, cmd_type: int) -> dict[str, str] | None:
        return self.last.get(cmd_type)

    @property
    def states(self) -> SdkStates:
        return SdkStates(True, 71, 2, 1, 3, False, False)


@pytest.fixture
def server(monkeypatch: pytest.MonkeyPatch) -> Iterator[SdkServer]:
    sims: list[FakeSim] = []

    def new_sim(cycle_time_ms: int = 10, library: Any = None) -> FakeSim:
        sims.append(FakeSim(cycle_time_ms, library))
        return sims[-1]

    monkeypatch.setattr(server_module, "SdkSimulator", new_sim)
    srv = SdkServer(port=0, request_size=SIZE, response_size=SIZE)
    srv.enable_control(port=0)
    with srv:
        yield srv


def ask(srv: SdkServer, *lines: str) -> list[str]:
    """Sends the request lines over TCP and returns the answer lines."""
    assert srv.control is not None
    with socket.create_connection(srv.control.address, timeout=2.0) as conn:
        conn.sendall("".join(f"{line}\r\n" for line in lines).encode())
        data = b""
        while data.count(b"\n") < len(lines):
            chunk = conn.recv(4096)
            assert chunk, data
            data += chunk
    return data.decode().splitlines()


def test_ping_and_errors(server: SdkServer) -> None:
    """Control channel: PING answers with the protocol version, invalid requests with ERR and the reason."""
    assert ask(server, "PING", "nonsense", "", "MOVE_CYCLES", "GET NOTHING") == [
        "OK SRCI-SDK-CONTROL 1",
        "ERR unknown command nonsense",
        "ERR empty request",
        "ERR argument 1 missing",
        "ERR unknown item NOTHING",
    ]


def test_simulator_setup_is_forwarded(server: SdkServer) -> None:
    """Control channel: the setup requests call the functions of the simulator (numbers as 123, 16#7B, 0x7B)."""
    answers = ask(
        server,
        "move_cycles 20",
        "FAIL_ENABLE 1",
        "MOTION_ERROR 16#6C02",
        "COMMAND_ERROR 2104 0x8123",
        "RESPONSE 4001 Values[0] 17",
        "CLEAR_RESPONSES",
        "ALL_FUNCTIONS 0",
    )
    assert answers == ["OK"] * 7
    assert server.sim.calls == [  # type: ignore[attr-defined]
        ("set_move_cycles", (20,)),
        ("set_fail_enable", (True,)),
        ("set_motion_error", (0x6C02,)),
        ("set_command_error", (2104, 0x8123)),
        ("set_response", (4001, {"Values[0]": "17"})),
        ("clear_responses", ()),
        ("set_all_functions_supported", (False,)),
    ]


def test_get_values(server: SdkServer) -> None:
    """Control channel: GET returns the state of the simulator (joints as REAL text without exponent)."""
    assert ask(server, "JOINTS 1 2.5 -3", "GET JOINT 2", "GET JOINTS", "GET ENABLED", "GET RI_STATE") == [
        "OK",
        "OK 2.5",
        "OK 1.0,2.5,-3.0," + ",".join(["0.0"] * 9),
        "OK 0",
        "OK 71",
    ]
    assert ask(server, "GET OVERRIDE", "GET SDK_VERSION", "JOINTS") == [
        "OK 100.0",
        "OK 1.5.9-fake",
        "ERR JOINTS needs 1..12 values",
    ]


def test_last_command_and_log_window(server: SdkServer) -> None:
    """Control channel: LAST returns a field of the decoded command; COUNT_COMMANDS / LOG_CONTAINS count from MARK on."""
    sim: FakeSim = server.sim  # type: ignore[assignment]
    sim.last[2104] = {"@ExecutionMode": "7", "VelocityRate": "5000"}
    sim.logs.append(SdkLog(0, 0, 0, 0, "Command MoveAxesAbsolute (2104), cmdID 1: EMPTY -> BUFFERED"))
    assert ask(server, "LAST 2104 @ExecutionMode", "LAST 2104 Missing", "LAST 1 x") == [
        "OK 7",
        "ERR no field Missing",
        "ERR no command received",
    ]
    assert ask(
        server, "COUNT_COMMANDS 2104", "LOG_CONTAINS EMPTY -> BUFFERED", "MARK", "COUNT_COMMANDS 2104"
    ) == [
        "OK 1",
        "OK 1",
        "OK",
        "OK 0",
    ]


def test_reset_starts_a_new_simulator(server: SdkServer) -> None:
    """Control channel: RESET starts a new simulator and switches the tampering off."""
    first = server.sim
    assert ask(server, "TAMPER FREEZE", "RESET") == ["OK", "OK"]
    assert server.sim is not first and first.closed  # type: ignore[attr-defined]
    assert not server.tamper.active


def test_tampering_of_the_telegrams(server: SdkServer) -> None:
    """Control channel: TAMPER SET / XOR / REQ_SET / FREEZE / KEEP_ACK change the telegrams between PLC and SDK."""
    host, port = server.address
    with TcpTransport(host, port, SIZE, SIZE, response_timeout=1.0) as tr:
        normal = tr.exchange(bytes(range(SIZE)))
        assert normal[1:4] == bytes([1, 2, 3])
        assert ask(server, "TAMPER SET 3 165", "TAMPER XOR 63 0x30", "TAMPER REQ_SET 2 16#FF") == ["OK"] * 3
        changed = tr.exchange(bytes(range(SIZE)))
        assert changed[3] == 165 and changed[63] == 63 ^ 0x30 and changed[2] == 0xFF
        assert ask(server, "TAMPER OFF", "TAMPER FREEZE") == ["OK", "OK"]
        frozen = tr.exchange(bytes(SIZE))
        assert tr.exchange(bytes([9] * SIZE)) == frozen
        assert ask(server, "TAMPER OFF", "TAMPER KEEP_ACK 20") == ["OK", "OK"]
        first = tr.exchange(bytes([5] * SIZE))
        second = tr.exchange(bytes([7] * SIZE))
        assert first[20:24] == bytes([5, 5, 0, 0]) and second[20:24] == bytes([5, 5, 0, 0])
        assert ask(server, "TAMPER WHAT") == ["ERR unknown tamper mode WHAT"]


def test_tamper_and_numbers() -> None:
    """Control channel: number formats of the requests; a byte beyond the telegram is ignored."""
    assert [parse_number(t) for t in ("12", "16#7B", "0x7b", "-3", "16#FF_FF")] == [12, 123, 123, -3, 0xFFFF]
    assert not Tamper().active and Tamper(answer_set={1: 2}).active
    assert Tamper(request_set={9: 1}).request(b"ab") == b"ab"  # index beyond the telegram


def test_cli_starts_the_control_channel(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """``--control-port`` starts the control channel, 0 switches it off."""
    monkeypatch.setattr(server_module, "SdkSimulator", lambda cycle_time_ms=10, library=None: FakeSim())

    def stop(_: float) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr("srci.sim.server.time.sleep", stop)
    with socket.socket() as probe:  # a free port (0 switches the control channel off)
        probe.bind(("127.0.0.1", 0))
        free = probe.getsockname()[1]
    assert server_module.main(["--port", "0", "--control-port", str(free)]) == 0
    assert f"control channel for PLC tests on 127.0.0.1:{free}" in capsys.readouterr().out
    assert server_module.main(["--port", "0", "--control-port", "0"]) == 0
    assert "control channel" not in capsys.readouterr().out
