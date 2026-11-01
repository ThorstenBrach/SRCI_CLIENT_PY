# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_move_direct_blending
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveDirectAbsolute against the SDK: blending modes and waiting at the blending zone.
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

"""MoveDirectAbsolute against the SDK: blending modes and waiting at the blending zone.

Blending modes (spec 6.3.3.3 BlendingMode / BlendingParameter) are optional: the RC either executes
the command or rejects an unsupported mode with ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED.
With WaitAtBlendingZone (ExchangeConfiguration, set by the RobotTask configuration) a single
blended command without a successor either waits in the blending zone (Active, not Done, InfoID
INFO_WAITING_AT_BLEND_ZONE) or is rejected by the RC; without an effective blending it completes.

The simulated robot does not blend geometrically (exact stop at every target), so the blended path
itself is not checked, only the command flags, the order of the commands and the end position.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import AbortingMode, BlendingMode, RobotLibraryErrorIdEnum, RobotLibraryInfoIdEnum
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, cartesian, enable, fb, finished, order, state, watch

E = RobotLibraryErrorIdEnum
I = RobotLibraryInfoIdEnum  # noqa: E741
NOT_SUPPORTED = E.ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED
B = BlendingMode


@pytest.fixture
def robot_wait(sdk: SdkSimulator) -> Iterator[RobotTaskHarness]:
    """Like ``robot``, but the RobotTask configures WaitAtBlendingZone = TRUE before the start-up."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.cfg.Rob.Parameter.WaitAtBlendingZone = True
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, h.history
        yield h


def _move(
    h: RobotTaskHarness,
    x: float,
    y: float = 0.0,
    mode: int = B.EXACT_STOP,
    par: tuple[float, float] = (0.0, 0.0),
    **inputs: Any,
) -> Any:
    """MoveDirectAbsolute to (x, y, 0) with the given blending mode / parameters, 100 % velocity."""
    mv = fb(h, "MC_MoveDirectAbsoluteFB", **inputs)
    cartesian(mv, x, y, 0.0)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0
    mv.ParCmd.JerkRate = -1.0
    mv.ParCmd.BlendingMode = mode
    mv.ParCmd.BlendingParameter[0], mv.ParCmd.BlendingParameter[1] = par
    return mv


def _run(h: RobotTaskHarness, mv: Any, cycles: int = 4 * MOVE_CYCLES) -> Any:
    mv.Execute = True
    s = watch(h, [mv], cycles, lambda: finished(mv))[0]
    s.final = state(mv)
    return s


def _done_or_not_supported(s: Any, sdk: SdkSimulator, x: float) -> None:
    """The command is executed (Done at ``x``) or rejected as unsupported without motion."""
    if s.final["Done"]:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
        assert sdk.joints[0] == pytest.approx(x)
    else:
        assert s.final["Error"] and s.final["ErrorID"] == NOT_SUPPORTED, (s.flags, s.final)
        assert "Active" not in s.flags and sdk.joints[0] == 0.0, (s.flags, sdk.joints[:2])


# ---------------------------------------------------------------- single command, no waiting


@pytest.mark.parametrize(
    ("mode", "par"),
    [
        (B.EXACT_STOP, (20.0, 0.0)),
        (B.EXACT_STOP, (0.0, 0.0)),
        (B.DEFINED_VELOCITY, (10.0, 0.0)),
        (B.DEFINED_VELOCITY, (50.0, 0.0)),
        (B.CORNER_DISTANCE, (10.0, 0.0)),
        (B.CORNER_DISTANCE, (50.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (10.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (50.0, 0.0)),
        (B.CORNER_DISTANCE_2R, (10.0, 30.0)),
        (B.CORNER_DISTANCE_2R, (50.0, 20.0)),
        (B.RAMP_OVERLAP, (10.0, 30.0)),
        (B.RAMP_OVERLAP, (50.0, 20.0)),
        (B.CORNER_DISTANCE_1R, (10.0, 0.0)),
        (B.CORNER_DISTANCE_1R, (50.0, 20.0)),
    ],
    ids=lambda v: getattr(v, "name", None) or "_".join(f"{p:g}" for p in v),
)
def test_single_blended_command(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: int, par: tuple[float, float]
) -> None:
    """A single MoveDirectAbsolute with a blending mode completes at the target (no successor) or is rejected as unsupported.

    WaitAtBlendingZone is FALSE: the robot moves to the end position.
    """
    enable(robot)
    s = _run(robot, _move(robot, 100.0, mode=mode, par=par))
    _done_or_not_supported(s, sdk, 100.0)


# ---------------------------------------------------------------- single command, WaitAtBlendingZone


@pytest.mark.parametrize(
    ("mode", "par"),
    [
        (B.EXACT_STOP, (20.0, 0.0)),
        (B.CORNER_DISTANCE, (0.0, 0.0)),
        (B.CORNER_DISTANCE, (0.0, 50.0)),
        (B.MAX_CORNER_DEVIATION, (0.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (0.0, 50.0)),
        (B.CORNER_DISTANCE_2R, (0.0, 0.0)),
        (B.CORNER_DISTANCE_2R, (0.0, 30.0)),
        (B.RAMP_OVERLAP, (0.0, 0.0)),
        (B.RAMP_OVERLAP, (0.0, 30.0)),
        (B.CORNER_DISTANCE_1R, (0.0, 0.0)),
        (B.CORNER_DISTANCE_1R, (0.0, 30.0)),
    ],
    ids=lambda v: getattr(v, "name", None) or "_".join(f"{p:g}" for p in v),
)
def test_wait_at_blending_zone_without_blending(
    robot_wait: RobotTaskHarness, sdk: SdkSimulator, mode: int, par: tuple[float, float]
) -> None:
    """With WaitAtBlendingZone a single command without effective blending (exact stop or first parameter 0)
    completes or is rejected as unsupported.

    The second blending parameter is ignored when the first one is 0.
    """
    enable(robot_wait)
    s = _run(robot_wait, _move(robot_wait, 100.0, mode=mode, par=par))
    _done_or_not_supported(s, sdk, 100.0)


_NO_WAIT = (
    "SDK-GAP: the SDK accepts WaitAtBlendingZone (isWaitAtBlendingZoneSupported) but the simulated "
    "robot ignores it: a single blended command completes with Done instead of waiting in the "
    "blending zone with InfoID 16#6C13 (spec 6.3.3.3 BlendingMode, ExchangeConfiguration WaitAtBlendingZone)"
)


@pytest.mark.parametrize(
    ("mode", "par"),
    [
        (B.DEFINED_VELOCITY, (20.0, 0.0)),
        (B.DEFINED_VELOCITY, (20.0, 30.0)),
        (B.DEFINED_VELOCITY, (100.0, 0.0)),
        pytest.param(B.CORNER_DISTANCE, (50.0, 0.0), marks=pytest.mark.xfail(strict=True, reason=_NO_WAIT)),
        pytest.param(
            B.MAX_CORNER_DEVIATION, (30.0, 50.0), marks=pytest.mark.xfail(strict=True, reason=_NO_WAIT)
        ),
        (B.CORNER_DISTANCE_2R, (50.0, 30.0)),
        pytest.param(B.RAMP_OVERLAP, (50.0, 30.0), marks=pytest.mark.xfail(strict=True, reason=_NO_WAIT)),
        (B.CORNER_DISTANCE_1R, (50.0, 30.0)),
    ],
    ids=lambda v: getattr(v, "name", None) or "_".join(f"{p:g}" for p in v),
)
def test_wait_at_blending_zone_single_command(
    robot_wait: RobotTaskHarness, sdk: SdkSimulator, mode: int, par: tuple[float, float]
) -> None:
    """With WaitAtBlendingZone a single blended command waits in the blending zone (Active, not Done, waiting InfoID) or is rejected.

    The robot stops before the target; the command stays Active until a successor or a stop arrives.
    """
    enable(robot_wait)
    mv = _move(robot_wait, 100.0, mode=mode, par=par)
    s = _run(robot_wait, mv)
    if s.final["Error"]:
        assert "Active" not in s.flags and sdk.joints[0] == 0.0, (s.flags, s.final)
        return
    assert order(s, "Busy", "CommandBuffered", "Active"), s.flags
    assert mv.Active and not mv.Done, state(mv)
    assert mv.InfoID == I.INFO_WAITING_AT_BLEND_ZONE, hex(mv.InfoID)
    assert sdk.joints[0] < 100.0


# ---------------------------------------------------------------- two commands


@pytest.mark.parametrize(
    ("mode", "par"),
    [
        (B.DEFINED_VELOCITY, (20.0, 0.0)),
        (B.DEFINED_VELOCITY, (5.0, 0.0)),
        (B.DEFINED_VELOCITY, (80.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (20.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (5.0, 0.0)),
        (B.MAX_CORNER_DEVIATION, (80.0, 0.0)),
        (B.CORNER_DISTANCE, (20.0, 0.0)),
        (B.CORNER_DISTANCE, (5.0, 0.0)),
        (B.CORNER_DISTANCE, (80.0, 0.0)),
        (B.CORNER_DISTANCE_2R, (20.0, 10.0)),
        (B.CORNER_DISTANCE_2R, (5.0, 60.0)),
        (B.RAMP_OVERLAP, (20.0, 10.0)),
        (B.RAMP_OVERLAP, (80.0, 10.0)),
        (B.CORNER_DISTANCE_1R, (20.0, 10.0)),
        (B.CORNER_DISTANCE_1R, (5.0, 60.0)),
    ],
    ids=lambda v: getattr(v, "name", None) or "_".join(f"{p:g}" for p in v),
)
def test_blending_into_a_second_command(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: int, par: tuple[float, float]
) -> None:
    """A blended first command followed by a buffered second command: the second one becomes Active only after
    the first one finished and ends at its target.

    An unsupported blending mode rejects the first command only; the second one still runs.
    """
    enable(robot)
    first = _move(robot, 100.0, mode=mode, par=par)
    second = _move(robot, 100.0, 100.0)
    first.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(first.CommandBuffered or first.Error))
    second.Execute = True
    both_active = False

    def step() -> bool:
        nonlocal both_active
        both_active = both_active or bool(first.Active and second.Active)
        if second.Active:
            assert finished(first), (state(first), state(second))
        return finished(first) and finished(second)

    seen = watch(robot, [first, second], 6 * MOVE_CYCLES, step)
    assert not both_active
    if not first.Done:
        assert first.Error and first.ErrorID == NOT_SUPPORTED, state(first)
    else:
        assert order(seen[0], "Busy", "CommandBuffered", "Active", "Done"), seen[0].flags
    assert order(seen[1], "Busy", "CommandBuffered", "Active", "Done"), seen[1].flags
    assert sdk.joints[:2] == pytest.approx([100.0, 100.0])


@pytest.mark.parametrize(
    "mode", [B.CORNER_DISTANCE, B.MAX_CORNER_DEVIATION, B.RAMP_OVERLAP], ids=lambda m: m.name
)
def test_blended_command_aborted_by_second(robot: RobotTaskHarness, sdk: SdkSimulator, mode: int) -> None:
    """A blended active command is aborted by a second command with AbortingMode ABORT, which then finishes at its target."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    first = _move(robot, 300.0, mode=mode, par=(20.0, 0.0))
    second = _move(robot, 100.0, 100.0, AbortingMode=AbortingMode.ABORT)
    first.Execute = True
    robot.run(MOVE_CYCLES, until=lambda: bool(first.Active or first.Error))
    assert first.Active, state(first)
    second.Execute = True
    seen = watch(robot, [first, second], 6 * MOVE_CYCLES, lambda: finished(first) and finished(second))
    assert order(seen[0], "Busy", "CommandBuffered", "Active", "CommandAborted"), seen[0].flags
    assert order(seen[1], "Busy", "CommandBuffered", "Active", "Done"), seen[1].flags
    assert sdk.joints[:2] == pytest.approx([100.0, 100.0])


def test_ten_short_blended_moves(robot_wait: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Ten short commands with corner-distance blending, each started when the previous is buffered, run in order and all end with Done.

    With WaitAtBlendingZone an RC that supports waiting may report the waiting InfoID on the last
    command instead of Done; then it stays Active.
    """
    h = robot_wait
    enable(h)
    moves = [_move(h, 20.0 * (i + 1), mode=B.CORNER_DISTANCE, par=(10.0, 0.0)) for i in range(10)]
    moves[0].Execute = True
    active_order: list[int] = []
    for _ in range(30 * MOVE_CYCLES):
        h.cycle()
        for i, mv in enumerate(moves):
            if mv.CommandBuffered and i + 1 < len(moves):
                moves[i + 1].Execute = True
            if mv.Active and i not in active_order:
                active_order.append(i)
            assert not mv.Error, state(mv)
        if all(finished(m) for m in moves[:-1]) and (finished(moves[-1]) or moves[-1].InfoID):
            break
    assert active_order == list(range(10)), active_order
    assert all(m.Done for m in moves[:-1]), [state(m) for m in moves]
    last = moves[-1]
    assert last.Done or (last.Active and last.InfoID == I.INFO_WAITING_AT_BLEND_ZONE), state(last)
    if last.Done:
        assert sdk.joints[0] == pytest.approx(200.0)
