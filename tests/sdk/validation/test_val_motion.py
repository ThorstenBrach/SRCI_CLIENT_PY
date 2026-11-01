# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_val_motion
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Motion blocks without a reference test set (VAL-MOV): stop, interrupt,
#    override, disable, user data states and tool / frame numbers.
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

"""Motion blocks without a reference test set (area VAL-MOV).

The reference test sets of MoveLinear / MoveDirect / MoveAxesAbsolute check the interplay of a
motion with GroupStop, GroupInterrupt / GroupContinue, the speed override, the power of the robot
and the user data. The same checks run here for every other motion block of the planner
(relative, circular, cam, offset, approach / depart, pick and place, SearchHardStop). Buffering,
aborting and the secondary sequence of these blocks are covered by MET PM-01, PM-02 and SEQ-01.

The simulated robot moves every motion as a joint motion of the planner (identity kinematics);
a motion has "moved" as soon as a joint left its start value.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import RobotLibraryErrorIdEnum, RobotLibraryInfoIdEnum
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import enable
from tests.sdk.test_methodology import (
    CLASSES_ALL,
    MOTION,
    MOTION_KNOWN,
    _motion,
    outputs,
    robot,
    start,
)
from tests.sdk.validation.test_val_parameters import REFERENCE

MOVE_CYCLES = 200
SEARCH = ["MC_SearchHardStopFB", "MC_SearchHardStopJFB"]
NAMES = sorted(n for n in [*MOTION, *SEARCH] if n[3:-2] not in REFERENCE and n not in MOTION_KNOWN)
KNOWN: dict[tuple[str, str], str] = {}


def _params(test: str, names: list[str] = NAMES) -> list[Any]:
    return [
        pytest.param(n, marks=pytest.mark.xfail(strict=True, reason=KNOWN[(test, n)]))
        if (test, n) in KNOWN
        else pytest.param(n)
        for n in names
    ]


@contextmanager
def _robot() -> Iterator[tuple[SdkSimulator, RobotTaskHarness, Any]]:
    """SDK + RobotTask + enabled robot; returns the EnableRobot block as well."""
    with robot(enable_robot=False) as (sim, h):
        sim.set_move_cycles(MOVE_CYCLES)
        yield sim, h, enable(h, sim)


def _moving(sim: SdkSimulator, h: RobotTaskHarness, name: str) -> Any:
    """Starts ``name`` and waits until it is Active and the robot moves."""
    mv = _motion(name, h)
    before = list(sim.joints)
    start(mv)
    h.run(MOVE_CYCLES, until=lambda: bool(mv.Error) or (bool(mv.Active) and sim.joints != before))
    assert mv.Active and sim.joints != before, outputs(mv)
    return mv


def _held(sim: SdkSimulator, h: RobotTaskHarness, cycles: int = 20) -> bool:
    before = list(sim.joints)
    h.run(cycles)
    return bool(sim.joints == before)


def _group(h: RobotTaskHarness, name: str, **par: Any) -> Any:
    block = h.add(CLASSES_ALL[name](), Execute=True)
    for key, value in par.items():
        setattr(block.ParCmd, key, value)
    h.run(100, until=lambda: bool(block.Done or block.Error))
    assert block.Done and not block.Error, outputs(block)
    return block


# ------------------------------------------------------------------ GroupStop / GroupInterrupt


@pytest.mark.parametrize("name", _params("stop"))
def test_stop_aborts_the_motion(name: str) -> None:
    """GroupStop during the motion: CommandAborted, not Done, the robot stands still."""
    with _robot() as (sim, h, _):
        mv = _moving(sim, h, name)
        _group(h, "MC_GroupStopFB")
        h.run(20, until=lambda: bool(mv.CommandAborted or mv.Done or mv.Error))
        assert mv.CommandAborted and not mv.Done and not mv.Active, outputs(mv)
        assert _held(sim, h)


@pytest.mark.parametrize("name", _params("interrupt"))
def test_interrupt_and_continue(name: str) -> None:
    """GroupInterrupt during the motion: CommandInterrupted, Busy, the robot stands still;
    GroupContinue: the motion ends with Done."""
    with _robot() as (sim, h, _):
        mv = _moving(sim, h, name)
        _group(h, "MC_GroupInterruptFB")
        h.run(5)
        assert mv.CommandInterrupted and mv.Busy and not mv.Active and not mv.Done, outputs(mv)
        assert h.user_data.Interrupted
        assert _held(sim, h)
        _group(h, "MC_GroupContinueFB")
        h.run(4 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done and not mv.Error, outputs(mv)


# ------------------------------------------------------------------ override / power


@pytest.mark.parametrize("name", _params("override"))
def test_override_zero_holds_the_motion(name: str) -> None:
    """Speed override 0 %: the motion becomes Active but the robot does not move; 100 %: Done."""
    with _robot() as (sim, h, _):
        sim.set_override_motion(True)
        _group(h, "MC_ChangeSpeedOverrideFB", Override=0.0)
        mv = _motion(name, h)
        before = list(sim.joints)
        start(mv)
        h.run(100, until=lambda: bool(mv.Active or mv.Error))
        h.run(20)
        assert mv.Active and not (mv.Done or mv.Error), outputs(mv)
        assert sim.joints == before
        _group(h, "MC_ChangeSpeedOverrideFB", Override=100.0)
        h.run(4 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done and not mv.Error, outputs(mv)


@pytest.mark.parametrize("name", _params("disable"))
def test_disable_robot_interrupts_the_motion(name: str) -> None:
    """Power off during the motion: CommandInterrupted with INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED,
    not Active, not Done, the robot stands still."""
    with _robot() as (sim, h, en):
        mv = _moving(sim, h, name)
        en.Enable = False
        h.run(100, until=lambda: bool(mv.CommandInterrupted or mv.Error or mv.Done))
        assert mv.CommandInterrupted and not mv.Active and not mv.Done, outputs(mv)
        assert mv.InfoID == RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED, hex(mv.InfoID)
        assert _held(sim, h)


# ------------------------------------------------------------------ user data


@pytest.mark.parametrize("name", _params("states"))
def test_user_data_follow_the_motion(name: str) -> None:
    """While the motion is Active the RC reports Executing (not Idle); after Done it is Idle again."""
    with _robot() as (sim, h, _):
        mv = _moving(sim, h, name)
        assert h.user_data.Executing and not h.user_data.Idle
        h.run(4 * MOVE_CYCLES, until=lambda: bool(mv.Done or mv.Error))
        assert mv.Done, outputs(mv)
        h.run(5)
        assert h.user_data.Idle and not h.user_data.Executing


# ------------------------------------------------------------------ tool / frame numbers

RANGE_ERRORS = {"ToolNo": "ERR_TOOLNO_RANGE", "FrameNo": "ERR_FRAMENO_RANGE"}


def _numbered() -> list[Any]:
    cases = [(n, f) for n in NAMES for f in ("ToolNo", "FrameNo") if hasattr(CLASSES_ALL[n]().ParCmd, f)]
    return [
        pytest.param(n, f, marks=pytest.mark.xfail(strict=True, reason=KNOWN[("number", n)]))
        if ("number", n) in KNOWN
        else pytest.param(n, f)
        for n, f in cases
    ]


@pytest.mark.parametrize(("name", "field"), _numbered())
def test_tool_or_frame_outside_the_range_is_rejected(name: str, field: str) -> None:
    """Tool / frame number 255 (outside 0..254) is rejected by the block with its range error; the robot does not move."""
    with _robot() as (sim, h, _):
        mv = _motion(name, h)
        setattr(mv.ParCmd, field, 255)
        before = list(sim.joints)
        start(mv)
        h.run(MOVE_CYCLES, until=lambda: bool(mv.Error or mv.Done))
        assert mv.Error and not mv.Done, outputs(mv)
        assert mv.ErrorID == RobotLibraryErrorIdEnum[RANGE_ERRORS[field]], hex(mv.ErrorID)
        assert sim.joints == before
