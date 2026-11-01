# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_userdata_position
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests: client checks of ReadActualPosition, ReadActualPositionCyclic and the
#    RobotTask configuration (UserData).
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

"""Validation tests: client checks of ReadActualPosition, ReadActualPositionCyclic and the
RobotTask configuration (UserData).

The client library rejects invalid parameters before anything is sent to the RC (error IDs of
spec table 7-1), corrects a too small LifeSignTimeOut and detects a change of the optional cyclic
telegram data during operation.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import (
    CmdType,
    ProcessingMode,
    RobotLibraryInfoIdEnum,
    RobotLibraryWarningIdEnum,
    SequenceFlag,
)
from srci.types import (
    RobotLibraryErrorIdEnum as E,
)
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import MOVE_CYCLES, fb, state

PM = ProcessingMode
SF = SequenceFlag
READ = int(CmdType.ReadActualPosition)


@contextmanager
def _unstarted(sdk: SdkSimulator) -> Iterator[RobotTaskHarness]:
    """RobotTask harness before the start-up (configuration can still be changed)."""
    sdk.set_move_cycles(MOVE_CYCLES)
    clock = FakeClock()
    with use_clock(clock):
        yield RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)


def _start(h: RobotTaskHarness) -> None:
    h.run(300, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))


def _position_is_zero(rp: Any) -> bool:
    c, j = rp.OutCmd.ActualCartesianPosition, rp.OutCmd.ActualJointPosition
    values = (c.X, c.Y, c.Z, c.Rx, c.Ry, c.Rz, j.J1, j.J2, j.J3, j.J4, j.J5, j.J6)
    return all(v == 0.0 for v in values) and rp.OutCmd.ToolNoReturn == 0 and rp.OutCmd.FrameNoReturn == 0


# ---------------------------------------------------------------- ReadActualPosition: parameter checks


@pytest.mark.parametrize(
    ("inputs", "error"),
    [
        ({"ToolNo": 99}, E.ERR_TOOLNO_UNAVAILABLE),
        ({"FrameNo": 99}, E.ERR_FRAMENO_UNAVAILABLE),
        ({"ToolNo": 255}, E.ERR_TOOLNO_RANGE),
        ({"FrameNo": 255}, E.ERR_FRAMENO_RANGE),
        ({"ToolNo": 257}, E.ERR_TOOLNO_RANGE),
        ({"FrameNo": 257}, E.ERR_FRAMENO_RANGE),
        ({"ToolNo": -2}, E.ERR_TOOLNO_RANGE),
    ],
    ids=[
        "tool-99-not-on-rc",
        "frame-99-not-on-rc",
        "tool-255",
        "frame-255",
        "tool-257",
        "frame-257",
        "tool-minus2",
    ],
)
def test_read_invalid_tool_or_frame_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, inputs: dict[str, int], error: int
) -> None:
    """ReadActualPosition with a tool / frame number outside -1..254 or above the RC's highest index is rejected.

    The RC reports 19 as highest tool / frame index. Error with the client ErrorID, no Done, nothing
    sent; the position outputs stay 0.
    """
    rp = fb(robot, "MC_ReadActualPositionFB")
    for name, value in inputs.items():
        setattr(rp.ParCmd, name, value)
    rp.Execute = True
    robot.run(10, until=lambda: bool(rp.Error or rp.Done))
    assert rp.Error and rp.ErrorID == error and not rp.Done, state(rp)
    assert sdk.last_command(READ) is None
    assert _position_is_zero(rp)


@pytest.mark.parametrize(
    ("mode", "flag", "listener", "error"),
    [
        (PM.PARALLEL, SF.PRIMARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, SF.SECONDARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.CONTINUOUS, SF.PRIMARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.CONTINUOUS, SF.SECONDARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.BUFFERED, SF.NO_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.ABORTING, SF.NO_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, 3, 0, E.ERR_SEQFLAG_NOT_ALLOWED),
        pytest.param(
            5,
            SF.NO_SEQUENCE,
            0,
            E.ERR_PROCESSINGMODE_NOT_DEFINED,
            marks=pytest.mark.xfail(
                strict=True,
                reason="LIB-BUG F122: MC_ReadActualPositionFB.CheckParameterValid reports a ProcessingMode "
                "inside 0..14 that the spec does not define (4..8) as 16#8603 'not allowed' instead "
                "of 16#8602 'not defined' (table 5-77 / 7-1); only values outside 0..14 give 16#8602.",
            ),
        ),
        (PM.TRIGGER_ONCE, SF.NO_SEQUENCE, 0, E.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
        (PM.TRIGGER_MULTIPLE, SF.NO_SEQUENCE, 0, E.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
    ],
    ids=[
        "parallel-primary",
        "parallel-secondary",
        "continuous-primary",
        "continuous-secondary",
        "buffered-no-sequence",
        "aborting-no-sequence",
        "sequence-flag-3",
        "processing-mode-5",
        "trigger-once-listener-0",
        "trigger-multiple-listener-0",
    ],
)
def test_read_invalid_mode_combination_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, mode: int, flag: int, listener: int, error: int
) -> None:
    """ReadActualPosition with a ProcessingMode / SequenceFlag / ListenerID combination that is not
    allowed is rejected by the client: Error with the ErrorID of table 7-1, nothing sent, position 0."""
    rp = fb(robot, "MC_ReadActualPositionFB")
    rp.ProcessingMode, rp.SequenceFlag = mode, flag
    rp.ParCmd.ListenerID = listener
    rp.Execute = True
    robot.run(10, until=lambda: bool(rp.Error or rp.Done))
    assert rp.Error and rp.ErrorID == error and not rp.Done and not rp.Valid, state(rp)
    assert sdk.last_command(READ) is None
    assert _position_is_zero(rp)


@pytest.mark.parametrize(
    ("field", "error"),
    [("ToolNo", E.ERR_TOOLNO_UNAVAILABLE), ("FrameNo", E.ERR_FRAMENO_UNAVAILABLE)],
    ids=["tool", "frame"],
)
def test_continuous_read_changed_to_invalid_number(robot: RobotTaskHarness, field: str, error: int) -> None:
    """A running continuous read whose ToolNo / FrameNo is changed to 99 (not on the RC) ends with an error.

    The continuous read is Valid first; after the change: Error with the client ErrorID, not Valid.
    """
    rp = fb(robot, "MC_ReadActualPositionFB", ProcessingMode=PM.CONTINUOUS, SequenceFlag=SF.NO_SEQUENCE)
    rp.Execute = True
    robot.run(30, until=lambda: bool(rp.Valid or rp.Error))
    assert rp.Valid and rp.Busy and not rp.Error, state(rp)
    setattr(rp.ParCmd, field, 99)
    robot.run(30, until=lambda: bool(rp.Error))
    assert rp.Error and rp.ErrorID == error and not rp.Valid, state(rp)


# ---------------------------------------------------------------- ReadActualPositionCyclic: online change


@pytest.mark.parametrize(
    ("option", "parameter"),
    [
        ("UseCartesianPositionExt", "ReadCartesianPositionExt"),
        ("UseJointPosition", "ReadJointPosition"),
        ("UseJointPositionExt", "ReadJointPositionExt"),
    ],
    ids=["cartesian-ext", "joint", "joint-ext"],
)
def test_cyclic_data_changed_online_without_restart(sdk: SdkSimulator, option: str, parameter: str) -> None:
    """Optional cyclic data activated after the start-up (no restart): warning, the cyclic read is rejected.

    RobotTask stays initialized with WarningID 16#7003 (telegram number changed during operation);
    ReadActualPositionCyclic for the new data ends with Error ERR_INVALID_PAR_CMD.
    """
    with _unstarted(sdk) as h:
        _start(h)
        assert h.ag.State.CMDsEnabled and not h.rt.Error
        setattr(h.cfg.Rob.OptionalCyclic, option, True)
        h.run(5)
        assert h.rt.WarningID == RobotLibraryWarningIdEnum.WARN_TELEGRAM_NO_CHANGED_DURING_OPERATION
        assert h.rt.Initialized and not h.rt.Error and h.ag.State.CMDsEnabled
        cy = fb(h, "MC_ReadActualPositionCyclicFB")
        setattr(cy.ParCmd, parameter, True)
        cy.Enable = True
        h.run(10, until=lambda: bool(cy.Error or cy.Enabled))
        assert cy.Error and cy.ErrorID == E.ERR_INVALID_PAR_CMD and not cy.Enabled, state(cy)


def test_cyclic_enabled_for_data_not_in_telegram(robot: RobotTaskHarness) -> None:
    """ReadActualPositionCyclic for the Cartesian position without that data in the telegram: Error.

    The start-up was done without optional cyclic data; Enable -> Error ERR_INVALID_PAR_CMD, no
    Reading flag.
    """
    cy = fb(robot, "MC_ReadActualPositionCyclicFB")
    cy.ParCmd.ReadCartesianPosition = True
    cy.ParCmd.ReadJointPosition = True
    cy.Enable = True
    robot.run(10, until=lambda: bool(cy.Error or cy.Enabled))
    assert cy.Error and cy.ErrorID == E.ERR_INVALID_PAR_CMD and not cy.Enabled, state(cy)
    assert not cy.OutCmd.ReadingCartesianPosition and not robot.user_data.ReadingCartesianPosition


# ---------------------------------------------------------------- RobotTask configuration


def test_lifesign_timeout_below_minimum_is_raised_to_10ms(sdk: SdkSimulator) -> None:
    """LifeSignTimeOut 8 ms (< 10 ms) is corrected by the client to 10 ms with an info before it is sent.

    RobotTask InfoID 16#6001; ExchangeConfiguration carries 10; UserData.LifeSignTimeOut = 10.
    """
    with _unstarted(sdk) as h:
        h.cfg.Com.LifeSignTimeOut = 8
        h.run(30, until=lambda: sdk.last_command(int(CmdType.ExchangeConfiguration)) is not None)
        assert h.rt.InfoID == RobotLibraryInfoIdEnum.INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS
        sent = sdk.last_command(int(CmdType.ExchangeConfiguration)) or {}
        assert sent.get("LifeSignTimeOut") == "10"
        assert h.user_data.LifeSignTimeOut == 10


@pytest.mark.parametrize("target", ["log-level", "message-level"])
def test_undefined_log_or_message_level_rejected(sdk: SdkSimulator, target: str) -> None:
    """An undefined LogLevel (RC server log) or MessageLevel (PLC message log) of 30 stops the start-up.

    The client rejects the value (RobotTask Error ERR_INVALID_PAR_CMD) before the command is sent;
    the RobotTask is not initialized and commands stay disabled.
    """
    with _unstarted(sdk) as h:
        if target == "log-level":
            h.rt.LogLevel = 30  # type: ignore[assignment]  # not a Severity value
        else:
            h.cfg.Rob.Parameter.MessageLevel = 30  # type: ignore[assignment]  # not a MessageLevel value
        _start(h)
        assert h.rt.Error and h.rt.ErrorID == E.ERR_INVALID_PAR_CMD, (hex(h.rt.ErrorID), h.history[-3:])
        assert not h.rt.Initialized and not h.ag.State.CMDsEnabled
        cmd = CmdType.ExchangeConfiguration if target == "log-level" else CmdType.ReadMessages
        assert sdk.last_command(int(cmd)) is None
