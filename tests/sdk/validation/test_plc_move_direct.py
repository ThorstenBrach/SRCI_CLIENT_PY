# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_move_direct
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    MoveDirectAbsolute block of the client: outputs, Execute edges, parameter checks.
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

"""MoveDirectAbsolute block of the client: outputs, Execute edges, parameter checks.

Behaviour of the function block itself (spec 6.3.3.3, output status 5.5.x, client ErrorIDs table
7-1): outputs of a block that is not executed, Done after a falling edge of Execute, a second rising
edge while Busy, parameters changed while the command is running, and the parameter checks of the
client (range of the rates, undefined enum values, tool / frame numbers). A parameter error of the
client ends the command at once with Error (Busy is not shown) and nothing is sent to the RC.
"""

from __future__ import annotations

from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import AxesGroup, CmdType, RobotLibraryErrorIdEnum
from srci.types.iec import new_instance
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import (
    FLAGS,
    MOVE_CYCLES,
    cartesian,
    enable,
    fb,
    finished,
    order,
    state,
    watch,
)

E = RobotLibraryErrorIdEnum
MOVE_DIRECT = int(CmdType.MoveDirectAbsolute)  # 2102


def _move(h: RobotTaskHarness, x: float, y: float = 0.0, z: float = 0.0, **inputs: Any) -> Any:
    """MoveDirectAbsolute to (x, y, z) with 100 % velocity / acceleration (deceleration / jerk: default)."""
    mv = fb(h, "MC_MoveDirectAbsoluteFB", **inputs)
    cartesian(mv, x, y, z)
    mv.ParCmd.VelocityRate = 100.0
    mv.ParCmd.AccelerationRate = 100.0
    mv.ParCmd.DecelerationRate = -1.0
    mv.ParCmd.JerkRate = -1.0
    return mv


def _accepted(sdk: SdkSimulator, since: int) -> int:
    """MoveDirectAbsolute commands the SDK accepted since log entry ``since``."""
    return sum(
        1
        for log in sdk.logs[since:]
        if f"({MOVE_DIRECT}), cmdID" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _rejected(h: RobotTaskHarness, sdk: SdkSimulator, mv: Any) -> Any:
    """Execute ``mv``: returns the outputs; checks that nothing was sent and the robot did not move."""
    since = len(sdk.logs)
    start = sdk.joints[:6]
    mv.Execute = True
    s = watch(h, [mv], MOVE_CYCLES, lambda: finished(mv))[0]
    final = state(mv)
    assert _accepted(sdk, since) == 0, "nothing is sent to the RC"
    assert sdk.joints[:6] == start, "the robot does not move"
    assert "Active" not in s.flags and "CommandBuffered" not in s.flags, s.flags
    mv.Execute = False
    h.run(2)
    return final


# ---------------------------------------------------------------- outputs and Execute edges


def test_not_executed_outputs_are_zero(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A valid MoveDirectAbsolute that is never executed keeps every BOOL output FALSE, every number 0 and sends nothing."""
    enable(robot)
    since = len(sdk.logs)
    mv = _move(robot, 100.0)
    robot.run(20)
    assert not any(getattr(mv, f, False) for f in FLAGS), state(mv)
    assert mv.ErrorID == 0 and mv.InfoID == 0 and mv.WarningID == 0
    assert mv.OutCmd.Progress == 0.0 and mv.OutCmd.RemainingDistance == 0.0 and mv.OutCmd.FollowID == 0
    assert _accepted(sdk, since) == 0
    assert sdk.joints[0] == 0.0


def test_execute_reset_while_busy_shows_done_one_cycle(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Execute reset while Busy does not cancel the move: the robot reaches the target and Done is TRUE for exactly one cycle."""
    enable(robot)
    mv = _move(robot, 100.0)
    mv.Execute = True
    robot.run(5, until=lambda: bool(mv.Busy))
    assert mv.Busy, state(mv)
    mv.Execute = False
    seen: list[str] = []
    done_cycles = 0
    for _ in range(3 * MOVE_CYCLES):
        robot.cycle()
        for f in ("Busy", "CommandBuffered", "Active", "Done", "Error"):
            if getattr(mv, f) and f not in seen:
                seen.append(f)
        done_cycles += int(mv.Done)
        if done_cycles and not mv.Done:
            break
    assert [f for f in seen if f != "Error"] == ["Busy", "CommandBuffered", "Active", "Done"], seen
    assert done_cycles == 1
    assert not mv.Busy and not mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)


def test_axes_group_not_ready_rejected() -> None:
    """MoveDirectAbsolute on an axes group whose RobotTask never enabled the commands ends with ERR_COMMANDS_NOT_ENABLED."""
    group = AxesGroup()
    mv = new_instance("MC_MoveDirectAbsoluteFB")
    cartesian(mv, 100.0, 0.0, 0.0)
    for _ in range(3):
        mv(AxesGroup=group, Execute=True)
    assert mv.Error and mv.ErrorID == E.ERR_COMMANDS_NOT_ENABLED, state(mv)
    assert not mv.Busy and not mv.CommandBuffered


def test_second_edge_while_active_is_ignored(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """A new rising edge of Execute while the move is Active sends no second command; the move finishes with Done at its target."""
    sdk.set_move_cycles(2 * MOVE_CYCLES)
    enable(robot)
    since = len(sdk.logs)
    mv = _move(robot, 200.0)
    mv.Execute = True
    robot.run(5, until=lambda: bool(mv.Busy))
    mv.Execute = False
    robot.run(MOVE_CYCLES, until=lambda: bool(mv.Active))
    assert mv.Active, state(mv)
    mv.Execute = True
    s = watch(robot, [mv], 4 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert mv.Done and not mv.Error and "CommandAborted" not in s.flags, state(mv)
    assert _accepted(sdk, since) == 1
    assert sdk.joints[0] == pytest.approx(200.0)


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F114: a ParCmd change while the command is Busy but not yet sent turns the queued ACR "
    "entry (state CREATED) into a parameter update (UPDATE_AVAILABLE); the command is never sent and "
    "ends after the command timeout with ERR_TIMEOUT_CMD (ActiveCommandRegisterFB NotifyParameterChanged, "
    "MC_MoveDirectAbsoluteFB.CheckParameterChanged; parameters are latched at the rising edge, spec 6.3.3.3)",
)
@pytest.mark.parametrize("new_edge", [False, True], ids=["execute_held", "execute_retriggered"])
def test_position_changed_before_transmission(
    robot: RobotTaskHarness, sdk: SdkSimulator, new_edge: bool
) -> None:
    """Changing the target in the first Busy cycle (before the command is sent) does not lose the command: it finishes with Done.

    The target is latched with the rising edge, so the robot ends at the first target; with a new
    edge of Execute (reset and set again) no second command is started.
    """
    enable(robot)
    mv = _move(robot, 200.0)
    mv.Execute = True
    robot.cycle()
    assert mv.Busy and not mv.CommandBuffered, state(mv)
    cartesian(mv, 50.0, 30.0, 0.0)
    if new_edge:
        mv.Execute = False
        robot.cycle()
        mv.Execute = True
    robot.run(6 * MOVE_CYCLES, until=lambda: finished(mv))
    assert mv.Done and not mv.Error, (state(mv), hex(mv.ErrorID))
    assert sdk.joints[:2] == pytest.approx([200.0, 0.0])


# ---------------------------------------------------------------- dynamics rates above 100 %


@pytest.mark.parametrize(
    ("rate", "error"),
    [
        ("VelocityRate", E.ERR_VELOCITY_INVALID),
        ("AccelerationRate", E.ERR_ACCELERATION_INVALID),
        ("DecelerationRate", E.ERR_DECELERATION_INVALID),
        ("JerkRate", E.ERR_JERK_INVALID),
    ],
    ids=["velocity", "acceleration", "deceleration", "jerk"],
)
@pytest.mark.parametrize("value", [200.0, 655.36], ids=["200pct", "beyond_telegram_range"])
def test_rate_above_100_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, rate: str, error: int, value: float
) -> None:
    """A dynamics rate above 100 % is rejected by the client with the rate-specific ErrorID; nothing is sent and the robot does not move."""
    enable(robot)
    mv = _move(robot, 100.0)
    setattr(mv.ParCmd, rate, value)
    final = _rejected(robot, sdk, mv)
    assert final["Error"] and final["ErrorID"] == error, final


# ---------------------------------------------------------------- undefined enum values / numbers


@pytest.mark.parametrize("flag", [0, 78], ids=["no_sequence", "undefined_78"])
def test_invalid_sequence_flag_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, flag: int) -> None:
    """A SequenceFlag other than primary / secondary is rejected with ERR_SEQFLAG_NOT_ALLOWED and the robot does not move."""
    enable(robot)
    mv = _move(robot, 100.0)
    mv.SequenceFlag = flag
    final = _rejected(robot, sdk, mv)
    assert final["Error"] and final["ErrorID"] == E.ERR_SEQFLAG_NOT_ALLOWED, final
    assert not robot.ag.State.StatusRobotArm.SecondarySequenceActive


def test_invalid_aborting_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """An undefined AbortingMode (12) is rejected with ERR_ABORTINGMODE_INVALID and the robot does not move."""
    enable(robot)
    mv = _move(robot, 100.0)
    mv.AbortingMode = 12
    final = _rejected(robot, sdk, mv)
    assert final["Error"] and final["ErrorID"] == E.ERR_ABORTINGMODE_INVALID, final


@pytest.mark.parametrize(
    ("field", "value"),
    [("BlendingMode", 1), ("BlendingMode", 99), ("TurnMode", 55)],
    ids=["blending_mode_1", "blending_mode_99", "turn_mode_55"],
)
def test_undefined_mode_rejected(robot: RobotTaskHarness, sdk: SdkSimulator, field: str, value: int) -> None:
    """An undefined BlendingMode or TurnMode is rejected by the client (ERR_INVALID_PAR_CMD) and nothing is sent.

    The client has no specific ErrorID for these parameters (table 7-1); an RC would answer
    ERR_INVALID_PARAM_BLENDING_MODE / ERR_INVALID_PARAM_TURN_MODE.
    """
    enable(robot)
    mv = _move(robot, 100.0)
    setattr(mv.ParCmd, field, value)
    final = _rejected(robot, sdk, mv)
    assert final["Error"] and final["ErrorID"] == E.ERR_INVALID_PAR_CMD, final


CONFIG_ERRORS = {
    "Shoulder": (E.ERR_CONFIGMODE_SHOULDER_INVALID, E.ERR_INVALID_PARAM_CONFIG_MODE_SHOULDER),
    "Elbow": (E.ERR_CONFIGMODE_ELBOW_INVALID, E.ERR_INVALID_PARAM_CONFIGMODE_ELBOW),
    "Wrist": (E.ERR_CONFIGMODE_WRIST_INVALID, E.ERR_INVALID_PARAM_CONFIG_MODE_WRIST),
}


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F111: an undefined ParCmd.ConfigMode.<joint> is rejected with the generic ERR_INVALID_PAR_CMD "
    "(16#0008) instead of the client ErrorID for ConfigMode ERR_CONFIGMODE_<JOINT>_INVALID 16#8405..16#8407 "
    "(table 7-1 'commands using the parameter ConfigMode'); the library uses these IDs for Position.Config "
    "(MC_MoveDirectAbsoluteFB.CheckParameterValid)",
)
@pytest.mark.parametrize(
    ("joints", "value"),
    [
        (("Shoulder",), 14),
        (("Elbow",), 14),
        (("Wrist",), 14),
        (("Shoulder", "Elbow", "Wrist"), 14),
        (("Shoulder", "Elbow", "Wrist"), 55),
        (("Shoulder", "Elbow", "Wrist"), 99),
    ],
    ids=["shoulder_14", "elbow_14", "wrist_14", "all_14", "all_55", "all_99"],
)
def test_undefined_config_mode_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, joints: tuple[str, ...], value: int
) -> None:
    """An undefined ConfigMode value is rejected with the ConfigMode ErrorID of an affected joint and the robot does not move."""
    enable(robot)
    mv = _move(robot, 100.0)
    for joint in joints:
        setattr(mv.ParCmd.ConfigMode, joint, value)
    final = _rejected(robot, sdk, mv)
    allowed = {e for joint in joints for e in CONFIG_ERRORS[joint]}
    assert final["Error"] and final["ErrorID"] in allowed, (final, hex(final["ErrorID"]))


@pytest.mark.parametrize(
    ("field", "number", "error"),
    [
        ("ToolNo", 255, E.ERR_TOOLNO_RANGE),
        ("ToolNo", 20, E.ERR_TOOLNO_UNAVAILABLE),
        ("FrameNo", 20, E.ERR_FRAMENO_UNAVAILABLE),
        ("FrameNo", 255, E.ERR_FRAMENO_RANGE),
    ],
    ids=["tool_255", "tool_not_on_rc", "frame_not_on_rc", "frame_255"],
)
def test_undefined_tool_or_frame_rejected(
    robot: RobotTaskHarness, sdk: SdkSimulator, field: str, number: int, error: int
) -> None:
    """A ToolNo / FrameNo outside the range or above the highest index of the RC is rejected by the client and the robot does not move.

    The SDK reports 20 tools / frames (0..19).
    """
    enable(robot)
    mv = _move(robot, 100.0)
    setattr(mv.ParCmd, field, number)
    final = _rejected(robot, sdk, mv)
    assert final["Error"] and final["ErrorID"] == error, final


def test_valid_move_after_rejected_one(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """After a rejected command (Execute reset) the same block executes a corrected command normally."""
    enable(robot)
    mv = _move(robot, 100.0)
    mv.ParCmd.VelocityRate = 200.0
    _rejected(robot, sdk, mv)
    assert not mv.Error, state(mv)
    mv.ParCmd.VelocityRate = 50.0
    mv.Execute = True
    s = watch(robot, [mv], 3 * MOVE_CYCLES, lambda: finished(mv))[0]
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
    assert sdk.joints[0] == pytest.approx(100.0)
