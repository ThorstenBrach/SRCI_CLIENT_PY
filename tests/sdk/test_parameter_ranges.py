# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_parameter_ranges
#  Author:      Thorsten Brach
#  Date:        2026-10-16
#
#  Description:
#    Ranges of the command parameters against the SRCI SDK: numbers of
#    tools, frames and loads, dynamics rates, override, trajectory mode;
#    values written and read back unchanged.
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

"""Ranges of the command parameters against the SRCI SDK.

Errors of the client (table 7-1) end the command before anything is sent to the RC; values the
client may not judge (e.g. dynamics above 100 %, spec 6.2.14) are sent and the RC decides.
"""

# ruff: noqa: F811  (fixtures imported from test_core_fbs)
from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import CmdType, RobotLibraryErrorIdEnum, TrajectoryMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import (  # noqa: F401 (fixtures)
    enable,
    execute,
    fb,
    move_axes,
    robot,
    sdk_parameters,
    state,
)

E = RobotLibraryErrorIdEnum

# the SDK has 20 tools, frames and loads (index 0..19)
RC_HIGHEST = 19


def sent(sdk: SdkSimulator, since: int) -> int:
    """Number of commands the SDK accepted after log entry ``since``."""
    return sum(1 for log in sdk.logs[since:] if "EMPTY -> BUFFERED" in log.text)


def rejected(h: RobotTaskHarness, sdk: SdkSimulator, block: Any, error: int) -> None:
    """``Execute``: the client rejects the command with ``error`` and sends nothing."""
    since = len(sdk.logs)
    block.Execute = True
    h.run(50, until=lambda: bool(block.Done or block.Error))
    assert block.Error and block.ErrorID == error, (state(block), hex(block.ErrorID))
    assert sent(sdk, since) == 0, "nothing is sent to the RC"
    block.Execute = False
    h.run(2)


# ---------------------------------------------------------------- numbers of tools, frames, loads

NUMBERED = [
    ("MC_ReadToolDataFB", "ToolNo", E.ERR_TOOLNO_RANGE, E.ERR_TOOLNO_UNAVAILABLE),
    ("MC_WriteToolDataFB", "ToolNo", E.ERR_TOOLNO_RANGE, E.ERR_TOOLNO_UNAVAILABLE),
    ("MC_ReadFrameDataFB", "FrameNo", E.ERR_FRAMENO_RANGE, E.ERR_FRAMENO_UNAVAILABLE),
    ("MC_WriteFrameDataFB", "FrameNo", E.ERR_FRAMENO_RANGE, E.ERR_FRAMENO_UNAVAILABLE),
    ("MC_ReadLoadDataFB", "LoadNo", E.ERR_LOADNO_RANGE, E.ERR_LOADNO_UNAVAILABLE),
    ("MC_WriteLoadDataFB", "LoadNo", E.ERR_LOADNO_RANGE, E.ERR_LOADNO_UNAVAILABLE),
]


def numbered(h: RobotTaskHarness, name: str, field: str, number: int) -> Any:
    block = fb(h, name)
    setattr(block.ParCmd, field, number)
    if name == "MC_WriteToolDataFB":
        block.ParCmd.ToolData.LoadNo = 1  # valid tool (the RC rejects load 0)
    return block


@pytest.mark.parametrize("number", [255, -2], ids=["255", "-2"])
@pytest.mark.parametrize(
    ("name", "field", "range_error", "unavailable"), NUMBERED, ids=[n[0] for n in NUMBERED]
)
def test_number_outside_the_range(
    robot: RobotTaskHarness,
    sdk: SdkSimulator,
    name: str,
    field: str,
    range_error: int,
    unavailable: int,
    number: int,
) -> None:
    """A number outside -1..254 is a range error of the client (table 7-1), nothing is sent (ST-FIX F98)."""
    if number < 0 and name.startswith("MC_Write"):
        pytest.skip("the write blocks have a USINT number (no negative values in the PLC library)")
    rejected(robot, sdk, numbered(robot, name, field, number), range_error)


@pytest.mark.parametrize(
    ("name", "field", "range_error", "unavailable"), NUMBERED, ids=[n[0] for n in NUMBERED]
)
def test_number_not_available_on_the_rc(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, field: str, range_error: int, unavailable: int
) -> None:
    """A number within -1..254 above the highest index of the RC is not available on the RC, nothing is sent."""
    rejected(robot, sdk, numbered(robot, name, field, RC_HIGHEST + 1), unavailable)


@pytest.mark.parametrize(
    ("name", "field", "range_error", "unavailable"), NUMBERED, ids=[n[0] for n in NUMBERED]
)
def test_valid_number_after_an_invalid_one(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, field: str, range_error: int, unavailable: int
) -> None:
    """The same instance first with an invalid, then with a valid number: Done, the error is gone."""
    block = numbered(robot, name, field, 255)
    rejected(robot, sdk, block, range_error)
    setattr(block.ParCmd, field, 3)
    execute(robot, block, reset=False)
    assert block.ErrorID == 0 and not block.Error
    if hasattr(block.OutCmd, f"{field}Return"):
        assert getattr(block.OutCmd, f"{field}Return") == 3


def test_tool_number_of_a_motion_outside_the_range(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Motion commands check ToolNo / FrameNo the same way (range before availability, ST-FIX F98)."""
    enable(robot, sdk)
    for number, error in ((255, E.ERR_TOOLNO_RANGE), (RC_HIGHEST + 1, E.ERR_TOOLNO_UNAVAILABLE)):
        mv = move_axes(robot, 5.0)
        mv.ParCmd.ToolNo = number
        rejected(robot, sdk, mv, error)


# ---------------------------------------------------------------- dynamics rates


@pytest.mark.parametrize("rate", ["VelocityRate", "AccelerationRate", "DecelerationRate", "JerkRate"])
def test_negative_rate_of_a_motion_is_the_default(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str
) -> None:
    """Every rate < 0 is the default ("<0%: (default)", e.g. 6.3.2): sent as 16#FFFF (ST-FIX F96)."""
    enable(robot, sdk)
    mv = move_axes(robot, 5.0)
    setattr(mv.ParCmd, rate, -2.5)
    execute(robot, mv, cycles=300)
    received = sdk.last_command(CmdType.MoveAxesAbsolute)
    assert received is not None and int(received[rate]) == 0xFFFF, received


@pytest.mark.parametrize(
    ("rate", "error"),
    [
        ("VelocityRate", E.ERR_VELOCITY_INVALID),
        ("AccelerationRate", E.ERR_ACCELERATION_INVALID),
        ("DecelerationRate", E.ERR_DECELERATION_INVALID),
        ("JerkRate", E.ERR_JERK_INVALID),
    ],
)
def test_rate_of_a_motion_above_100(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, error: int
) -> None:
    """A rate above 100 % of a motion is rejected by the client, nothing is sent."""
    enable(robot, sdk)
    mv = move_axes(robot, 5.0)
    setattr(mv.ParCmd, rate, 100.5)
    rejected(robot, sdk, mv, error)


def default_dynamics(h: RobotTaskHarness, **rates: float) -> Any:
    block = fb(h, "MC_WriteRobotDefaultDynamicsFB")
    values = block.ParCmd.DynamicValues
    values.VelocityRate, values.AccelerationRate, values.DecelerationRate, values.JerkRate = (
        50.0,
        50.0,
        50.0,
        50.0,
    )
    for name, value in rates.items():
        setattr(values, name, value)
    return block


@pytest.mark.parametrize(
    ("rate", "error"),
    [
        ("VelocityRate", E.ERR_VELOCITY_INVALID),
        ("AccelerationRate", E.ERR_ACCELERATION_INVALID),
        ("DecelerationRate", E.ERR_DECELERATION_INVALID),
        ("JerkRate", E.ERR_JERK_INVALID),
    ],
)
def test_default_dynamics_rate_too_large_for_the_telegram(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, error: int
) -> None:
    """A default rate above 655.35 % does not fit into the telegram (UINT * 100): client error (ST-FIX F97)."""
    rejected(robot, sdk, default_dynamics(robot, **{rate: 655.36}), error)


def test_default_dynamics_above_100_is_sent(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Default rates above 100 % are allowed by the spec (6.2.14): the client sends them, the RC decides."""
    block = default_dynamics(robot, VelocityRate=120.0)
    since = len(sdk.logs)
    block.Execute = True
    robot.run(100, until=lambda: bool(block.Done or block.Error))
    assert sent(sdk, since) == 1
    received = sdk.last_command(CmdType.WriteRobotDefaultDynamics)
    assert received is not None and int(received["VelocityRate"]) == 12000, received


def test_default_dynamics_negative_rate_keeps_the_value(robot: RobotTaskHarness) -> None:
    """A negative default rate keeps the current value of the RC (6.2.14), also other values than -1."""
    execute(robot, default_dynamics(robot, VelocityRate=40.0))
    execute(robot, default_dynamics(robot, VelocityRate=-2.0, AccelerationRate=60.0))
    read = fb(robot, "MC_ReadRobotDefaultDynamicsFB")
    execute(robot, read, reset=False)
    assert read.OutCmd.DynamicValues.VelocityRate == pytest.approx(40.0)
    assert read.OutCmd.DynamicValues.AccelerationRate == pytest.approx(60.0)


def test_default_dynamics_written_twice(robot: RobotTaskHarness) -> None:
    """Written twice with different values: the read back shows the values of the second write."""
    execute(
        robot,
        default_dynamics(
            robot, VelocityRate=30.0, AccelerationRate=31.0, DecelerationRate=32.0, JerkRate=33.0
        ),
    )
    execute(
        robot,
        default_dynamics(
            robot, VelocityRate=40.0, AccelerationRate=41.0, DecelerationRate=42.0, JerkRate=43.0
        ),
    )
    read = fb(robot, "MC_ReadRobotDefaultDynamicsFB")
    execute(robot, read, reset=False)
    values = read.OutCmd.DynamicValues
    assert (
        values.VelocityRate,
        values.AccelerationRate,
        values.DecelerationRate,
        values.JerkRate,
    ) == pytest.approx((40.0, 41.0, 42.0, 43.0))


# ---------------------------------------------------------------- override


@pytest.mark.parametrize("override", [-1.0, 100.5, 150.0])
def test_override_outside_the_range(robot: RobotTaskHarness, sdk: SdkSimulator, override: float) -> None:
    """ChangeSpeedOverride outside 0..100 %: 16#8410, nothing is sent, the override of the RC stays."""
    before = sdk.override
    block = fb(robot, "MC_ChangeSpeedOverrideFB")
    block.ParCmd.Override = override
    rejected(robot, sdk, block, E.ERR_OVERRIDE_INVALID)
    assert sdk.override == before


def test_override_zero(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ChangeSpeedOverride 0 % is valid: Done, the override of the RC is 0."""
    block = fb(robot, "MC_ChangeSpeedOverrideFB")
    block.ParCmd.Override = 0.0
    execute(robot, block)
    assert sdk.override == 0.0


# ---------------------------------------------------------------- ReturnToPrimary


def test_return_to_primary_without_trajectory_mode(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """TrajectoryMode 0 (Invalid, the default) is rejected with 16#8409 (6.3.11, ST-FIX F99)."""
    enable(robot, sdk)
    rtp = fb(robot, "MC_ReturnToPrimaryFB")
    rtp.ParCmd.TrajectoryMode = TrajectoryMode.INVALID
    since = len(sdk.logs)
    rtp.Enable = True
    robot.run(50, until=lambda: bool(rtp.Error))
    assert rtp.Error and rtp.ErrorID == E.ERR_TRAJECTORYMODE_INVALID, (state(rtp), hex(rtp.ErrorID))
    assert sent(sdk, since) == 0


# ---------------------------------------------------------------- values written and read back


def test_load_data_round_trip(robot: RobotTaskHarness) -> None:
    """WriteLoadData with every field set to a distinct value: ReadLoadData returns every field unchanged."""
    write = fb(robot, "MC_WriteLoadDataFB")
    write.ParCmd.LoadNo = 4
    data = write.ParCmd.LoadData
    for i, field in enumerate(f for f in data.__slots__ if f not in ("Timestamp",)):
        value = getattr(data, field)
        if isinstance(value, float):
            setattr(data, field, 1.5 + i)
    execute(robot, write)
    read = fb(robot, "MC_ReadLoadDataFB")
    read.ParCmd.LoadNo = 4
    execute(robot, read, reset=False)
    for field in data.__slots__:
        if isinstance(getattr(data, field), float):
            assert getattr(read.OutCmd.LoadData, field) == pytest.approx(getattr(data, field)), field


def test_reference_dynamics_round_trip(robot: RobotTaskHarness) -> None:
    """WriteRobotReferenceDynamics with distinct values: ReadRobotReferenceDynamics returns exactly these."""
    write = fb(robot, "MC_WriteRobotReferenceDynamicsFB")
    values = write.ParCmd.DynamicValues
    values.VelocityReference, values.AccelerationReference = 1234.0, 2345.0
    values.DecelerationReference, values.JerkReference = 3456.0, 4567.0
    execute(robot, write)
    read = fb(robot, "MC_ReadRobotReferenceDynamicsFB")
    execute(robot, read, reset=False)
    out = read.OutCmd.DynamicValues
    assert (
        out.VelocityReference,
        out.AccelerationReference,
        out.DecelerationReference,
        out.JerkReference,
    ) == (pytest.approx((1234.0, 2345.0, 3456.0, 4567.0)))
