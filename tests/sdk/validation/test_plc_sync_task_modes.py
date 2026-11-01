# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_plc_sync_task_modes
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the user data synchronization of the RobotTask: modes
#    during and after the start-up, user interaction, invalid modes and
#    modes changed while the RobotTask runs, for all data sets.
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

"""Validation of the user data synchronization of the RobotTask (spec 5.6.7) against the SDK simulator.

Every test runs for the six data sets the simulator stores (tools, frames, loads, software limits,
default and reference dynamics). The configuration of a data set is the pair of synchronization
modes ``SynchronizationModes.<set>[DURING_START_UP, AFTER_START_UP]`` (table 5-109) plus the flag
``SyncUserInteraction.<set>``. The modes are read when the RobotTask starts; a mode changed while
it runs is reported with an info and used from the next start-up on.

A "difference at the start-up" is made like this: a first RobotTask copies the data of the RC into
the PLC data, then one value of the PLC data is changed before the RobotTask under test starts.
Changes on the RC side are made like with a teach pendant (``SdkSimulator.rc_change``).
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.iec.clock import FakeClock, use_clock
from srci.iec.rt import copy_into
from srci.types import (
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    RobotLibraryWarningIdEnum,
    SyncMode,
    SyncTime,
)
from tests.robot_task_harness import SIZE, RobotTaskHarness

E = RobotLibraryErrorIdEnum
W = RobotLibraryWarningIdEnum
I = RobotLibraryInfoIdEnum  # noqa: E741

NONE = SyncMode.NO_SYNCHRONIZATION
C2S = SyncMode.CLIENT_TO_SERVER
S2C = SyncMode.SERVER_TO_CLIENT
AUTO = SyncMode.AUTOMATIC
UNDEFINED = 5  # no SyncMode value (0..3)

START_UP_CYCLES = 1500
WATCH_CYCLES = 400
RESTART_CYCLES = 50


@dataclass(frozen=True)
class DataSet:
    """A data set of table 5-106: how the test changes it and which messages belong to it."""

    name: str  # item of SynchronizationModes / SyncUserInteraction
    in_sync: str  # item of SyncStatePlc.InSync
    get: Callable[[RobotTaskHarness], float]
    put: Callable[[RobotTaskHarness, float], None]
    plc_value: float  # value of a change on the PLC
    rc_kind: int  # SdkSimulator.rc_change
    rc_no: int
    rc_values: tuple[float, ...]
    rc_value: float  # PLC value after the RC change was read
    write_log: str  # command names in the SDK log
    read_log: str
    mode_invalid: int
    user_conflict: int
    both_sides: int
    mode_changed: int


def _tool(h: RobotTaskHarness) -> Any:
    return h.tools[1].Data


def _frame(h: RobotTaskHarness) -> Any:
    return h.frames[1].Data


def _load(h: RobotTaskHarness) -> Any:
    return h.loads[1].Data


DATA_SETS = [
    DataSet(
        "Tool",
        "Tool",
        lambda h: _tool(h).X,
        lambda h, v: setattr(_tool(h), "X", v),
        12.5,
        SdkSimulator.RC_TOOL,
        1,
        (7.5, 0.0, 0.0, 0.0, 0.0, 0.0),
        7.5,
        "WriteToolData",
        "ReadToolData",
        W.WARN_TOOL_DATA_SYNC_MODE_INVALID,
        W.WARN_TOOL_NUMBER_SYNC_ERROR,
        W.WARN_TOOL_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "Frame",
        "Frame",
        lambda h: _frame(h).X,
        lambda h, v: setattr(_frame(h), "X", v),
        12.5,
        SdkSimulator.RC_FRAME,
        1,
        (7.5, 0.0, 0.0, 0.0, 0.0, 0.0),
        7.5,
        "WriteFrameData",
        "ReadFrameData",
        W.WARN_FRAME_DATA_SYNC_MODE_INVALID,
        W.WARN_FRAME_NUMBER_SYNC_ERROR,
        W.WARN_FRAME_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "Load",
        "Load",
        lambda h: _load(h).Mass,
        lambda h, v: setattr(_load(h), "Mass", v),
        2.5,
        SdkSimulator.RC_LOAD,
        1,
        (4.5, 0.0, 0.0, 0.0),
        4.5,
        "WriteLoadData",
        "ReadLoadData",
        W.WARN_LOAD_DATA_SYNC_MODE_INVALID,
        W.WARN_LOAD_NUMBER_SYNC_ERROR,
        W.WARN_LOAD_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "SWLimits",
        "SwLimits",
        lambda h: h.sw_limits.J1UpperLimit,
        lambda h, v: setattr(h.sw_limits, "J1UpperLimit", v),
        150.0,
        SdkSimulator.RC_SW_LIMITS,
        0,
        (-160.0, 160.0) * 6,
        160.0,
        "WriteSWLimits",
        "ReadRobotSWLimits",
        W.WARN_SW_LIMITS_SYNC_MODE_INVALID,
        W.WARN_SW_LIMITS_SYNC_ERROR,
        W.WARN_SW_LIMITS_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "DefaultDynamics",
        "DefaultDynamics",
        lambda h: h.default_dynamics.VelocityRate,
        lambda h, v: setattr(h.default_dynamics, "VelocityRate", v),
        33.0,
        SdkSimulator.RC_DEFAULT_DYNAMICS,
        0,
        (55.0, 60.0, 65.0, 70.0),
        55.0,
        "WriteDefaultDynamics",
        "ReadDefaultDynamics",
        W.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID,
        W.WARN_DEFAULT_DYNAMICS_SYNC_ERROR,
        W.WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "ReferenceDynamics",
        "ReferenceDynamics",
        lambda h: h.reference_dynamics.VelocityReference,
        lambda h, v: setattr(h.reference_dynamics, "VelocityReference", v),
        777.0,
        SdkSimulator.RC_REFERENCE_DYNAMICS,
        0,
        (500.0, 600.0, 700.0, 800.0),
        500.0,
        "WriteReferenceDynamics",
        "ReadReferenceDynamics",
        W.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID,
        W.WARN_REFERENCE_DYNAMICS_SYNC_ERROR,
        W.WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED,
        I.INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
]
IDS = [d.name for d in DATA_SETS]
MODE_NAMES = {NONE: "none", C2S: "c2s", S2C: "s2c", AUTO: "auto"}


# ---------------------------------------------------------------- helpers


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    fake = FakeClock()
    with use_clock(fake):
        yield fake


def _harness(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, start: int, after: int, user: bool = False
) -> RobotTaskHarness:
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    _set_modes(h, data, start, after)
    setattr(h.cfg.Plc.Parameter.SyncUserInteraction, data.name, user)
    return h


def _set_modes(h: RobotTaskHarness, data: DataSet, start: int, after: int) -> None:
    modes = getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)
    modes[SyncTime.DURING_START_UP] = start
    modes[SyncTime.AFTER_START_UP] = after


def _take_over_rc_data(sdk: SdkSimulator, clock: FakeClock, data: DataSet, h: RobotTaskHarness) -> None:
    """The PLC data of ``h`` are made equal to the RC data (a first RobotTask reads them and is stopped)."""
    first = _harness(sdk, clock, data, S2C, S2C)
    first.run(START_UP_CYCLES, until=lambda: bool(first.rt.Synchronized or first.rt.Error))
    assert first.rt.Synchronized, first.history
    first.enable = False
    first.run(RESTART_CYCLES)
    sdk.reset()  # the SDK notices a stopped client only by its real-time lifesign timeout
    for name in ("sw_limits", "default_dynamics", "reference_dynamics"):
        copy_into(getattr(h, name), getattr(first, name))
    for name in ("tools", "frames", "loads"):
        for target, source in zip(getattr(h, name), getattr(first, name), strict=True):
            copy_into(target, source)


def _start_up(h: RobotTaskHarness, until: Callable[[], bool] | None = None) -> None:
    h.run(START_UP_CYCLES, until=until or (lambda: bool(h.rt.Synchronized or h.rt.Error or h.rt.WarningID)))
    h.run(20)


def _count(sdk: SdkSimulator, name: str, since: int) -> int:
    return sum(
        1 for log in sdk.logs[since:] if f"(type: {name} (" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def _transfers(sdk: SdkSimulator, data: DataSet, since: int) -> tuple[int, int]:
    return _count(sdk, data.write_log, since), _count(sdk, data.read_log, since)


def _change(sdk: SdkSimulator, h: RobotTaskHarness, data: DataSet, side: str) -> None:
    if side == "plc":
        data.put(h, data.plc_value)
    else:
        sdk.rc_change(data.rc_kind, data.rc_no, list(data.rc_values))


def _watch(h: RobotTaskHarness, cycles: int = WATCH_CYCLES) -> list[bool]:
    seen = []
    for _ in range(cycles):
        h.cycle()
        seen.append(bool(h.rt.Synchronized))
    return seen


def _restart(h: RobotTaskHarness) -> None:
    h.enable = False
    h.run(RESTART_CYCLES)
    h.enable = True


# ---------------------------------------------------------------- invalid modes at the start-up


INVALID_AT_START = [
    pytest.param(AUTO, AUTO, id="auto-auto"),
    pytest.param(AUTO, S2C, id="auto-s2c"),
    pytest.param(AUTO, C2S, id="auto-c2s"),
    pytest.param(UNDEFINED, UNDEFINED, id="undefined"),
]


@pytest.mark.parametrize(("start", "after"), INVALID_AT_START)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_invalid_mode_at_start_up_is_reported(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, start: int, after: int
) -> None:
    """An invalid start-up mode (AUTOMATIC or undefined) gives the mode warning of the data set and no synchronization.

    AUTOMATIC is not available during the start-up (table 5-109). Nothing of the data set is read or
    written and the RobotTask is not synchronized.
    """
    h = _harness(sdk, clock, data, start, after)
    data.put(h, data.plc_value)
    h.run(300, until=lambda: bool(h.rt.WarningID))
    h.run(50)
    assert h.rt.WarningID == data.mode_invalid, hex(h.rt.WarningID)
    assert not h.rt.Synchronized
    assert _transfers(sdk, data, 0) == (0, 0)
    assert data.get(h) == data.plc_value


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F130: an invalid SyncMode also sets the own (non-spec) error ERR_SYNC_MODE_INVALID and stops the "
    "initialization; the spec only defines the warning WARN_*_SYNC_MODE_INVALID (16#7011 ...), the RobotTask "
    "should stay initialized without error (MC_RobotTaskFB.CheckParameterValid)",
)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_invalid_mode_at_start_up_is_only_a_warning(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet
) -> None:
    """An invalid start-up mode leaves the RobotTask initialized without error, only the mode warning is set."""
    h = _harness(sdk, clock, data, AUTO, AUTO)
    h.run(300, until=lambda: bool(h.rt.WarningID))
    h.run(50)
    assert h.rt.WarningID == data.mode_invalid
    assert not h.rt.Error and h.rt.Initialized and not h.rt.Synchronized, h.history


# ---------------------------------------------------------------- data set without synchronization


def _other(data: DataSet) -> DataSet:
    return DATA_SETS[4] if data.name == "SWLimits" else DATA_SETS[3]


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_data_set_without_synchronization_is_not_compared(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet
) -> None:
    """A data set with NO_SYNCHRONIZATION during and after the start-up does not affect Synchronized.

    Another data set is synchronized (CLIENT_TO_SERVER); the data set under test is changed on the PLC
    and on the RC: Synchronized stays TRUE, nothing of it is transferred, no warning and no error.
    """
    other = _other(data)
    h = _harness(sdk, clock, other, C2S, C2S)
    _set_modes(h, data, NONE, NONE)
    _start_up(h)
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    assert not getattr(
        h.ag.State.DataEnableSync, f"EnableSync{'SWLimits' if data.name == 'SWLimits' else data.name}"
    )
    since = len(sdk.logs)
    _change(sdk, h, data, "plc")
    _change(sdk, h, data, "rc")
    seen = _watch(h)
    assert all(seen) and not h.rt.Error and not h.rt.WarningID, h.history
    assert _transfers(sdk, data, since) == (0, 0)
    assert data.get(h) == data.plc_value


def test_all_data_sets_without_synchronization(sdk: SdkSimulator, clock: FakeClock) -> None:
    """All data sets without synchronization: the RobotTask is initialized, never synchronized, no error.

    Changes of the data on the PLC have no influence on the synchronization state and nothing is transferred.
    """
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    h.run(300, until=lambda: bool(h.rt.Initialized))
    h.run(100)
    assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    since = len(sdk.logs)
    for data in DATA_SETS:
        _change(sdk, h, data, "plc")
    seen = _watch(h)
    assert not any(seen) and h.rt.Initialized and not h.rt.Error and not h.rt.WarningID
    for data in DATA_SETS:
        assert _transfers(sdk, data, since) == (0, 0), data.name
    sync = h.ag.State.SyncStatePlc.InSync
    assert not any(getattr(sync, d.in_sync) for d in DATA_SETS)


def test_all_data_sets_switched_off_while_running(sdk: SdkSimulator, clock: FakeClock) -> None:
    """Synchronization switched off for all data sets while synchronized: used only after a restart.

    While the RobotTask runs the old modes stay active (Synchronized TRUE). After the restart the
    RobotTask is initialized but not synchronized, without error, and a change has no effect.
    """
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    for data in DATA_SETS:
        _set_modes(h, data, C2S, C2S)
    _start_up(h, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    for data in DATA_SETS:
        _set_modes(h, data, NONE, NONE)
    h.run(100)
    assert h.rt.Synchronized and not h.rt.Error, "the old modes stay active until the restart"
    _restart(h)
    h.run(300, until=lambda: bool(h.rt.Initialized))
    h.run(100)
    since = len(sdk.logs)
    for data in DATA_SETS:
        _change(sdk, h, data, "plc")
    seen = _watch(h)
    assert not any(seen) and h.rt.Initialized and not h.rt.Error and not h.rt.WarningID, h.history
    for data in DATA_SETS:
        assert _transfers(sdk, data, since) == (0, 0), data.name


# ---------------------------------------------------------------- no synchronization during the start-up


AFTER_ONLY_EQUAL = [
    pytest.param(C2S, ("plc", "rc"), id="c2s-plc-then-rc"),
    pytest.param(S2C, ("rc", "plc"), id="s2c-rc-then-plc"),
    pytest.param(AUTO, ("rc",), id="auto-rc"),
    pytest.param(AUTO, ("plc",), id="auto-plc"),
]


@pytest.mark.parametrize(("after", "sides"), AFTER_ONLY_EQUAL)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_after_start_up_mode_with_equal_data(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, after: int, sides: tuple[str, ...]
) -> None:
    """Without start-up synchronization and equal data, later changes are synchronized in the after-start-up direction.

    CLIENT_TO_SERVER: changes on the PLC are written, changes on the RC are overwritten with the PLC
    data. SERVER_TO_CLIENT: changes on the RC are read, changes on the PLC are overwritten with the RC
    data. AUTOMATIC: the side changed last wins. Synchronized drops while the data differ and comes back.
    """
    h = _harness(sdk, clock, data, NONE, after)
    _take_over_rc_data(sdk, clock, data, h)
    _start_up(h)
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    before = data.get(h)
    since = len(sdk.logs)
    for side in sides:
        _change(sdk, h, data, side)
        seen = _watch(h)
        assert not all(seen), f"Synchronized must drop after the change on the {side}"
        assert seen[-1] and not h.rt.Error and not h.rt.WarningID, h.history
    writes, reads = _transfers(sdk, data, since)
    if after == C2S:
        assert data.get(h) == data.plc_value and writes >= 2 and reads == 0
    elif after == S2C:
        assert data.get(h) == data.rc_value and reads >= 1
    elif sides == ("plc",):
        assert data.get(h) == data.plc_value and writes == 1 and reads == 0
    else:
        assert data.get(h) == data.rc_value and reads >= 1
    assert data.get(h) != before


AFTER_ONLY_DIFFERENT = [
    pytest.param(C2S, None, id="c2s"),
    pytest.param(S2C, None, id="s2c"),
    pytest.param(AUTO, None, id="auto"),
    pytest.param(AUTO, "plc", id="auto-then-plc-change"),
    pytest.param(AUTO, "rc", id="auto-then-rc-change"),
]


@pytest.mark.parametrize(("after", "side"), AFTER_ONLY_DIFFERENT)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_after_start_up_mode_with_a_difference_at_the_start_up(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, after: int, side: str | None
) -> None:
    """Without start-up synchronization a difference found at the start-up is handled like a change after it.

    CLIENT_TO_SERVER writes the PLC data, SERVER_TO_CLIENT reads the RC data, both end synchronized.
    AUTOMATIC cannot decide which side changed: warning "changed on both sides", not synchronized,
    nothing is transferred - also not after a further change on the PLC or the RC.
    """
    h = _harness(sdk, clock, data, NONE, after)
    _take_over_rc_data(sdk, clock, data, h)
    rc_before = data.get(h)
    data.put(h, data.plc_value)
    _start_up(h)
    h.run(200)
    writes, reads = _transfers(sdk, data, 0)
    assert not h.rt.Error, h.history
    if after == C2S:
        assert h.rt.Synchronized and not h.rt.WarningID and writes >= 1
        assert data.get(h) == data.plc_value
    elif after == S2C:
        assert h.rt.Synchronized and not h.rt.WarningID and reads >= 1
        assert data.get(h) == rc_before
    else:
        assert not h.rt.Synchronized and h.rt.WarningID == data.both_sides, hex(h.rt.WarningID)
        assert data.get(h) == data.plc_value
        assert not getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync)
        if side is not None:
            since = len(sdk.logs)
            if side == "plc":
                data.put(h, data.plc_value + 1.0)
            else:
                _change(sdk, h, data, "rc")
            seen = _watch(h)
            assert not any(seen) and not h.rt.Error
            assert _transfers(sdk, data, since) == (0, 0)


# ---------------------------------------------------------------- synchronization during and after the start-up


START_AND_AFTER = [
    pytest.param(C2S, C2S, ("plc",), id="c2s-c2s-plc"),
    pytest.param(C2S, C2S, ("rc",), id="c2s-c2s-rc"),
    pytest.param(C2S, C2S, ("plc", "rc"), id="c2s-c2s-plc-then-rc"),
    pytest.param(C2S, AUTO, ("plc",), id="c2s-auto-plc"),
    pytest.param(S2C, C2S, ("plc",), id="s2c-c2s-plc"),
    pytest.param(S2C, C2S, ("rc",), id="s2c-c2s-rc"),
    pytest.param(S2C, AUTO, ("plc",), id="s2c-auto-plc"),
]


@pytest.mark.parametrize(("start", "after", "sides"), START_AND_AFTER)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_start_up_direction_then_after_start_up_direction(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, start: int, after: int, sides: tuple[str, ...]
) -> None:
    """A difference at the start-up is resolved in the start-up direction, later changes in the after-start-up one.

    Without user interaction: CLIENT_TO_SERVER at the start-up writes the PLC data, SERVER_TO_CLIENT
    reads the RC data; the RobotTask becomes synchronized without warning. A later change on the PLC
    or the RC is handled like configured for the time after the start-up.
    """
    h = _harness(sdk, clock, data, start, after)
    _take_over_rc_data(sdk, clock, data, h)
    rc_before = data.get(h)
    data.put(h, data.plc_value - 1.0)
    _start_up(h, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    writes, reads = _transfers(sdk, data, 0)
    if start == C2S:
        assert data.get(h) == data.plc_value - 1.0 and writes >= 1
    else:
        assert data.get(h) == rc_before and reads >= 1
    for side in sides:
        before = data.get(h)
        _change(sdk, h, data, side)
        seen = _watch(h)
        assert not all(seen), f"Synchronized must drop after the change on the {side}"
        assert seen[-1] and not h.rt.Error and not h.rt.WarningID, h.history
        if side == "plc" and after in (C2S, AUTO):
            assert data.get(h) == data.plc_value, "the PLC change is kept"
        elif side == "rc" and after == C2S:
            assert data.get(h) == before, "the RC change is overwritten with the PLC data"
        else:
            assert data.get(h) == data.rc_value, "the RC data are read"


USER_INTERACTION = [
    pytest.param(C2S, C2S, id="c2s-c2s"),
    pytest.param(C2S, S2C, id="c2s-s2c"),
    pytest.param(C2S, AUTO, id="c2s-auto"),
    pytest.param(S2C, C2S, id="s2c-c2s"),
    pytest.param(S2C, S2C, id="s2c-s2c"),
    pytest.param(S2C, AUTO, id="s2c-auto"),
]


@pytest.mark.parametrize(("start", "after"), USER_INTERACTION)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_start_up_difference_with_user_interaction(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, start: int, after: int
) -> None:
    """With user interaction a difference at the start-up is not resolved: sync warning, not synchronized.

    The RobotTask is initialized without error, reports the synchronization warning of the data set
    (input of the user needed) and neither reads nor writes the data set; the PLC data stay unchanged.
    """
    h = _harness(sdk, clock, data, start, after, user=True)
    _take_over_rc_data(sdk, clock, data, h)
    since = len(sdk.logs)
    data.put(h, data.plc_value)
    _start_up(h)
    h.run(200)
    assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error, h.history
    assert h.rt.WarningID == data.user_conflict, hex(h.rt.WarningID)
    assert _count(sdk, data.write_log, since) == 0
    assert data.get(h) == data.plc_value


# ---------------------------------------------------------------- modes changed while the RobotTask runs


@dataclass(frozen=True)
class OnlineChange:
    start: tuple[int, int]  # modes at the start of the RobotTask
    new: tuple[int, int]  # modes written while it runs
    side: str | None  # data changed afterwards (plc / rc)


ONLINE = [
    pytest.param(OnlineChange((S2C, AUTO), (UNDEFINED, UNDEFINED), "plc"), id="synced-to-undefined"),
    pytest.param(OnlineChange((NONE, NONE), (AUTO, AUTO), "plc"), id="none-to-auto-at-start-up"),
    pytest.param(OnlineChange((NONE, NONE), (NONE, C2S), "plc"), id="none-to-c2s-plc"),
    pytest.param(OnlineChange((NONE, NONE), (NONE, S2C), "plc"), id="none-to-s2c-plc"),
    pytest.param(OnlineChange((NONE, NONE), (NONE, S2C), "rc"), id="none-to-s2c-rc"),
    pytest.param(OnlineChange((NONE, NONE), (NONE, AUTO), "plc"), id="none-to-auto-plc"),
    pytest.param(OnlineChange((NONE, NONE), (NONE, AUTO), "rc"), id="none-to-auto-rc"),
    pytest.param(OnlineChange((NONE, NONE), (C2S, C2S), "plc"), id="none-to-c2s-c2s"),
    pytest.param(OnlineChange((NONE, NONE), (C2S, S2C), "plc"), id="none-to-c2s-s2c"),
    pytest.param(OnlineChange((NONE, NONE), (C2S, AUTO), "plc"), id="none-to-c2s-auto"),
    pytest.param(OnlineChange((NONE, NONE), (S2C, C2S), "plc"), id="none-to-s2c-c2s"),
    pytest.param(OnlineChange((NONE, NONE), (S2C, S2C), "plc"), id="none-to-s2c-s2c"),
    pytest.param(OnlineChange((NONE, NONE), (S2C, AUTO), "plc"), id="none-to-s2c-auto"),
]


@pytest.mark.parametrize("change", ONLINE)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_mode_changed_while_running_is_used_after_a_restart(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, change: OnlineChange
) -> None:
    """A mode changed while the RobotTask runs is reported with an info and only used after a restart.

    Until the restart the modes of the start stay active: a RobotTask started without synchronization
    transfers nothing and stays initialized, not synchronized; a synchronized data set keeps its old direction (also
    when the new mode is undefined - no error). After the restart a valid start-up mode resolves the
    difference made while running (CLIENT_TO_SERVER writes the PLC data, SERVER_TO_CLIENT reads the RC
    data), an invalid one gives the mode warning.
    """
    h = _harness(sdk, clock, data, *change.start)
    if change.start == (NONE, NONE):
        _start_up(h, until=lambda: bool(h.rt.Initialized or h.rt.Error))
        assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error, h.history
    else:
        _take_over_rc_data(sdk, clock, data, h)
        _start_up(h, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
        assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    _set_modes(h, data, *change.new)
    since = len(sdk.logs)
    assert change.side is not None
    _change(sdk, h, data, change.side)
    seen = _watch(h)
    assert h.rt.InfoID == data.mode_changed, hex(h.rt.InfoID)
    assert not h.rt.Error and not h.rt.WarningID, h.history
    if change.start == (NONE, NONE):
        assert not any(seen) and h.rt.Initialized, "the data set is still not synchronized"
        assert _transfers(sdk, data, since) == (0, 0)
    else:
        assert seen[-1], "the old mode (AUTOMATIC) synchronizes the change"
        assert _count(sdk, data.write_log, since) == 1
        return
    # restart with the new modes
    start, after = change.new
    since = len(sdk.logs)
    _restart(h)
    if start == AUTO:
        h.run(300, until=lambda: bool(h.rt.WarningID))
        assert h.rt.WarningID == data.mode_invalid and not h.rt.Synchronized
        return
    _start_up(h, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    if start == NONE and after == AUTO:
        # no start-up synchronization: AUTOMATIC cannot decide which side changed
        assert not h.rt.Synchronized and h.rt.WarningID == data.both_sides, hex(h.rt.WarningID)
        return
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    writes, reads = _transfers(sdk, data, since)
    direction = start if start != NONE else after
    if direction == S2C:
        assert reads >= 1, "the RC data are read"
        if change.side == "rc":
            assert data.get(h) == data.rc_value
        else:
            assert data.get(h) != data.plc_value, "the PLC change is overwritten with the RC data"
    else:
        assert writes >= 1, "the PLC data are written"
        assert data.get(h) == data.plc_value


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F131: MC_RobotTaskFB.CheckParameterChanged returns at once when Initialized is FALSE, and Initialized "
    "is set to NOT Synchronized (OnExecRun) - a mode changed while synchronized is reported only after the "
    "synchronization is lost",
)
def test_mode_change_is_reported_while_synchronized(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A mode changed while the RobotTask is synchronized is reported with the info at once."""
    data = DATA_SETS[3]
    h = _harness(sdk, clock, data, C2S, C2S)
    _start_up(h, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized, h.history
    _set_modes(h, data, C2S, S2C)
    h.run(20)
    assert h.rt.InfoID == data.mode_changed, hex(h.rt.InfoID)


# ---------------------------------------------------------------- more elements on the RC than on the PLC


@pytest.mark.parametrize("data", DATA_SETS[:3], ids=IDS[:3])
def test_more_elements_on_the_rc_than_in_the_plc_array(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet
) -> None:
    """The RC has 15 elements, the PLC array only 10: the count error of the data set, not synchronized.

    Spec 5.6.7.5.1: the RobotTask does not synchronize when the RC has more tools / frames / loads
    than the array of the PLC can hold.
    """
    sdk.set_highest_index(**{data.name.lower(): 14})
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, count=10)
    _set_modes(h, data, C2S, C2S)
    h.run(600, until=lambda: bool(h.rt.Error))
    expected = {
        "Tool": E.ERR_SYNC_TOOL_COUNT_RC_HIGHER_THAN_PLC,
        "Frame": E.ERR_SYNC_FRAME_COUNT_RC_HIGHER_THAN_PLC,
        "Load": E.ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC,
    }[data.name]
    assert h.rt.ErrorID == expected, h.history
    assert not h.rt.Synchronized
    assert _count(sdk, data.write_log, 0) == 0
