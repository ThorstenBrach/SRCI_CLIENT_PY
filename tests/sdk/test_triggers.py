# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_triggers
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Trigger concept (spec 5.5.12) against the trigger engine of the SDK (modified SDK by Thorsten, group TRIG).
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

"""Trigger concept (spec 5.5.12) against the trigger engine of the SDK (modified SDK by Thorsten, group TRIG).

"Actions" (ListenerID > 0) are held by the RC until a trigger function with EmitterID = ListenerID
fires; InvocationCounter / OriginID (= FollowID, the ACR ID of the trigger function; negative: the
action was stopped) are reported in the trigger response header. Skipped for an SDK without the
trigger commands (the harness then answers every action at once).
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, find_sdk_library, sdk_transport

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.types import ProcessingMode, SequenceFlag
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tools.payload_check import fb_classes

CLASSES = dict(fb_classes())
LISTENER = 5


@pytest.fixture(autouse=True, scope="module")
def sdk_parameters() -> Iterator[None]:
    try:
        find_sdk_library()
    except Exception as exc:
        pytest.skip(str(exc))
    with SdkSimulator(10) as sim:
        if not getattr(sim, "answered_by_sdk", lambda _: False)(3005):
            pytest.skip("SDK without the trigger commands (modified SDK by Thorsten, group TRIG)")
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@contextmanager
def robot() -> Iterator[tuple[SdkSimulator, RobotTaskHarness]]:
    from tests.sdk.test_core_fbs import enable

    clock = FakeClock()
    with SdkSimulator(10) as sim, use_clock(clock):
        h = RobotTaskHarness(sdk_transport(sim, SIZE, SIZE), advance=clock.advance)
        h.run(100, until=lambda: bool(h.ag.State.CMDsEnabled))
        enable(h, sim)
        yield sim, h


def add(h: RobotTaskHarness, name: str, **parcmd: Any) -> Any:
    fb = CLASSES[name]()
    for key, value in parcmd.items():
        target = fb.ParCmd
        parts = key.split(".")
        for part in parts[:-1]:
            target = getattr(target, part)
        if "[" in parts[-1]:
            base, index = parts[-1].rstrip("]").split("[")
            getattr(target, base)[int(index)] = value
        else:
            setattr(target, parts[-1], value)
    h.add(fb)
    return fb


def pulse(h: RobotTaskHarness, fb: Any, cycles: int = 100) -> int:
    """Rising edge of Execute, wait for Done / Error, falling edge; returns the WarningID."""
    fb.Execute = True
    h.run(cycles, until=lambda: bool(fb.Done or fb.Error))
    assert fb.Done and not fb.Error, (fb.ErrorID, fb.WarningID)
    warning = int(fb.WarningID)
    fb.Execute = False
    h.run(2)
    return warning


def read_integers(h: RobotTaskHarness, mode: ProcessingMode) -> Any:
    fb = add(h, "MC_ReadIntegersFB", **{"Index[0]": 1, "ListenerID": LISTENER})
    fb.ProcessingMode = mode
    fb.Execute = True
    h.run(10)
    return fb


def test_action_waits_for_its_trigger() -> None:
    """ReadIntegers with ListenerID: buffered (Busy, CommandBuffered) until SetTriggerUser fires the
    EmitterID; then executed once (Trigger Once) with InvocationCounter 1 and OriginID > 0."""
    with robot() as (_, h):
        action = read_integers(h, ProcessingMode.TRIGGER_ONCE)
        h.run(30)
        assert action.Busy and action.CommandBuffered and not action.Done and not action.Error
        user = add(h, "MC_SetTriggerUserFB", EmitterID=LISTENER)
        assert pulse(h, user) == 0  # an "Action" with this ListenerID exists
        h.run(30, until=lambda: bool(action.Done or action.Error))
        assert action.Done and not action.Error, action.ErrorID
        assert action.OutCmd.InvocationCounter == 1
        assert action.OutCmd.OriginID > 0


def test_trigger_without_action_warns() -> None:
    """SetTriggerUser without an "Action" with its EmitterID: Done with warning 16#7C12."""
    with robot() as (_, h):
        user = add(h, "MC_SetTriggerUserFB", EmitterID=LISTENER)
        assert pulse(h, user) == 0x7C12


def test_trigger_multiple_counts_invocations() -> None:
    """Trigger Multiple: the action stays buffered and is executed per trigger (InvocationCounter)."""
    with robot() as (_, h):
        action = read_integers(h, ProcessingMode.TRIGGER_MULTIPLE)
        user = add(h, "MC_SetTriggerUserFB", EmitterID=LISTENER)
        for invocation in (1, 2, 3):
            pulse(h, user)

            def counted(n: int = invocation) -> bool:
                return bool(action.OutCmd.InvocationCounter == n)

            h.run(10, until=counted)
            assert action.OutCmd.InvocationCounter == invocation
            assert action.Busy and not action.Error
        assert not action.Done


def test_trigger_continuous_stopped_by_negative_emitter() -> None:
    """Trigger Continuous: started by EmitterID 5, stopped by EmitterID -5: buffered again with
    OriginID negative (spec 5.5.12.5.1). The client applies OutCmd only in the states ACTIVE / DONE,
    the negative OriginID of the BUFFERED response is checked in the received response."""
    with robot() as (_, h):
        action = read_integers(h, ProcessingMode.TRIGGER_CONTINUOUS)
        start = add(h, "MC_SetTriggerUserFB", EmitterID=LISTENER)
        pulse(h, start)
        h.run(20, until=lambda: action.OutCmd.OriginID > 0)
        origin = action.OutCmd.OriginID
        assert origin > 0 and action.OutCmd.InvocationCounter == 1
        stop = add(h, "MC_SetTriggerUserFB", EmitterID=-LISTENER)
        pulse(h, stop)
        h.run(20, until=lambda: action._response.OriginID < 0)
        assert action._response.OriginID < 0  # -FollowID of the stopping SetTriggerUser
        assert action.Busy and action.CommandBuffered and not action.Error
        pulse(h, start)  # started again
        h.run(20, until=lambda: action.OutCmd.InvocationCounter == 2)
        assert action.OutCmd.InvocationCounter == 2 and action.OutCmd.OriginID > 0


def test_set_trigger_register_releases_action() -> None:
    """SetTriggerRegister (integer register 2 exceeds 10) releases the action with ListenerID 5;
    OriginID = FollowID of the trigger function (its ACR ID)."""
    with robot() as (_, h):
        action = read_integers(h, ProcessingMode.TRIGGER_ONCE)
        trigger = add(
            h,
            "MC_SetTriggerRegisterFB",
            EmitterID=LISTENER,
            TriggerMode=50,
            Index=2,
            **{"IntValue[1]": 10},
        )
        trigger.Execute = True
        h.run(20)
        assert trigger.Busy and not trigger.Done and not action.Done
        write = add(h, "MC_WriteIntegersFB", **{"Index[0]": 2, "Values[0]": 11})
        pulse(h, write)
        h.run(30, until=lambda: bool(trigger.Done and action.Done))
        assert trigger.Done and trigger.WarningID == 0, (trigger.ErrorID, trigger.WarningID)
        assert action.Done and action.OutCmd.InvocationCounter == 1
        assert action.OutCmd.OriginID > 0


def test_wait_for_trigger_holds_the_sequence() -> None:
    """WaitForTrigger in the sequence: Active until the trigger, the next motion waits for it."""
    from tests.sdk.test_core_fbs import move_axes

    with robot() as (sim, h):
        sim.set_move_cycles(5)
        wait = add(h, "MC_WaitForTriggerFB", ListenerID=LISTENER)
        wait.ProcessingMode = ProcessingMode.TRIGGER_BUFFERED
        wait.SequenceFlag = SequenceFlag.PRIMARY_SEQUENCE
        wait.Execute = True
        h.run(10)
        move = move_axes(h, 5.0)
        move.Execute = True
        h.run(40)
        assert wait.Active and not wait.Done
        assert not move.Done and not move.Active
        user = add(h, "MC_SetTriggerUserFB", EmitterID=LISTENER)
        pulse(h, user)
        h.run(20, until=lambda: bool(wait.Done))
        assert wait.Done and wait.OutCmd.InvocationCounter == 1 and wait.OutCmd.OriginID > 0
        h.run(100, until=lambda: bool(move.Done or move.Error))
        assert move.Done


def test_set_trigger_motion_on_move_command() -> None:
    """SetTriggerMotion (ListenerID = EmitterID of a move command) releases the action with
    ListenerID 5 when 50 % of the motion is traversed."""
    from tests.sdk.test_core_fbs import move_axes

    with robot() as (sim, h):
        sim.set_move_cycles(20)
        action = read_integers(h, ProcessingMode.TRIGGER_ONCE)
        motion = add(
            h,
            "MC_SetTriggerMotionFB",
            ListenerID=3,
            TriggerMode_1=1,
            TriggerParameter_1=50.0,
            **{"EmitterID[0]": LISTENER},
        )
        motion.Execute = True
        h.run(10)
        assert motion.Busy and not motion.Done
        move = move_axes(h, 10.0)
        move.ParCmd.EmitterID[0] = 3
        move.Execute = True
        h.run(200, until=lambda: bool(action.Done or action.Error))
        assert action.Done and action.OutCmd.InvocationCounter == 1
        assert not move.Done  # released during the motion
        h.run(100, until=lambda: bool(move.Done and motion.Done))
        assert motion.Done and move.Done


def test_deactivate_buffered_action() -> None:
    """ProcessingMode Deactivate (new rising edge) deletes a buffered action: Done."""
    with robot() as (_, h):
        action = read_integers(h, ProcessingMode.TRIGGER_MULTIPLE)
        h.run(10)
        action.ProcessingMode = ProcessingMode.DEACTIVATE
        action.Execute = False
        h.run(1)
        action.Execute = True
        h.run(50, until=lambda: bool(action.Done or action.Error or not action.Busy))
        assert not action.Error, action.ErrorID
        assert not action.Busy
