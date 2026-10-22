# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_subprogram
#  Author:      Thorsten Brach
#  Date:        2026-10-22
#
#  Description:
#    CallSubprogram / StopSubprogram as long running commands against the SRCI SDK.
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

"""CallSubprogram / StopSubprogram as long running commands (SDK-SUB).

The SDK does not implement subprograms; the harness simulates one (C-007,
``SdkSimulator.set_subprogram_cycles``): it runs a number of cycles with Progress and
InProgress, stands still while the sequence is interrupted, ends with ABORTED on an abort
request or StopSubprogram, and starts again after every run in ProcessingMode CONTINUOUS
(InvocationCounter + 1) until it is stopped.
"""

from __future__ import annotations

import itertools
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ProcessingMode, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import enable, execute, fb, move_axes, robot, sdk_parameters, state

__all__ = ["robot", "sdk_parameters"]  # fixtures

CYCLES = 30  # cycles of the simulated subprogram
CALL_SUBPROGRAM = 7001


@pytest.fixture(autouse=True)
def subprogram(sdk: SdkSimulator) -> None:
    sdk.set_subprogram_cycles(CYCLES)


def call(h: RobotTaskHarness, job: int = 1, **inputs: Any) -> Any:
    cs = fb(h, "MC_CallSubprogramFB", **inputs)
    cs.ParCmd.JobID = job
    return cs


def flags(block: Any) -> dict[str, Any]:
    return {**state(block), "InProgress": block.InProgress, "Progress": block.OutCmd.Progress}


def in_progress(h: RobotTaskHarness, cs: Any) -> None:
    h.run(20, until=lambda: bool(cs.InProgress or cs.Error))
    assert cs.InProgress and cs.Busy and not cs.Error, flags(cs)


def stop(h: RobotTaskHarness, target: int) -> Any:
    st = fb(h, "MC_StopSubprogramFB")
    st.ParCmd.TargetID = target
    execute(h, st)
    return st


# ---------------------------------------------------------------- run


def test_runs_with_progress(robot: RobotTaskHarness) -> None:
    """InProgress while it runs, Progress rises, then Done with InProgress FALSE and Progress 100."""
    cs = call(robot, Execute=True)
    in_progress(robot, cs)
    seen = []
    for _ in range(CYCLES + 20):
        robot.run(1)
        seen.append(int(cs.OutCmd.Progress))
        if cs.Done:
            break
    assert cs.Done and not cs.InProgress and not cs.Error, flags(cs)
    assert cs.OutCmd.Progress == 100
    rising = [p for p in seen if p < 100]
    assert rising == sorted(rising) and len(set(rising)) > 5, seen


def test_parallel_without_power(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """PARALLEL with the robot disabled: runs to Done (no motion)."""
    assert not sdk.enabled
    cs = call(robot, Execute=True)
    robot.run(CYCLES + 30, until=lambda: bool(cs.Done or cs.Error))
    assert cs.Done, flags(cs)


def test_return_data(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """The ReturnData of the RC arrive in OutCmd.ReturnData."""
    sdk.set_response(CALL_SUBPROGRAM, {"ReturnData[0]": 0x12, "ReturnData[1]": 0x34})
    cs = call(robot)
    execute(robot, cs, cycles=CYCLES + 30, reset=False)
    assert (cs.OutCmd.ReturnData[0], cs.OutCmd.ReturnData[1]) == (0x12, 0x34)


def test_rc_error_while_running(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An error of the RC while it runs: Error with the ErrorID of the RC, InProgress FALSE."""
    cs = call(robot, Execute=True)
    in_progress(robot, cs)
    sdk.set_command_error(CALL_SUBPROGRAM, 0x8E33)
    robot.run(20, until=lambda: bool(cs.Error or cs.Done))
    assert cs.Error and cs.ErrorID == 0x8E33 and not cs.Busy, flags(cs)


# ---------------------------------------------------------------- sequence


def test_buffered_behind_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """BUFFERED in the primary sequence behind a motion: starts after the motion is Done."""
    sdk.set_move_cycles(60)
    enable(robot, sdk)
    mv = move_axes(robot, 10.0)
    cs = call(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    mv.Execute = cs.Execute = True
    robot.run(200, until=lambda: bool(mv.Done or mv.Error))
    assert mv.Done, state(mv)
    assert not cs.Done, flags(cs)
    robot.run(CYCLES + 30, until=lambda: bool(cs.Done or cs.Error))
    assert cs.Done, flags(cs)


def test_interrupt_and_continue(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupInterrupt while it runs in the sequence: CommandInterrupted, InProgress FALSE, Progress
    kept; GroupContinue: Done."""
    enable(robot, sdk)
    cs = call(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    cs.Execute = True
    in_progress(robot, cs)
    robot.run(5)
    execute(robot, fb(robot, "MC_GroupInterruptFB"))
    robot.run(3)
    assert cs.CommandInterrupted and not cs.InProgress and cs.Busy, flags(cs)
    kept = cs.OutCmd.Progress
    robot.run(20)
    assert cs.OutCmd.Progress == kept and 0 < kept < 100, flags(cs)
    execute(robot, fb(robot, "MC_GroupContinueFB"))
    robot.run(CYCLES + 30, until=lambda: bool(cs.Done or cs.Error))
    assert cs.Done and not cs.CommandInterrupted, flags(cs)


def test_group_stop_aborts(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupStop while it runs in the sequence: CommandAborted."""
    enable(robot, sdk)
    cs = call(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    cs.Execute = True
    in_progress(robot, cs)
    execute(robot, fb(robot, "MC_GroupStopFB"))
    robot.run(20, until=lambda: bool(cs.CommandAborted or cs.Done or cs.Error))
    assert cs.CommandAborted and not cs.Done and not cs.Busy, flags(cs)


def test_aborting_mode_aborts_motion(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ProcessingMode ABORTING: the running motion ends with CommandAborted, the subprogram runs
    to Done."""
    sdk.set_move_cycles(200)
    enable(robot, sdk)
    mv = move_axes(robot, 50.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 2.0)
    cs = call(robot, ProcessingMode=ProcessingMode.ABORTING, SequenceFlag=SequenceFlag.PRIMARY_SEQUENCE)
    cs.Execute = True
    robot.run(CYCLES + 50, until=lambda: bool(cs.Done or cs.Error))
    assert mv.CommandAborted and not mv.Done, state(mv)
    assert cs.Done, flags(cs)


def test_secondary_while_primary_interrupted(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """SequenceFlag SECONDARY after SetSequence(SECONDARY): runs to Done while the primary motion
    stays interrupted; back in the primary sequence the motion finishes."""
    sdk.set_move_cycles(100)
    enable(robot, sdk)
    mv = move_axes(robot, 30.0)
    mv.Execute = True
    robot.run(100, until=lambda: sdk.joints[0] > 3.0)
    seq = fb(robot, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    execute(robot, seq)
    held = sdk.joints[0]
    cs = call(robot, ProcessingMode=ProcessingMode.BUFFERED, SequenceFlag=SequenceFlag.SECONDARY_SEQUENCE)
    execute(robot, cs, cycles=CYCLES + 30)
    assert sdk.joints[0] == held and mv.Busy and not mv.Done, state(mv)


# ---------------------------------------------------------------- continuous, stop


def test_continuous_and_deactivate(robot: RobotTaskHarness) -> None:
    """CONTINUOUS: stays InProgress and Busy, the subprogram starts again after every run (Progress
    falls back); DEACTIVATE + new edge (ST-FIX F104) ends it with Done and the number of runs in
    InvocationCounter."""
    cs = call(robot, ProcessingMode=ProcessingMode.CONTINUOUS, Execute=True)
    in_progress(robot, cs)
    progress = []
    for _ in range(3 * CYCLES + 5):
        robot.run(1)
        progress.append(int(cs.OutCmd.Progress))
        assert cs.Busy and cs.InProgress and not cs.Done, flags(cs)
    restarts = sum(1 for a, b in itertools.pairwise(progress) if b < a)
    assert restarts >= 2, progress
    cs.Execute = False
    robot.run(2)
    cs.ProcessingMode = ProcessingMode.DEACTIVATE
    cs.Execute = True
    robot.run(20, until=lambda: bool(cs.Done or cs.Error or cs.CommandAborted))
    assert cs.Done and not cs.Busy and not cs.InProgress, flags(cs)
    assert cs.OutCmd.InvocationCounter >= 3, flags(cs)


def test_stop_subprogram_by_job_id(robot: RobotTaskHarness) -> None:
    """StopSubprogram with the JobID of a running call: CommandAborted of that call."""
    cs = call(robot, job=7, Execute=True)
    in_progress(robot, cs)
    stop(robot, 7)
    robot.run(10, until=lambda: bool(cs.CommandAborted or cs.Done))
    assert cs.CommandAborted and not cs.Done and not cs.Busy, flags(cs)


def test_stop_subprogram_only_matching_job(robot: RobotTaskHarness) -> None:
    """StopSubprogram aborts only the call with the matching JobID; the other runs to Done."""
    first = call(robot, job=1, Execute=True)
    second = call(robot, job=2, Execute=True)
    in_progress(robot, first)
    in_progress(robot, second)
    stop(robot, 2)
    robot.run(CYCLES + 30, until=lambda: bool(first.Done or first.Error))
    assert first.Done and not first.CommandAborted, flags(first)
    assert second.CommandAborted and not second.Done, flags(second)


def test_stop_continuous_subprogram(robot: RobotTaskHarness) -> None:
    """StopSubprogram ends a CONTINUOUS call (CommandAborted)."""
    cs = call(robot, job=9, ProcessingMode=ProcessingMode.CONTINUOUS, Execute=True)
    in_progress(robot, cs)
    robot.run(CYCLES + 5)
    stop(robot, 9)
    robot.run(10, until=lambda: bool(cs.CommandAborted or cs.Done))
    assert cs.CommandAborted and not cs.Busy, flags(cs)


def test_restart_with_new_job(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After Done the same instance starts a call with another JobID."""
    cs = call(robot, job=3)
    execute(robot, cs, cycles=CYCLES + 30)
    cs.ParCmd.JobID = 4
    execute(robot, cs, cycles=CYCLES + 30)
    assert (sdk.last_command(CALL_SUBPROGRAM) or {}).get("JobID") == "4"
