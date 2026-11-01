# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_move_linear_params
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveLinearAbsolute against the SDK: dynamics, time, blending, configuration,
#    turn, orientation, tool and frame parameters.
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

"""MoveLinearAbsolute against the SDK: dynamics, time, blending, configuration, turn, orientation,
tool and frame parameters (spec 6.3.2, 5.5.7 robot dynamics).

The simulated robot moves point to point within a fixed number of cycles and uses an identity
kinematics: the parameters are validated by the SDK and passed to the firmware, their effect on the
path (blending, orientation interpolation, dynamics) is not simulated. The tests therefore check the
command outputs, the end position and the values the RC received (``sdk.last_command``).
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import (
    ArmConfigElbow,
    ArmConfigShoulder,
    ArmConfigWrist,
    BlendingMode,
    OriMode,
    RobotLibraryErrorIdEnum,
    TurnMode,
)
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    cartesian,
    enable,
    execute,
    fb,
    finished,
    order,
    read_position,
    state,
    watch,
)

MOVE_LINEAR = 2103  # command type MoveLinearAbsolute
DEFAULT_RATE = "65535"  # 16#FFFF: default rate in the telegram (rate < 0 %)


def _move_linear(h: RobotTaskHarness, x: float, y: float = 0.0, z: float = 0.0, **par: Any) -> Any:
    """MoveLinearAbsolute to (x, y, z), 100 % velocity / acceleration; ``par`` are ParCmd fields."""
    mv = fb(h, "MC_MoveLinearAbsoluteFB")
    cartesian(mv, x, y, z)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    for name, value in par.items():
        setattr(mv.ParCmd, name, value)
    return mv


def _expect_done(h: RobotTaskHarness, sdk: SdkSimulator, mv: Any, target: list[float]) -> None:
    seen = execute(h, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), (seen.flags, seen.final)
    assert not seen.final["Error"], seen.final
    assert sdk.joints[: len(target)] == pytest.approx(target)


def _expect_rejected(h: RobotTaskHarness, sdk: SdkSimulator, mv: Any, error: RobotLibraryErrorIdEnum) -> None:
    seen = execute(h, mv)
    assert order(seen, "Busy", "Error"), (seen.flags, seen.final)
    assert seen.final["ErrorID"] == error, hex(seen.final["ErrorID"])
    assert "Active" not in seen.flags and "CommandBuffered" not in seen.flags
    assert sdk.joints[:3] == [0.0, 0.0, 0.0]


# ---------------------------------------------------------------- dynamics rates

RATES = ("VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate")


@pytest.mark.parametrize("rate", RATES)
@pytest.mark.parametrize(
    ("value", "sent"),
    [(-25.0, DEFAULT_RATE), (0.0, "0"), (100.0, "10000")],
    ids=["negative-is-default", "zero-is-minimum", "maximum"],
)
def test_dynamics_rate_accepted(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, value: float, sent: str
) -> None:
    """MoveLinearAbsolute with a dynamics rate of -25 %, 0 % or 100 % reaches the target with Done; the RC
    receives the default, the minimum or 100 %.
    """
    enable(robot)
    mv = _move_linear(robot, 200.0, 50.0)
    setattr(mv.ParCmd, rate, value)
    _expect_done(robot, sdk, mv, [200.0, 50.0])
    assert sdk.last_command(MOVE_LINEAR)[rate] == sent


def _duration(h: RobotTaskHarness, sdk: SdkSimulator, x: float, **par: Any) -> int:
    """Cycles from the rising edge until Done of a motion to x (from the current position)."""
    mv = _move_linear(h, x, **par)
    seen = execute(h, mv, cycles=2000)
    assert seen.final["Done"], seen.final
    return seen.cycles


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated robot needs a fixed number of cycles per motion, the dynamics rates "
    "are passed to the firmware but do not change the duration (spec 5.5.7 robot dynamics).",
)
@pytest.mark.parametrize("rate", RATES)
def test_dynamics_rate_changes_duration(robot: RobotTaskHarness, sdk: SdkSimulator, rate: str) -> None:
    """A motion with a dynamics rate of 5 % takes longer than the same distance with 95 %."""
    enable(robot)
    slow = _duration(robot, sdk, 1000.0, **{rate: 5.0})
    fast = _duration(robot, sdk, 0.0, **{rate: 95.0})
    assert slow > fast


# ---------------------------------------------------------------- Time (optional)


def test_move_time_not_supported_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveLinearAbsolute with a Time on an RC without the optional Time parameter ends with Error
    ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED and no motion.

    Also covers a very short Time for a long segment: the command is rejected before the motion."""
    enable(robot)
    for time_ms in (150, 5):
        mv = _move_linear(robot, 1000.0, MoveTime=time_ms)
        _expect_rejected(robot, sdk, mv, RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulator does not offer the optional Time parameter (16#8E06) and moves in a "
    "fixed number of cycles; a motion of the given duration cannot be checked (spec 6.3.2 Time).",
)
def test_move_time_defines_duration(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Two motions with the same Time and different VelocityRate take the same time, given by Time."""
    enable(robot)
    first = _duration(robot, sdk, 500.0, MoveTime=1500, VelocityRate=80.0)
    second = _duration(robot, sdk, 0.0, MoveTime=1500, VelocityRate=10.0)
    assert first == second == pytest.approx(150, abs=5)  # 1.5 s at 10 ms per cycle


# ---------------------------------------------------------------- blending, single command

SUPPORTED_BLENDING = [
    BlendingMode.CORNER_DISTANCE,
    BlendingMode.MAX_CORNER_DEVIATION,
    BlendingMode.RAMP_OVERLAP,
]
UNSUPPORTED_BLENDING = [
    BlendingMode.DEFINED_VELOCITY,
    BlendingMode.CORNER_DISTANCE_2R,
    BlendingMode.CORNER_DISTANCE_1R,
]
BLENDING_PARAMETERS = [[0.0, 0.0], [20.0, 0.0], [50.0, 30.0], [0.0, 30.0]]


@pytest.mark.parametrize("parameter", BLENDING_PARAMETERS, ids=lambda p: f"param-{p[0]:g}-{p[1]:g}")
@pytest.mark.parametrize("mode", [BlendingMode.EXACT_STOP, *SUPPORTED_BLENDING], ids=lambda m: m.name.lower())
def test_blending_single_command_stops_at_target(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: BlendingMode, parameter: list[float]
) -> None:
    """A single MoveLinearAbsolute with a supported blending mode and any blending parameters has no successor
    and ends with Done exactly at the target.
    """
    enable(robot)
    mv = _move_linear(robot, 300.0, 40.0, BlendingMode=mode, BlendingParameter=list(parameter))
    _expect_done(robot, sdk, mv, [300.0, 40.0])
    sent = sdk.last_command(MOVE_LINEAR)
    assert sent["BlendingMode"] == str(int(mode))
    assert float(sent["BlendingParameter[0]"]) == parameter[0]


@pytest.mark.parametrize("parameter", BLENDING_PARAMETERS, ids=lambda p: f"param-{p[0]:g}-{p[1]:g}")
@pytest.mark.parametrize("mode", UNSUPPORTED_BLENDING, ids=lambda m: m.name.lower())
def test_blending_mode_not_offered_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: BlendingMode, parameter: list[float]
) -> None:
    """A blending mode the RC does not offer (optional) ends with Error ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED without motion."""
    enable(robot)
    mv = _move_linear(robot, 300.0, 40.0, BlendingMode=mode, BlendingParameter=list(parameter))
    _expect_rejected(robot, sdk, mv, RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED)


# ---------------------------------------------------------------- blending, two commands


@pytest.mark.parametrize(
    "parameter", [[5.0, 60.0], [20.0, 10.0], [80.0, 10.0]], ids=lambda p: f"param-{p[0]:g}-{p[1]:g}"
)
@pytest.mark.parametrize("mode", SUPPORTED_BLENDING + UNSUPPORTED_BLENDING, ids=lambda m: m.name.lower())
def test_blending_into_second_command(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: BlendingMode, parameter: list[float]
) -> None:
    """Two commands, the first with blending: the second is buffered and gets Active only after the first is
    Done; both end with Done at the second target.

    A blending mode the RC does not offer rejects the first command (16#8E05); the second one still
    runs to its target."""
    enable(robot)
    first = _move_linear(robot, 200.0, 0.0, BlendingMode=mode, BlendingParameter=list(parameter))
    second = _move_linear(robot, 200.0, 100.0)
    first.Execute = True
    robot.run(50, until=lambda: bool(first.CommandBuffered or first.Error))
    second.Execute = True
    early: list[bool] = []
    seen = watch(
        robot,
        [first, second],
        500,
        lambda: (
            early.append(bool(second.Active and not (first.Done or first.Error)))
            or (finished(first) and finished(second))
        ),
    )
    if mode in SUPPORTED_BLENDING:
        assert order(seen[0], "Busy", "CommandBuffered", "Active", "Done"), seen[0].flags
    else:
        assert (
            first.Error
            and first.ErrorID == RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED
        ), state(first)
    assert order(seen[1], "Busy", "CommandBuffered", "Active", "Done"), seen[1].flags
    assert not any(early)
    assert sdk.joints[:2] == pytest.approx([200.0, 100.0])


def test_blending_with_aborting_second_command(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second command with AbortingMode ABORT started while a blended first command is active aborts it and
    ends with Done at its own target.
    """
    from srci.types import AbortingMode

    sdk.set_move_cycles(100)
    enable(robot)
    first = _move_linear(
        robot, 200.0, 0.0, BlendingMode=BlendingMode.CORNER_DISTANCE, BlendingParameter=[20.0, 0.0]
    )
    second = _move_linear(robot, 100.0, 100.0)
    second.AbortingMode = AbortingMode.ABORT
    first.Execute = True
    seen_first = watch(robot, [first], 100, lambda: bool(first.Active))[0]
    second.Execute = True
    seen = watch(robot, [first, second], 500, lambda: finished(first) and finished(second))
    seen[0].flags = seen_first.flags + [f for f in seen[0].flags if f not in seen_first.flags]
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert order(seen[1], "Busy", "CommandBuffered", "Active", "Done"), seen[1].flags
    assert sdk.joints[:2] == pytest.approx([100.0, 100.0])


# ---------------------------------------------------------------- configuration

FIXED_CONFIG = (ArmConfigShoulder.FRONT, ArmConfigElbow.UP, ArmConfigWrist.NON_FLIP)  # of the simulated robot
OTHER_CONFIG = (ArmConfigShoulder.BACK, ArmConfigElbow.DOWN, ArmConfigWrist.FLIP)


def _move_direct_then_linear(
    h: RobotTaskHarness, sdk: SdkSimulator, config: tuple[Any, Any, Any], mode: tuple[Any, Any, Any]
) -> Any:
    """MoveDirectAbsolute (config of the robot), then MoveLinearAbsolute with the target ``config``
    and ConfigMode ``mode`` (Shoulder, Elbow, Wrist); returns the actual position."""
    md = fb(h, "MC_MoveDirectAbsoluteFB")
    cartesian(md, 100.0, 0.0, 50.0)
    md.ParCmd.VelocityRate = md.ParCmd.AccelerationRate = 100.0
    md.ParCmd.ConfigMode.Shoulder, md.ParCmd.ConfigMode.Elbow, md.ParCmd.ConfigMode.Wrist = (
        ArmConfigShoulder.SAME,
        ArmConfigElbow.SAME,
        ArmConfigWrist.SAME,
    )
    md.Execute = True
    h.run(100, until=lambda: bool(md.Active or md.Error))
    mv = _move_linear(h, 200.0, 50.0, 50.0)
    cfg = mv.ParCmd.Position.Config
    cfg.Shoulder, cfg.Elbow, cfg.Wrist = config
    mv.ParCmd.ConfigMode.Shoulder, mv.ParCmd.ConfigMode.Elbow, mv.ParCmd.ConfigMode.Wrist = mode
    seen = execute(h, mv)
    assert md.Done and not md.Error, state(md)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), (seen.flags, seen.final)
    assert sdk.joints[:3] == pytest.approx([200.0, 50.0, 50.0])
    sent = sdk.last_command(MOVE_LINEAR)
    assert int(sent["ConfigMode[0]"]) == int(mode[0]) | int(mode[1]) << 4
    assert int(sent["ConfigMode[1]"]) == int(mode[2])
    return read_position(h).ActualCartesianPosition


S, E, W = ArmConfigShoulder, ArmConfigElbow, ArmConfigWrist


@pytest.mark.parametrize(
    ("config", "mode"),
    [
        (FIXED_CONFIG, (S.SAME, E.SAME, W.SAME)),
        (OTHER_CONFIG, (S.SAME, E.SAME, W.SAME)),
        (FIXED_CONFIG, (S.FREE, E.FREE, W.FREE)),
        (OTHER_CONFIG, (S.FREE, E.FREE, W.FREE)),
        (FIXED_CONFIG, (S.SAME, E.UP, W.SAME)),
        (FIXED_CONFIG, (S.FRONT, E.SAME, W.SAME)),
        (FIXED_CONFIG, (S.SAME, E.SAME, W.NON_FLIP)),
    ],
    ids=[
        "same-unchanged",
        "same-config-differs",
        "free-unchanged",
        "free-config-differs",
        "elbow-up",
        "shoulder-front",
        "wrist-non-flip",
    ],
)
def test_config_mode_accepted(
    robot: RobotTaskHarness, sdk: SdkSimulator, config: tuple[Any, Any, Any], mode: tuple[Any, Any, Any]
) -> None:
    """MoveLinearAbsolute after a MoveDirectAbsolute with ConfigMode SAME, FREE or an explicit configuration
    ends with Done; the robot keeps or takes the expected configuration.

    SAME / FREE ignore the configuration in the target position; explicit modes set the axis to
    the given configuration (here equal to the configuration of the simulated robot)."""
    enable(robot)
    actual = _move_direct_then_linear(robot, sdk, config, mode)
    assert (actual.Config.Shoulder, actual.Config.Elbow, actual.Config.Wrist) == FIXED_CONFIG


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated kinematics always reports Front / Up / NonFlip; a configuration taken "
    "from the target position (ConfigMode USE_CONFIG) or set explicitly (Back / Down / Flip) is not "
    "applied (spec 6.3.2 ConfigMode, 5.5.8 arm configuration).",
)
@pytest.mark.parametrize(
    ("config", "mode", "expected"),
    [
        (OTHER_CONFIG, (S.USE_CONFIG, E.USE_CONFIG, W.USE_CONFIG), OTHER_CONFIG),
        (OTHER_CONFIG, (S.SAME, E.SAME, W.USE_CONFIG), (S.FRONT, E.UP, W.FLIP)),
        (OTHER_CONFIG, (S.USE_CONFIG, E.SAME, W.SAME), (S.BACK, E.UP, W.NON_FLIP)),
        (OTHER_CONFIG, (S.SAME, E.USE_CONFIG, W.SAME), (S.FRONT, E.DOWN, W.NON_FLIP)),
        (FIXED_CONFIG, (S.SAME, E.DOWN, W.SAME), (S.FRONT, E.DOWN, W.NON_FLIP)),
        (FIXED_CONFIG, (S.BACK, E.SAME, W.SAME), (S.BACK, E.UP, W.NON_FLIP)),
        (FIXED_CONFIG, (S.SAME, E.SAME, W.FLIP), (S.FRONT, E.UP, W.FLIP)),
    ],
    ids=[
        "use-config-all",
        "use-config-wrist",
        "use-config-shoulder",
        "use-config-elbow",
        "elbow-down",
        "shoulder-back",
        "wrist-flip",
    ],
)
def test_config_mode_applied(
    robot: RobotTaskHarness,
    sdk: SdkSimulator,
    config: tuple[Any, Any, Any],
    mode: tuple[Any, Any, Any],
    expected: tuple[Any, Any, Any],
) -> None:
    """MoveLinearAbsolute with ConfigMode USE_CONFIG or an explicit configuration ends with the commanded configuration at the target."""
    enable(robot)
    actual = _move_direct_then_linear(robot, sdk, config, mode)
    assert (actual.Config.Shoulder, actual.Config.Elbow, actual.Config.Wrist) == expected


# ---------------------------------------------------------------- turn numbers


@pytest.mark.parametrize("turns", [1, 7], ids=["one-turn", "far-turn"])
@pytest.mark.parametrize("mode", [TurnMode.FREE, TurnMode.SAME], ids=["free", "same"])
def test_turn_mode_ignores_turn_number(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: TurnMode, turns: int
) -> None:
    """With TurnMode FREE or SAME the turn number of the target is not used; the command ends with Done at the target."""
    enable(robot)
    first = _move_linear(robot, 100.0, TurnMode=mode)
    first.ParCmd.Position.TurnNumber.J4Turns = 1
    _expect_done(robot, sdk, first, [100.0])
    mv = _move_linear(robot, 200.0, 10.0, TurnMode=mode)
    mv.ParCmd.Position.TurnNumber.J4Turns = turns
    _expect_done(robot, sdk, mv, [200.0, 10.0])
    assert sdk.last_command(MOVE_LINEAR)["TurnMode"] == str(int(mode))
    assert read_position(robot).ActualCartesianPosition.TurnNumber.J4Turns == 0


def test_turn_mode_use_turn_number(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With TurnMode USE_TURN_NUMBER a reachable turn number is passed to the RC and the command ends with Done."""
    enable(robot)
    mv = _move_linear(robot, 200.0, 10.0, TurnMode=TurnMode.USE_TURN_NUMBER)
    _expect_done(robot, sdk, mv, [200.0, 10.0])
    assert sdk.last_command(MOVE_LINEAR)["TurnMode"] == "0"


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated kinematics does not check turn numbers against the axis limits; a "
    "target that is not reachable with the given turn number is executed (spec 6.3.2 TurnMode).",
)
def test_turn_mode_use_turn_number_not_reachable(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """With TurnMode USE_TURN_NUMBER and a turn number outside the axis range the command ends with Error and the robot does not move."""
    enable(robot)
    mv = _move_linear(robot, 200.0, 10.0, TurnMode=TurnMode.USE_TURN_NUMBER)
    mv.ParCmd.Position.TurnNumber.J4Turns = 7  # 7 turns: far outside +-360 deg
    seen = execute(robot, mv)
    assert seen.final["Error"] and seen.final["ErrorID"] != 0, seen.final
    assert sdk.joints[:2] == [0.0, 0.0]


# ---------------------------------------------------------------- orientation


@pytest.mark.parametrize(
    "mode", [OriMode.LINEAR_INTERPOLATED, OriMode.JOINT_INTERPOLATED], ids=["linear", "joint"]
)
def test_ori_mode_interpolated(robot: RobotTaskHarness, sdk: SdkSimulator, mode: OriMode) -> None:
    """MoveLinearAbsolute with a changed orientation and OriMode linear or joint interpolated ends with Done at the target pose."""
    enable(robot)
    mv = _move_linear(robot, 200.0, 10.0, OriMode=mode)
    mv.ParCmd.Position.Rz = 45.0
    seen = execute(robot, mv)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert sdk.joints[0] == pytest.approx(200.0) and sdk.joints[5] == pytest.approx(45.0)
    assert sdk.last_command(MOVE_LINEAR)["OriMode"] == str(int(mode))


@pytest.mark.parametrize("rz", [0.0, 45.0], ids=["same-orientation", "other-orientation"])
@pytest.mark.parametrize("mode", [OriMode.FIX, OriMode.PATH], ids=["fix", "path"])
def test_ori_mode_not_offered_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: OriMode, rz: float
) -> None:
    """OriMode FIX or PATH on an RC that does not offer them (optional) ends with Error
    ERR_OPTIONAL_PARAM_ORI_MODE_NOT_SUPPORTED without motion.
    """
    enable(robot)
    mv = _move_linear(robot, 200.0, 10.0, OriMode=mode)
    mv.ParCmd.Position.Rz = rz
    _expect_rejected(robot, sdk, mv, RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_ORI_MODE_NOT_SUPPORTED)


# ---------------------------------------------------------------- tool and frame


def _write(h: RobotTaskHarness, name: str, no: int, z: float, **data: Any) -> None:
    """WriteToolData / WriteFrameData with an offset of z mm; expects Done."""
    w = fb(h, name)
    if name == "MC_WriteToolDataFB":
        w.ParCmd.ToolNo = no
        d = w.ParCmd.ToolData
        d.LoadNo = 1
    else:
        w.ParCmd.FrameNo = no
        d = w.ParCmd.FrameData
    d.Z = z
    for key, value in data.items():
        setattr(d, key, value)
    seen = execute(h, w)
    assert seen.final["Done"] and not seen.final["Error"], seen.final


@pytest.mark.parametrize("no", [0, 5], ids=["default", "written"])
@pytest.mark.parametrize("kind", ["ToolNo", "FrameNo"])
def test_tool_and_frame_number(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str, no: int) -> None:
    """MoveLinearAbsolute with tool / frame 0 (default) or a tool / frame written before ends with Done; the RC receives the number."""
    enable(robot)
    if no:
        _write(robot, "MC_WriteToolDataFB" if kind == "ToolNo" else "MC_WriteFrameDataFB", no, 10.0)
    mv = _move_linear(robot, 200.0, 10.0, **{kind: no})
    _expect_done(robot, sdk, mv, [200.0, 10.0])
    assert sdk.last_command(MOVE_LINEAR)[kind] == str(no)


def test_external_tcp_tool(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveLinearAbsolute with a tool written as external TCP ends with Done."""
    enable(robot)
    _write(robot, "MC_WriteToolDataFB", 1, 100.0, ExternalTCP=True)
    mv = _move_linear(robot, 200.0, 10.0, ToolNo=1)
    _expect_done(robot, sdk, mv, [200.0, 10.0])
    assert sdk.last_command(MOVE_LINEAR)["ToolNo"] == "1"
