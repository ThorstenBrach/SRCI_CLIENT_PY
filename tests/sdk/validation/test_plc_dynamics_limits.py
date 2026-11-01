# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_dynamics_limits
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of the client library: parameter checks, flags and
#    outputs of the dynamics and software limit blocks.
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

"""Validation tests of the client library: default / reference dynamics and software limit blocks.

Behaviour of the function blocks themselves (spec 5.5.3 / 5.5.10, 6.2.9 .. 6.2.16): rates that do
not fit into the telegram are rejected before anything is sent, the blocks refuse to work on an
axes group whose RobotTask is not initialized, Done of a short Execute pulse is shown for exactly
one cycle, and a new execution clears the outputs of the previous one.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import CmdType
from srci.types import RobotLibraryErrorIdEnum as E
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, execute, fb, state

RATES = ("VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate")
BASE_RATES = (20.0, 30.0, 40.0, 50.0)
CMD_TYPES = {
    "MC_WriteRobotDefaultDynamicsFB": CmdType.WriteRobotDefaultDynamics,
    "MC_ReadRobotDefaultDynamicsFB": CmdType.ReadRobotDefaultDynamics,
    "MC_WriteRobotReferenceDynamicsFB": CmdType.WriteRobotReferenceDynamics,
    "MC_ReadRobotReferenceDynamicsFB": CmdType.ReadRobotReferenceDynamics,
    "MC_WriteRobotSWLimitsFB": CmdType.WriteRobotSWLimits,
    "MC_ReadRobotSWLimitsFB": CmdType.ReadRobotSWLimits,
}
# output structure with the values of the RC (the SW limit write block only reports RestartRequested)
VALUE_OUTPUTS = {
    "MC_WriteRobotDefaultDynamicsFB": ("DefaultDynamicValues", "VelocityRate"),
    "MC_ReadRobotDefaultDynamicsFB": ("DynamicValues", "VelocityRate"),
    "MC_WriteRobotReferenceDynamicsFB": ("ReferenceDynamicValues", "VelocityReference"),
    "MC_ReadRobotReferenceDynamicsFB": ("DynamicValues", "VelocityReference"),
    "MC_ReadRobotSWLimitsFB": ("LimitValues", "J1UpperLimit"),
}


# ---------------------------------------------------------------- helpers


def _sent(sdk: SdkSimulator, cmd_type: int, since: int) -> int:
    """Commands of ``cmd_type`` the RC accepted since log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({int(cmd_type)}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _valid_block(h: RobotTaskHarness, name: str) -> Any:
    block = fb(h, name)
    if name == "MC_WriteRobotDefaultDynamicsFB":
        for rate, value in zip(RATES, (10.0, -1.0, -1.0, -1.0), strict=True):
            setattr(block.ParCmd.DynamicValues, rate, value)
    elif name == "MC_WriteRobotReferenceDynamicsFB":
        values = block.ParCmd.DynamicValues
        values.VelocityReference, values.AccelerationReference = 1500.0, -1.0
        values.DecelerationReference, values.JerkReference = -1.0, -1.0
    elif name == "MC_WriteRobotSWLimitsFB":
        for j in range(1, 7):
            setattr(block.ParCmd.LimitValues, f"J{j}LowerLimit", -150.0)
            setattr(block.ParCmd.LimitValues, f"J{j}UpperLimit", 150.0)
    return block


def _read_rates(h: RobotTaskHarness) -> tuple[float, ...]:
    rd = fb(h, "MC_ReadRobotDefaultDynamicsFB")
    _ = execute(h, rd, reset=False)
    assert rd.Done and not rd.Error, state(rd)
    values = tuple(getattr(rd.OutCmd.DynamicValues, n) for n in RATES)
    rd.Execute = False
    h.run(2)
    return values


@contextmanager
def _uninitialized() -> Iterator[tuple[SdkSimulator, RobotTaskHarness]]:
    """SDK + RobotTask that is never enabled: the axes group is not initialized (CMDsEnabled FALSE)."""
    clock = FakeClock()
    with SdkSimulator(10) as sdk, use_clock(clock):
        sdk.set_move_cycles(MOVE_CYCLES)
        h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
        h.enable = False
        yield sdk, h


# ---------------------------------------------------------------- parameter checks of the client


@pytest.mark.parametrize(
    ("rates", "error"),
    [
        ((655.36, -1.0, -1.0, -1.0), E.ERR_VELOCITY_INVALID),
        ((-1.0, 655.36, -1.0, -1.0), E.ERR_ACCELERATION_INVALID),
        ((-1.0, -1.0, 655.36, -1.0), E.ERR_DECELERATION_INVALID),
        ((-1.0, -1.0, -1.0, 655.36), E.ERR_JERK_INVALID),
        ((1000.0, 1000.0, 1000.0, -1.0), E.ERR_VELOCITY_INVALID),
        ((3000.0, -1.0, -1.0, -1.0), E.ERR_VELOCITY_INVALID),
    ],
    ids=[
        "velocity-655.36",
        "acceleration-655.36",
        "deceleration-655.36",
        "jerk-655.36",
        "three-rates-1000",
        "velocity-3000",
    ],
)
def test_default_rate_too_large_for_the_telegram_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, rates: tuple[float, ...], error: int
) -> None:
    """A default rate above 655.35 % (does not fit into the UINT * 100 of the telegram) is rejected by the block.

    Error with ErrorID 16#8401..16#8404 of the first invalid rate, Busy is never set, nothing is
    sent; ReadRobotDefaultDynamics afterwards returns the rates written before (20/30/40/50 %)."""
    base = _valid_block(robot, "MC_WriteRobotDefaultDynamicsFB")
    for rate, value in zip(RATES, BASE_RATES, strict=True):
        setattr(base.ParCmd.DynamicValues, rate, value)
    _ = execute(robot, base)
    write = fb(robot, "MC_WriteRobotDefaultDynamicsFB")
    for rate, value in zip(RATES, rates, strict=True):
        setattr(write.ParCmd.DynamicValues, rate, value)
    since = len(sdk.logs)
    seen = execute(robot, write, reset=False)
    assert seen.final["Error"] and write.ErrorID == error, (seen.flags, hex(write.ErrorID))
    assert "Busy" not in seen.flags and "Done" not in seen.flags, seen.flags
    assert _sent(sdk, CmdType.WriteRobotDefaultDynamics, since) == 0
    write.Execute = False
    robot.run(2)
    assert not write.Error and write.ErrorID == 0
    assert _read_rates(robot) == pytest.approx(BASE_RATES)


# ---------------------------------------------------------------- axes group not initialized


@pytest.mark.parametrize("name", list(CMD_TYPES))
def test_rejected_on_an_axes_group_that_is_not_initialized(name: str) -> None:
    """On an axes group whose RobotTask is not initialized the block ends with Error 16#8612 and sends nothing.

    16#8612: commands are not enabled (the robot must be initialized first)."""
    with _uninitialized() as (sdk, h):
        block = _valid_block(h, name)
        seen = execute(h, block, cycles=100, reset=False)
        assert seen.final["Error"] and block.ErrorID == E.ERR_COMMANDS_NOT_ENABLED, (
            seen.flags,
            hex(block.ErrorID),
        )
        assert "Done" not in seen.flags
        assert _sent(sdk, CMD_TYPES[name], 0) == 0


# ---------------------------------------------------------------- flags and outputs


@pytest.mark.parametrize("name", list(CMD_TYPES))
def test_done_of_a_short_execute_pulse_for_one_cycle(robot: RobotTaskHarness, name: str) -> None:
    """Execute reset while Busy: the command completes, Done is TRUE for exactly one cycle, with valid outputs in that cycle.

    Flags: Busy, then Done (one cycle), then all flags FALSE."""
    block = _valid_block(robot, name)
    block.Execute = True
    robot.run(50, until=lambda: bool(block.Busy or block.Error))
    assert block.Busy, state(block)
    block.Execute = False
    done_cycles, values = 0, []
    for _ in range(60):
        robot.run(1)
        assert not block.Error, state(block)
        if block.Done:
            done_cycles += 1
            if name in VALUE_OUTPUTS:
                struct, field = VALUE_OUTPUTS[name]
                values.append(getattr(getattr(block.OutCmd, struct), field))
    assert done_cycles == 1
    assert not any(v for k, v in state(block).items() if k != "ErrorID")
    assert all(v != 0.0 for v in values), values


@pytest.mark.parametrize("name", list(VALUE_OUTPUTS))
def test_new_execution_clears_the_previous_outputs(robot: RobotTaskHarness, name: str) -> None:
    """The outputs of a finished command stay after Execute falls and are cleared by the next rising edge of Execute.

    Until the RC answers the new command the value outputs are 0; after Done they show the values again."""
    block = _valid_block(robot, name)
    struct, field = VALUE_OUTPUTS[name]
    _ = execute(robot, block, reset=False)
    assert block.Done, state(block)
    first = getattr(getattr(block.OutCmd, struct), field)
    assert first != 0.0
    block.Execute = False
    robot.run(3)
    assert not block.Done and getattr(getattr(block.OutCmd, struct), field) == first
    block.Execute = True
    robot.run(1)
    assert block.Busy and not block.Done, state(block)
    assert getattr(getattr(block.OutCmd, struct), field) == 0.0
    robot.run(50, until=lambda: bool(block.Done or block.Error))
    assert block.Done and getattr(getattr(block.OutCmd, struct), field) == first, state(block)
