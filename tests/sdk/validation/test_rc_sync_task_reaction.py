# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_sync_task_reaction
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the reaction of the robot controller when the user data
#    are not synchronized (SyncReaction, SyncDelay).
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

"""Validation of the synchronization reaction of the RC (table 5-108, SyncReaction / SyncDelay).

The software limits are the synchronized data set (CLIENT_TO_SERVER during the start-up). To make
the client "not synchronized" the PLC data are changed with NO_SYNCHRONIZATION after the start-up
(the change is detected but not transferred, spec 5.6.7.3); with AUTOMATIC the change is written at
once and the client becomes synchronized again. SyncReaction and SyncDelay are sent to the RC with
ExchangeConfiguration at the start of the RobotTask.

* 0 NO_REACTION: the RC ignores the synchronization state.
* 1 NO_AUTOMATIC_DISABLE: the RA can only be enabled when synchronized.
* 2 INTERRUPT_WHEN_SEQUENCE_IS_EMPTY: additionally the sequence is interrupted when it is empty and
  can only be continued when synchronized.
* 3 IMMEDIATE_INTERRUPT: additionally the sequence is interrupted at once.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.types import RaSequenceState, RobotLibraryErrorIdEnum, SyncMode, SyncReaction, SyncTime
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import execute, fb, move_axes, order, state, watch

E = RobotLibraryErrorIdEnum
RI_INITIALIZED, RI_SYNCHRONIZED = 71, 72
REACTIONS_WITH_ENABLE_CHECK = [
    pytest.param(SyncReaction.NO_AUTOMATIC_DISABLE, id="no-automatic-disable"),
    pytest.param(SyncReaction.INTERRUPT_WHEN_SEQUENCE_IS_EMPTY, id="interrupt-when-empty"),
    pytest.param(SyncReaction.IMMEDIATE_INTERRUPT, id="interrupt-immediately"),
]


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    fake = FakeClock()
    with use_clock(fake):
        yield fake


def _running(
    sdk: SdkSimulator, clock: FakeClock, reaction: int, after: int, delay_ms: int = 0
) -> RobotTaskHarness:
    """Synchronized RobotTask (software limits) with ``reaction``; the RC errors are reset (GroupReset)."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    modes = h.cfg.Plc.Parameter.SynchronizationModes.SWLimits
    modes[SyncTime.DURING_START_UP] = SyncMode.CLIENT_TO_SERVER
    modes[SyncTime.AFTER_START_UP] = SyncMode(after)
    h.cfg.Rob.Parameter.SyncReaction = SyncReaction(reaction)
    h.cfg.Rob.Parameter.SyncDelay = delay_ms
    h.run(1500, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    reset = fb(h, "MC_GroupResetFB")
    assert execute(h, reset).final["Done"]
    return h


def _lose_sync(h: RobotTaskHarness) -> None:
    """Change the PLC data (not transferred with NO_SYNCHRONIZATION after the start-up)."""
    h.sw_limits.J1UpperLimit = 150.0
    h.run(100, until=lambda: not h.rt.Synchronized)
    h.run(20)
    assert not h.rt.Synchronized and not h.rt.Error, h.history


def _enable(h: RobotTaskHarness, on: bool = True) -> Any:
    en = fb(h, "MC_EnableRobotFB", Enable=on)
    h.run(200, until=lambda: bool(en.Enabled or en.Error) if on else not en.Busy)
    return en


def _interrupted(h: RobotTaskHarness) -> bool:
    return h.ag.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.INTERRUPTED


def _robot_enabled(h: RobotTaskHarness) -> bool:
    return bool(h.ag.Cyclic.RobToPlc.StatusRobotArm.Enabled)


# ---------------------------------------------------------------- no reaction


@pytest.mark.parametrize("synchronized", [False, True], ids=["not-synchronized", "synchronized"])
def test_no_reaction_enable_is_independent_of_the_synchronization(
    sdk: SdkSimulator, clock: FakeClock, synchronized: bool
) -> None:
    """SyncReaction 0: the robot can be enabled whether the client is synchronized or not.

    The data are changed on the PLC before the robot is enabled (not synchronized afterwards) or not
    changed (synchronized); EnableRobot shows Busy then Enabled, the RC is not interrupted.
    """
    h = _running(sdk, clock, SyncReaction.NO_REACTION, SyncMode.NO_SYNCHRONIZATION)
    if not synchronized:
        _lose_sync(h)
    en = fb(h, "MC_EnableRobotFB")
    en.Enable = True
    seen = watch(h, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(seen, "Busy", "Enabled") and not en.Error, state(en)
    assert _robot_enabled(h) and not _interrupted(h)
    assert h.rt.Synchronized == synchronized and not h.rt.Error and not h.rt.WarningID


# ---------------------------------------------------------------- enable / continue only when synchronized


@pytest.mark.parametrize("reaction", REACTIONS_WITH_ENABLE_CHECK)
def test_enable_is_refused_when_not_synchronized(sdk: SdkSimulator, clock: FakeClock, reaction: int) -> None:
    """SyncReaction 1..3: enabling while the client is not synchronized ends with the RC error "not synchronized".

    EnableRobot shows Busy then Error with ERR_RI_NOT_SYNCHRONIZED, the robot stays disabled; a
    GroupContinue afterwards ends with an error as well. With 2 and 3 the sequence of the RC is
    interrupted.
    """
    h = _running(sdk, clock, reaction, SyncMode.NO_SYNCHRONIZATION)
    _lose_sync(h)
    en = fb(h, "MC_EnableRobotFB")
    en.Enable = True
    seen = watch(h, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(seen, "Busy", "Error") and not en.Enabled, state(en)
    assert en.ErrorID == E.ERR_RI_NOT_SYNCHRONIZED, hex(en.ErrorID)
    assert not _robot_enabled(h)
    cont = fb(h, "MC_GroupContinueFB")
    s = execute(h, cont)
    assert s.final["Error"] and not s.final["Done"], s.final
    assert _interrupted(h) == (reaction != SyncReaction.NO_AUTOMATIC_DISABLE)
    assert not h.rt.Error


@pytest.mark.parametrize("reaction", REACTIONS_WITH_ENABLE_CHECK[:2])
def test_enable_is_allowed_after_resynchronization(
    sdk: SdkSimulator, clock: FakeClock, reaction: int
) -> None:
    """SyncReaction 1 / 2: data changed with AUTOMATIC are synchronized again, then enable and continue work.

    The PLC change is written to the RC (Synchronized drops and comes back); EnableRobot shows
    Busy then Enabled and GroupContinue Busy then Done; the RC sequence is not interrupted afterwards.
    """
    h = _running(sdk, clock, reaction, SyncMode.AUTOMATIC)
    h.sw_limits.J1UpperLimit = 150.0
    h.run(400)
    assert h.rt.Synchronized and not h.rt.Error, h.history
    en = fb(h, "MC_EnableRobotFB")
    en.Enable = True
    seen = watch(h, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(seen, "Busy", "Enabled") and not en.Error, state(en)
    cont = fb(h, "MC_GroupContinueFB")
    s = execute(h, cont)
    assert order(s, "Busy", "Done") and not s.final["Error"], s.final
    assert _robot_enabled(h) and not _interrupted(h)


@pytest.mark.parametrize("reaction", REACTIONS_WITH_ENABLE_CHECK)
def test_robot_stays_enabled_when_data_change(sdk: SdkSimulator, clock: FakeClock, reaction: int) -> None:
    """SyncReaction 1..3: a data change while the robot is enabled does not disable the robot on the RC.

    The change is synchronized again (AUTOMATIC), Synchronized comes back to TRUE without error and
    warning, and the RC still reports the robot enabled (no automatic disable).
    """
    h = _running(sdk, clock, reaction, SyncMode.AUTOMATIC)
    en = _enable(h)
    assert en.Enabled and not en.Error, state(en)
    h.sw_limits.J1UpperLimit = 150.0
    h.run(400)
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    assert _robot_enabled(h) and sdk.enabled


@pytest.mark.parametrize("reaction", REACTIONS_WITH_ENABLE_CHECK)
def test_enable_block_stays_enabled_when_data_change(
    sdk: SdkSimulator, clock: FakeClock, reaction: int
) -> None:
    """SyncReaction 1..3: the EnableRobot block keeps Enabled without error when the data change and are resynchronized."""
    h = _running(sdk, clock, reaction, SyncMode.AUTOMATIC)
    en = _enable(h)
    assert en.Enabled and not en.Error, state(en)
    h.sw_limits.J1UpperLimit = 150.0
    h.run(400)
    assert h.rt.Synchronized
    assert en.Enabled and not en.Error, state(en)


@pytest.mark.parametrize("reaction", REACTIONS_WITH_ENABLE_CHECK[1:])
def test_continue_is_refused_when_not_synchronized(
    sdk: SdkSimulator, clock: FakeClock, reaction: int
) -> None:
    """SyncReaction 2 / 3: when the sync is lost the robot stays enabled, but it cannot be continued or enabled again.

    The robot is enabled and continued while synchronized; then the PLC data change (not
    transferred). The robot is not disabled automatically and the sequence is interrupted;
    GroupContinue ends with ERR_RI_NOT_SYNCHRONIZED_CONTINUE_DENIED; after a disable a new enable ends
    with ERR_RI_NOT_SYNCHRONIZED.
    """
    h = _running(sdk, clock, reaction, SyncMode.NO_SYNCHRONIZATION)
    en = _enable(h)
    assert en.Enabled, state(en)
    first = fb(h, "MC_GroupContinueFB")
    assert execute(h, first).final["Done"]
    _lose_sync(h)
    h.run(50)
    assert en.Enabled and _robot_enabled(h), "no automatic disable"
    assert _interrupted(h)
    cont = fb(h, "MC_GroupContinueFB")
    s = execute(h, cont)
    assert order(s, "Busy", "Error"), s.flags
    assert s.final["ErrorID"] == E.ERR_RI_NOT_SYNCHRONIZED_CONTINUE_DENIED, hex(s.final["ErrorID"])
    en.Enable = False
    h.run(200, until=lambda: not _robot_enabled(h))
    h.run(5)
    again = _enable(h)
    assert again.Error and again.ErrorID == E.ERR_RI_NOT_SYNCHRONIZED, state(again)


# ---------------------------------------------------------------- change during a motion


@pytest.mark.parametrize(
    ("reaction", "motion_flag"),
    [
        pytest.param(SyncReaction.INTERRUPT_WHEN_SEQUENCE_IS_EMPTY, "Done", id="interrupt-when-empty"),
        pytest.param(SyncReaction.IMMEDIATE_INTERRUPT, "CommandInterrupted", id="interrupt-immediately"),
    ],
)
def test_data_change_during_a_motion(
    sdk: SdkSimulator, clock: FakeClock, reaction: int, motion_flag: str
) -> None:
    """A data change during a motion: reaction 2 lets the motion end (Done), reaction 3 interrupts it at once.

    In both cases the RC sequence is interrupted afterwards and the robot stays enabled.
    """
    sdk.set_move_cycles(100)
    h = _running(sdk, clock, reaction, SyncMode.NO_SYNCHRONIZATION)
    en = _enable(h)
    assert execute(h, fb(h, "MC_GroupContinueFB")).final["Done"]
    mv = move_axes(h, 30.0)
    mv.Execute = True
    h.run(30)
    assert mv.Active, state(mv)
    h.sw_limits.J1UpperLimit = 150.0
    seen = watch(
        h, [mv], 400, lambda: bool(mv.Done or mv.Error or mv.CommandInterrupted) and _interrupted(h)
    )[0]
    assert order(seen, "Busy", "CommandBuffered", "Active", motion_flag), seen.flags
    assert not mv.Error and _interrupted(h)
    if motion_flag == "Done":
        assert sdk.joints[0] == pytest.approx(30.0)
    else:
        assert sdk.joints[0] < 30.0
    assert en.Enabled and _robot_enabled(h)


# ---------------------------------------------------------------- sync delay


def test_sync_delay_postpones_the_reaction(sdk: SdkSimulator, clock: FakeClock) -> None:
    """SyncDelay: the RC keeps "synchronized" for the delay after the loss, then it interrupts the sequence.

    SyncReaction 3, SyncDelay 1000 ms (real time of the RC). Directly after the change the RC is
    still synchronized and the robot can be enabled; after the delay the RC state is "not
    synchronized", the sequence is interrupted, and a new enable is refused.
    """
    h = _running(sdk, clock, SyncReaction.IMMEDIATE_INTERRUPT, SyncMode.NO_SYNCHRONIZATION, delay_ms=1000)
    en = _enable(h)
    assert execute(h, fb(h, "MC_GroupContinueFB")).final["Done"]
    en.Enable = False
    h.run(200, until=lambda: not _robot_enabled(h))
    t0 = time.monotonic()
    _lose_sync(h)
    assert sdk.states.ri_state == RI_SYNCHRONIZED and not _interrupted(h), "the RC waits for the delay"
    early = _enable(h)
    assert early.Enabled and not early.Error and time.monotonic() - t0 < 1.0, state(early)
    deadline = t0 + 5.0
    while not (sdk.states.ri_state == RI_INITIALIZED and _interrupted(h)) and time.monotonic() < deadline:
        h.run(10)
    assert sdk.states.ri_state == RI_INITIALIZED and _interrupted(h)
    assert time.monotonic() - t0 >= 1.0
    early.Enable = False
    h.run(200, until=lambda: not _robot_enabled(h))
    h.run(5)
    late = _enable(h)
    assert late.Error and late.ErrorID == E.ERR_RI_NOT_SYNCHRONIZED, state(late)


# ---------------------------------------------------------------- undefined reaction


def test_undefined_sync_reaction(sdk: SdkSimulator, clock: FakeClock) -> None:
    """SyncReaction 4 (undefined) is rejected: RobotTask error, entry in the message log, not initialized."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    h.cfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] = SyncMode.CLIENT_TO_SERVER
    h.cfg.Rob.Parameter.SyncReaction = 4  # type: ignore[assignment]  # undefined value on purpose
    h.run(300, until=lambda: bool(h.rt.Error))
    h.run(10)
    assert h.rt.Error and h.rt.ErrorID == E.ERR_INVALID_PAR_CMD, h.history
    assert not h.rt.Initialized and not h.rt.Synchronized
    texts = [m.MessageText for m in h.ag.MessageLog.Messages if m.MessageText]
    assert any("Invalid command parameter" in t for t in texts), texts
