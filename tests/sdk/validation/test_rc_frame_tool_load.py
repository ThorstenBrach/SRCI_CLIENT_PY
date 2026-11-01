# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_frame_tool_load
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the RC behaviour of the frame, tool and load data commands.
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

"""Validation of the RC behaviour of ReadFrameData, ReadToolData, ReadLoadData, WriteFrameData,
WriteToolData and WriteLoadData against the SDK simulator.

Covered: values written and read back (including the user data arrays), special numbers (0, -1),
errors of the RC, commands while the robot is disabled or in T1 external, the write commands
together with motions (parallel, buffered, aborting, GroupStop, GroupInterrupt) and the
processing in the primary and secondary sequence.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import OperationMode, ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import cartesian, enable, execute, fb, finished, order, state, watch

E = RobotLibraryErrorIdEnum
PM, SF = ProcessingMode, SequenceFlag

KINDS = ("frame", "tool", "load")
READ = {"frame": "MC_ReadFrameDataFB", "tool": "MC_ReadToolDataFB", "load": "MC_ReadLoadDataFB"}
WRITE = {"frame": "MC_WriteFrameDataFB", "tool": "MC_WriteToolDataFB", "load": "MC_WriteLoadDataFB"}
NUMBER = {"frame": "FrameNo", "tool": "ToolNo", "load": "LoadNo"}
DATA = {"frame": "FrameData", "tool": "ToolData", "load": "LoadData"}


# ---------------------------------------------------------------- helpers


def _write(
    h: RobotTaskHarness, kind: str, number: int, values: dict[str, Any] | None = None, **inputs: Any
) -> Any:
    """Write block of ``kind`` for ``number``; ``values`` are fields of the data (a tool gets load 1
    unless ``LoadNo`` is given: the RC rejects load 0 in a tool)."""
    block = fb(h, WRITE[kind], **inputs)
    setattr(block.ParCmd, NUMBER[kind], number)
    data = getattr(block.ParCmd, DATA[kind])
    if kind == "tool":
        data.LoadNo = 1
    for field, value in (values or {}).items():
        setattr(data, field, value)
    return block


def _read(h: RobotTaskHarness, kind: str, number: int) -> tuple[int, Any]:
    """Read ``number`` of ``kind``; returns (returned number, data). Asserts Done without error."""
    block = fb(h, READ[kind])
    setattr(block.ParCmd, NUMBER[kind], number)
    seen = execute(h, block, reset=False)
    assert seen.final["Done"] and not seen.final["Error"], (seen.final, hex(block.ErrorID))
    result = getattr(block.OutCmd, f"{NUMBER[kind]}Return"), getattr(block.OutCmd, DATA[kind])
    block.Execute = False
    h.run(2)
    return result


def _user_data(h: RobotTaskHarness, kind: str, number: int) -> Any:
    """Entry of the user data array (ToolData / FrameData / LoadData of the RobotTask)."""
    tables: dict[str, Any] = {"frame": h.frames, "tool": h.tools, "load": h.loads}
    return tables[kind][number]


def _same(data: Any, values: dict[str, Any]) -> None:
    for field, value in values.items():
        assert getattr(data, field) == pytest.approx(value), field


def _linear(h: RobotTaskHarness, x: float, frame_no: int = 0, tool_no: int = 0, **inputs: Any) -> Any:
    """MoveLinearAbsolute to (x, 0, 0) with 100 % dynamics (not started)."""
    mv = fb(h, "MC_MoveLinearAbsoluteFB", **inputs)
    cartesian(mv, x, 0.0, 0.0)
    mv.ParCmd.VelocityRate = mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.FrameNo, mv.ParCmd.ToolNo = frame_no, tool_no
    return mv


def _active(h: RobotTaskHarness, mv: Any) -> None:
    mv.Execute = True
    h.run(20, until=lambda: bool(mv.Active or mv.Error))
    assert mv.Active, state(mv)


def _set_sequence(h: RobotTaskHarness, target: SequenceFlag) -> None:
    seq = fb(h, "MC_SetSequenceFB")
    seq.ParCmd.TargetSequence = target
    seen = execute(h, seq)
    assert seen.final["Done"], seen.final


# ---------------------------------------------------------------- values written and read back

FRAMES = [
    pytest.param(
        1,
        {"ReferenceFrame": 2, "X": 100.0, "Y": 200.0, "Z": 300.0, "Rx": 10.0, "Ry": 20.0, "Rz": 30.0},
        id="frame-1",
    ),
    pytest.param(
        5,
        {"ReferenceFrame": 3, "X": 600.0, "Y": 500.0, "Z": 400.0, "Rx": -90.0, "Ry": 90.0, "Rz": 180.0},
        id="frame-5",
    ),
    pytest.param(
        5,
        {"ReferenceFrame": 3, "X": 100.0, "Y": 200.0, "Z": 300.0, "Rx": 45.0, "Ry": 90.0, "Rz": 135.0},
        id="frame-5-other-angles",
    ),
]
TOOLS = [
    pytest.param(
        1,
        {
            "ID": 2,
            "X": 100.0,
            "Y": 200.0,
            "Z": 300.0,
            "Rx": 10.0,
            "Ry": 20.0,
            "Rz": 30.0,
            "LoadNo": 1,
            "ExternalTCP": False,
        },
        id="tool-1",
    ),
    pytest.param(
        5,
        {
            "ID": 3,
            "X": 600.0,
            "Y": 500.0,
            "Z": 400.0,
            "Rx": 90.0,
            "Ry": -90.0,
            "Rz": 180.0,
            "LoadNo": 5,
            "ExternalTCP": True,
        },
        id="tool-5-external-tcp",
    ),
]
# inertia and orientation within the ranges the simulated RC supports (inertia 0..1000, angles -180..180)
LOADS = [
    pytest.param(
        1,
        {
            "X": 100.0,
            "Y": 200.0,
            "Z": 300.0,
            "Mass": 3.0,
            "Rx": 10.0,
            "Ry": 20.0,
            "Rz": 30.0,
            "Ix": 10.1,
            "Iy": 10.2,
            "Iz": 10.3,
        },
        id="load-1",
    ),
    pytest.param(
        5,
        {
            "X": 600.0,
            "Y": 500.0,
            "Z": 400.0,
            "Mass": 2.0,
            "Rx": 30.0,
            "Ry": 20.0,
            "Rz": 10.0,
            "Ix": 200.0,
            "Iy": 150.0,
            "Iz": 100.0,
        },
        id="load-5",
    ),
]


def _round_trip(h: RobotTaskHarness, kind: str, number: int, values: dict[str, Any]) -> None:
    wr = _write(h, kind, number, values)
    seen = execute(h, wr, reset=False)
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, (seen.flags, seen.final)
    h.run(5)
    assert wr.Done and not wr.Busy, "Done stays TRUE while Execute is TRUE"
    wr.Execute = False
    h.run(1)
    assert not wr.Done
    returned, data = _read(h, kind, number)
    assert returned == number
    _same(data, values)
    entry = _user_data(h, kind, number)
    assert entry.Available
    _same(entry.Data, values)


@pytest.mark.parametrize(("number", "values"), FRAMES)
def test_frame_written_and_read_back(robot: RobotTaskHarness, number: int, values: dict[str, Any]) -> None:
    """WriteFrameData stores all fields of a frame (incl. the reference frame) on the RC: ReadFrameData
    returns them unchanged and the entry of the user data array is Available with these values."""
    _round_trip(robot, "frame", number, values)


@pytest.mark.parametrize(("number", "values"), TOOLS)
def test_tool_written_and_read_back(robot: RobotTaskHarness, number: int, values: dict[str, Any]) -> None:
    """WriteToolData stores all fields of a tool (ID, TCP, load number, external TCP) on the RC:
    ReadToolData returns them unchanged and the entry of the user data array is Available."""
    _round_trip(robot, "tool", number, values)


@pytest.mark.parametrize(("number", "values"), LOADS)
def test_load_written_and_read_back(robot: RobotTaskHarness, number: int, values: dict[str, Any]) -> None:
    """WriteLoadData stores mass, centre of mass, orientation and inertia of a load on the RC: ReadLoadData
    returns them unchanged and the entry of the user data array is Available."""
    _round_trip(robot, "load", number, values)


@pytest.mark.parametrize("kind", KINDS)
def test_same_instance_writes_two_numbers(robot: RobotTaskHarness, kind: str) -> None:
    """One write instance executed twice in a row, first number 3 with X = 100, then number 4 with
    X = 300: both numbers keep their own value on the RC."""
    wr = _write(robot, kind, 3, {"X": 100.0})
    assert execute(robot, wr).final["Done"]
    setattr(wr.ParCmd, NUMBER[kind], 4)
    getattr(wr.ParCmd, DATA[kind]).X = 300.0
    seen = execute(robot, wr)
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, seen.final
    assert _read(robot, kind, 3)[1].X == 100.0
    assert _read(robot, kind, 4)[1].X == 300.0


@pytest.mark.parametrize("kind", KINDS)
def test_timestamp_written_and_read_back(robot: RobotTaskHarness, kind: str) -> None:
    """The time stamp (date and time of day) written with the data is returned unchanged by the read
    command."""
    wr = _write(robot, kind, 5, {"X": 600.0})
    stamp = getattr(wr.ParCmd, DATA[kind]).Timestamp
    stamp.IEC_DATE, stamp.IEC_TIME = 19688, 4454230  # 2023-11-27, 01:14:14.230
    assert execute(robot, wr).final["Done"]
    data = _read(robot, kind, 5)[1]
    assert (data.Timestamp.IEC_DATE, data.Timestamp.IEC_TIME) == (19688, 4454230)
    assert data.X == 600.0


@pytest.mark.parametrize(
    ("kind", "number", "values"),
    [
        pytest.param("frame", 6, {}, id="frame-6"),
        pytest.param("frame", 9, {}, id="frame-9"),
        pytest.param("tool", 6, {"LoadNo": 6}, id="tool-6"),
        pytest.param("load", 8, {}, id="load-8"),
    ],
)
def test_empty_data_overwrites_old_values(
    robot: RobotTaskHarness, kind: str, number: int, values: dict[str, Any]
) -> None:
    """Writing data with all values at their default (0) is accepted and replaces earlier values: the read
    command returns 0 for every field (a tool keeps its load number)."""
    assert execute(robot, _write(robot, kind, number, {"X": 11.0, "Y": 22.0, "Z": 33.0, **values})).final[
        "Done"
    ]
    seen = execute(robot, _write(robot, kind, number, values))
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, seen.final
    returned, data = _read(robot, kind, number)
    assert returned == number
    assert (data.X, data.Y, data.Z, data.Rx, data.Ry, data.Rz) == (0.0,) * 6
    if kind == "tool":
        assert data.LoadNo == 6 and data.ID == 0 and not data.ExternalTCP
    if kind == "load":
        assert (data.Mass, data.Ix, data.Iy, data.Iz) == (0.0,) * 4


def test_tool_with_another_load_number(robot: RobotTaskHarness) -> None:
    """A tool may use a load with another number (tool 3, load 4): WriteToolData is Done and ReadToolData
    returns load number 4."""
    seen = execute(robot, _write(robot, "tool", 3, {"X": 10.0, "LoadNo": 4}))
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, seen.final
    returned, data = _read(robot, "tool", 3)
    assert returned == 3 and data.X == 10.0 and data.LoadNo == 4


# ---------------------------------------------------------------- special numbers


@pytest.mark.parametrize("kind", ["frame", "tool"])
def test_read_number_zero(robot: RobotTaskHarness, kind: str) -> None:
    """Reading frame 0 (world) or tool 0 (flange) is Done and returns number 0."""
    returned, data = _read(robot, kind, 0)
    assert returned == 0
    assert (data.X, data.Y, data.Z) == (0.0, 0.0, 0.0)


@pytest.mark.parametrize(("kind", "active"), [("frame", 0), ("tool", 0), ("load", 1)])
def test_read_active_number_at_standstill(robot: RobotTaskHarness, kind: str, active: int) -> None:
    """Number -1 at standstill returns the number currently active on the RC: frame 0, tool 0 and the load
    of tool 0 (load 1)."""
    returned, _ = _read(robot, kind, -1)
    assert returned == active


@pytest.mark.parametrize("kind", ["frame", "tool"])
def test_read_active_number_during_motion(robot: RobotTaskHarness, kind: str) -> None:
    """Number -1 while a MoveLinearAbsolute with frame 5 and tool 5 is active returns 5 and the data of
    number 5; the read runs in parallel and does not disturb the motion."""
    enable(robot)
    assert execute(robot, _write(robot, kind, 5, {"X": 42.0})).final["Done"]
    mv = _linear(robot, 50.0, frame_no=5 if kind == "frame" else 0, tool_no=5 if kind == "tool" else 0)
    _active(robot, mv)
    rd = fb(robot, READ[kind])
    setattr(rd.ParCmd, NUMBER[kind], -1)
    seen = execute(robot, rd, reset=False)
    assert order(seen, "Busy", "Done") and "CommandBuffered" not in seen.flags, seen.flags
    assert getattr(rd.OutCmd, f"{NUMBER[kind]}Return") == 5
    assert getattr(rd.OutCmd, DATA[kind]).X == 42.0
    assert mv.Active and not mv.Done, state(mv)
    robot.run(200, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, state(mv)


# ---------------------------------------------------------------- errors of the RC


def test_write_frame_zero_is_rejected(robot: RobotTaskHarness) -> None:
    """Frame 0 (the world frame, also the default value of FrameNo) cannot be overwritten: the RC answers
    WriteFrameData with ERR_INVALID_PARAM_FRAMENO (16#8D08)."""
    wr = _write(robot, "frame", 0, {"X": 100.0})
    seen = execute(robot, wr)
    assert order(seen, "Busy", "Error") and "Done" not in seen.flags, seen.flags
    assert seen.final["ErrorID"] == E.ERR_INVALID_PARAM_FRAMENO, hex(seen.final["ErrorID"])


def test_frame_referring_to_itself_is_rejected(robot: RobotTaskHarness) -> None:
    """A frame whose reference frame is the frame itself (frame 2 relative to frame 2) is rejected by the
    RC with ERR_FRAME_INVALID (16#8C13)."""
    seen = execute(robot, _write(robot, "frame", 2, {"X": 500.0, "ReferenceFrame": 2}))
    assert order(seen, "Busy", "Error") and "Done" not in seen.flags, seen.flags
    assert seen.final["ErrorID"] == E.ERR_FRAME_INVALID, hex(seen.final["ErrorID"])


def test_load_heavier_than_the_payload_is_rejected(robot: RobotTaskHarness) -> None:
    """A load of 4000 kg exceeds the payload of the robot: the RC rejects WriteLoadData with
    ERR_INVALID_PARAM_MASS_EXCEEDS_PAYLOAD (16#8D49) and keeps the old load."""
    seen = execute(robot, _write(robot, "load", 1, {"Mass": 4000.0}))
    assert order(seen, "Busy", "Error") and "Done" not in seen.flags, seen.flags
    assert seen.final["ErrorID"] == E.ERR_INVALID_PARAM_MASS_EXCEEDS_PAYLOAD, hex(seen.final["ErrorID"])
    assert _read(robot, "load", 1)[1].Mass != 4000.0


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        pytest.param("Ix", 2000.0, E.ERR_INVALID_PARAM_LOAD_IX_OUT_OF_RANGE, id="inertia-x"),
        pytest.param("Iy", 1500.0, E.ERR_INVALID_PARAM_LOAD_IY_OUT_OF_RANGE, id="inertia-y"),
        pytest.param("Iz", 1030.0, E.ERR_INVALID_PARAM_LOAD_IZ_OUT_OF_RANGE, id="inertia-z"),
        pytest.param("Rx", 300.0, E.ERR_INVALID_PARAM_LOAD_RX_OUT_OF_RANGE, id="angle-x"),
        pytest.param("Ry", 200.0, E.ERR_INVALID_PARAM_LOAD_RY_OUT_OF_RANGE, id="angle-y"),
        pytest.param("Rz", -181.0, E.ERR_INVALID_PARAM_LOAD_RZ_OUT_OF_RANGE, id="angle-z"),
    ],
)
def test_load_value_outside_the_rc_range_is_rejected(
    robot: RobotTaskHarness, field: str, value: float, error: int
) -> None:
    """A load value outside the range the RC supports (here inertia above 1000, angle outside -180..180) is
    rejected by the RC with the ErrorID of that field."""
    seen = execute(robot, _write(robot, "load", 5, {"Mass": 2.0, field: value}))
    assert order(seen, "Busy", "Error") and "Done" not in seen.flags, seen.flags
    assert seen.final["ErrorID"] == error, hex(seen.final["ErrorID"])


# ---------------------------------------------------------------- robot state


def _any_block(h: RobotTaskHarness, name: str) -> Any:
    kind = next(k for k in KINDS if name in (READ[k], WRITE[k]))
    if name == WRITE[kind]:
        return _write(h, kind, 6, {"X": 100.0})
    block = fb(h, name)
    setattr(block.ParCmd, NUMBER[kind], 1)
    return block


ALL_BLOCKS = [*READ.values(), *WRITE.values()]


@pytest.mark.parametrize("name", ALL_BLOCKS)
def test_data_command_while_robot_disabled(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """With the robot disabled (commands enabled, drives off) a data command with the default processing
    mode (parallel) is executed: Busy, then Done without error."""
    assert not sdk.enabled
    seen = execute(robot, _any_block(robot, name))
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, (seen.flags, seen.final)


@pytest.mark.parametrize("name", ALL_BLOCKS)
def test_data_command_in_t1_external(robot: RobotTaskHarness, sdk: SdkSimulator, name: str) -> None:
    """In operation mode T1 external (5) the data commands are executed: Busy, then Done without error."""
    mode = fb(robot, "MC_SetOperationModeFB")
    mode.ParCmd.OperationMode = OperationMode(5)
    assert execute(robot, mode).final["Done"]
    assert sdk.states.operation_mode == 5
    seen = execute(robot, _any_block(robot, name))
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, (seen.flags, seen.final)


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK executes a primary-sequence data command at once while the robot is disabled; "
    "spec (5.6.4, info 16#6F02 INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED): the sequence does not run, the "
    "command stays buffered and interrupted",
)
@pytest.mark.parametrize("kind", KINDS)
def test_sequence_data_command_waits_while_robot_disabled(
    robot: RobotTaskHarness, sdk: SdkSimulator, kind: str
) -> None:
    """A buffered write of the primary sequence while the robot is disabled is not executed: it is
    CommandBuffered and CommandInterrupted with info 16#6F02; a following GroupStop aborts it."""
    assert not sdk.enabled
    wr = _write(robot, kind, 7, {"Y": 50.0}, ProcessingMode=PM.BUFFERED, SequenceFlag=SF.PRIMARY_SEQUENCE)
    wr.Execute = True
    seen = watch(robot, [wr], 30, lambda: bool(wr.Done or wr.Error or wr.CommandInterrupted))[0]
    assert order(seen, "Busy", "CommandBuffered", "CommandInterrupted") and "Done" not in seen.flags, (
        seen.flags
    )
    assert wr.InfoID == 0x6F02, hex(wr.InfoID)
    stop = fb(robot, "MC_GroupStopFB")
    stop.Execute = True
    robot.run(50, until=lambda: bool(wr.CommandAborted or wr.Done))
    assert wr.CommandAborted and not wr.Done, state(wr)


# ---------------------------------------------------------------- together with motions


@pytest.mark.parametrize("kind", KINDS)
def test_parallel_write_during_motion(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str) -> None:
    """A parallel write while a motion is active is executed at once (Done without error) and the motion is
    not disturbed: it stays active and reaches its target afterwards; the new value can be read back."""
    enable(robot)
    mv = _linear(robot, 50.0, tool_no=4 if kind == "tool" else 0)
    _active(robot, mv)
    seen = execute(robot, _write(robot, kind, 4, {"X": 100.0, "Y": 200.0, "Z": 300.0}))
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, seen.final
    assert mv.Active and not mv.Done, state(mv)
    robot.run(200, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, state(mv)
    assert sdk.joints[0] == pytest.approx(50.0)
    _same(_read(robot, kind, 4)[1], {"X": 100.0, "Y": 200.0, "Z": 300.0})


@pytest.mark.parametrize("kind", KINDS)
def test_buffered_write_waits_for_the_motion(robot: RobotTaskHarness, kind: str) -> None:
    """A buffered write of the primary sequence between two motions is CommandBuffered while the first
    motion is active, Done only after the first motion and before the second one; both motions end Done."""
    enable(robot)
    first = _linear(robot, 50.0)
    _active(robot, first)
    wr = _write(robot, kind, 1, {"X": 7.0}, ProcessingMode=PM.BUFFERED, SequenceFlag=SF.PRIMARY_SEQUENCE)
    wr.Execute = True
    second = _linear(robot, 80.0, tool_no=1 if kind == "tool" else 0, frame_no=1 if kind == "frame" else 0)
    second.Execute = True
    write_done_with: list[tuple[bool, bool]] = []

    def note() -> bool:
        if wr.Done and not write_done_with:
            write_done_with.append((bool(first.Done), bool(second.Done)))
        return bool(second.Done or second.Error or wr.Error)

    seen = watch(robot, [wr, first, second], 400, note)
    assert order(seen[0], "Busy", "CommandBuffered", "Done") and not wr.Error, (seen[0].flags, state(wr))
    assert write_done_with == [(True, False)], "the write ends after the first and before the second motion"
    assert first.Done and second.Done, (state(first), state(second))


@pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the simulated robot ignores the frame of a Cartesian motion (identity kinematics without "
    "frame transformation), so the effect of written frame data on the motion cannot be observed",
)
def test_motion_uses_the_written_frame(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A MoveLinearAbsolute to X = 10 in frame 5 after frame 5 was written with an offset of X = 100 ends at
    X = 110 in world coordinates."""
    enable(robot)
    assert execute(robot, _write(robot, "frame", 5, {"X": 100.0})).final["Done"]
    mv = _linear(robot, 10.0, frame_no=5)
    assert execute(robot, mv).final["Done"]
    assert sdk.joints[0] == pytest.approx(110.0)


@pytest.mark.parametrize("kind", KINDS)
def test_aborting_write_aborts_the_motions(robot: RobotTaskHarness, sdk: SdkSimulator, kind: str) -> None:
    """A write with processing mode aborting in the primary sequence aborts the active motion and the
    buffered one (CommandAborted) and is executed (Done); the robot stops before the target."""
    enable(robot)
    first = _linear(robot, 50.0)
    _active(robot, first)
    second = _linear(robot, 80.0)
    second.Execute = True
    robot.run(20, until=lambda: bool(second.CommandBuffered))
    assert second.CommandBuffered, state(second)
    wr = _write(robot, kind, 1, {"X": 5.0}, ProcessingMode=PM.ABORTING, SequenceFlag=SF.PRIMARY_SEQUENCE)
    seen = execute(robot, wr, reset=False)
    robot.run(5)
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, seen.final
    assert first.CommandAborted and not first.Done, state(first)
    assert second.CommandAborted and not second.Done, state(second)
    assert sdk.joints[0] < 50.0


@pytest.mark.parametrize("kind", KINDS)
def test_group_stop_aborts_a_buffered_write(robot: RobotTaskHarness, kind: str) -> None:
    """GroupStop while a buffered write waits behind an active motion aborts both: the write reports
    CommandAborted and is never Done."""
    enable(robot)
    mv = _linear(robot, 50.0)
    _active(robot, mv)
    wr = _write(robot, kind, 3, {"X": 9.0}, ProcessingMode=PM.BUFFERED, SequenceFlag=SF.PRIMARY_SEQUENCE)
    wr.Execute = True
    robot.run(5, until=lambda: bool(wr.CommandBuffered))
    assert wr.CommandBuffered, state(wr)
    stop = fb(robot, "MC_GroupStopFB")
    stop.Execute = True
    seen = watch(robot, [wr, mv], 100, lambda: bool(stop.Done or stop.Error))
    robot.run(5)
    assert stop.Done, state(stop)
    assert order(seen[0], "Busy", "CommandBuffered", "CommandAborted") and "Done" not in seen[0].flags, seen[
        0
    ].flags
    assert mv.CommandAborted, state(mv)


@pytest.mark.parametrize("kind", KINDS)
def test_group_interrupt_holds_a_buffered_write(robot: RobotTaskHarness, kind: str) -> None:
    """GroupInterrupt while a buffered write waits behind an active motion: the motion is interrupted, the
    write stays buffered (not Done, not aborted); after GroupContinue the motion and then the write are Done."""
    enable(robot)
    mv = _linear(robot, 50.0)
    _active(robot, mv)
    wr = _write(robot, kind, 3, {"X": 9.0}, ProcessingMode=PM.BUFFERED, SequenceFlag=SF.PRIMARY_SEQUENCE)
    wr.Execute = True
    robot.run(5, until=lambda: bool(wr.CommandBuffered))
    interrupt = fb(robot, "MC_GroupInterruptFB")
    assert execute(robot, interrupt).final["Done"]
    robot.run(20)
    assert mv.CommandInterrupted, state(mv)
    assert wr.Busy and wr.CommandBuffered and not (wr.Done or wr.CommandAborted or wr.Error), state(wr)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    robot.run(300, until=lambda: bool(wr.Done or wr.Error))
    assert mv.Done and wr.Done and not wr.Error, (state(mv), state(wr))


# ---------------------------------------------------------------- primary and secondary sequence

DONE, BUFFERED_UNTIL_PRIMARY = "done", "buffered until primary"
SEQUENCES = [
    pytest.param(SF.PRIMARY_SEQUENCE, SF.NO_SEQUENCE, PM.PARALLEL, DONE, id="primary-active-parallel"),
    pytest.param(
        SF.PRIMARY_SEQUENCE, SF.PRIMARY_SEQUENCE, PM.BUFFERED, DONE, id="primary-active-buffered-primary"
    ),
    pytest.param(
        SF.PRIMARY_SEQUENCE, SF.PRIMARY_SEQUENCE, PM.ABORTING, DONE, id="primary-active-aborting-primary"
    ),
    pytest.param(
        SF.PRIMARY_SEQUENCE,
        SF.SECONDARY_SEQUENCE,
        PM.BUFFERED,
        E.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE,
        id="primary-active-buffered-secondary",
    ),
    pytest.param(
        SF.PRIMARY_SEQUENCE,
        SF.SECONDARY_SEQUENCE,
        PM.ABORTING,
        E.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE,
        id="primary-active-aborting-secondary",
    ),
    pytest.param(SF.SECONDARY_SEQUENCE, SF.NO_SEQUENCE, PM.PARALLEL, DONE, id="secondary-active-parallel"),
    pytest.param(
        SF.SECONDARY_SEQUENCE,
        SF.SECONDARY_SEQUENCE,
        PM.BUFFERED,
        DONE,
        id="secondary-active-buffered-secondary",
    ),
    pytest.param(
        SF.SECONDARY_SEQUENCE,
        SF.SECONDARY_SEQUENCE,
        PM.ABORTING,
        DONE,
        id="secondary-active-aborting-secondary",
    ),
    pytest.param(
        SF.SECONDARY_SEQUENCE,
        SF.PRIMARY_SEQUENCE,
        PM.BUFFERED,
        BUFFERED_UNTIL_PRIMARY,
        id="secondary-active-buffered-primary",
    ),
    pytest.param(
        SF.SECONDARY_SEQUENCE,
        SF.PRIMARY_SEQUENCE,
        PM.ABORTING,
        BUFFERED_UNTIL_PRIMARY,
        id="secondary-active-aborting-primary",
    ),
]


@pytest.mark.parametrize(("active", "flag", "mode", "expected"), SEQUENCES)
@pytest.mark.parametrize("kind", KINDS)
def test_write_in_primary_and_secondary_sequence(
    robot: RobotTaskHarness,
    kind: str,
    active: SequenceFlag,
    flag: SequenceFlag,
    mode: ProcessingMode,
    expected: Any,
) -> None:
    """A write with the given SequenceFlag / ProcessingMode while the primary or the secondary sequence is
    active: parallel writes and writes for the active sequence are Done, a write for the inactive secondary
    sequence is rejected with 16#8F16, a write for the primary sequence while the secondary one is active
    waits (CommandBuffered) and is Done after SetSequence back to the primary sequence."""
    enable(robot)
    if active == SF.SECONDARY_SEQUENCE:
        _set_sequence(robot, SF.SECONDARY_SEQUENCE)
    wr = _write(robot, kind, 2, {"X": 21.0}, ProcessingMode=mode, SequenceFlag=flag)
    wr.Execute = True
    seen = watch(robot, [wr], 30, lambda: bool(wr.Done or wr.Error))[0]
    if expected == DONE:
        assert order(seen, "Busy", "Done") and wr.ErrorID == 0, (seen.flags, state(wr))
    elif expected == BUFFERED_UNTIL_PRIMARY:
        assert wr.Busy and wr.CommandBuffered and not (wr.Done or wr.Error), (seen.flags, state(wr))
        _set_sequence(robot, SF.PRIMARY_SEQUENCE)
        robot.run(30, until=lambda: bool(wr.Done or wr.Error))
        assert wr.Done and not wr.Error, state(wr)
    else:
        assert order(seen, "Busy", "Error") and wr.ErrorID == expected, (seen.flags, hex(wr.ErrorID))
        return
    wr.Execute = False
    robot.run(2)
    if active == SF.SECONDARY_SEQUENCE and expected == DONE:
        _set_sequence(robot, SF.PRIMARY_SEQUENCE)
    assert _read(robot, kind, 2)[1].X == 21.0


@pytest.mark.parametrize("kind", KINDS)
def test_aborting_write_in_the_secondary_sequence(
    robot: RobotTaskHarness, sdk: SdkSimulator, kind: str
) -> None:
    """Primary motion interrupted, secondary sequence selected and continued, a secondary motion active: an
    aborting write of the secondary sequence aborts the secondary motion and is Done; the interrupted
    primary motion is not affected."""
    enable(robot)
    primary = _linear(robot, 50.0)
    _active(robot, primary)
    assert execute(robot, fb(robot, "MC_GroupInterruptFB")).final["Done"]
    _set_sequence(robot, SF.SECONDARY_SEQUENCE)
    assert execute(robot, fb(robot, "MC_GroupContinueFB")).final["Done"]
    secondary = _linear(robot, 20.0, SequenceFlag=SF.SECONDARY_SEQUENCE)
    _active(robot, secondary)
    wr = _write(robot, kind, 1, {"X": 3.0}, ProcessingMode=PM.ABORTING, SequenceFlag=SF.SECONDARY_SEQUENCE)
    seen = execute(robot, wr, reset=False)
    robot.run(5)
    assert order(seen, "Busy", "Done") and seen.final["ErrorID"] == 0, (seen.flags, seen.final)
    assert secondary.CommandAborted and not secondary.Done, state(secondary)
    assert primary.CommandInterrupted and not (primary.CommandAborted or primary.Done), state(primary)
