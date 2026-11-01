# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_group_stop
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of GroupStop against the SDK simulator (robot controller side).
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

"""Validation of GroupStop against the SDK simulator (robot controller side).

* a stop aborts the active and all buffered motions of the stopped sequence
* AbortedSequence names the sequence that was stopped (primary or secondary)
* a stop in the secondary sequence keeps the interrupted primary motion
* several stops and motions in the same PLC cycle are processed in call order
* a stop is accepted without power and in a manual operation mode
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import OperationMode, SequenceFlag
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


def _linear(h: RobotTaskHarness, x: float, **inputs: Any) -> Any:
    """MoveLinearAbsolute to (x, 0, 0) with default dynamics."""
    mv = cartesian(fb(h, "MC_MoveLinearAbsoluteFB", **inputs), x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = mv.ParCmd.JerkRate = -1.0
    return mv


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    s = execute(h, seq)
    assert s.final["Done"], s.final


def _set_mode(h: RobotTaskHarness, mode: OperationMode) -> None:
    om = fb(h, "MC_SetOperationModeFB")
    om.ParCmd.OperationMode = mode
    s = execute(h, om)
    assert s.final["Done"], s.final


def _moving(h: RobotTaskHarness, sdk: SdkSimulator, block: Any) -> None:
    block.Execute = True
    h.run(200, until=lambda: sdk.joints[0] > 5.0 or bool(block.Error))
    assert block.Active and sdk.joints[0] > 5.0, state(block)


@pytest.mark.parametrize("hold", [True, False], ids=["execute-held", "execute-pulse"])
def test_stop_aborts_active_and_buffered_motions(
    robot: RobotTaskHarness, sdk: SdkSimulator, hold: bool
) -> None:
    """GroupStop during a linear motion aborts it and the buffered next motion, the robot stands still.

    With Execute held Done stays TRUE until the falling edge; with a one-cycle pulse Done is still
    shown for at least one cycle. AbortedSequence reports the primary sequence."""
    sdk.set_move_cycles(200)
    enable(robot)
    first = _linear(robot, 100.0)
    second = _linear(robot, 0.0)
    _moving(robot, sdk, first)
    second.Execute = True
    robot.run(5)
    assert second.CommandBuffered and not second.Active, state(second)
    stop = fb(robot, "MC_GroupStopFB")
    stop.Execute = True
    if hold:
        seen = watch(robot, [stop], 100, lambda: finished(stop))[0]
        robot.run(10)
        assert stop.Done and not stop.Busy, state(stop)
        stop.Execute = False
        robot.run(2)
        assert not stop.Done, state(stop)
    else:
        robot.run(1)
        stop.Execute = False
        seen = watch(robot, [stop], 100, lambda: bool(stop.Done or stop.Error))[0]
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    assert stop.AbortedSequence == SequenceFlag.PRIMARY_SEQUENCE
    robot.run(50, until=lambda: finished(first) and finished(second))
    assert first.CommandAborted and not first.Done, state(first)
    assert second.CommandAborted and not second.Done, state(second)
    held = list(sdk.joints)
    robot.run(30)
    assert sdk.joints == held and 5.0 < held[0] < 100.0


def test_stop_shows_active_until_stopped(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop during a motion passes Busy, Active and Done in this order and aborts the motion."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    seen = execute(robot, fb(robot, "MC_GroupStopFB"))
    assert order(seen, "Busy", "Active", "Done"), seen.flags
    robot.run(10)
    assert mv.CommandAborted, state(mv)


def test_stop_in_secondary_keeps_primary_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop while the secondary sequence is active reports AbortedSequence 2 and keeps the paused primary motion.

    After SetSequence(primary) and GroupContinue the primary motion reaches its target."""
    sdk.set_move_cycles(200)
    enable(robot)
    mv = _linear(robot, 100.0)
    _moving(robot, sdk, mv)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    stop = fb(robot, "MC_GroupStopFB")
    s = execute(robot, stop, reset=False)
    assert s.final["Done"] and stop.AbortedSequence == SequenceFlag.SECONDARY_SEQUENCE, (
        s.final,
        stop.AbortedSequence,
    )
    stop.Execute = False
    robot.run(5)
    assert mv.Busy and not mv.CommandAborted, state(mv)
    _set_sequence(robot, SequenceFlag.PRIMARY_SEQUENCE)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(500, until=lambda: finished(mv))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)


def test_stop_aborts_secondary_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop during a motion of the secondary sequence aborts it and reports AbortedSequence 2."""
    sdk.set_move_cycles(200)
    enable(robot)
    _set_sequence(robot, SequenceFlag.SECONDARY_SEQUENCE)
    mv = _linear(robot, 100.0, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    mv.Execute = True
    robot.run(5)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(200, until=lambda: sdk.joints[0] > 5.0)
    assert mv.Active, state(mv)
    stop = fb(robot, "MC_GroupStopFB")
    s = execute(robot, stop, reset=False)
    assert s.final["Done"] and stop.AbortedSequence == SequenceFlag.SECONDARY_SEQUENCE
    robot.run(20, until=lambda: finished(mv))
    assert mv.CommandAborted and not mv.Done, state(mv)


def test_stop_and_set_sequence_in_one_cycle(robot: RobotTaskHarness) -> None:
    """SetSequence(secondary) and GroupStop started in the same cycle both end Done, the stop reports the secondary sequence."""
    enable(robot)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    stop = fb(robot, "MC_GroupStopFB")
    seq.Execute = stop.Execute = True
    watch(robot, [seq, stop], 100, lambda: finished(seq) and finished(stop))
    assert seq.Done and stop.Done, (state(seq), state(stop))
    assert stop.AbortedSequence == SequenceFlag.SECONDARY_SEQUENCE
    assert robot.user_data.SecondarySequenceActive


@pytest.mark.parametrize("running", [False, True], ids=["from-standstill", "while-moving"])
def test_stops_and_motions_in_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator, running: bool) -> None:
    """Motion, stop, motion, stop, motion started in one cycle: the first two motions are aborted, the last one is executed.

    Every GroupStop increases the stop counter (high half byte of the cyclic byte) by one.
    Variant: a joint motion is already running and is aborted as well."""
    sdk.set_move_cycles(100)
    enable(robot)
    before = None
    if running:
        before = move_axes(robot, 80.0)
        _moving(robot, sdk, before)
    counter = robot.ag.Cyclic.PlcToRob.FastStop
    blocks = [
        _linear(robot, 30.0),
        fb(robot, "MC_GroupStopFB"),
        _linear(robot, 60.0),
        fb(robot, "MC_GroupStopFB"),
        _linear(robot, 90.0),
    ]
    for b in blocks:
        b.Execute = True
    watch(robot, blocks, 800, lambda: all(finished(b) for b in blocks))
    m0, s0, m1, s1, m2 = blocks
    assert s0.Done and s1.Done, (state(s0), state(s1))
    assert m0.CommandAborted and m1.CommandAborted, (state(m0), state(m1))
    assert m2.Done, state(m2)
    assert sdk.joints[0] == pytest.approx(90.0)
    assert robot.ag.Cyclic.PlcToRob.FastStop == counter + 2
    if before is not None:
        assert before.CommandAborted and not before.Done, state(before)


@pytest.mark.parametrize("condition", ["power-off", "manual-t1-external"])
def test_stop_accepted_without_motion(robot: RobotTaskHarness, condition: str) -> None:
    """GroupStop without power or in operation mode T1 external ends Done without error."""
    if condition == "manual-t1-external":
        _set_mode(robot, OperationMode.T1_EXT)
        enable(robot)
    seen = execute(robot, fb(robot, "MC_GroupStopFB"))
    assert order(seen, "Busy", "Done") and not seen.final["Error"], (seen.flags, seen.final)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: 16 stopping commands in one cycle overflow the 4-bit stop counter (spec 5.6.6.2.1); "
        "the SDK only logs a warning and answers every GroupStop Done, no error is reported"
    ),
)
def test_more_than_15_stops_in_one_cycle(robot: RobotTaskHarness) -> None:
    """Sixteen GroupStop blocks started in the same cycle (more than the 4-bit stop counter can count) end with an error of the RC."""
    stops = [fb(robot, "MC_GroupStopFB") for _ in range(16)]
    for s in stops:
        s.Execute = True
    robot.run(300, until=lambda: all(finished(s) for s in stops))
    assert all(finished(s) for s in stops), [state(s) for s in stops]
    assert any(s.Error and s.ErrorID for s in stops), [state(s) for s in stops]
