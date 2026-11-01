# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_sequence_return
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of ReturnToPrimary against the SDK simulator.
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

"""Validation of ReturnToPrimary against the SDK simulator (robot controller side).

Setup of most tests (``_away``): a joint motion to J1 = 50 is interrupted with GroupInterrupt
at J1 > 10 and the robot is jogged away along J2 (secondary sequence, 0.1 per cycle).

* return to the interrupt position (ReturnMode 0) or to the end position (ReturnMode 1)
* DistanceLimit, tool / frame of the interrupted motion and AllowDifferences
* rejected while another ReturnToPrimary runs, during a primary motion, during an interrupt
  of the secondary sequence
* interrupt, stop, power off while returning
* dynamics and inputs changed while returning; the optional parameter Time

The simulator does not model dynamics (every motion takes the configured number of cycles), so
the rate tests check the values sent to the RC and the final position, not the duration.
"""

from __future__ import annotations

from typing import Any, cast

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import JogMode, ReturnMode, RobotLibraryErrorIdEnum, SequenceFlag, TrajectoryMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    cartesian,
    enable,
    execute,
    fb,
    finished,
    move_axes,
    order,
    state,
    watch,
)

E = RobotLibraryErrorIdEnum
RETURN_TO_PRIMARY = 2104  # CmdType


def _jog(h: RobotTaskHarness, axis: str, cycles: int) -> None:
    j = fb(h, "MC_GroupJogFB", Enable=True)
    j.ParCmd.Mode = JogMode.JOG_AXES
    j.ParCmd.Override = 100
    h.run(50, until=lambda: bool(j.Enabled or j.Error))
    assert j.Enabled, state(j)
    setattr(j.ParCmd.Control, axis, True)
    h.run(cycles)
    setattr(j.ParCmd.Control, axis, False)
    h.run(5)
    j.Enable = False
    h.run(50, until=lambda: not j.Busy)


def _linear(h: RobotTaskHarness, x: float, **inputs: Any) -> Any:
    mv = cartesian(fb(h, "MC_MoveLinearAbsoluteFB", **inputs), x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def _away(
    h: RobotTaskHarness, sdk: SdkSimulator, jog_cycles: int = 100, motion: Any = None, jog: bool = True
) -> tuple[Any, list[float], Any]:
    """Motion to J1 = 50 interrupted at J1 > 10, J2 jogged away (``jog_cycles`` * 0.1).
    Returns the motion, the interrupt position and the EnableRobot block."""
    sdk.set_move_cycles(100)
    en = enable(h)
    mv = motion(h) if motion is not None else move_axes(h, 50.0)
    mv.Execute = True
    h.run(100, until=lambda: sdk.joints[0] > 10.0 or bool(mv.Error))
    assert mv.Active, state(mv)
    execute(h, fb(h, "MC_GroupInterruptFB"))
    at = list(sdk.joints)
    if jog:
        _jog(h, "Y_J2_Pos", jog_cycles)
    return mv, at, en


def _rtp(h: RobotTaskHarness, enable_: bool = False, **par: Any) -> Any:
    """ReturnToPrimary, linear trajectory and default dynamics unless given."""
    block = fb(h, "MC_ReturnToPrimaryFB")
    block.ParCmd.TrajectoryMode = TrajectoryMode.LINEAR_MOVEMENT
    for name, value in par.items():
        setattr(block.ParCmd, name, value)
    block.Enable = enable_
    return block


def _run(h: RobotTaskHarness, block: Any, cycles: int = 400) -> Any:
    block.Enable = True
    return watch(h, [block], cycles, lambda: bool(block.Done or block.Error))[0]


def _active(h: RobotTaskHarness, block: Any) -> None:
    block.Enable = True
    h.run(100, until=lambda: bool(block.Active and block.OutCmd.Progress > 10.0))
    assert block.Active, state(block)


def _held(h: RobotTaskHarness, sdk: SdkSimulator, cycles: int = 20) -> bool:
    before = list(sdk.joints)
    h.run(cycles)
    return bool(sdk.joints == before)


# ---------------------------------------------------------------- target position


def test_return_to_interrupt_position(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReturnToPrimary (linear, ReturnMode 0) passes Busy, CommandBuffered, Active, Done and ends at the interrupt position.

    InPrimaryPos is FALSE before and TRUE after the return; Enable FALSE resets all outputs."""
    _, at, _ = _away(robot, sdk)
    assert not robot.user_data.InPrimaryPos
    block = _rtp(robot)
    seen = _run(robot, block)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert block.OutCmd.Progress == 100.0
    assert sdk.joints == pytest.approx(at)
    assert robot.user_data.InPrimaryPos
    block.Enable = False
    robot.run(2)
    assert not (block.Busy or block.Done or block.Active or block.CommandBuffered or block.Error), state(
        block
    )


@pytest.mark.parametrize("limit", [100.0, 5000.0])
def test_return_within_distance_limit(robot: RobotTaskHarness, sdk: SdkSimulator, limit: float) -> None:
    """A DistanceLimit larger than the distance to the path does not prevent the return (Done at the interrupt position)."""
    _, at, _ = _away(robot, sdk)
    block = _rtp(robot, DistanceLimit=limit)
    seen = _run(robot, block)
    assert "Active" in seen.flags and block.Done, state(block)
    assert sdk.joints == pytest.approx(at)


def test_return_beyond_distance_limit_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A DistanceLimit below the distance to the path: ERR_LIMIT_EXCEEDED_RETURN_POS, the robot does not move."""
    _away(robot, sdk)  # 10 away from the path
    away_at = list(sdk.joints)
    block = _rtp(robot, DistanceLimit=4.0)
    seen = _run(robot, block)
    assert order(seen, "Busy", "Error") and "Active" not in seen.flags, seen.flags
    assert block.ErrorID == E.ERR_LIMIT_EXCEEDED_RETURN_POS, state(block)
    assert sdk.joints == away_at and not robot.user_data.InPrimaryPos


def test_return_to_end_position(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReturnMode 1 moves to the target of the interrupted motion (Done); after GroupContinue the interrupted motion ends Done."""
    mv, _, _ = _away(robot, sdk)
    block = _rtp(robot, ReturnMode=ReturnMode.END_POSITION, DistanceLimit=5000.0)
    seen = _run(robot, block)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert sdk.joints[:2] == pytest.approx([50.0, 0.0])
    assert robot.user_data.InPrimaryPos
    block.Enable = False
    robot.run(2)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done, state(mv)


def test_return_to_end_position_without_leaving_path(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Interrupted but not jogged away: ReturnMode 1 ends Done at the target of the interrupted motion, InPrimaryPos TRUE."""
    _away(robot, sdk, jog=False)
    block = _rtp(robot, ReturnMode=ReturnMode.END_POSITION)
    seen = _run(robot, block)
    assert seen.flags[-1] == "Done" and block.Done, (seen.flags, state(block))
    assert sdk.joints[0] == pytest.approx(50.0)
    assert robot.user_data.InPrimaryPos


def test_return_after_group_stop_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After GroupStop, ReturnToPrimary (ReturnMode 1, DistanceLimit 10) fails with ERR_LIMIT_EXCEEDED_RETURN_POS.

    GroupStop deleted the interrupted motion; the robot does not move."""
    mv, _, _ = _away(robot, sdk)
    execute(robot, fb(robot, "MC_GroupStopFB"))
    robot.run(5)
    assert mv.CommandAborted, state(mv)
    away_at = list(sdk.joints)
    block = _rtp(robot, ReturnMode=ReturnMode.END_POSITION, DistanceLimit=10.0)
    seen = _run(robot, block, 100)
    assert order(seen, "Busy", "Error"), seen.flags
    assert block.ErrorID == E.ERR_LIMIT_EXCEEDED_RETURN_POS and not robot.user_data.InPrimaryPos, state(block)
    assert sdk.joints == away_at


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: after a completed motion and a jog the SDK answers ReturnToPrimary Done without "
        "moving; spec 6.3.11 requires the return to the position where the primary sequence was left"
    ),
)
@pytest.mark.parametrize(
    "mode",
    [ReturnMode.INTERRUPT_POSITION, ReturnMode.END_POSITION],
    ids=["interrupt-position", "end-position"],
)
def test_return_after_completed_motion(robot: RobotTaskHarness, sdk: SdkSimulator, mode: ReturnMode) -> None:
    """Motion to P1 completed, robot jogged away: ReturnToPrimary (ReturnMode 0 or 1) moves back to P1 and ends Done."""
    sdk.set_move_cycles(50)
    enable(robot)
    execute(robot, move_axes(robot, 30.0))
    p1 = list(sdk.joints)
    _jog(robot, "Y_J2_Pos", 100)
    block = _rtp(robot, ReturnMode=mode)
    seen = _run(robot, block)
    assert block.Done and "Active" in seen.flags, (seen.flags, state(block))
    assert sdk.joints == pytest.approx(p1)


# ---------------------------------------------------------------- rejected


def test_second_return_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A second ReturnToPrimary during an active one fails with ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD.

    The first one ends Done at the interrupt position."""
    _, at, _ = _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    first = _rtp(robot)
    _active(robot, first)
    second = _rtp(robot)
    seen = _run(robot, second, 50)
    assert order(seen, "Busy", "Error") and second.ErrorID == E.ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD, state(
        second
    )
    robot.run(400, until=lambda: bool(first.Done or first.Error))
    assert first.Done, state(first)
    assert sdk.joints == pytest.approx(at)


@pytest.mark.parametrize("jogged", [True, False], ids=["returned-and-continued", "continued-on-path"])
def test_return_rejected_during_primary_motion(
    robot: RobotTaskHarness, sdk: SdkSimulator, jogged: bool
) -> None:
    """ReturnToPrimary during the continued primary motion fails with ERR_CMD_REQUIRES_INTERRUPT_OR_IDLE_STATE.

    The motion goes on to its target."""
    mv, _, _ = _away(robot, sdk, jog=jogged)
    if jogged:
        first = _rtp(robot)
        _run(robot, first)
        first.Enable = False
        robot.run(2)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(3)
    assert mv.Active, state(mv)
    block = _rtp(robot)
    seen = _run(robot, block, 50)
    assert order(seen, "Busy", "Error") and block.ErrorID == E.ERR_CMD_REQUIRES_INTERRUPT_OR_IDLE_STATE, (
        state(block)
    )
    robot.run(300, until=lambda: finished(mv))
    assert mv.Done and sdk.joints[0] == pytest.approx(50.0), state(mv)


def test_return_rejected_in_interrupted_secondary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReturnToPrimary in the interrupted secondary sequence fails with ERR_CMD_NOT_ALLOWED_DURING_ACTIVE_INTERRUPT.

    The secondary sequence was selected with SetSequence but not continued."""
    _away(robot, sdk)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    away_at = list(sdk.joints)
    block = _rtp(robot)
    seen = _run(robot, block, 100)
    assert order(seen, "Busy", "Error") and block.ErrorID == E.ERR_CMD_NOT_ALLOWED_DURING_ACTIVE_INTERRUPT, (
        state(block)
    )
    assert sdk.joints == away_at


def test_return_in_running_secondary(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After SetSequence(secondary) and GroupContinue, ReturnToPrimary ends Done at the interrupt position.

    InPrimaryPos and SecondarySequenceActive are TRUE afterwards."""
    _, at, _ = _away(robot, sdk)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    assert execute(robot, seq).final["Done"]
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    block = _rtp(robot)
    seen = _run(robot, block)
    assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), seen.flags
    assert sdk.joints == pytest.approx(at)
    assert robot.user_data.InPrimaryPos and robot.user_data.SecondarySequenceActive


# ---------------------------------------------------------------- interrupt / stop / power


def test_second_return_while_first_interrupted(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An interrupted ReturnToPrimary is CommandInterrupted; a second one fails (ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD)."""
    _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    first = _rtp(robot)
    _active(robot, first)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    robot.run(3)
    assert first.CommandInterrupted and first.Busy and not first.Active, state(first)
    second = _rtp(robot)
    seen = _run(robot, second, 50)
    assert order(seen, "Busy", "Error") and second.ErrorID == E.ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD, state(
        second
    )


def test_stop_interrupted_return(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop after GroupInterrupt of an active ReturnToPrimary aborts it (CommandAborted, not Done)."""
    _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot)
    _active(robot, block)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    robot.run(3)
    assert block.CommandInterrupted, state(block)
    execute(robot, fb(robot, "MC_GroupStopFB"))
    robot.run(20, until=lambda: bool(block.CommandAborted or block.Done or block.Error))
    assert block.CommandAborted and not block.Done and not block.Busy, state(block)


def test_return_without_power_waits(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReturnToPrimary without power stays Busy and CommandBuffered; power on and GroupContinue finish it.

    It ends Done at the interrupt position."""
    _, at, en = _away(robot, sdk)
    en.Enable = False
    robot.run(100, until=lambda: not en.Enabled)
    block = _rtp(robot)
    seen = _run(robot, block, 100)
    assert block.Busy and block.CommandBuffered and not (block.Active or block.Done or block.Error), state(
        block
    )
    assert order(seen, "Busy", "CommandBuffered"), seen.flags
    en.Enable = True
    robot.run(100, until=lambda: bool(en.Enabled))
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(400, until=lambda: bool(block.Done or block.Error))
    assert block.Done, state(block)
    assert sdk.joints == pytest.approx(at)


def test_power_off_while_returning(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Power off during ReturnToPrimary: CommandInterrupted, Busy and CommandBuffered TRUE, Active FALSE.

    Progress and position are frozen; after power on and GroupContinue the block ends Done."""
    _, at, en = _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot)
    _active(robot, block)
    en.Enable = False
    robot.run(100, until=lambda: not en.Enabled)
    robot.run(5)
    assert block.CommandInterrupted and block.Busy and block.CommandBuffered and not block.Active, state(
        block
    )
    progress = block.OutCmd.Progress
    assert _held(robot, sdk) and block.OutCmd.Progress == progress
    en.Enable = True
    robot.run(100, until=lambda: bool(en.Enabled))
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(400, until=lambda: bool(block.Done or block.Error))
    assert block.Done, state(block)
    assert sdk.joints == pytest.approx(at)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: a motion error during ReturnToPrimary switches the power off but the SDK reports "
        "the command BUFFERED again instead of ERROR (spec 6.3.11 / 5.5.10)"
    ),
)
def test_rc_error_while_returning(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An RC motion error during ReturnToPrimary ends the block with Error and an ErrorID."""
    _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot)
    _active(robot, block)
    sdk.set_motion_error(0x6C02)
    robot.run(100, until=lambda: bool(block.Error or block.Done))
    assert block.Error and block.ErrorID != 0, state(block)


# ---------------------------------------------------------------- dynamics and inputs


@pytest.mark.parametrize("value", [5.0, 50.0, 95.0, 100.0, 0.0, -25.0])
@pytest.mark.parametrize("rate", ["VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate"])
def test_dynamics_rate_sent(robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, value: float) -> None:
    """A dynamics rate of ReturnToPrimary is sent as value * 100 and the return ends Done.

    A negative rate is sent as 16#FFFF (use the default). The simulator does not model the
    effect on the duration."""
    _, at, _ = _away(robot, sdk)
    block = _rtp(robot, **cast(dict[str, Any], {rate: value}))
    _run(robot, block)
    assert block.Done, state(block)
    sent = sdk.last_command(RETURN_TO_PRIMARY) or {}
    expected = 0xFFFF if value < 0 else round(value * 100)
    assert int(sent[rate]) == expected, sent
    assert sdk.joints == pytest.approx(at)


@pytest.mark.parametrize("rate", ["VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate"])
def test_dynamics_rate_changed_while_returning(robot: RobotTaskHarness, sdk: SdkSimulator, rate: str) -> None:
    """A dynamics rate changed from 5 % to 100 % while returning does not disturb the active return (Done at the interrupt position)."""
    _, at, _ = _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot, **cast(dict[str, Any], {rate: 5.0}))
    _active(robot, block)
    setattr(block.ParCmd, rate, 100.0)
    robot.run(400, until=lambda: bool(block.Done or block.Error))
    assert block.Done, state(block)
    assert sdk.joints == pytest.approx(at)


@pytest.mark.parametrize(
    ("name", "first", "changed", "end_position"),
    [
        ("ReturnMode", ReturnMode.INTERRUPT_POSITION, ReturnMode.END_POSITION, False),
        ("ReturnMode", ReturnMode.END_POSITION, ReturnMode.INTERRUPT_POSITION, True),
        ("DistanceLimit", 100.0, 1.0, False),
        ("TrajectoryMode", TrajectoryMode.LINEAR_MOVEMENT, TrajectoryMode.PTP_MOVEMENT, False),
    ],
    ids=["return-mode-0-to-1", "return-mode-1-to-0", "distance-limit", "trajectory-mode"],
)
def test_input_changed_while_returning(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, first: Any, changed: Any, end_position: bool
) -> None:
    """ReturnMode, DistanceLimit or TrajectoryMode changed while returning: the active return keeps its target and ends Done."""
    _, at, _ = _away(robot, sdk, jog_cycles=200)
    sdk.set_move_cycles(200)
    block = _rtp(robot, **{name: first})
    _active(robot, block)
    setattr(block.ParCmd, name, changed)
    robot.run(400, until=lambda: bool(block.Done or block.Error))
    assert block.Done, state(block)
    expected = [50.0, 0.0] if end_position else at[:2]
    assert sdk.joints[:2] == pytest.approx(expected)


@pytest.mark.parametrize("move_time", [5, 10, 150, 1000])
def test_move_time_not_supported(robot: RobotTaskHarness, sdk: SdkSimulator, move_time: int) -> None:
    """ReturnToPrimary with Time > 0 is answered with ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED, no return.

    Time is an optional parameter the simulated RC does not support."""
    _away(robot, sdk)
    block = _rtp(robot, MoveTime=move_time)
    seen = _run(robot, block, 100)
    assert "Error" in seen.flags and block.ErrorID == E.ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED, state(block)
    assert int((sdk.last_command(RETURN_TO_PRIMARY) or {}).get("Time", -1)) == move_time
    assert not robot.user_data.InPrimaryPos


# ---------------------------------------------------------------- tool and frame


def _with_tool(h: RobotTaskHarness, tool: int, frame: int) -> Any:
    mv = _linear(h, 50.0)
    mv.ParCmd.ToolNo, mv.ParCmd.FrameNo = tool, frame
    return mv


@pytest.mark.parametrize(
    ("motion_tf", "par", "error"),
    [
        ((0, 0), {"ToolNo": 0}, None),
        ((0, 0), {"FrameNo": 0}, None),
        ((2, 2), {"ToolNo": 1, "FrameNo": 2}, E.ERR_TOOLNO_DIFFERS_TARGET),
        ((2, 2), {"ToolNo": 2, "FrameNo": 1}, E.ERR_FRAMENO_DIFFERS_TARGET),
        ((2, 2), {"ToolNo": 4, "FrameNo": 2, "AllowDifferences": True}, None),
        ((2, 2), {"ToolNo": 2, "FrameNo": 4, "AllowDifferences": True}, None),
    ],
    ids=["tool-0", "frame-0", "other-tool", "other-frame", "other-tool-allowed", "other-frame-allowed"],
)
def test_tool_and_frame_of_interrupted_motion(
    robot: RobotTaskHarness,
    sdk: SdkSimulator,
    motion_tf: tuple[int, int],
    par: dict[str, Any],
    error: int | None,
) -> None:
    """ToolNo / FrameNo must match the interrupted motion unless AllowDifferences is set.

    PrimaryPosToolNo / PrimaryPosFrameNo report the numbers of the interrupted motion."""
    tool, frame = motion_tf
    _, at, _ = _away(robot, sdk, motion=lambda h: _with_tool(h, tool, frame))
    away_at = list(sdk.joints)
    block = _rtp(robot, **par)
    seen = _run(robot, block)
    if error is None:
        assert order(seen, "Busy", "CommandBuffered", "Active", "Done"), (seen.flags, state(block))
        assert (block.OutCmd.PrimaryPosToolNo, block.OutCmd.PrimaryPosFrameNo) == (tool, frame)
        assert sdk.joints == pytest.approx(at)
    else:
        assert order(seen, "Busy", "Error") and block.ErrorID == error, state(block)
        assert sdk.joints == away_at


@pytest.mark.parametrize("allow", [False, True], ids=["differences-rejected", "differences-allowed"])
@pytest.mark.parametrize("data", ["tool", "frame"])
def test_tool_or_frame_data_changed(
    robot: RobotTaskHarness, sdk: SdkSimulator, data: str, allow: bool
) -> None:
    """Tool or frame data rewritten after the interrupt: ReturnToPrimary fails unless AllowDifferences is set.

    Errors: ERR_TOOLID_DIFFERS_TARGET (tool 2) / ERR_FRAMEDATA_DIFFERS (frame 2)."""
    _, at, _ = _away(robot, sdk, motion=lambda h: _with_tool(h, 2, 2))
    if data == "tool":
        wr = fb(robot, "MC_WriteToolDataFB")
        wr.ParCmd.ToolNo = 2
        wr.ParCmd.ToolData.X = 200.0
        wr.ParCmd.ToolData.LoadNo = 1
    else:
        wr = fb(robot, "MC_WriteFrameDataFB")
        wr.ParCmd.FrameNo = 2
        wr.ParCmd.FrameData.X = 200.0
    assert execute(robot, wr).final["Done"]
    away_at = list(sdk.joints)
    block = _rtp(robot, ToolNo=2, FrameNo=2, AllowDifferences=allow)
    _run(robot, block)
    if allow:
        assert block.Done, state(block)
        assert (block.OutCmd.PrimaryPosToolNo, block.OutCmd.PrimaryPosFrameNo) == (2, 2)
        assert sdk.joints == pytest.approx(at)
    else:
        expected = E.ERR_TOOLID_DIFFERS_TARGET if data == "tool" else E.ERR_FRAMEDATA_DIFFERS
        assert block.Error and block.ErrorID == expected, state(block)
        assert sdk.joints == away_at
