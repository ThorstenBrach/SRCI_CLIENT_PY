# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_sdk_server
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    srci.sim.server: the SDK simulator behind a lockstep TCP server (for PLC tests).
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

"""srci.sim.server: the SDK simulator behind a lockstep TCP server (for PLC tests)."""

from __future__ import annotations

from pathlib import Path

import pytest

from srci.api import SrciClient
from srci.fb import MC_EnableRobotFB, MC_GroupResetFB
from srci.sim.server import SdkServer, decode_header, main
from srci.transport import TcpTransport


def _client(server: SdkServer) -> SrciClient:
    host, port = server.address
    transport = TcpTransport(host, port, 256, 256, response_timeout=0.5)
    return SrciClient(transport, realtime=False)


def test_sdk_server_serves_a_plc_and_resets_the_rc_per_connection(sdk_library: str) -> None:
    """A client (here the Python library instead of the PLC) initializes, resets and enables the
    robot over TCP; a new connection finds a restarted RC and initializes again."""
    with SdkServer(port=0, library=Path(sdk_library)) as server:
        for _ in range(2):
            with _client(server) as client:
                client.wait_initialized(timeout=10.0)
                client.execute(MC_GroupResetFB())
                enable = client.enable(MC_EnableRobotFB())
                assert enable.Enabled and server.sim.enabled
            assert "enabled" in server.status()
        assert server.connections == 2 and server.telegrams > 20
        assert not server.gateway.errors


def test_sdk_server_cli_reports_a_missing_sdk(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    assert main(["--lib", str(tmp_path / "missing.so"), "--status", "0"]) == 2
    assert "SDK simulator not available" in capsys.readouterr().err


def test_sdk_server_reports_gaps_in_the_plc_lifesign(sdk_library: str) -> None:
    """Diagnosis for PLC tests: the Python client (one RobotTask cycle per telegram) sends the
    LifeSign without gaps; a PLC that runs its RobotTask several cycles per telegram shows gaps."""
    from srci.api import RobotProgram

    with SdkServer(port=0, library=Path(sdk_library)) as server:
        with _client(server) as client:
            client.wait_initialized(timeout=10.0)
            client.run(40)
        assert server.number_gaps == 0 and server.number_repeats == 0
        host, port = server.address
        transport = TcpTransport(host, port, 256, 256, response_timeout=0.5)
        program, out, inp = RobotProgram(256, 256), bytes(256), bytes(256)
        for cycle in range(90):  # 3 RobotTask cycles per telegram
            if cycle % 3 == 0:
                inp = transport.exchange(out)
            out = program.step(inp)
        transport.close()
        assert server.number_gaps > 0
        assert "gaps" in server.status()


def test_sdk_server_dump_shows_the_initialization(sdk_library: str) -> None:
    """--dump diagnosis: the decoded headers show Control INITIALIZE and the TelegramState."""
    lines: list[str] = []
    with SdkServer(port=0, library=Path(sdk_library)) as server:
        server.on_exchange = lambda telegram, answer: lines.append(decode_header(telegram, answer))
        with _client(server) as client:
            client.wait_initialized(timeout=10.0)
    assert any("axesgroup 0 control 1 INITIALIZE" in line for line in lines), lines[:5]
    assert any("READY_FOR_INITIALIZATION" in line for line in lines)
    assert "state 255 INITIALIZED" in lines[-1]
    assert "len 256/256" in lines[-1] and "ver 16#25" in lines[-1]


def test_decode_header_of_short_or_unknown_values() -> None:
    """--dump diagnosis: short telegrams and unknown Control/TelegramState values are shown."""
    assert decode_header(b"\x25", b"").startswith("short telegram")
    line = decode_header(bytes([0x25, 0x03, 1, 0, 1, 0, 0x1F] + [0] * 11), bytes([0x25, 0x30, 0, 99]))
    assert (
        "axesgroup 1 control 15 UNDEFINED_15" in line
        and "state 99 UNDEFINED_99" in line
        and "lifesign  3" in line
    )
