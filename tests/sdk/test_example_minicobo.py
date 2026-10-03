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
    assert minicobo.main(["info", "--sdk-tcp", "--fast", "--no-log"]) == 0
    out = capsys.readouterr().out
    assert "TelegramState                  INITIALIZED" in out
    assert "RCManufacturer" in out and "J6 [deg]" in out
    assert "EnableRobot" not in out


def test_minicobo_move_relative_and_back(minicobo: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """move: one joint relative to the actual position and back, then disabled."""
    assert (
        minicobo.main(["move", "--sdk-tcp", "--fast", "--yes", "--joint", "3", "--delta", "-7.5", "--no-log"])
        == 0
    )
    out = capsys.readouterr().out
    assert "J3=   -7.50" in out.split("reached")[1].splitlines()[0]
    assert "back at start" in out and out.rstrip().endswith("done")
    assert out.count("EnableRobot.Enabled            False") == 1


def test_minicobo_move_is_cancelled_without_confirmation(
    minicobo: ModuleType, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """move without --yes asks first; anything but yes cancels before the robot is enabled."""
    monkeypatch.setattr("builtins.input", lambda _prompt: "no")
    assert minicobo.main(["move", "--sdk-tcp", "--fast", "--no-log"]) == 0
    out = capsys.readouterr().out
    assert "cancelled" in out and "EnableRobot" not in out


def test_minicobo_reports_an_unreachable_gateway(
    minicobo: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    import socket

    with socket.socket() as s:  # a free port nobody listens on
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    assert minicobo.main(["info", "--host", "127.0.0.1", "--port", str(port), "--no-log"]) == 1
    assert "FB_SrciTcpGateway enabled" in capsys.readouterr().out


@pytest.mark.parametrize(
    "args", [["--delta", "0"], ["--delta", "45"], ["--override", "150"], ["--velocity", "0"]]
)
def test_minicobo_rejects_unsafe_arguments(minicobo: ModuleType, args: list[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        minicobo.main(["move", "--sdk-tcp", "--no-log", *args])
    assert exc.value.code == 2


def test_minicobo_shows_a_core_only_robot(minicobo: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """A robot with only the profile "Core" (e.g. JAKA MiniCobo): missing Core functions are named,
    no other functions are reported."""
    from srci.types import AxesGroup

    functions = AxesGroup().State.RobotData.RCSupportedFunctions
    for name in minicobo.CORE:
        setattr(functions, name, True)
    functions.GroupJog = False
    minicobo.show_supported_functions(functions)
    out = capsys.readouterr().out
    assert "27 of 28" in out and "Core functions missing         GroupJog" in out
    assert "none (Core profile only)" in out


def test_minicobo_uses_only_core_functions() -> None:
    """The example calls only blocks of Core functions (the JAKA MiniCobo supports only Core)."""
    import re

    used = set(re.findall(r"MC_(\w+?)FB\(", SCRIPT.read_text(encoding="utf-8")))
    core = {"GroupReset", "EnableRobot", "ChangeSpeedOverride", "ReadRobotSWLimits", "ReadActualPosition",
            "MoveAxesAbsolute", "MoveLinearAbsolute", "GroupStop"}  # fmt: skip
    assert used and used <= core, used - core


def test_minicobo_writes_a_log_file(
    minicobo: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The log file holds the system log of the library, the telegrams and the transport."""
    log = tmp_path / "minicobo.log"
    assert minicobo.main(["info", "--sdk-tcp", "--fast", "--log", str(log)]) == 0
    text = log.read_text(encoding="utf-8")
    assert "srci.plc" in text and "Robot Task Enabled" in text
    assert "srci.telegram" in text and "PLC->RC 25 " in text and "RC->PLC 25 " in text
    assert str(log) in capsys.readouterr().out


def test_minicobo_diagnoses_a_robot_that_sends_nothing(
    minicobo: ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """The PLC answers, but RobotInData stays 0 (PROFINET not in data exchange): the diagnosis
    shows the step, the TelegramState and the raw headers."""
    from srci.sim.gateway import PlcGatewaySimulator

    with PlcGatewaySimulator(lambda _telegram: bytes(256), 256, 256) as gateway:
        args = ["info", "--host", "127.0.0.1", "--port", str(gateway.port), "--timeout", "8", "--no-log"]
        assert minicobo.main(args) == 1
    out = capsys.readouterr().out
    assert "RobotTask step / ErrorID       1 / 16#0006" in out
    assert "RobotInData is all 0" in out and "header PLC -> RC               25 " in out


def test_minicobo_sends_an_older_srci_version(minicobo: ModuleType, tmp_path: Path) -> None:
    """--srci-version 1.3: byte 0 of the PLC -> RC header is 16#23 (major 1 in bits 5..7, minor 3);
    the version of the library is restored afterwards."""
    from srci.types import RobotLibraryConstants

    log = tmp_path / "v13.log"
    assert minicobo.main(["info", "--sdk-tcp", "--fast", "--srci-version", "1.3", "--log", str(log)]) == 0
    assert "PLC->RC 23 " in log.read_text(encoding="utf-8")
    version = RobotLibraryConstants.SRCIVersion
    assert (version.MajorVersion, version.MinorVersion) == (1, 5)


@pytest.mark.parametrize("value", ["1", "1.x", "8.0", "1.32"])
def test_minicobo_rejects_an_invalid_srci_version(minicobo: ModuleType, value: str) -> None:
    with pytest.raises(SystemExit) as exc:
        minicobo.main(["info", "--sdk-tcp", "--no-log", "--srci-version", value])
    assert exc.value.code == 2


def test_minicobo_probes_the_blending_modes(minicobo: ModuleType, capsys: pytest.CaptureFixture[str]) -> None:
    """blending: every TurnMode of MoveLinearAbsolute, then every BlendingMode with MoveLinearAbsolute
    and MoveAxesAbsolute; the simulator (harness) supports all TurnModes and CORNER_DISTANCE /
    RAMP_OVERLAP, the other blending modes are rejected with 16#8E05 and the probe goes on."""
    assert minicobo.main(["blending", "--sdk-tcp", "--fast", "--yes", "--no-log"]) == 0
    out = capsys.readouterr().out
    assert "TurnMode FREE, ConfigMode SAME accepted" in out
    assert "CORNER_DISTANCE (linear)       accepted" in out
    assert "DEFINED_VELOCITY (axes)        rejected 16#8E05 (BlendingMode not supported)" in out
    assert "RAMP_OVERLAP (axes)            accepted" in out  # the probe goes on after a rejection
    assert (
        "blending supported             CORNER_DISTANCE (linear), CORNER_DISTANCE (axes), RAMP_OVERLAP" in out
    )
