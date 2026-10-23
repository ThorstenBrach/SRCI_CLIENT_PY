# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_logs
#  Author:      Thorsten Brach
#  Date:        2026-10-23
#
#  Description:
#    CreateServerLog / ReadServerLog (spec 6.2.5 / 6.2.6) against the SRCI SDK.
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

"""CreateServerLog / ReadServerLog (spec 6.2.5 / 6.2.6) against the SRCI SDK.

The SDK (1.1) writes the server logs as files (harness: one folder per simulator, 3 logs, then
the oldest one is overwritten) and sends them line by line, a line in parts of up to 179
characters (telegram layout of the SDK: Offset as request counter, IsStartOfLine / IsEndOfLine /
EndOfLogReached / LogLine in the response; spec tables 6-123 / 6-124 differ).
"""

from __future__ import annotations

from typing import Any

from srci_sdk_sim.sdk import SdkSimulator

from srci.types import ProcessingMode
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.test_core_fbs import execute, fb, robot, sdk_parameters, state

__all__ = ["robot", "sdk_parameters"]  # fixtures


def create_log(h: RobotTaskHarness) -> Any:
    cl = fb(h, "MC_CreateServerLogFB")
    execute(h, cl, cycles=200)
    return cl


def read_log(h: RobotTaskHarness, lines: int = 200, cycles: int = 3000, **par: Any) -> Any:
    rl = fb(h, "MC_ReadServerLogFB", LogFile=[""] * lines)
    for key, value in par.items():
        setattr(rl.ParCmd, key, value)
    rl.Execute = True
    h.run(cycles, until=lambda: bool(rl.Done or rl.Error))
    return rl


def used(rl: Any) -> list[str]:
    return [line for line in rl.LogFile if line]


def test_create_server_log_returns_id(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """CreateServerLog: Done, OutCmd.ServerLogID 1, then 2."""
    first = create_log(robot)
    assert first.OutCmd.ServerLogID == 1, first.OutCmd
    second = create_log(robot)
    assert second.OutCmd.ServerLogID == 2, second.OutCmd


def test_read_server_log_complete(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ReadServerLog of the latest log: Done with EndOfLogReached, every line in LogFile, header first."""
    create_log(robot)
    rl = read_log(robot)
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    out = rl.OutCmd
    lines = used(rl)
    assert out.EndOfLogReached, out
    assert out.ReceivedLogLines == len(lines) == out.AvailableFilteredLogLines > 1, (out, len(lines))
    assert abs(out.Progress - 100.0) < 1e-3


def test_read_server_log_context_filter(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ContextFilter 1 (LogHeader): only the header line; 50 (SysData.Info): its child contexts."""
    create_log(robot)
    rl = read_log(robot, ContextFilter=[1] + [0] * 9)
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    assert rl.OutCmd.AvailableFilteredLogLines == 1 < rl.OutCmd.AvailableLogLines, rl.OutCmd
    lines = used(rl)
    assert len(lines) == 1 and ";LogHeader;" in lines[0], lines
    rl2 = read_log(robot, ContextFilter=[50] + [0] * 9)
    lines = used(rl2)
    assert rl2.Done and lines and all(";SysData.Info." in line for line in lines), lines


def test_read_server_log_log_file_full(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """LogFile with 3 elements: Done after 3 lines, EndOfLogReached FALSE (spec figure 6-44)."""
    create_log(robot)
    rl = read_log(robot, lines=3)
    assert rl.Done and not rl.Error, (state(rl), hex(rl.ErrorID))
    assert rl.OutCmd.ReceivedLogLines == 3 and not rl.OutCmd.EndOfLogReached, rl.OutCmd
    assert all(rl.LogFile) and ";LogHeader;" in rl.LogFile[0]


def test_read_server_log_start_line(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """StartLine 3: the first element of LogFile is line 3 of the log (spec figure 6-45)."""
    create_log(robot)
    full = used(read_log(robot))
    rl = read_log(robot, StartLine=3)
    lines = used(rl)
    assert rl.Done and lines == full[2:], (lines[:2], full[:4])


def test_read_server_log_oldest_and_latest(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ServerLogID -1: latest log, 0: oldest log, n: the log with this ID (header eventlogID)."""
    create_log(robot)
    create_log(robot)
    latest = used(read_log(robot, lines=1, ServerLogID=-1))[0]
    oldest = used(read_log(robot, lines=1, ServerLogID=0))[0]
    second = used(read_log(robot, lines=1, ServerLogID=2))[0]
    assert '"eventlogID":2' in latest and '"eventlogID":1' in oldest and second == latest, (latest, oldest)


def test_create_server_log_overwrites_oldest(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """More logs than the RC can store (3): InfoID 16#6C70, the IDs start again at 1."""
    for _ in range(3):
        create_log(robot)
    cl = fb(robot, "MC_CreateServerLogFB")
    cl.Execute = True
    robot.run(200, until=lambda: bool(cl.Done or cl.Error))
    assert cl.Done and cl.InfoID == 0x6C70 and cl.OutCmd.ServerLogID == 1, (
        state(cl),
        hex(cl.InfoID),
        cl.OutCmd,
    )


def test_read_server_log_unknown_id(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A log that does not exist: Error 16#8D95 of the RC."""
    rl = read_log(robot, ServerLogID=2)
    assert rl.Error and rl.ErrorID == 0x8D95 and not rl.Done, (state(rl), hex(rl.ErrorID))


def test_read_server_log_start_line_behind_the_log(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """StartLine behind the last line: Error 16#8D96 of the RC."""
    create_log(robot)
    rl = read_log(robot, StartLine=100000)
    assert rl.Error and rl.ErrorID == 0x8D96, (state(rl), hex(rl.ErrorID))


def test_read_server_log_unknown_context_filter(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A ContextFilter value of no context: Error 16#8D97 of the RC."""
    create_log(robot)
    rl = read_log(robot, ContextFilter=[2] + [0] * 9)
    assert rl.Error and rl.ErrorID == 0x8D97, (state(rl), hex(rl.ErrorID))


def test_read_server_log_export_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ExportMode 1 (export to a file, optional): client error 16#8419, nothing sent."""
    rl = read_log(robot, cycles=20, ExportMode=1)
    assert rl.Error and rl.ErrorID == 0x8419, (state(rl), hex(rl.ErrorID))
    assert sdk.last_command(9004) is None


def test_read_server_log_execute_reset_during_transfer(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Execute FALSE during the transfer: it goes on to the end (spec figure 6-44), Done for one cycle."""
    create_log(robot)
    rl = fb(robot, "MC_ReadServerLogFB", LogFile=[""] * 200)
    rl.Execute = True
    robot.run(5)
    assert rl.Busy, state(rl)
    rl.Execute = False
    done = []
    for _ in range(3000):
        robot.run(1)
        done.append(bool(rl.Done))
        if not rl.Busy and len(done) > 1 and not done[-1]:
            break
    assert done.count(True) == 1 and not rl.Error, (state(rl), hex(rl.ErrorID))
    assert rl.OutCmd.EndOfLogReached and rl.OutCmd.ReceivedLogLines == len(used(rl))


def test_read_server_log_restart(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """New rising edge of Execute during the transfer: the transfer starts again, LogFile from the start."""
    create_log(robot)
    full = used(read_log(robot))
    rl = fb(robot, "MC_ReadServerLogFB", LogFile=[""] * 200)
    rl.Execute = True
    robot.run(10)
    assert rl.Busy and 0 < rl.OutCmd.ReceivedLogLines < len(full), (state(rl), rl.OutCmd)
    rl.Execute = False
    robot.run(1)
    rl.Execute = True
    robot.run(3000, until=lambda: bool(rl.Done or rl.Error))
    assert rl.Done and used(rl) == full and rl.OutCmd.ReceivedLogLines == len(full), (state(rl), rl.OutCmd)


def test_create_server_log_continuous_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """ProcessingMode CONTINUOUS is not allowed for CreateServerLog: client error, nothing sent."""
    cl = fb(robot, "MC_CreateServerLogFB", ProcessingMode=ProcessingMode.CONTINUOUS)
    cl.Execute = True
    robot.run(20, until=lambda: bool(cl.Done or cl.Error))
    assert cl.Error and cl.ErrorID == 0x8603 and not cl.Done, (state(cl), hex(cl.ErrorID))
    assert sdk.last_command(9003) is None
