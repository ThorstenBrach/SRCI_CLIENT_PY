# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_subprogram_log_server
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation tests of CreateServerLog / ReadServerLog: behaviour of the robot controller.
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

"""Validation tests of CreateServerLog / ReadServerLog: behaviour of the robot controller.

The SDK writes a server log on CreateServerLog (the harness keeps 3 logs) and sends it line by
line on ReadServerLog. A log line is ``date;context name;context number;...;JSON``; the first line
is the log header. The ContextFilter selects a context and all its child contexts (e.g. 10 = SysData,
110 = EventLog, 1 = LogHeader).
"""

from __future__ import annotations

import json
import re
from typing import Any

import pytest

from srci.types import ProcessingMode, RobotLibraryErrorIdEnum, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, state

E = RobotLibraryErrorIdEnum
PM = ProcessingMode
SF = SequenceFlag
LOG_FILE = 200  # elements of LogFile (more than the lines of a fresh log)

_GAP_HEADER_KEYS = pytest.mark.xfail(
    strict=True,
    reason="SDK-GAP: the SDK writes the header keys 'eventlogID' / 'serverLogCreationTime' (example of "
    "5.5.11.8.3); spec tables 5-56 / 6-109 name them 'ServerLogID' / 'ServerLogCreationTime'",
)


def _create(h: RobotTaskHarness, **inputs: Any) -> Any:
    cl = fb(h, "MC_CreateServerLogFB", **inputs)
    seen = execute(h, cl, cycles=200, reset=False)
    assert seen.final["Done"] and not seen.final["Error"], seen.final
    out = cl.OutCmd.ServerLogID
    cl.Execute = False
    h.run(2)
    return out


def _read(
    h: RobotTaskHarness,
    lines: int = LOG_FILE,
    filters: list[int] | None = None,
    name: str = "ReadServerLog",
    **par: Any,
) -> Any:
    rl = fb(h, "MC_ReadServerLogFB", LogFile=[""] * lines, Name=name)
    if filters is not None:
        rl.ParCmd.ContextFilter = filters + [0] * (10 - len(filters))
    for key, value in par.items():
        setattr(rl.ParCmd, key, value)
    rl.Execute = True
    h.run(3000, until=lambda: bool(rl.Done or rl.Error))
    return rl


def _lines(rl: Any) -> list[str]:
    return [line for line in rl.LogFile if line]


def _context(line: str) -> tuple[str, int]:
    """(context name, context number) of a log line."""
    parts = line.split(";")
    return parts[1], int(parts[2])


# ---------------------------------------------------------------- CreateServerLog


@pytest.mark.parametrize(
    ("mode", "sequence"),
    [
        ((PM.PARALLEL, SF.NO_SEQUENCE), None),
        ((PM.BUFFERED, SF.PRIMARY_SEQUENCE), None),
        ((PM.BUFFERED, SF.SECONDARY_SEQUENCE), SF.SECONDARY_SEQUENCE),
    ],
    ids=["parallel", "primary-sequence", "secondary-sequence"],
)
def test_create_server_log_done(robot: RobotTaskHarness, mode: tuple[int, int], sequence: int | None) -> None:
    """CreateServerLog ends with Done and a ServerLogID > 0, without Error / CommandAborted / CommandInterrupted.

    Secondary sequence: SetSequence(SECONDARY) is executed first.
    """
    enable(robot)
    if sequence is not None:
        seq = fb(robot, "MC_SetSequenceFB")
        seq.ParCmd.TargetSequence = sequence
        assert execute(robot, seq).final["Done"]
    cl = fb(robot, "MC_CreateServerLogFB", ProcessingMode=mode[0], SequenceFlag=mode[1])
    seen = execute(robot, cl, cycles=200, reset=False)
    assert seen.final["Done"] and not seen.final["Busy"], seen.final
    assert not {"Error", "CommandAborted", "CommandInterrupted"} & set(seen.flags), seen.flags
    assert cl.ErrorID == 0 and cl.OutCmd.ServerLogID > 0, (seen.final, cl.OutCmd)


def test_log_header_holds_id_and_creation_time(robot: RobotTaskHarness) -> None:
    """The header of a new log (ContextFilter 1) holds its ServerLogID and a creation time 'YYYY-MM-DD hh:mm:ss'."""
    log_id = _create(robot)
    rl = _read(robot, filters=[1])
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    lines = _lines(rl)
    assert len(lines) == 1 and _context(lines[0]) == ("LogHeader", 1), lines
    header = {k.lower(): v for k, v in json.loads(lines[0][lines[0].index("{") :]).items()}
    ids = [v for k, v in header.items() if k.endswith("logid")]
    times = [v for k, v in header.items() if k.endswith("creationtime")]
    assert ids == [log_id], header
    assert len(times) == 1 and re.fullmatch(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d", times[0]), header


@_GAP_HEADER_KEYS
def test_log_header_uses_the_key_names_of_the_spec(robot: RobotTaskHarness) -> None:
    """The log header names its fields ServerLogID and ServerLogCreationTime."""
    log_id = _create(robot)
    line = _lines(_read(robot, filters=[1]))[0]
    header = json.loads(line[line.index("{") :])
    assert header.get("ServerLogID") == log_id and "ServerLogCreationTime" in header, header


# ---------------------------------------------------------------- ReadServerLog


@pytest.mark.parametrize(
    ("name", "export_name"), [("", ""), ("ReadLog", "IgnoredName")], ids=["no-names", "export-name-ignored"]
)
def test_read_server_log_to_log_file(robot: RobotTaskHarness, name: str, export_name: str) -> None:
    """ReadServerLog into LogFile (export to a file not requested) ends with Done, every line received, Progress 100.

    An ExportName is ignored in this mode; an empty Name is allowed.
    """
    _create(robot)
    rl = _read(robot, name=name, ExportName=export_name)
    assert rl.Done and not rl.Error and rl.ErrorID == 0, (state(rl), hex(rl.ErrorID))
    out = rl.OutCmd
    assert out.EndOfLogReached and out.Progress == pytest.approx(100.0), out
    assert out.ReceivedLogLines == out.AvailableLogLines == len(_lines(rl)) > 1, out


def test_read_server_log_log_file_exactly_fits(robot: RobotTaskHarness) -> None:
    """LogFile with exactly as many elements as the log has lines: Done, all lines, EndOfLogReached TRUE."""
    _create(robot)
    count = len(_lines(_read(robot)))
    rl = _read(robot, lines=count)
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    assert rl.OutCmd.ReceivedLogLines == rl.OutCmd.AvailableLogLines == count, rl.OutCmd
    assert all(rl.LogFile) and rl.OutCmd.EndOfLogReached, rl.OutCmd


@pytest.mark.parametrize(
    ("value", "prefix"),
    [(1, "LogHeader"), (10, "SysData."), (110, "EventLog.")],
    ids=["log-header", "sys-data", "event-log"],
)
def test_read_server_log_single_context(robot: RobotTaskHarness, value: int, prefix: str) -> None:
    """ContextFilter with one context: only lines of this context and its children, as many as the full log has."""
    _create(robot)
    full = _lines(_read(robot))
    rl = _read(robot, filters=[value])
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    lines = _lines(rl)
    expected = [line for line in full if _context(line)[0].startswith(prefix)]
    assert lines and all(_context(line)[0].startswith(prefix) for line in lines), lines[:3]
    assert len(lines) == len(expected) == rl.OutCmd.AvailableFilteredLogLines, (len(lines), len(expected))
    assert rl.OutCmd.AvailableLogLines == len(full) > rl.OutCmd.AvailableFilteredLogLines


def test_read_server_log_ten_contexts(robot: RobotTaskHarness) -> None:
    """ContextFilter with all 10 elements used: the selected contexts are sent, the others are left out.

    Filter 1, 21, 24, 31, 32, 41, 50, 60, 122, 124 (header, ACR content, tools, frames, interpreter
    configuration, info, state, event log ACR content); loads (33) and dynamics (34) are not selected.
    """
    _create(robot)
    rl = _read(robot, filters=[1, 21, 24, 31, 32, 41, 50, 60, 122, 124])
    assert rl.Done and not rl.Error and rl.OutCmd.Progress == pytest.approx(100.0), (
        state(rl),
        hex(rl.ErrorID),
    )
    numbers = {_context(line)[1] for line in _lines(rl)}
    assert {1, 31, 32, 41} <= numbers and not {33, 34} & numbers, sorted(numbers)
    assert 0 < rl.OutCmd.ReceivedLogLines == rl.OutCmd.AvailableFilteredLogLines < rl.OutCmd.AvailableLogLines


def test_number_of_server_logs(robot: RobotTaskHarness) -> None:
    """The RC reports the number of server logs; the log with that ID can be read, the next ID is unknown.

    NumberOfServerLogs comes with the ExchangeConfiguration response the RobotTask keeps alive (not
    exposed in the axes group state, read from the RobotTask's internal block).
    """
    _create(robot)
    _create(robot)
    robot.run(30)
    number = robot.rt._exchangeConfiguration.OutCmd.NumberOfServerLogs
    assert number == 2
    ok = _read(robot, lines=1, ServerLogID=number)
    assert ok.Done and not ok.Error, (state(ok), hex(ok.ErrorID))
    bad = _read(robot, lines=1, ServerLogID=number + 1)
    assert bad.Error and bad.ErrorID == E.ERR_INVALID_PARAM_SERVER_LOG_ID_UNKNOWN and not bad.Done, state(bad)


@pytest.mark.parametrize("filters", [[2], [174]], ids=["2", "174"])
def test_read_server_log_unknown_context_rejected(robot: RobotTaskHarness, filters: list[int]) -> None:
    """A ContextFilter value of no context is rejected by the RC with ERR_INVALID_PARAM_SERVER_LOG_CONTEXT_FILTER_UNKNOWN."""
    _create(robot)
    rl = _read(robot, filters=filters)
    assert rl.Error and not rl.Done, state(rl)
    assert rl.ErrorID == E.ERR_INVALID_PARAM_SERVER_LOG_CONTEXT_FILTER_UNKNOWN, hex(rl.ErrorID)
    assert not _lines(rl)
