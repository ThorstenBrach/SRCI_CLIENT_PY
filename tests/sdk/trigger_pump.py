# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.trigger_pump
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Trigger helpers of the SDK tests: emit the trigger an "Action" waits for.
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

"""Trigger helpers of the SDK tests (spec 5.5.12).

An "Action" (command with ``ListenerID`` > 0, e.g. ReactAtTrigger, WaitForTrigger, RedefineTrackingPos)
is held BUFFERED by an SDK with a trigger engine until a trigger function emits ``EmitterID`` =
``ListenerID``. ``attach_listener_trigger`` adds an ``MC_SetTriggerUserFB`` to the "PLC program" that
is executed (again) as long as the action waits (Busy, not Done, CommandBuffered / Active or Busy
for a few cycles), so the tests of single function blocks also complete against such an SDK. An SDK
without trigger engine answers the action at once; the trigger function is then never started.

``when_buffered`` starts another function block (companion: e.g. a register write, a move command)
once the block under test is on the RC - for trigger functions whose condition must change
after their start.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from tests.robot_task_harness import RobotTaskHarness

# SetTriggerMotion is triggered by move commands only (its ListenerID refers to a move command)
NOT_USER_TRIGGERED = {"MC_SetTriggerMotionFB"}


def _fb_classes() -> dict[str, Any]:
    from tools.payload_check import fb_classes

    return dict(fb_classes())


# cycles a block is Busy before its command is surely on the RC (CommandBuffered is not set by
# every block while the command is ACTIVE on the RC, e.g. a monitoring trigger function)
BUSY_CYCLES = 5


class _Waiting:
    """``fb`` waits on the RC: Busy, not Done, CommandBuffered / Active or Busy for BUSY_CYCLES."""

    def __init__(self, fb: Any) -> None:
        self.fb = fb
        self.busy = 0

    def __call__(self) -> bool:
        fb = self.fb
        self.busy = self.busy + 1 if fb.Busy else 0
        if not fb.Busy or getattr(fb, "Done", False) or fb.Error:
            return False
        return bool(getattr(fb, "CommandBuffered", False) or getattr(fb, "Active", False)) or (
            self.busy >= BUSY_CYCLES
        )


def attach_listener_trigger(h: RobotTaskHarness, fb: Any, name: str = "") -> Any | None:
    """Adds an MC_SetTriggerUserFB with EmitterID = ``fb.ParCmd.ListenerID`` (> 0) that is executed
    while ``fb`` waits for its trigger; returns the trigger function block (None: no listener)."""
    listener = int(getattr(getattr(fb, "ParCmd", None), "ListenerID", 0) or 0)
    if listener <= 0 or name in NOT_USER_TRIGGERED:
        return None
    user = _fb_classes()["MC_SetTriggerUserFB"]()
    user.ParCmd.EmitterID = listener
    waiting = _Waiting(fb)

    def pump() -> None:
        is_waiting = waiting()
        if user.Execute and (user.Done or user.Error):
            user.Execute = False  # falling edge: the next trigger needs a new rising edge
        elif not user.Execute and not user.Busy and is_waiting:
            user.Execute = True
        user(AxesGroup=h.ag)

    h.fbs.append(pump)
    return user


def when_buffered(
    name: str, setup: Callable[[Any], None] | None = None
) -> Callable[[RobotTaskHarness, Any], Any]:
    """Companion: starts the function block ``name`` (inputs set by ``setup``) once the block under
    test is on the RC (see ``_Waiting``)."""

    def attach(h: RobotTaskHarness, fb: Any) -> Any:
        companion = _fb_classes()[name]()
        if setup is not None:
            setup(companion)
        started = [False]
        waiting = _Waiting(fb)

        def run() -> None:
            if waiting() and not started[0]:
                started[0] = True
                if hasattr(companion, "Execute"):
                    companion.Execute = True
                else:
                    companion.Enable = True
            companion(AxesGroup=h.ag)

        h.fbs.append(run)
        return companion

    return attach
