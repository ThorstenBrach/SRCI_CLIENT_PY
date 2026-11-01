# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_enable_jog_groupjog
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    GroupJog against the SDK simulator: continuous and incremental jogging,
#    override, direction changes, sequences, rejected jog requests.
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

"""GroupJog against the SDK simulator (robot controller behaviour).

The simulated robot jogs 0.1 units per cycle at 100 % override (identity kinematics: frame and
tool jogging move the same values as joint jogging, so the direction in a tool or user frame
cannot be checked - the tests check that ToolNo / FrameNo / Mode reach the RC).

* enable / disable, motion while a direction key is pressed, override, direction changes
* incremental jogging (DistanceReached), a new key starts a new increment
* jogging is rejected during a motion, as second instance, in an interrupted secondary sequence
* undefined jog mode rejected by the RC
* SDK gaps (strict xfail): GroupInterrupt / GroupStop of a jog, MotionActive after the increment,
  SW limits, power loss while jogging
"""

from __future__ import annotations

from typing import Any, cast

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import CmdType, JogMode, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, move_axes, order, state, watch

STEP = 0.1  # jog distance per cycle at 100 % override
ERR_SECOND_JOG = 0x8F15
ERR_SEQUENCE_INTERRUPTED = 0x8F17
ERR_JOG_DURING_MOVE = 0x8C33
ERR_JOG_MODE = 0x8D21
INFO_NOT_ENABLED = 0x6F02
INFO_JOG_INTERRUPTED = 0x6C15
INFO_JOG_ABORTED = 0x6C14
INFO_NOT_REACHABLE = 0x6C03


def _jog(
    h: RobotTaskHarness, mode: JogMode = JogMode.JOG_FRAME, override: int = 100, wait: bool = True, **par: Any
) -> Any:
    """GroupJog with Enable TRUE; waits for Enabled when ``wait``."""
    j = fb(h, "MC_GroupJogFB")
    j.ParCmd.Mode = mode
    j.ParCmd.Override = override
    for k, v in par.items():
        setattr(j.ParCmd, k, v)
    j.Enable = True
    if wait:
        h.run(50, until=lambda: bool(j.Enabled or j.Error))
        assert j.Enabled and not j.Error, state(j)
    return j


def _key(j: Any, name: str, on: bool = True) -> None:
    setattr(j.ParCmd.Control, name, on)


def _travel(h: RobotTaskHarness, sdk: SdkSimulator, cycles: int, axis: int = 0) -> float:
    before = sdk.joints[axis]
    h.run(cycles)
    return float(sdk.joints[axis] - before)


# ---------------------------------------------------------------- continuous jogging


@pytest.mark.parametrize(
    ("mode", "tool", "frame"),
    [
        (JogMode.JOG_FRAME, 0, 0),
        (JogMode.JOG_FRAME, 0, 1),
        (JogMode.JOG_TOOL, 1, 0),
        (JogMode.JOG_AXES, 0, 0),
    ],
    ids=["frame_world", "frame_1", "tool_1", "axes"],
)
def test_jog_moves_while_key_pressed(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: JogMode, tool: int, frame: int
) -> None:
    """GroupJog: Enable gives Busy, CommandBuffered, Enabled; the first direction key moves the robot until Enable is reset.

    Mode, ToolNo and FrameNo reach the RC; after Enable FALSE Busy, CommandBuffered and Enabled are
    FALSE and the robot stands still."""
    enable(robot)
    j = fb(robot, "MC_GroupJogFB")
    j.ParCmd.Mode, j.ParCmd.Override, j.ParCmd.ToolNo, j.ParCmd.FrameNo = mode, 100, tool, frame
    j.Enable = True
    s = watch(robot, [j], 50, lambda: bool(j.Enabled or j.Error))[0]
    assert order(s, "Busy", "CommandBuffered", "Enabled") and not j.Error, s.flags
    assert _travel(robot, sdk, 10) == 0.0 and not j.OutCmd.MotionActive
    _key(j, "X_J1_Pos")
    robot.run(8)
    assert j.OutCmd.MotionActive and _travel(robot, sdk, 10) == pytest.approx(10 * STEP)
    sent = sdk.last_command(int(CmdType.GroupJog))
    assert sent is not None and (int(sent["Mode"]), int(sent["ToolNo"]), int(sent["FrameNo"])) == (
        mode,
        tool,
        frame,
    )
    j.Enable = False
    robot.run(50, until=lambda: not j.Busy and not j.Enabled)
    assert not j.Busy and not j.Enabled and not j.CommandBuffered and not j.Error, state(j)
    assert _travel(robot, sdk, 10) == 0.0


@pytest.mark.parametrize("override", [5, 50, 100])
def test_jog_speed_follows_override(robot: RobotTaskHarness, sdk: SdkSimulator, override: int) -> None:
    """The jog speed is proportional to the jog override (5 %, 50 %, 100 %)."""
    enable(robot)
    j = _jog(robot, override=override)
    _key(j, "X_J1_Pos")
    robot.run(3)
    assert _travel(robot, sdk, 20) == pytest.approx(20 * STEP * override / 100.0)


def test_jog_override_change_while_jogging(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Changing the override while jogging changes the speed without stopping (5 % -> 20 % -> 60 %)."""
    enable(robot)
    j = _jog(robot, override=5)
    _key(j, "Y_J2_Pos")
    robot.run(3)
    for override in (5, 20, 60):
        j.ParCmd.Override = override
        robot.run(5)
        assert j.OutCmd.MotionActive and not j.Error, state(j)
        assert _travel(robot, sdk, 10, axis=1) == pytest.approx(10 * STEP * override / 100.0)


@pytest.mark.parametrize("mode", [JogMode.JOG_FRAME, JogMode.JOG_TOOL], ids=["frame", "tool"])
def test_jog_direction_change(robot: RobotTaskHarness, sdk: SdkSimulator, mode: JogMode) -> None:
    """Changing the pressed key changes the jog direction (Y, then X, then Z) without leaving the jog mode."""
    enable(robot)
    j = _jog(robot, mode=mode)
    prev = None
    for axis, key in ((1, "Y_J2_Pos"), (0, "X_J1_Pos"), (2, "Z_J3_Pos")):
        if prev:
            _key(j, prev, False)
        _key(j, key)
        prev = key
        robot.run(3)
        others = [sdk.joints[i] for i in range(3) if i != axis]
        assert _travel(robot, sdk, 10, axis) == pytest.approx(10 * STEP)
        assert [sdk.joints[i] for i in range(3) if i != axis] == others
        assert j.Enabled and j.OutCmd.MotionActive and not j.Error, state(j)


def test_jog_key_release_stops_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Releasing the direction key stops the motion: MotionActive FALSE, Enabled stays TRUE."""
    enable(robot)
    j = _jog(robot)
    _key(j, "Y_J2_Pos")
    robot.run(10)
    _key(j, "Y_J2_Pos", False)
    robot.run(5)
    assert not j.OutCmd.MotionActive and j.Enabled and not j.Error, state(j)
    assert _travel(robot, sdk, 10, axis=1) == 0.0


def test_jog_robot_not_enabled(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupJog with the robot not enabled: the command is buffered with InfoID 16#6F02 and the robot does not move."""
    j = _jog(robot, override=50, wait=False)
    _key(j, "X_J1_Pos")
    robot.run(50, until=lambda: bool(j.InfoID or j.Error))
    assert j.InfoID == INFO_NOT_ENABLED and j.CommandBuffered and not j.Error, state(j)
    assert _travel(robot, sdk, 10) == 0.0


# ---------------------------------------------------------------- rejected jog requests


def test_second_jog_instance_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second GroupJog while the first one jogs ends with Error 16#8F15; the first jog keeps moving."""
    enable(robot)
    first = _jog(robot, override=50)
    _key(first, "X_J1_Pos")
    robot.run(5)
    second = _jog(robot, override=50, wait=False)
    _key(second, "Y_J2_Pos")
    robot.run(50, until=lambda: bool(second.Error or second.Enabled))
    assert second.Error and second.ErrorID == ERR_SECOND_JOG and not second.Enabled, state(second)
    assert first.Enabled and first.OutCmd.MotionActive and not first.Error, state(first)
    assert _travel(robot, sdk, 10) == pytest.approx(10 * STEP * 0.5) and sdk.joints[1] == 0.0


def test_jog_during_motion_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupJog while a move is active ends with Error 16#8C33; the move continues to Done."""
    enable(robot)
    mv = move_axes(robot, 0.0, 0.0, 10.0)
    mv.Execute = True
    robot.run(20, until=lambda: bool(mv.Active))
    j = _jog(robot, override=50, wait=False)
    _key(j, "X_J1_Pos")
    robot.run(50, until=lambda: bool(j.Error or j.Enabled))
    assert j.Error and j.ErrorID == ERR_JOG_DURING_MOVE, state(j)
    robot.run(300, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done and sdk.joints[2] == pytest.approx(10.0) and sdk.joints[0] == 0.0


def test_jog_in_secondary_sequence_after_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After SetSequence to the secondary sequence and GroupContinue a GroupJog moves the robot until Enable is reset."""
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    j = _jog(robot)
    _key(j, "X_J1_Pos")
    robot.run(8)
    assert j.OutCmd.MotionActive and _travel(robot, sdk, 10) == pytest.approx(10 * STEP)
    j.Enable = False
    robot.run(50, until=lambda: not j.Busy and not j.Enabled)
    assert not j.Enabled and not j.Error and _travel(robot, sdk, 10) == 0.0


def test_jog_rejected_in_interrupted_secondary_sequence(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupJog while the secondary sequence is interrupted ends with Error 16#8F17; the robot does not move."""
    sdk.set_move_cycles(200)
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    mv = move_axes(robot, 10.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    mv.Execute = True
    robot.run(10)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    j = _jog(robot, wait=False)
    _key(j, "Y_J2_Pos")
    robot.run(50, until=lambda: bool(j.Error or j.Enabled))
    assert j.Error and j.ErrorID == ERR_SEQUENCE_INTERRUPTED, state(j)
    assert _travel(robot, sdk, 10, axis=1) == 0.0


@pytest.mark.parametrize("mode", [12, 22])
def test_undefined_jog_mode_rejected_by_rc(robot: RobotTaskHarness, sdk: SdkSimulator, mode: int) -> None:
    """An undefined jog mode is sent to the RC and rejected: Busy then Error 16#8D21, no motion."""
    enable(robot)
    j = _jog(robot, wait=False)
    j.ParCmd.Mode = mode
    _key(j, "X_J1_Pos")
    s = watch(robot, [j], 50, lambda: bool(j.Error or j.Enabled))[0]
    assert order(s, "Busy", "Error") and j.ErrorID == ERR_JOG_MODE, s.flags
    assert _travel(robot, sdk, 10) == 0.0


# ---------------------------------------------------------------- incremental jogging


@pytest.mark.parametrize(
    ("mode", "kind", "increment"),
    [
        (JogMode.JOG_FRAME, "IncrementalTranslation", 5.0),
        (JogMode.JOG_TOOL, "IncrementalTranslation", 5.0),
        (JogMode.JOG_AXES, "IncrementalRotation", 1.5),
    ],
    ids=["frame_translation", "tool_translation", "axes_rotation"],
)
def test_jog_increment_reached(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: JogMode, kind: str, increment: float
) -> None:
    """Incremental jogging: the robot moves exactly the increment and reports DistanceReached; Enable FALSE resets the outputs."""
    enable(robot)
    j = _jog(robot, mode=mode, **cast(dict[str, Any], {kind: increment}))
    _key(j, "X_J1_Pos")
    robot.run(int(increment / STEP) + 20, until=lambda: bool(j.OutCmd.DistanceReached))
    assert j.OutCmd.DistanceReached and not j.Error, state(j)
    robot.run(10)
    assert sdk.joints[0] == pytest.approx(increment)
    j.Enable = False
    robot.run(50, until=lambda: not j.Busy and not j.Enabled)
    assert not j.Enabled and not j.CommandBuffered and not j.Error, state(j)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: after the increment is reached the RC keeps reporting MotionActive TRUE as long as the key is "
        "pressed (simulated jog: active = key pressed), although the robot stands still (spec 6.3.1 GroupJog "
        "outputs, MotionActive: RA is moving)"
    ),
)
def test_jog_not_moving_after_increment(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After the increment is reached the robot stands still and MotionActive is FALSE while the key stays pressed."""
    enable(robot)
    j = _jog(robot, IncrementalTranslation=2.0)
    _key(j, "X_J1_Pos")
    robot.run(60, until=lambda: bool(j.OutCmd.DistanceReached))
    robot.run(5)
    assert _travel(robot, sdk, 10) == 0.0
    assert j.OutCmd.DistanceReached and not j.OutCmd.MotionActive, state(j)


@pytest.mark.parametrize(
    ("mode", "kind"),
    [
        (JogMode.JOG_FRAME, "IncrementalRotation"),
        (JogMode.JOG_TOOL, "IncrementalRotation"),
        (JogMode.JOG_AXES, "IncrementalTranslation"),
    ],
    ids=["frame_rotation_only", "tool_rotation_only", "axes_translation_only"],
)
def test_jog_increment_of_other_kind_ignored(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: JogMode, kind: str
) -> None:
    """An increment that does not apply to the pressed key (rotation for X, translation for joints) is ignored: continuous jog."""
    enable(robot)
    j = _jog(robot, mode=mode, **cast(dict[str, Any], {kind: 1.0}))
    _key(j, "X_J1_Pos")
    robot.run(40)
    assert sdk.joints[0] > 2.0 and not j.OutCmd.DistanceReached and j.OutCmd.MotionActive, state(j)
    j.Enable = False
    robot.run(50, until=lambda: not j.Busy and not j.Enabled)
    assert not j.Enabled and not j.Error and _travel(robot, sdk, 10) == 0.0


def test_jog_second_key_starts_new_increment(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Pressing a second key during an incremental jog starts a new increment for both keys (X: 2.5 + 5, Y: 5)."""
    enable(robot)
    j = _jog(robot, IncrementalTranslation=5.0)
    _key(j, "X_J1_Pos")
    robot.run(200, until=lambda: sdk.joints[0] >= 2.5)
    _key(j, "Y_J2_Pos")
    robot.run(5)
    robot.run(200, until=lambda: bool(j.OutCmd.DistanceReached))
    robot.run(10)
    assert j.OutCmd.DistanceReached and not j.Error, state(j)
    assert sdk.joints[0] == pytest.approx(7.5, abs=STEP) and sdk.joints[1] == pytest.approx(5.0)


def test_jog_key_released_before_increment(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Releasing the key before the increment is reached stops the robot early; MotionActive FALSE, Enabled TRUE."""
    enable(robot)
    j = _jog(robot, mode=JogMode.JOG_AXES, IncrementalRotation=15.0)
    _key(j, "X_J1_Pos")
    robot.run(50)
    _key(j, "X_J1_Pos", False)
    robot.run(5)
    assert 0.0 < sdk.joints[0] < 15.0 and _travel(robot, sdk, 10) == 0.0
    assert not j.OutCmd.MotionActive and j.Enabled, state(j)


def test_jog_increment_change_ignored_until_key_change(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A new increment while the key is pressed is not used for the running jog step (5.0 stays); the next key press uses it."""
    enable(robot)
    j = _jog(robot, IncrementalTranslation=5.0)
    _key(j, "X_J1_Pos")
    robot.run(20)
    j.ParCmd.IncrementalTranslation = 2.0
    robot.run(100, until=lambda: bool(j.OutCmd.DistanceReached))
    robot.run(10)
    assert sdk.joints[0] == pytest.approx(5.0) and not j.Error, state(j)
    _key(j, "X_J1_Pos", False)
    robot.run(5)
    _key(j, "X_J1_Pos")
    robot.run(100, until=lambda: bool(j.OutCmd.DistanceReached))
    robot.run(10)
    assert sdk.joints[0] == pytest.approx(7.0)


# ---------------------------------------------------------------- SDK gaps


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: GroupInterrupt / GroupStop during a jog never complete (sequence state stays 'interrupting' 95) "
        "and the jog keeps moving; spec 6.3.1 / 5.6.6: jog stops, InfoID 16#6C15 (interrupt) / 16#6C14 (stop)"
    ),
)
@pytest.mark.parametrize(
    ("block", "info"),
    [("MC_GroupInterruptFB", INFO_JOG_INTERRUPTED), ("MC_GroupStopFB", INFO_JOG_ABORTED)],
    ids=["interrupt", "stop"],
)
def test_jog_interrupted_or_stopped(
    robot: RobotTaskHarness, sdk: SdkSimulator, block: str, info: int
) -> None:
    """GroupInterrupt / GroupStop during a jog: Done, the jog stops with InfoID 16#6C15 / 16#6C14 and stays Enabled."""
    enable(robot)
    j = _jog(robot, override=50)
    _key(j, "X_J1_Pos")
    robot.run(20)
    s = execute(robot, fb(robot, block), cycles=100)
    assert s.final["Done"], s.final
    robot.run(5)
    assert not j.OutCmd.MotionActive and j.InfoID == info and j.Enabled, state(j)
    assert _travel(robot, sdk, 10) == 0.0


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: the simulated jog ignores the SW limits (it moves past the limit, no InfoID 16#6C03); "
        "spec 7.5 / 6.3.1: the RC stops the jog at the limit"
    ),
)
def test_jog_stops_at_sw_limit(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Jogging towards a SW limit stops at the limit with InfoID 16#6C03; the jog stays Enabled."""
    sdk.rc_change(sdk.RC_SW_LIMITS, 0, [-1.0, 1.0] * 6)
    enable(robot)
    j = _jog(robot)
    _key(j, "X_J1_Pos")
    robot.run(50)
    assert sdk.joints[0] <= 1.0 + 1e-6, sdk.joints[0]
    assert j.InfoID == INFO_NOT_REACHABLE and not j.OutCmd.MotionActive and j.Enabled, state(j)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: when the drives are switched off during a jog the RC keeps MotionActive TRUE (only InfoID "
        "16#6F02); spec 6.3.1: MotionActive reports that the RA moves"
    ),
)
def test_disable_robot_while_jogging(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Switching the drives off while jogging stops the robot; the jog reports MotionActive FALSE and InfoID 16#6F02."""
    en = enable(robot)
    j = _jog(robot)
    _key(j, "X_J1_Pos")
    robot.run(20)
    en.Enable = False
    robot.run(20)
    assert _travel(robot, sdk, 10) == 0.0
    assert j.InfoID == INFO_NOT_ENABLED and not j.OutCmd.MotionActive, state(j)
