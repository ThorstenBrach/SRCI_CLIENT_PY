# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_sdk_modified_spline
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Scenario tests of the spline commands added to the SRCI SDK ("modified SDK by Thorsten", group SPLINE).
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

"""Scenario tests of the spline commands the SDK answers itself (modified SDK by Thorsten, group SPLINE).

MoveSpline needs a spline data set created with CreateSpline before (one point per command, ST-FIX
F33); the SDK stores the points per SplineID until DeleteSpline (spec 5.5.13, 6.5.29 - 6.5.32).
test_sdk_modified.py cannot test MoveSpline (one command per run), these tests run the sequence.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

import srci
from srci.iec.clock import FakeClock, use_clock
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.test_core_fbs import enable, fb, state

CREATE, DELETE, DYNAMIC, MOVE = 2600, 2601, 2602, 2603
NOT_POSSIBLE = 0x8F36  # spline data set does not exist (no code in the spec)


@pytest.fixture(autouse=True)
def sdk_parameters() -> Iterator[None]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.fixture
def robot(sdk: SdkSimulator) -> Iterator[RobotTaskHarness]:
    if not sdk.answered_by_sdk(MOVE):
        pytest.skip(
            "MoveSpline not implemented by this SDK (group SPLINE of the modified SDK by Thorsten not applied)"
        )
    sdk.set_move_cycles(10)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        enable(h, sdk)
        yield h


POINTS = ((10.0, 20.0, 30.0), (40.0, 50.0, 60.0), (70.0, 80.0, 90.0))


def _points(parcmd: Any, points: tuple[tuple[float, float, float], ...]) -> None:
    for i, (x, y, z) in enumerate(points, start=1):
        point = parcmd.SplineData[i]
        point.Position.X, point.Position.Y, point.Position.Z = x, y, z
        point.VelocityRate = 50.0
        point.AccelerationRate = 50.0
        point.DecelerationRate = -1.0
        point.JerkRate = -1.0


def _execute(h: RobotTaskHarness, block: Any, cycles: int = 400) -> Any:
    block.Execute = True
    h.run(cycles, until=lambda: bool(block.Done or block.Error or block.WarningID))
    return block


def create(
    h: RobotTaskHarness, spline_id: int, points: tuple[tuple[float, float, float], ...] = POINTS
) -> Any:
    cs = fb(h, "MC_CreateSplineFB")
    cs.ParCmd.SplineID = spline_id
    _points(cs.ParCmd, points)
    _execute(h, cs)
    assert cs.Done and not cs.Error, (state(cs), hex(cs.ErrorID))
    return cs


def move(h: RobotTaskHarness, spline_id: int) -> Any:
    mv = fb(h, "MC_MoveSplineFB")
    mv.ParCmd.SplineID = spline_id
    return _execute(h, mv)


def _rejected(block: Any, code: int) -> bool:
    # a non-motion command of the sequence: the SDK reports an execution error as warning and
    # interrupts the sequence (02_CmdManagement); MoveSpline is outside the motion type range
    return not block.Done and (block.ErrorID == code or block.WarningID == code)


def test_create_spline_one_point_per_command(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """CreateSpline: every point is one command, the firmware checks each point."""
    create(robot, 3)
    last = sdk.firmware_command(CREATE)
    assert last is not None
    assert last["SplineID"] == "3"
    assert float(last["SplineData.X"]) == POINTS[-1][0]


def test_move_spline_done(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """MoveSpline of a created spline: one motion through the planner of the SDK, Done with Progress 100 %."""
    create(robot, 4)
    mv = move(robot, 4)
    assert mv.Done and not mv.Error, (state(mv), hex(mv.ErrorID))
    assert mv.OutCmd.Progress == pytest.approx(100.0)
    fw = sdk.firmware_command(MOVE)
    assert fw is not None and fw["SplineID"] == "4"
    # simulated identity kinematics: the robot stands in the last point of the spline
    assert sdk.joints[:3] == pytest.approx(list(POINTS[-1]))


def test_move_spline_without_spline_rejected(robot: RobotTaskHarness) -> None:
    """MoveSpline without CreateSpline: the RC rejects the command (spec 6.5.31.4 (1))."""
    mv = move(robot, 9)
    assert _rejected(mv, NOT_POSSIBLE), (state(mv), hex(mv.ErrorID), hex(mv.WarningID))


def test_delete_spline(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """DeleteSpline: the spline data set is no longer available for MoveSpline (spec 6.5.31.4 (7))."""
    create(robot, 5)
    ds = fb(robot, "MC_DeleteSplineFB")
    ds.ParCmd.SplineID = 5
    _execute(robot, ds)
    assert ds.Done and not ds.Error, (state(ds), hex(ds.ErrorID))
    assert sdk.firmware_command(DELETE) == {"SplineID": "5"}
    mv = move(robot, 5)
    assert _rejected(mv, NOT_POSSIBLE), (state(mv), hex(mv.ErrorID), hex(mv.WarningID))


def test_delete_all_splines(robot: RobotTaskHarness) -> None:
    """DeleteSpline -1 deletes all spline data sets."""
    create(robot, 1)
    create(robot, 2)
    ds = fb(robot, "MC_DeleteSplineFB")
    ds.ParCmd.SplineID = -1
    _execute(robot, ds)
    assert ds.Done and not ds.Error, (state(ds), hex(ds.ErrorID))
    # one MoveSpline: the rejected command interrupts the sequence, a second one would wait behind it
    mv = move(robot, 2)
    assert _rejected(mv, NOT_POSSIBLE), (state(mv), hex(mv.ErrorID), hex(mv.WarningID))


def test_dynamic_spline_trajectory(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """DynamicSpline: points one by one, the end marker ends the trajectory -> TrajectoryCompleted."""
    dyn = fb(robot, "MC_DynamicSplineFB")
    dyn.ParCmd.StartPosition = 2
    _points(dyn.ParCmd, POINTS)
    dyn.Enable = True
    robot.run(600, until=lambda: bool(dyn.OutCmd.TrajectoryCompleted or dyn.Error))
    assert dyn.Enabled and not dyn.Error, (state(dyn), hex(dyn.ErrorID))
    assert dyn.OutCmd.TrajectoryCompleted
    assert dyn.OutCmd.Buffered == len(POINTS) and dyn.OutCmd.Calculated == len(POINTS)
    assert sdk.joints[:3] == pytest.approx(list(POINTS[-1]))
    dyn.Enable = False
    robot.run(50, until=lambda: not dyn.Busy)
    assert not dyn.Error, (state(dyn), hex(dyn.ErrorID))
