# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_group_reset
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of GroupReset against the SDK simulator (robot controller side).
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

"""Validation of GroupReset against the SDK simulator (robot controller side).

* a pending error of the RC is acknowledged (ErrorPending FALSE)
* without a pending error the command ends Done and changes nothing (also without power,
  in T1 external and in the secondary sequence)
* a running motion is not affected, the message buffer of the axes group is cleared

The simulator raises a motion error with ``set_motion_error`` while a motion is active.
"""

from __future__ import annotations

import pytest
from srci_sdk_sim.sdk import SdkSimulator

from srci.types import OperationMode, SequenceFlag
from tests.robot_task_harness import RobotTaskHarness
from tests.sdk.validation.conftest import enable, execute, fb, finished, move_axes, order, state

MOTION_ERROR = 0x6C02  # error the simulated RA reports for the active motion


def _error_pending(h: RobotTaskHarness, sdk: SdkSimulator, clear_cause: bool = True) -> None:
    """Motion running, the RA reports a motion error: ErrorPending TRUE, power off."""
    sdk.set_move_cycles(200)
    enable(h)
    mv = move_axes(h, 100.0)
    mv.Execute = True
    h.run(200, until=lambda: sdk.joints[0] > 5.0)
    sdk.set_motion_error(MOTION_ERROR)
    h.run(50, until=lambda: bool(h.user_data.ErrorPending))
    assert h.user_data.ErrorPending, state(mv)
    # the RC rejects a reset while its messages are not yet read by the client
    # (ERR_GROUPRESET_PENDING_MESSAGES): wait until the message buffer is read
    h.run(30)
    if clear_cause:
        sdk.set_motion_error(0)


@pytest.mark.parametrize("hold", [True, False], ids=["execute-held", "execute-pulse"])
def test_reset_acknowledges_pending_error(robot: RobotTaskHarness, sdk: SdkSimulator, hold: bool) -> None:
    """GroupReset with a pending RC error ends Done and the error is no longer pending.

    Execute held: Done stays TRUE until the falling edge. Execute reset while Busy: Done is shown
    for exactly one cycle."""
    _error_pending(robot, sdk)
    gr = fb(robot, "MC_GroupResetFB")
    gr.Execute = True
    if hold:
        seen = execute(robot, gr, reset=False)
        robot.run(5)
        assert gr.Done and not gr.Busy, state(gr)
        gr.Execute = False
        robot.run(2)
        assert not gr.Done, state(gr)
        assert order(seen, "Busy", "Done"), seen.flags
    else:
        robot.run(1)
        assert gr.Busy, state(gr)
        gr.Execute = False
        done = []
        for _ in range(50):
            robot.run(1)
            done.append(bool(gr.Done))
        assert done.count(True) == 1 and not gr.Error, done
    assert not robot.user_data.ErrorPending and not sdk.states.error_pending


@pytest.mark.xfail(
    strict=True,
    reason=(
        "SDK-GAP: no stimulus for an error that a reset cannot clear (spec 6.1.4.2); the simulator "
        "clears its injected motion error with every GroupReset"
    ),
)
def test_reset_with_lasting_error_cause(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupReset while the cause of the error persists ends Done, but the error stays pending."""
    _error_pending(robot, sdk, clear_cause=False)
    seen = execute(robot, fb(robot, "MC_GroupResetFB"))
    assert seen.final["Done"], seen.final
    robot.run(10)
    assert robot.user_data.ErrorPending


@pytest.mark.parametrize("condition", ["power-off", "power-on", "manual-t1-external", "secondary-sequence"])
def test_reset_without_pending_error(robot: RobotTaskHarness, condition: str) -> None:
    """GroupReset without a pending error ends Done without error and leaves power and sequence unchanged."""
    if condition == "manual-t1-external":
        om = fb(robot, "MC_SetOperationModeFB")
        om.ParCmd.OperationMode = OperationMode.T1_EXT
        assert execute(robot, om).final["Done"]
    if condition != "power-off":
        enable(robot)
    if condition == "secondary-sequence":
        seq = fb(robot, "MC_SetSequenceFB")
        seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
        assert execute(robot, seq).final["Done"]
    enabled = bool(robot.user_data.Enabled)
    secondary = bool(robot.user_data.SecondarySequenceActive)
    seen = execute(robot, fb(robot, "MC_GroupResetFB"))
    assert order(seen, "Busy", "Done") and not seen.final["Error"], (seen.flags, seen.final)
    assert robot.user_data.Enabled == enabled and robot.user_data.SecondarySequenceActive == secondary
    assert not robot.user_data.ErrorPending


def test_reset_keeps_motion_and_clears_messages(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """GroupReset during a motion clears the message buffer of the axes group; the motion continues to its target."""
    sdk.set_move_cycles(200)
    enable(robot)
    bad = fb(robot, "MC_SetSequenceFB", Execute=True)  # TargetSequence 0: rejected, creates a message
    robot.run(10, until=lambda: bool(bad.Error))
    robot.run(3)
    assert any(m.MessageCode for m in robot.ag.MessageLog.Messages)
    mv = move_axes(robot, 100.0)
    mv.Execute = True
    robot.run(200, until=lambda: sdk.joints[0] > 5.0)
    seen = execute(robot, fb(robot, "MC_GroupResetFB"))
    assert seen.final["Done"], seen.final
    assert mv.Active and not mv.CommandAborted, state(mv)
    robot.run(3)
    assert not any(m.MessageCode for m in robot.ag.MessageLog.Messages)
    robot.run(400, until=lambda: finished(mv))
    assert mv.Done, state(mv)
    assert sdk.joints[0] == pytest.approx(100.0)
