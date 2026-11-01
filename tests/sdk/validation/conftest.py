# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.conftest
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Fixtures and helpers of the validation tests.
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

"""Fixtures and helpers of the validation tests.

Every test starts with an initialized RobotTask (``robot``), the function blocks are called in
every cycle before the RobotTask like in a PLC program. The simulated robot of the SDK harness
moves linearly within ``MOVE_CYCLES`` cycles and uses an identity kinematics (X..Rz = J1..J6).

Typical test::

    def test_move_reaches_target(robot, sdk):
        enable(robot)
        mv = move_axes(robot, 10.0)
        seen = execute(robot, mv)
        assert order(seen, "Busy", "CommandBuffered", "Active", "Done")
        assert sdk.joints[0] == pytest.approx(10.0)
"""

from __future__ import annotations

import copy
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.types.iec import new_instance
from tests.robot_task_harness import SIZE, RobotTaskHarness

MOVE_CYCLES = 50
FLAGS = (
    "Busy",
    "CommandBuffered",
    "Active",
    "Done",
    "Enabled",
    "Valid",
    "Error",
    "CommandAborted",
    "CommandInterrupted",
    "ParameterAccepted",
)


@pytest.fixture(autouse=True)
def sdk_parameters() -> Iterator[None]:
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.fixture
def robot(sdk: SdkSimulator) -> Iterator[RobotTaskHarness]:
    """Initialized RobotTask, commands enabled (FakeClock: deterministic, no real time)."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        assert h.ag.State.CMDsEnabled and not h.rt.Error, h.history
        yield h


class Seen:
    """State flags a block showed, in the order of their first appearance (cycle by cycle)."""

    def __init__(self, block: Any) -> None:
        self.block = block
        self.flags: list[str] = []
        self.cycles = 0
        self.final: dict[str, Any] = {}

    def record(self) -> None:
        self.cycles += 1
        for f in FLAGS:
            if getattr(self.block, f, False) and f not in self.flags:
                self.flags.append(f)


def fb(h: RobotTaskHarness, name: str, **inputs: Any) -> Any:
    """Create the function block ``name`` (e.g. ``"MC_GroupResetFB"``) and add it to the program."""
    return h.add(new_instance(name), **inputs)


def state(block: Any) -> dict[str, Any]:
    return {n: getattr(block, n) for n in (*FLAGS, "ErrorID") if hasattr(block, n)}


def finished(block: Any) -> bool:
    return bool(block.Done or block.Error or getattr(block, "CommandAborted", False))


def watch(h: RobotTaskHarness, blocks: list[Any], cycles: int, until: Callable[[], bool]) -> list[Seen]:
    """Run until ``until()`` (max ``cycles``) and record the flags of ``blocks`` every cycle."""
    seen = [Seen(b) for b in blocks]

    def step() -> bool:
        for s in seen:
            s.record()
        return bool(until())

    h.run(cycles, until=step)
    return seen


def execute(h: RobotTaskHarness, block: Any, cycles: int = 500, reset: bool = True) -> Seen:
    """Rising edge on Execute, run until Done / Error / CommandAborted; returns the flags seen.
    ``Seen.final`` holds the outputs before Execute is reset. Does not assert the outcome."""
    block.Execute = True
    s = watch(h, [block], cycles, lambda: finished(block))[0]
    s.final = state(block)
    if reset:
        block.Execute = False
        h.run(2)
    return s


def start(h: RobotTaskHarness, name: str, **inputs: Any) -> Any:
    """Add a block and set Execute (it runs while the test does something else)."""
    b = fb(h, name, **inputs)
    b.Execute = True
    return b


def order(seen: Seen, *flags: str) -> bool:
    """The flags appeared in this order (other flags in between are allowed)."""
    got = [f for f in seen.flags if f in flags]
    return got == list(flags)


def enable(h: RobotTaskHarness) -> Any:
    """GroupReset + EnableRobot; returns the EnableRobot block (stays enabled)."""
    r = fb(h, "MC_GroupResetFB")
    execute(h, r)
    en = fb(h, "MC_EnableRobotFB", Enable=True)
    h.run(200, until=lambda: bool(en.Enabled or en.Error))
    assert en.Enabled and not en.Error, state(en)
    return en


def move_axes(
    h: RobotTaskHarness,
    j1: float,
    j2: float = 0.0,
    j3: float = 0.0,
    j4: float = 0.0,
    j5: float = 0.0,
    j6: float = 0.0,
    **inputs: Any,
) -> Any:
    """MoveAxesAbsolute to J1..J6 with 100 % dynamics (DecelerationRate / JerkRate not set)."""
    mv = fb(h, "MC_MoveAxesAbsoluteFB", **inputs)
    for i, v in enumerate((j1, j2, j3, j4, j5, j6), start=1):
        setattr(mv.ParCmd.JointPosition, f"J{i}", v)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0
    mv.ParCmd.JerkRate = -1.0
    return mv


def cartesian(
    block: Any, x: float, y: float, z: float, rx: float = 0.0, ry: float = 0.0, rz: float = 0.0
) -> Any:
    """Set ParCmd.Position of a Cartesian motion (MoveLinear / MoveDirect)."""
    p = block.ParCmd.Position
    p.X, p.Y, p.Z, p.Rx, p.Ry, p.Rz = x, y, z, rx, ry, rz
    return block


def read_position(h: RobotTaskHarness, tool_no: int = 0, frame_no: int = 0) -> Any:
    """ReadActualPosition; returns OutCmd."""
    rd = fb(h, "MC_ReadActualPositionFB")
    rd.ParCmd.ToolNo, rd.ParCmd.FrameNo = tool_no, frame_no
    s = execute(h, rd, reset=False)
    assert s.final["Done"] and not s.final["Error"], s.final
    out = copy.deepcopy(rd.OutCmd)
    rd.Execute = False
    h.run(2)
    return out
