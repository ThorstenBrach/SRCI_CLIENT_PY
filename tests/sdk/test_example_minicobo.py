# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_example_minicobo
#  Author:      Thorsten Brach
#  Date:        2026-10-02
#
#  Description:
#    examples/jaka_minicobo: the first-steps script runs against the SDK simulator.
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

"""examples/jaka_minicobo: the first-steps script runs against the SDK simulator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "examples" / "jaka_minicobo" / "minicobo.py"


@pytest.fixture
def minicobo(sdk_library: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location("minicobo", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_minicobo_info_does_not_enable(minicobo: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """info: initialization, robot data, SW limits and position over the TCP gateway - no enable."""
    assert minicobo.main(["info", "--sdk-tcp", "--fast"]) == 0
    out = capsys.readouterr().out
    assert "TelegramState                  INITIALIZED" in out
    assert "RCManufacturer" in out and "J6 [deg]" in out
    assert "EnableRobot" not in out


def test_minicobo_move_relative_and_back(minicobo: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """move: one joint relative to the actual position and back, then disabled."""
    assert minicobo.main(["move", "--sdk-tcp", "--fast", "--yes", "--joint", "3", "--delta", "-7.5"]) == 0
    out = capsys.readouterr().out
    assert "J3=   -7.50" in out.split("reached")[1].splitlines()[0]
    assert "back at start" in out and out.rstrip().endswith("done")
    assert out.count("EnableRobot.Enabled            False") == 1


def test_minicobo_move_is_cancelled_without_confirmation(
    minicobo: ModuleType, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """move without --yes asks first; anything but yes cancels before the robot is enabled."""
    monkeypatch.setattr("builtins.input", lambda _prompt: "no")
    assert minicobo.main(["move", "--sdk-tcp", "--fast"]) == 0
    out = capsys.readouterr().out
    assert "cancelled" in out and "EnableRobot" not in out


def test_minicobo_reports_an_unreachable_gateway(
    minicobo: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    import socket

    with socket.socket() as s:  # a free port nobody listens on
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    assert minicobo.main(["info", "--host", "127.0.0.1", "--port", str(port)]) == 1
    assert "FB_SrciTcpGateway enabled" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args", [["--delta", "0"], ["--delta", "45"], ["--override", "150"], ["--velocity", "0"]]
)
def test_minicobo_rejects_unsafe_arguments(minicobo: ModuleType, args: list[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        minicobo.main(["move", "--sdk-tcp", *args])
    assert exc.value.code == 2
