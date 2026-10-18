# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.test_sync
#  Author:      Thorsten Brach
#  Date:        2026-10-16
#
#  Description:
#    Synchronization of the user data (spec 5.6.7) against the SRCI SDK:
#    changes after the start-up, start-up conflicts, invalid and changed
#    synchronization modes.
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

"""Synchronization of the user data (spec 5.6.7) against the SRCI SDK.

Every data set of table 5-106 that the simulator stores (tools, frames, loads, software limits,
default and reference dynamics) is changed on the PLC after the start-up and the RobotTask has to
react according to the synchronization mode after the start-up (table 5-109); start-up conflicts
with user interaction, invalid modes and a mode changed while running complete the cases.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

import srci
from srci.iec.clock import FakeClock, use_clock
from srci.iec.rt import copy_into
from srci.types import (
    CmdType,
    RobotLibraryErrorIdEnum,
    RobotLibraryInfoIdEnum,
    RobotLibraryWarningIdEnum,
    SyncMode,
    SyncTime,
)
from srci.types.iec import new_instance
from tests.robot_task_harness import SIZE, RobotTaskHarness

W = RobotLibraryWarningIdEnum
E = RobotLibraryErrorIdEnum
I = RobotLibraryInfoIdEnum  # noqa: E741


@dataclass(frozen=True)
class DataSet:
    """A data set of table 5-106: how to change it on the PLC and how the client talks about it."""

    name: str  # item of SynchronizationModes / SyncStatePlc.InSync
    in_sync: str  # field of SyncStatePlc.InSync
    write: CmdType
    read: CmdType
    change: Callable[[RobotTaskHarness], None]
    value: Callable[[RobotTaskHarness], float]
    changed: float
    mode_invalid: int  # warning of an invalid synchronization mode
    user_conflict: int  # warning of a start-up conflict that needs the user
    write_fb: str
    write_input: Callable[[Any, RobotTaskHarness], None]
    mode_changed: int = 0  # info: synchronization mode changed while the RobotTask runs
    count_error: int = 0  # error: the RC has more elements than the array on the PLC (tools, frames, loads)


def _tool(h: RobotTaskHarness) -> None:
    h.tools[1].Data.X = 12.5


def _frame(h: RobotTaskHarness) -> None:
    h.frames[1].Data.X = 12.5


def _load(h: RobotTaskHarness) -> None:
    h.loads[1].Data.Mass = 2.5


def _sw(h: RobotTaskHarness) -> None:
    h.sw_limits.J1UpperLimit = 150.0


def _dd(h: RobotTaskHarness) -> None:
    h.default_dynamics.VelocityRate = 33.0


def _rd(h: RobotTaskHarness) -> None:
    h.reference_dynamics.VelocityReference = 777.0


def _write_sw(fb: Any, h: RobotTaskHarness) -> None:
    copy_into(fb.ParCmd.LimitValues, h.sw_limits)


def _write_dd(fb: Any, h: RobotTaskHarness) -> None:
    copy_into(fb.ParCmd.DynamicValues, h.default_dynamics)


def _write_rd(fb: Any, h: RobotTaskHarness) -> None:
    copy_into(fb.ParCmd.DynamicValues, h.reference_dynamics)


def _write_tool(fb: Any, h: RobotTaskHarness) -> None:
    fb.ParCmd.ToolNo = 1
    copy_into(fb.ParCmd.ToolData, h.tools[1].Data)


def _write_frame(fb: Any, h: RobotTaskHarness) -> None:
    fb.ParCmd.FrameNo = 1
    copy_into(fb.ParCmd.FrameData, h.frames[1].Data)


def _write_load(fb: Any, h: RobotTaskHarness) -> None:
    fb.ParCmd.LoadNo = 1
    copy_into(fb.ParCmd.LoadData, h.loads[1].Data)


def take_over_rc_data(sdk: SdkSimulator, clock: FakeClock, data: DataSet, h: RobotTaskHarness) -> None:
    """PLC data of ``h`` = data of the RC: a first RobotTask starts up with SERVER_TO_CLIENT and is stopped."""
    first = harness(sdk, clock, data, SyncMode.SERVER_TO_CLIENT, SyncMode.SERVER_TO_CLIENT)
    start_up(first)
    first.enable = False
    first.run(50)
    # the SDK notices the stopped client only by its lifesign timeout (real time, not the fake clock):
    # reset it so the second RobotTask starts up independent of the speed of the machine
    sdk.reset()
    for name in ("sw_limits", "default_dynamics", "reference_dynamics"):
        copy_into(getattr(h, name), getattr(first, name))
    for name in ("tools", "frames", "loads"):
        for target, source in zip(getattr(h, name), getattr(first, name), strict=True):
            copy_into(target, source)


def apply_read(fb: Any, h: RobotTaskHarness, data: DataSet) -> None:
    """The user takes over the RC data read by the read function (the read function does not change the PLC data)."""
    target, field = {
        "SWLimits": (h.sw_limits, "LimitValues"),
        "DefaultDynamics": (h.default_dynamics, "DynamicValues"),
        "ReferenceDynamics": (h.reference_dynamics, "DynamicValues"),
        "Tool": (h.tools[1].Data, "ToolData"),
        "Frame": (h.frames[1].Data, "FrameData"),
        "Load": (h.loads[1].Data, "LoadData"),
    }[data.name]
    source = getattr(fb.OutCmd, field)
    copy_into(target, source)


# a second change of the data sets (other values than the first change)
SECOND_CHANGE: dict[str, Callable[[RobotTaskHarness], None]] = {
    "SWLimits": lambda h: setattr(h.sw_limits, "J1UpperLimit", 140.0),
    "DefaultDynamics": lambda h: setattr(h.default_dynamics, "VelocityRate", 44.0),
    "ReferenceDynamics": lambda h: setattr(h.reference_dynamics, "VelocityReference", 888.0),
    "Tool": lambda h: setattr(h.tools[1].Data, "X", 22.5),
    "Frame": lambda h: setattr(h.frames[1].Data, "X", 22.5),
    "Load": lambda h: setattr(h.loads[1].Data, "Mass", 3.5),
}

DATA_SETS = [
    DataSet(
        "SWLimits",
        "SwLimits",
        CmdType.WriteRobotSWLimits,
        CmdType.ReadRobotSWLimits,
        _sw,
        lambda h: h.sw_limits.J1UpperLimit,
        150.0,
        W.WARN_SW_LIMITS_SYNC_MODE_INVALID,
        W.WARN_SW_LIMITS_SYNC_ERROR,
        "MC_WriteRobotSWLimitsFB",
        _write_sw,
        I.INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "DefaultDynamics",
        "DefaultDynamics",
        CmdType.WriteRobotDefaultDynamics,
        CmdType.ReadRobotDefaultDynamics,
        _dd,
        lambda h: h.default_dynamics.VelocityRate,
        33.0,
        W.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID,
        W.WARN_DEFAULT_DYNAMICS_SYNC_ERROR,
        "MC_WriteRobotDefaultDynamicsFB",
        _write_dd,
        I.INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "ReferenceDynamics",
        "ReferenceDynamics",
        CmdType.WriteRobotReferenceDynamics,
        CmdType.ReadRobotReferenceDynamics,
        _rd,
        lambda h: h.reference_dynamics.VelocityReference,
        777.0,
        W.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID,
        W.WARN_REFERENCE_DYNAMICS_SYNC_ERROR,
        "MC_WriteRobotReferenceDynamicsFB",
        _write_rd,
        I.INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
    ),
    DataSet(
        "Tool",
        "Tool",
        CmdType.WriteToolData,
        CmdType.ReadToolData,
        _tool,
        lambda h: h.tools[1].Data.X,
        12.5,
        W.WARN_TOOL_DATA_SYNC_MODE_INVALID,
        W.WARN_TOOL_NUMBER_SYNC_ERROR,
        "MC_WriteToolDataFB",
        _write_tool,
        I.INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
        E.ERR_SYNC_TOOL_COUNT_RC_HIGHER_THAN_PLC,
    ),
    DataSet(
        "Frame",
        "Frame",
        CmdType.WriteFrameData,
        CmdType.ReadFrameData,
        _frame,
        lambda h: h.frames[1].Data.X,
        12.5,
        W.WARN_FRAME_DATA_SYNC_MODE_INVALID,
        W.WARN_FRAME_NUMBER_SYNC_ERROR,
        "MC_WriteFrameDataFB",
        _write_frame,
        I.INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
        E.ERR_SYNC_FRAME_COUNT_RC_HIGHER_THAN_PLC,
    ),
    DataSet(
        "Load",
        "Load",
        CmdType.WriteLoadData,
        CmdType.ReadLoadData,
        _load,
        lambda h: h.loads[1].Data.Mass,
        2.5,
        W.WARN_LOAD_DATA_SYNC_MODE_INVALID,
        W.WARN_LOAD_NUMBER_SYNC_ERROR,
        "MC_WriteLoadDataFB",
        _write_load,
        I.INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED,
        E.ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC,
    ),
]
IDS = [d.name for d in DATA_SETS]


@pytest.fixture(autouse=True)
def sdk_parameters() -> Iterator[None]:
    """The SDK has 20 tools/frames/loads (index 0..19)."""
    old = srci.parameters()
    srci.configure(force=True, TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)
    yield
    srci.configure(force=True, **{k: old[k] for k in ("TOOL_MAX", "FRAME_MAX", "LOAD_MAX")})


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    fake = FakeClock()
    with use_clock(fake):
        yield fake


def harness(sdk: SdkSimulator, clock: FakeClock, data: DataSet, start: int, after: int) -> RobotTaskHarness:
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    modes = getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)
    modes[SyncTime.DURING_START_UP] = start
    modes[SyncTime.AFTER_START_UP] = after
    return h


def start_up(h: RobotTaskHarness) -> None:
    h.run(1500, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history


def commands(sdk: SdkSimulator, cmd: CmdType, since: int) -> int:
    """Number of commands of type ``cmd`` the SDK accepted after log entry ``since``."""
    name = {
        CmdType.WriteRobotSWLimits: "WriteSWLimits",
        CmdType.WriteRobotDefaultDynamics: "WriteDefaultDynamics",
        CmdType.WriteRobotReferenceDynamics: "WriteReferenceDynamics",
        CmdType.ReadRobotDefaultDynamics: "ReadDefaultDynamics",
        CmdType.ReadRobotReferenceDynamics: "ReadReferenceDynamics",
    }.get(cmd, cmd.name)
    return sum(
        1 for log in sdk.logs[since:] if f"(type: {name} (" in log.text and "EMPTY -> BUFFERED" in log.text
    )


def change_and_watch(h: RobotTaskHarness, data: DataSet, cycles: int = 400) -> list[bool]:
    data.change(h)
    seen = []
    for _ in range(cycles):
        h.cycle()
        seen.append(bool(h.rt.Synchronized))
    return seen


# ---------------------------------------------------------------- after the start-up


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_change_after_start_up_client_to_server(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """CLIENT_TO_SERVER after the start-up: a change on the PLC is written to the RC; Synchronized drops and comes back."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    start_up(h)
    since = len(sdk.logs)
    seen = change_and_watch(h, data)
    assert not all(seen), "Synchronized must drop while the data are not in sync"
    assert seen[-1] and not h.rt.Error and not h.rt.WarningID, h.history
    assert commands(sdk, data.write, since) == 1, "one write command"
    assert data.value(h) == data.changed, "the PLC keeps its data"
    assert getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync)


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_change_after_start_up_server_to_client(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """SERVER_TO_CLIENT after the start-up: a change on the PLC is overwritten with the data of the RC."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.SERVER_TO_CLIENT)
    start_up(h)
    since = len(sdk.logs)
    seen = change_and_watch(h, data)
    assert not all(seen), "Synchronized must drop while the data are not in sync"
    assert seen[-1] and not h.rt.Error and not h.rt.WarningID, h.history
    assert commands(sdk, data.read, since) >= 1, "the RC data are read"
    assert data.value(h) != data.changed, "the PLC data are overwritten with the data of the RC"


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_change_after_start_up_automatic(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """AUTOMATIC after the start-up: a change on the PLC (the most recent change) is written to the RC."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.AUTOMATIC)
    start_up(h)
    since = len(sdk.logs)
    seen = change_and_watch(h, data)
    assert not all(seen), "Synchronized must drop while the data are not in sync"
    assert seen[-1] and not h.rt.Error and not h.rt.WarningID, h.history
    assert commands(sdk, data.write, since) == 1
    assert data.value(h) == data.changed
    # a second change: AUTOMATIC keeps watching (ST-FIX F95)
    since = len(sdk.logs)
    SECOND_CHANGE[data.name](h)
    h.run(400)
    assert h.rt.Synchronized and not h.rt.Error, h.history
    assert commands(sdk, data.write, since) == 1, "the second change is written"


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_change_after_start_up_without_synchronization(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet
) -> None:
    """NO_SYNCHRONIZATION after the start-up: nothing is transferred, but the change is detected (Synchronized FALSE).

    Spec 5.6.7.3: the detection of changed data is independent of the SyncMode; the data set is enabled
    for synchronization (start-up mode), so the client is no longer synchronized.
    """
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.NO_SYNCHRONIZATION)
    if data.name in ("Tool", "Frame", "Load"):
        # the SDK reports its tools, frames and loads as changed until the client writes them - with
        # NO_SYNCHRONIZATION nothing is written, so the client is not synchronized from the start
        h.run(
            1500,
            until=lambda: bool(h.rt.Initialized and getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync)),
        )
        assert h.rt.Initialized and not h.rt.Error, h.history
        h.run(50)
        assert getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync), (
            "the PLC data are in sync after the start-up"
        )
    else:
        start_up(h)
    since = len(sdk.logs)
    seen = change_and_watch(h, data)
    assert commands(sdk, data.write, since) == 0 and commands(sdk, data.read, since) == 0, (
        "nothing is transferred"
    )
    assert data.value(h) == data.changed
    assert not h.rt.Error
    assert not seen[-1], "the client is not synchronized"
    assert not getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync)


def test_change_of_a_data_set_without_synchronization(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A data set disabled for synchronization (NO_SYNCHRONIZATION during and after the start-up) is not compared.

    Spec 5.6.7.1: a change of it does not affect Synchronized, which only depends on the enabled data sets.
    """
    sw = DATA_SETS[0]
    h = harness(sdk, clock, DATA_SETS[1], SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    start_up(h)
    assert not h.ag.State.DataEnableSync.EnableSyncSWLimits
    since = len(sdk.logs)
    seen = change_and_watch(h, sw)
    assert all(seen) and not h.rt.Error and not h.rt.WarningID, h.history
    assert commands(sdk, sw.write, since) == 0 and commands(sdk, sw.read, since) == 0


# ---------------------------------------------------------------- configuration


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_automatic_during_start_up_is_rejected(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """AUTOMATIC is not available during the start-up (table 5-109): the RobotTask rejects the configuration."""
    h = harness(sdk, clock, data, SyncMode.AUTOMATIC, SyncMode.AUTOMATIC)
    h.run(300, until=lambda: bool(h.rt.Error))
    assert h.rt.Error and h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, h.history
    assert h.rt.WarningID == data.mode_invalid
    assert not h.rt.Initialized and not h.rt.Synchronized


@pytest.mark.parametrize(
    "time", [SyncTime.DURING_START_UP, SyncTime.AFTER_START_UP], ids=["start-up", "after"]
)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_undefined_sync_mode_is_rejected(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, time: SyncTime
) -> None:
    """An undefined synchronization mode (7) is rejected with ERR_SYNC_MODE_INVALID and the warning of the data set."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)[time] = 7
    h.run(300, until=lambda: bool(h.rt.Error))
    assert h.rt.Error and h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, h.history
    assert h.rt.WarningID == data.mode_invalid
    assert not h.rt.Initialized and not h.rt.Synchronized


@pytest.mark.parametrize(
    ("old", "new"),
    [
        (SyncMode.CLIENT_TO_SERVER, SyncMode.SERVER_TO_CLIENT),
        (SyncMode.CLIENT_TO_SERVER, SyncMode.NO_SYNCHRONIZATION),
        (SyncMode.NO_SYNCHRONIZATION, SyncMode.CLIENT_TO_SERVER),
        (SyncMode.CLIENT_TO_SERVER, SyncMode.AUTOMATIC),
    ],
    ids=["c2s-to-s2c", "c2s-to-none", "none-to-c2s", "c2s-to-auto"],
)
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_sync_mode_changed_while_running(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, old: SyncMode, new: SyncMode
) -> None:
    """A synchronization mode changed while the RobotTask runs is reported (info) and only used after a restart.

    The old mode stays active: a later change of the data is handled as configured at the start.
    """
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, old)
    if old == SyncMode.NO_SYNCHRONIZATION and data.name in ("Tool", "Frame", "Load"):
        h.run(
            1500,
            until=lambda: bool(h.rt.Initialized and getattr(h.ag.State.SyncStatePlc.InSync, data.in_sync)),
        )
        h.run(50)
    else:
        start_up(h)
    getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)[SyncTime.AFTER_START_UP] = new
    since = len(sdk.logs)
    seen = change_and_watch(h, data)
    assert h.rt.InfoID == data.mode_changed, hex(h.rt.InfoID)
    assert not h.rt.Error, h.history
    assert data.value(h) == data.changed
    if old == SyncMode.CLIENT_TO_SERVER:
        assert commands(sdk, data.write, since) == 1, "the old mode CLIENT_TO_SERVER stays active"
        assert seen[-1]
    else:
        assert commands(sdk, data.write, since) == 0, "the old mode NO_SYNCHRONIZATION stays active"
        assert not seen[-1]


def test_sync_mode_during_start_up_changed_while_running(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A changed start-up mode is only used at the next start-up: no transfer, no error or warning while running."""
    data = DATA_SETS[0]
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    start_up(h)
    getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)[SyncTime.DURING_START_UP] = (
        SyncMode.SERVER_TO_CLIENT
    )
    since = len(sdk.logs)
    h.run(300)
    assert h.rt.Synchronized and not h.rt.Error and not h.rt.WarningID, h.history
    assert commands(sdk, data.write, since) == 0 and commands(sdk, data.read, since) == 0


# ---------------------------------------------------------------- data sets together, all disabled


def test_all_data_sets_disabled(sdk: SdkSimulator, clock: FakeClock) -> None:
    """Synchronization deactivated for all data sets: initialized, but never synchronized (spec 5.6.7.3)."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    h.run(600)
    assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error, h.history
    assert not h.rt.WarningID


def test_all_data_sets_changed_together(sdk: SdkSimulator, clock: FakeClock) -> None:
    """All data sets CLIENT_TO_SERVER: changed together after the start-up, every set is written once."""
    h = harness(sdk, clock, DATA_SETS[0], SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    for data in DATA_SETS:
        modes = getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)
        modes[SyncTime.DURING_START_UP] = modes[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    h.run(3000, until=lambda: bool(h.rt.Synchronized or h.rt.Error))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    since = len(sdk.logs)
    for data in DATA_SETS:
        data.change(h)
    h.run(1000, until=lambda: not h.rt.Synchronized)
    assert not h.rt.Synchronized
    h.run(1500, until=lambda: bool(h.rt.Synchronized))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    for data in DATA_SETS:
        assert commands(sdk, data.write, since) == 1, data.name
        assert data.value(h) == data.changed


# ---------------------------------------------------------------- configuration numbers (spec 5.6.7.5)


@pytest.mark.parametrize("data", [d for d in DATA_SETS if d.count_error], ids=lambda d: d.name)
def test_more_elements_on_the_rc_than_on_the_plc(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """The RC has more tools / frames / loads (20) than the PLC array (10): error, no synchronization (5.6.7.5.1)."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, count=10)
    modes = getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)
    modes[SyncTime.DURING_START_UP] = modes[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    h.run(600, until=lambda: bool(h.rt.Error))
    assert h.rt.Error and h.rt.ErrorID == data.count_error, h.history
    assert not h.rt.Synchronized


@pytest.mark.parametrize("data", [d for d in DATA_SETS if d.count_error], ids=lambda d: d.name)
def test_more_elements_on_the_plc_than_on_the_rc(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """The PLC array (30) is longer than on the RC (20): only the elements of the RC are read (5.6.7.5.2)."""
    srci.configure(force=True, TOOL_MAX=30, FRAME_MAX=30, LOAD_MAX=30)
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, count=30)
    modes = getattr(h.cfg.Plc.Parameter.SynchronizationModes, data.name)
    modes[SyncTime.DURING_START_UP] = modes[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    since = len(sdk.logs)
    start_up(h)
    assert commands(sdk, data.read, since) <= 20, "no element above the highest index of the RC is read"


# ---------------------------------------------------------------- synchronization reaction


@pytest.mark.parametrize("reaction", [4, 9, 255])
def test_undefined_sync_reaction_is_rejected(sdk: SdkSimulator, clock: FakeClock, reaction: int) -> None:
    """An undefined SyncReaction (table 5-108) is rejected by the client: error, the configuration is not sent."""
    h = harness(sdk, clock, DATA_SETS[0], SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    h.cfg.Rob.Parameter.SyncReaction = reaction  # type: ignore[assignment]  # undefined value on purpose
    h.run(300, until=lambda: bool(h.rt.Error))
    assert h.rt.Error and h.rt.ErrorID == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, h.history
    assert not h.rt.Initialized and not h.rt.Synchronized
    assert commands(sdk, CmdType.ExchangeConfiguration, 0) == 0


# ---------------------------------------------------------------- start-up conflicts


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_start_up_conflict_server_to_client(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """SERVER_TO_CLIENT during the start-up: different PLC data are overwritten with the RC data, then Synchronized."""
    h = harness(sdk, clock, data, SyncMode.SERVER_TO_CLIENT, SyncMode.CLIENT_TO_SERVER)
    data.change(h)
    start_up(h)
    assert data.value(h) != data.changed, "the PLC data are overwritten with the RC data"


@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_start_up_conflict_client_to_server(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """CLIENT_TO_SERVER during the start-up: different PLC data are written to the RC, then Synchronized."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    data.change(h)
    since = len(sdk.logs)
    start_up(h)
    assert data.value(h) == data.changed
    assert commands(sdk, data.write, since) >= 1


@pytest.mark.parametrize("resolve", ["write", "read"])
@pytest.mark.parametrize("data", DATA_SETS, ids=IDS)
def test_start_up_conflict_with_user_interaction(
    sdk: SdkSimulator, clock: FakeClock, data: DataSet, resolve: str
) -> None:
    """Start-up conflict with user interaction: warning, not synchronized until the user writes or reads the data.

    Spec 5.6.7.3 (synchronization during start-up): the user resolves the conflict with the write or
    read functions of the data set; afterwards the RobotTask is synchronized.
    """
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    take_over_rc_data(sdk, clock, data, h)  # only the changed value differs between PLC and RC
    setattr(h.cfg.Plc.Parameter.SyncUserInteraction, data.name, True)
    data.change(h)
    h.run(600)
    assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error, h.history
    assert h.rt.WarningID == data.user_conflict
    if resolve == "write":
        fb = h.add(new_instance(data.write_fb))
        data.write_input(fb, h)
    else:
        fb = h.add(new_instance(data.write_fb.replace("Write", "Read")))
        if hasattr(fb.ParCmd, "ToolNo"):
            fb.ParCmd.ToolNo = 1
        if hasattr(fb.ParCmd, "FrameNo"):
            fb.ParCmd.FrameNo = 1
        if hasattr(fb.ParCmd, "LoadNo"):
            fb.ParCmd.LoadNo = 1
    fb.Execute = True
    h.run(200, until=lambda: bool(fb.Done or fb.Error))
    assert fb.Done and not fb.Error, hex(fb.ErrorID)
    fb.Execute = False
    if resolve == "read":
        apply_read(fb, h, data)
    # the RobotTask reads the RC data again (sync timeout) and compares them with the PLC data
    h.run(1500, until=lambda: bool(h.rt.Synchronized))
    assert h.rt.Synchronized and not h.rt.Error, h.history
    if resolve == "write":
        assert data.value(h) == data.changed
    else:
        assert data.value(h) != data.changed


# ---------------------------------------------------------------- findings of the PLC tests (RobotTask reused)


# DefaultDynamics: the RC answers rate 0 with its minimum (1 %), SWLimits: 0 is below the lower limit
ZERO: dict[str, Callable[[RobotTaskHarness], None]] = {
    "Tool": lambda h: setattr(h.tools[1].Data, "X", 0.0),
    "Frame": lambda h: setattr(h.frames[1].Data, "X", 0.0),
    "Load": lambda h: setattr(h.loads[1].Data, "Mass", 0.0),
    "ReferenceDynamics": lambda h: setattr(h.reference_dynamics, "VelocityReference", 0.0),
}


@pytest.mark.parametrize("data", [d for d in DATA_SETS if d.name in ZERO], ids=lambda d: d.name)
def test_value_zero_after_a_change(sdk: SdkSimulator, clock: FakeClock, data: DataSet) -> None:
    """A value changed back to 0 stays 0: the RC leaves out trailing zero bytes of the response, the
    write block must not take the values of its previous response (ST-FIX F100)."""
    h = harness(sdk, clock, data, SyncMode.CLIENT_TO_SERVER, SyncMode.CLIENT_TO_SERVER)
    start_up(h)
    data.change(h)
    h.run(400)
    assert data.value(h) == data.changed
    ZERO[data.name](h)
    h.run(400)
    assert data.value(h) == 0.0, "the PLC value is replaced by the value of the previous response"
    assert h.rt.Synchronized and not h.rt.Error, h.history


def test_write_block_takes_no_values_of_the_previous_response(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A write block used twice: the second (shortened) response does not keep the values of the first
    one (ST-FIX F100)."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    h.run(200, until=lambda: bool(h.ag.State.CMDsEnabled or h.rt.Error))
    assert h.ag.State.CMDsEnabled, h.history
    fb = h.add(new_instance("MC_WriteRobotReferenceDynamicsFB"))
    for value in (777.0, 0.0):
        fb.ParCmd.DynamicValues.VelocityReference = value
        fb.Execute = True
        h.run(200, until=lambda: bool(fb.Done or fb.Error))
        assert fb.Done and not fb.Error, hex(fb.ErrorID)
        assert fb.OutCmd.ReferenceDynamicValues.VelocityReference == value
        fb.Execute = False
        h.run(2)


def test_count_check_uses_the_current_configuration(sdk: SdkSimulator, clock: FakeClock) -> None:
    """The count check (RC has more elements than the PLC array) runs after the initialization with the
    configuration of this enable - not with the modes and RC data of the previous one (ST-FIX F102)."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, count=10)
    modes = h.cfg.Plc.Parameter.SynchronizationModes
    modes.Frame[SyncTime.DURING_START_UP] = modes.Frame[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    h.run(600, until=lambda: bool(h.rt.Error))
    assert h.rt.ErrorID == E.ERR_SYNC_FRAME_COUNT_RC_HIGHER_THAN_PLC, h.history
    h.enable = False
    h.run(50)
    modes.Frame[SyncTime.DURING_START_UP] = modes.Frame[SyncTime.AFTER_START_UP] = SyncMode.NO_SYNCHRONIZATION
    modes.Load[SyncTime.DURING_START_UP] = modes.Load[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    h.enable = True
    h.run(600, until=lambda: bool(h.rt.Error))
    assert h.rt.ErrorID == E.ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC, h.history


def test_load_count_uses_the_highest_load_index(sdk: SdkSimulator, clock: FakeClock) -> None:
    """The load count of the RC is HighestLoadIndex, not HighestToolIndex (ST-FIX F101): an RC with 6 tools
    and 20 loads does not fit into a load array of 10."""
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance, count=10)
    modes = h.cfg.Plc.Parameter.SynchronizationModes
    modes.Load[SyncTime.DURING_START_UP] = modes.Load[SyncTime.AFTER_START_UP] = SyncMode.CLIENT_TO_SERVER
    exchange = h.rt._exchangeConfiguration
    apply = exchange.OnApplyOutCmd

    def fewer_tools(**kwargs: Any) -> None:
        apply(**kwargs)
        exchange.OutCmd.HighestToolIndex = 5

    exchange.OnApplyOutCmd = fewer_tools  # type: ignore[method-assign]
    h.run(1500, until=lambda: bool(h.rt.Error or h.rt.Synchronized))
    assert h.rt.Error and h.rt.ErrorID == E.ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC, h.history
