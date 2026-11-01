# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_frame_tool_load
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the client side of the frame, tool and load data blocks.
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

"""Validation of the client side of ReadFrameData, ReadToolData, ReadLoadData, WriteFrameData,
WriteToolData and WriteLoadData.

These tests check what the function blocks decide on their own: parameter checks before anything
is sent (table 7-1), the behaviour of the Execute input and the outputs, and the user data arrays
(ToolData / FrameData / LoadData) the blocks keep up to date. The RC is the SDK simulator.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.types import AxesGroup, CmdType, ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from srci.types.iec import new_instance
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import execute, fb, finished, order, state

E = RobotLibraryErrorIdEnum

# block -> (number input of ParCmd, command type, number output of OutCmd or None)
BLOCKS: dict[str, tuple[str, CmdType, str | None]] = {
    "MC_ReadFrameDataFB": ("FrameNo", CmdType.ReadFrameData, "FrameNoReturn"),
    "MC_ReadToolDataFB": ("ToolNo", CmdType.ReadToolData, "ToolNoReturn"),
    "MC_ReadLoadDataFB": ("LoadNo", CmdType.ReadLoadData, "LoadNoReturn"),
    "MC_WriteFrameDataFB": ("FrameNo", CmdType.WriteFrameData, None),
    "MC_WriteToolDataFB": ("ToolNo", CmdType.WriteToolData, None),
    "MC_WriteLoadDataFB": ("LoadNo", CmdType.WriteLoadData, None),
}
READ_BLOCKS = [n for n in BLOCKS if n.startswith("MC_Read")]
WRITE_BLOCKS = [n for n in BLOCKS if n.startswith("MC_Write")]


def _sent(sdk: SdkSimulator, cmd_type: CmdType, since: int) -> int:
    """Commands of ``cmd_type`` the SDK accepted after log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({int(cmd_type)}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _prepare(block: Any, name: str, number: int) -> Any:
    """Set the number input; a tool gets a valid load number (the RC rejects load 0 in a tool)."""
    setattr(block.ParCmd, BLOCKS[name][0], number)
    if name == "MC_WriteToolDataFB":
        block.ParCmd.ToolData.LoadNo = 1
    return block


def _block(h: RobotTaskHarness, name: str, number: int = 1, **inputs: Any) -> Any:
    return _prepare(fb(h, name, **inputs), name, number)


def _rejected(h: RobotTaskHarness, sdk: SdkSimulator, name: str, block: Any, error: int) -> None:
    """Execute ``block``: Busy is never set, Error with ``error``, nothing is sent to the RC."""
    since = len(sdk.logs)
    seen = execute(h, block, cycles=50, reset=False)
    assert seen.final["Error"] and seen.final["ErrorID"] == error, (state(block), hex(block.ErrorID))
    assert "Done" not in seen.flags
    assert _sent(sdk, BLOCKS[name][1], since) == 0, "nothing is sent to the RC"
    block.Execute = False
    h.run(2)


# ---------------------------------------------------------------- axes group


@pytest.mark.parametrize("name", list(BLOCKS))
def test_axes_group_not_connected_is_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """A data block called with an axes group that no RobotTask serves reports ERR_COMMANDS_NOT_ENABLED
    (16#8612) and sends nothing.

    The axes group variable exists and is valid, but it is not connected to an MC_RobotTask, so the
    commands of this group are not enabled (table 7-1).
    """
    block = _prepare(new_instance(name), name, 1)
    lonely = AxesGroup()
    robot.fbs.append(lambda: block(AxesGroup=lonely))
    since = len(sdk.logs)
    block.Execute = True
    robot.run(50, until=lambda: bool(block.Error or block.Done))
    assert block.Error and block.ErrorID == E.ERR_COMMANDS_NOT_ENABLED, (state(block), hex(block.ErrorID))
    assert not block.Done and not block.Busy
    assert _sent(sdk, BLOCKS[name][1], since) == 0


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F116: ERR_AXESGROUP_CHANGED (16#8614, table 7-1) is defined but never set; a block whose "
    "AxesGroup input changes while it is Busy keeps running and reports Done of the first group",
)
def test_axes_group_changed_while_busy_is_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReadToolData whose AxesGroup input is switched to a second, fully initialized axes group while the
    command is Busy ends with ERR_AXESGROUP_CHANGED (16#8614)."""
    other_sdk = SdkSimulator(cycle_time_ms=10)
    try:
        other = RobotTaskHarness(sdk_transport(other_sdk, SIZE, SIZE))
        other.run(100, until=lambda: bool(other.ag.State.CMDsEnabled))
        assert other.ag.State.CMDsEnabled
        robot.fbs.append(other.cycle)  # the second robot task runs in the same PLC cycle
        block = _prepare(new_instance("MC_ReadToolDataFB"), "MC_ReadToolDataFB", 1)
        group = [robot.ag]
        robot.fbs.insert(0, lambda: block(AxesGroup=group[0]))
        block.Execute = True
        robot.run(1)
        assert block.Busy, state(block)
        group[0] = other.ag
        robot.run(50, until=lambda: finished(block))
        assert block.Error and block.ErrorID == E.ERR_AXESGROUP_CHANGED, (state(block), hex(block.ErrorID))
    finally:
        other_sdk.close()


# ---------------------------------------------------------------- numbers


@pytest.mark.parametrize("name", ["MC_ReadLoadDataFB", "MC_WriteLoadDataFB"])
def test_load_number_zero_is_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """Load number 0 (also the default value of LoadNo) is rejected by the load blocks with ERR_LOADNO_RANGE
    (16#8418) before anything is sent.

    Load 0 is no user load; the default value 0 of the input therefore never reaches the RC.
    """
    block = fb(robot, name)
    assert block.ParCmd.LoadNo == 0  # the default value
    _rejected(robot, sdk, name, block, E.ERR_LOADNO_RANGE)


# ---------------------------------------------------------------- ProcessingMode / SequenceFlag

PM, SF = ProcessingMode, SequenceFlag
COMBINATIONS_NOT_ALLOWED = [
    pytest.param(PM.PARALLEL, SF.PRIMARY_SEQUENCE, id="parallel-primary"),
    pytest.param(PM.PARALLEL, SF.SECONDARY_SEQUENCE, id="parallel-secondary"),
    pytest.param(PM.BUFFERED, SF.NO_SEQUENCE, id="buffered-no-sequence"),
    pytest.param(PM.ABORTING, SF.NO_SEQUENCE, id="aborting-no-sequence"),
]


@pytest.mark.parametrize(("mode", "flag"), COMBINATIONS_NOT_ALLOWED)
@pytest.mark.parametrize("name", WRITE_BLOCKS)
def test_sequence_flag_does_not_fit_the_processing_mode(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, mode: ProcessingMode, flag: SequenceFlag
) -> None:
    """A write block whose SequenceFlag does not fit the ProcessingMode (parallel with a sequence, buffered or
    aborting without one) is rejected with ERR_SEQFLAG_INVALID_IN_PROC_MODE (16#8625), nothing is sent."""
    _rejected(
        robot,
        sdk,
        name,
        _block(robot, name, ProcessingMode=mode, SequenceFlag=flag),
        E.ERR_SEQFLAG_INVALID_IN_PROC_MODE,
    )


@pytest.mark.parametrize(
    ("mode", "flag", "error"),
    [
        pytest.param(PM.BUFFERED, 22, E.ERR_SEQFLAG_NOT_ALLOWED, id="sequence-flag-22"),
        pytest.param(33, SF.NO_SEQUENCE, E.ERR_PROCESSINGMODE_NOT_DEFINED, id="processing-mode-33"),
        pytest.param(99, SF.NO_SEQUENCE, E.ERR_PROCESSINGMODE_NOT_DEFINED, id="processing-mode-99"),
    ],
)
@pytest.mark.parametrize("name", WRITE_BLOCKS)
def test_undefined_sequence_flag_or_processing_mode(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str, mode: int, flag: int, error: int
) -> None:
    """A write block with an undefined SequenceFlag (ERR_SEQFLAG_NOT_ALLOWED, 16#8616) or an undefined
    ProcessingMode (ERR_PROCESSINGMODE_NOT_DEFINED, 16#8602) is rejected before anything is sent."""
    block = _block(robot, name)
    block.ProcessingMode, block.SequenceFlag = mode, flag
    _rejected(robot, sdk, name, block, error)


# ---------------------------------------------------------------- Execute and outputs


@pytest.mark.parametrize("name", list(BLOCKS))
def test_execute_pulse_shows_done_for_one_cycle(
    robot: RobotTaskHarness, sdk: SdkSimulator, name: str
) -> None:
    """Execute TRUE for a single cycle: the command is still executed once, Done is TRUE for exactly one
    cycle (with the returned number of a read block), then all flags are FALSE again."""
    block = _block(robot, name, 5)
    since = len(sdk.logs)
    block.Execute = True
    robot.run(1)
    block.Execute = False
    done_cycles, returned = 0, []
    for _ in range(50):
        robot.run(1)
        if block.Done:
            done_cycles += 1
            if BLOCKS[name][2]:
                returned.append(getattr(block.OutCmd, str(BLOCKS[name][2])))
    assert done_cycles == 1, state(block)
    assert not block.Busy and not block.Error and not block.Done
    assert _sent(sdk, BLOCKS[name][1], since) == 1
    if BLOCKS[name][2]:
        assert returned == [5]


@pytest.mark.parametrize("name", list(BLOCKS))
def test_continuous_execute_keeps_done(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """Execute held TRUE: the command is sent once, Done stays TRUE until Execute is reset, then Busy, Done
    and Error are FALSE and ErrorID is 0."""
    block = _block(robot, name, 1)
    since = len(sdk.logs)
    seen = execute(robot, block, reset=False)
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    robot.run(20)
    assert block.Done and not block.Busy, state(block)
    assert _sent(sdk, BLOCKS[name][1], since) == 1
    block.Execute = False
    robot.run(1)
    assert not (block.Done or block.Busy or block.Error) and block.ErrorID == 0, state(block)


@pytest.mark.parametrize("name", list(BLOCKS))
def test_new_edge_while_busy_is_ignored(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """Execute FALSE and TRUE again (with another number) while the block is still Busy: the running command
    is finished and sent only once, the new edge starts nothing; a read block reports the first number."""
    block = _block(robot, name, 1)
    since = len(sdk.logs)
    block.Execute = True
    robot.run(1)
    assert block.Busy
    block.Execute = False
    _prepare(block, name, 5)
    robot.run(1)
    assert block.Busy, "a falling edge does not cancel the command"
    block.Execute = True
    robot.run(50, until=lambda: finished(block))
    robot.run(10)
    assert block.Done and not block.Error, state(block)
    if BLOCKS[name][2]:
        assert getattr(block.OutCmd, str(BLOCKS[name][2])) == 1
    assert _sent(sdk, BLOCKS[name][1], since) == 1


@pytest.mark.parametrize("name", READ_BLOCKS)
def test_same_instance_reads_another_number(robot: RobotTaskHarness, name: str) -> None:
    """The same read instance executed twice in a row, first with number 1, then (new rising edge after
    Done) with number 5: the second Done returns number 5."""
    block = _block(robot, name, 1)
    first = execute(robot, block, reset=False)
    assert first.final["Done"] and getattr(block.OutCmd, str(BLOCKS[name][2])) == 1
    block.Execute = False
    robot.run(2)
    _prepare(block, name, 5)
    second = execute(robot, block, reset=False)
    assert order(second, "Busy", "Done") and second.final["ErrorID"] == 0, second.flags
    assert getattr(block.OutCmd, str(BLOCKS[name][2])) == 5


# ---------------------------------------------------------------- user data arrays


def _bad_frame(h: RobotTaskHarness) -> tuple[Any, Any]:
    wr = fb(h, "MC_WriteFrameDataFB")
    wr.ParCmd.FrameNo = 2
    wr.ParCmd.FrameData.ReferenceFrame = 2  # a frame cannot refer to itself (RC: 16#8C13)
    wr.ParCmd.FrameData.X = 100.0
    return wr, h.frames[2]


def _bad_tool(h: RobotTaskHarness) -> tuple[Any, Any]:
    wr = fb(h, "MC_WriteToolDataFB")
    wr.ParCmd.ToolNo = 3
    wr.ParCmd.ToolData.X = 100.0
    wr.ParCmd.ToolData.LoadNo = 0  # RC: 16#8D17
    return wr, h.tools[3]


def _bad_load(h: RobotTaskHarness) -> tuple[Any, Any]:
    wr = fb(h, "MC_WriteLoadDataFB")
    wr.ParCmd.LoadNo = 4
    wr.ParCmd.LoadData.Mass = 4000.0  # above the payload of the robot (RC: 16#8D49)
    return wr, h.loads[4]


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F115: MC_WriteFrameData/ToolData/LoadDataFB update the user data array for every final state "
    "(State >= DONE, also ERROR and ABORTED); the read blocks only for DONE (ST-FIX F16)",
)
@pytest.mark.parametrize("make", [_bad_frame, _bad_tool, _bad_load], ids=["frame", "tool", "load"])
def test_rejected_write_keeps_the_user_data(robot: RobotTaskHarness, make: Any) -> None:
    """A write the RC rejects with an error leaves the entry of the user data array (FrameData / ToolData /
    LoadData) unchanged: it stays not Available and keeps its old values."""
    block, entry = make(robot)
    before = repr(entry)
    seen = execute(robot, block, reset=False)
    assert seen.final["Error"] and seen.final["ErrorID"] != 0, seen.final
    robot.run(5)
    assert repr(entry) == before
