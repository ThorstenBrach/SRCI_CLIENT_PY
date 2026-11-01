# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_subprogram_log
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of CallSubprogram / StopSubprogram / CreateServerLog / ReadServerLog:
#    parameter checks of the client library.
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

"""Validation tests of the subprogram and server log blocks: parameter checks of the client library.

An invalid combination of ProcessingMode / SequenceFlag / ListenerID / StopMode / ExportMode is
rejected by the function block itself with the ErrorID of table 7-1: Error in the first cycle,
no Busy / Done, and nothing is sent to the RC.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import fb, state

CMD_TYPE = {
    "MC_CallSubprogramFB": 7001,
    "MC_StopSubprogramFB": 7008,
    "MC_CreateServerLogFB": 9003,
    "MC_ReadServerLogFB": 9004,
}
E = RobotLibraryErrorIdEnum
PM = ProcessingMode
SF = SequenceFlag

_BUG_LISTENER = pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F119: MC_CreateServerLogFB.CheckParameterValid tests 'ListenerID > 0 only with a trigger "
    "based ProcessingMode' as (~ProcessingMode & 255) >= TRIGGER_BUFFERED, i.e. a bitwise NOT; it is TRUE "
    "for every mode, so each trigger mode with ListenerID > 0 is rejected with 16#8605 (table 7-1, 5.5.12.4: "
    "trigger based ProcessingModes need a ListenerID > 0). MC_CallSubprogramFB uses the correct boolean NOT",
)


def _rejected(
    h: RobotTaskHarness, sdk: SdkSimulator, name: str, inputs: dict[str, Any], par: dict[str, Any], error: int
) -> None:
    """Execute ``name`` with the inputs / ParCmd values; assert the client error and that nothing was sent."""
    block = fb(h, name, **inputs)
    for key, value in par.items():
        setattr(block.ParCmd, key, value)
    block.Execute = True
    h.run(1)
    first = state(block)
    h.run(10)
    assert first["Error"] and first["ErrorID"] == error, (first, hex(block.ErrorID))
    assert not block.Busy and not block.Done and block.Error and block.ErrorID == error, state(block)
    assert sdk.last_command(CMD_TYPE[name]) is None
    block.Execute = False
    h.run(2)
    assert not block.Error and block.ErrorID == 0, state(block)


@pytest.mark.parametrize(
    ("pm", "sf", "listener", "error"),
    [
        (PM.BUFFERED, SF.NO_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, SF.PRIMARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, SF.SECONDARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.CONTINUOUS, SF.PRIMARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.CONTINUOUS, SF.SECONDARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.BUFFERED, 12, 0, E.ERR_SEQFLAG_NOT_ALLOWED),
        (22, SF.PRIMARY_SEQUENCE, 0, E.ERR_PROCESSINGMODE_NOT_DEFINED),
        (4, SF.PRIMARY_SEQUENCE, 0, E.ERR_PROCESSINGMODE_NOT_ALLOWED),
        (5, SF.PRIMARY_SEQUENCE, 0, E.ERR_PROCESSINGMODE_NOT_ALLOWED),
        (PM.TRIGGER_CONTINUOUS, SF.NO_SEQUENCE, 0, E.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
    ],
    ids=[
        "buffered-no-sequence",
        "parallel-primary",
        "parallel-secondary",
        "continuous-primary",
        "continuous-secondary",
        "sequence-flag-12",
        "processing-mode-22",
        "processing-mode-4",
        "processing-mode-5",
        "trigger-continuous-listener-0",
    ],
)
def test_call_subprogram_invalid_parameters(
    robot: RobotTaskHarness, sdk: SdkSimulator, pm: int, sf: int, listener: int, error: int
) -> None:
    """CallSubprogram with an invalid ProcessingMode / SequenceFlag / ListenerID combination is rejected by the client."""
    _rejected(
        robot,
        sdk,
        "MC_CallSubprogramFB",
        {"ProcessingMode": pm, "SequenceFlag": sf},
        {"JobID": 1, "ListenerID": listener},
        error,
    )


@pytest.mark.parametrize(
    ("inputs", "par", "error"),
    [
        ({"ProcessingMode": 99}, {}, E.ERR_PROCESSINGMODE_NOT_DEFINED),
        ({}, {"StopMode": 7}, E.ERR_INVALID_PAR_CMD),
        ({"SequenceFlag": 7}, {}, E.ERR_SEQFLAG_NOT_ALLOWED),
    ],
    ids=["processing-mode-99", "stop-mode-7", "sequence-flag-7"],
)
def test_stop_subprogram_invalid_parameters(
    robot: RobotTaskHarness, sdk: SdkSimulator, inputs: dict[str, Any], par: dict[str, Any], error: int
) -> None:
    """StopSubprogram with an undefined ProcessingMode, StopMode or SequenceFlag is rejected by the client."""
    _rejected(robot, sdk, "MC_StopSubprogramFB", inputs, {"TargetID": 1, **par}, error)


@pytest.mark.parametrize(
    ("pm", "sf", "listener", "error"),
    [
        (PM.CONTINUOUS, SF.PRIMARY_SEQUENCE, 0, E.ERR_PROCESSINGMODE_NOT_ALLOWED),
        (PM.BUFFERED, 3, 0, E.ERR_SEQFLAG_NOT_ALLOWED),
        (PM.BUFFERED, SF.PRIMARY_SEQUENCE, -1, E.ERR_LISTENERID_MUST_BE_POSITIVE),
        (PM.BUFFERED, SF.NO_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, SF.PRIMARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.PARALLEL, SF.SECONDARY_SEQUENCE, 0, E.ERR_SEQFLAG_INVALID_IN_PROC_MODE),
        (PM.TRIGGER_ONCE, SF.NO_SEQUENCE, 0, E.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
        (PM.TRIGGER_MULTIPLE, SF.NO_SEQUENCE, 0, E.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO),
    ],
    ids=[
        "continuous",
        "sequence-flag-3",
        "listener-negative",
        "buffered-no-sequence",
        "parallel-primary",
        "parallel-secondary",
        "trigger-once-listener-0",
        "trigger-multiple-listener-0",
    ],
)
def test_create_server_log_invalid_parameters(
    robot: RobotTaskHarness, sdk: SdkSimulator, pm: int, sf: int, listener: int, error: int
) -> None:
    """CreateServerLog with an invalid ProcessingMode / SequenceFlag / ListenerID combination is rejected by the client."""
    _rejected(
        robot,
        sdk,
        "MC_CreateServerLogFB",
        {"ProcessingMode": pm, "SequenceFlag": sf},
        {"ListenerID": listener},
        error,
    )


@_BUG_LISTENER
@pytest.mark.parametrize(
    ("pm", "sf"),
    [
        (PM.TRIGGER_ONCE, SF.PRIMARY_SEQUENCE),
        (PM.TRIGGER_ONCE, SF.SECONDARY_SEQUENCE),
        (PM.TRIGGER_MULTIPLE, SF.PRIMARY_SEQUENCE),
        (PM.TRIGGER_MULTIPLE, SF.SECONDARY_SEQUENCE),
    ],
    ids=[
        "trigger-once-primary",
        "trigger-once-secondary",
        "trigger-multiple-primary",
        "trigger-multiple-secondary",
    ],
)
def test_create_server_log_trigger_mode_with_sequence_flag(
    robot: RobotTaskHarness, sdk: SdkSimulator, pm: int, sf: int
) -> None:
    """CreateServerLog in a parallel trigger mode with ListenerID > 0 and a SequenceFlag is rejected with
    ERR_SEQFLAG_INVALID_IN_PROC_MODE.
    """
    _rejected(
        robot,
        sdk,
        "MC_CreateServerLogFB",
        {"ProcessingMode": pm, "SequenceFlag": sf},
        {"ListenerID": 5},
        E.ERR_SEQFLAG_INVALID_IN_PROC_MODE,
    )


@_BUG_LISTENER
@pytest.mark.parametrize(
    "pm", [PM.TRIGGER_ONCE, PM.TRIGGER_MULTIPLE], ids=["trigger-once", "trigger-multiple"]
)
def test_create_server_log_trigger_mode_with_listener_is_sent(
    robot: RobotTaskHarness, sdk: SdkSimulator, pm: int
) -> None:
    """CreateServerLog in a trigger mode with ListenerID > 0 passes the client checks and is sent with that ListenerID."""
    cl = fb(robot, "MC_CreateServerLogFB", ProcessingMode=pm, SequenceFlag=SF.NO_SEQUENCE)
    cl.ParCmd.ListenerID = 10
    cl.Execute = True
    robot.run(3)
    assert cl.ErrorID != E.ERR_LISTENERID_NOT_ALLOWED, state(cl)
    sent = sdk.last_command(CMD_TYPE["MC_CreateServerLogFB"])
    assert sent is not None and sent["ListenerID"] == "10", sent


@pytest.mark.parametrize("export_mode", [2, 3, 255])
def test_read_server_log_undefined_export_mode(
    robot: RobotTaskHarness, sdk: SdkSimulator, export_mode: int
) -> None:
    """ReadServerLog with an undefined ExportMode is rejected by the client with ERR_EXPORTMODE_NOT_EXIST."""
    _rejected(
        robot,
        sdk,
        "MC_ReadServerLogFB",
        {"LogFile": [""] * 10},
        {"ExportMode": export_mode},
        E.ERR_EXPORTMODE_NOT_EXIST,
    )
