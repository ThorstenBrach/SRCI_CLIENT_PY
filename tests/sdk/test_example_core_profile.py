# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_example_core_profile
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    examples/core_profile: the Core profile demo runs against the SDK simulator.
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

"""examples/core_profile: the Core profile demo runs against the SDK simulator."""

from __future__ import annotations

import importlib.util
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType

import pytest

import srci

DEMO = Path(__file__).resolve().parents[2] / "examples" / "core_profile" / "core_profile_demo.py"


@pytest.fixture
def demo(sdk_library: str) -> Iterator[ModuleType]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=16, FRAME_MAX=16, LOAD_MAX=16)
    spec = importlib.util.spec_from_file_location("core_profile_demo", DEMO)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.mark.parametrize("target", ["--sdk", "--sdk-tcp"])
def test_core_profile_demo(demo: ModuleType, target: str, capsys: pytest.CaptureFixture[str]) -> None:
    """Every function of the profile "Core" (spec table 5-2) is executed without error."""
    assert demo.main([target, "--fast"]) == 0
    out = capsys.readouterr().out
    assert "all Core functions executed" in out
    for title in ("RobotTask - robot data, configuration, messages", "GroupReset, EnableRobot",
                  "ChangeSpeedOverride", "ReadActualPositionCyclic", "WriteToolData", "WriteFrameData",
                  "WriteLoadData", "ReadRobotSWLimits", "Read/WriteRobotDefaultDynamics",
                  "Read/WriteRobotReferenceDynamics", "MoveAxesAbsolute", "MoveDirectAbsolute",
                  "MoveLinearAbsolute", "GroupInterrupt, GroupJog, ReturnToPrimary, GroupContinue",
                  "GroupStop", "SetSequence", "Client log"):  # fmt: skip
        assert f"=== {title}" in out
    assert "cyclic position              X=   40.00  Y=   30.00" in out  # F59: follows the robot
