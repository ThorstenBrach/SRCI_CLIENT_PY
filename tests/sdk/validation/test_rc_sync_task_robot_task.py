# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.validation.test_rc_sync_task_robot_task
#  Author:      Thorsten Brach
#  Date:        2026-11-01
#
#  Description:
#    Validation of the RobotTask: restarts of the PLC and the RC, lost
#    connection during a motion, several RobotTasks on one interface,
#    blending between different motion commands, Done after a short Execute.
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

"""Validation of the RobotTask (spec 6.1.1) against the SDK simulator.

A restart of the RC is simulated with a new SDK simulator behind the same transport, a lost
connection (cable pulled) with a transport that returns empty telegrams and does not reach the RC.
A restart of the PLC is a new RobotTask instance with fresh data; the RC is told that the old client
is gone (``SdkSimulator.reset``: the SDK notices it otherwise only with its real-time lifesign timeout).
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from srci_sdk_sim.sdk import SdkSimulator, sdk_transport

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB import MC_RobotTaskFB
from srci.iec.clock import FakeClock, use_clock
from srci.runtime.systemtime import system_time_now
from srci.types import AxesGroup, BlendingMode, ProcessingMode, RobotLibraryErrorIdEnum
from tests.robot_task_harness import SIZE, RobotTaskHarness
from tests.sdk.validation.conftest import cartesian, enable, execute, fb, move_axes, order, state, watch

E = RobotLibraryErrorIdEnum
RESTART_CYCLES = 600  # disable time of the RobotTask (cancel timeouts of the internal blocks)


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    fake = FakeClock()
    with use_clock(fake):
        yield fake


class _Cable:
    """Transport to the SDK that can be unplugged (empty telegrams) and plugged into another RC."""

    def __init__(self, sdk: SdkSimulator) -> None:
        self.connected = True
        self.plug(sdk)

    def plug(self, sdk: SdkSimulator) -> None:
        self.sdk = sdk
        self._inner = sdk_transport(sdk, SIZE, SIZE)

    def exchange(self, data: bytes) -> bytes:
        return self._inner.exchange(data) if self.connected else bytes(SIZE)


def _initialized(h: RobotTaskHarness) -> None:
    h.run(300, until=lambda: bool(h.ag.State.CMDsEnabled))
    assert h.rt.Initialized and not h.rt.Error, h.history


def _restart_robot_task(h: RobotTaskHarness) -> None:
    """The user acknowledges the error of the RobotTask: Enable FALSE, then TRUE."""
    h.enable = False
    h.run(RESTART_CYCLES)
    h.enable = True
    h.run(300, until=lambda: bool(h.ag.State.CMDsEnabled))
    assert h.rt.Initialized and not h.rt.Error, h.history


def _ready_to_move(h: RobotTaskHarness) -> None:
    """GroupReset, EnableRobot and GroupContinue end with Done / Enabled; a new motion reaches its target."""
    reset = execute(h, fb(h, "MC_GroupResetFB"))
    assert order(reset, "Busy", "Done") and not reset.final["Error"], reset.final
    en = fb(h, "MC_EnableRobotFB", Enable=True)
    seen = watch(h, [en], 200, lambda: bool(en.Enabled or en.Error))[0]
    assert order(seen, "Busy", "Enabled") and not en.Error, state(en)
    cont = execute(h, fb(h, "MC_GroupContinueFB"))
    assert order(cont, "Busy", "Done") and not cont.final["Error"], cont.final
    mv = move_axes(h, 10.0)
    s = execute(h, mv)
    assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags


# ---------------------------------------------------------------- restarts after the initialization


def test_plc_restart_after_initialization(sdk: SdkSimulator, clock: FakeClock) -> None:
    """After a PLC restart a new RobotTask initializes again: Initialized TRUE, not synchronized, no error.

    The old RobotTask stops being called (PLC stop), the RC drops the client; the new instance
    (PLC start, fresh data) reaches Initialized without error, warning or info.
    """
    first = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    _initialized(first)
    sdk.reset()  # the RC notices the stopped client
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    assert not h.rt.Initialized
    _initialized(h)
    h.run(50)
    assert h.rt.Initialized and not h.rt.Synchronized and not h.rt.Error, h.history
    assert not h.rt.WarningID and not h.rt.InfoID


def test_rc_restart_after_initialization(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A restarted RC (three times): Initialized drops, the reset of the interface is reported, then it initializes again.

    The RobotTask sets ERR_INTERFACE_WAS_RESET_AFTER_INIT (16#80A7) when the RC starts anew; after the
    acknowledgement (Enable FALSE / TRUE) it is initialized without error, every time.
    """
    cable = _Cable(sdk)
    h = RobotTaskHarness(cable, advance=clock.advance)
    _initialized(h)
    for _ in range(3):
        cable.plug(SdkSimulator())
        h.run(300, until=lambda: bool(h.rt.Error))
        assert not h.rt.Initialized
        assert h.rt.ErrorID == E.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7, h.history
        _restart_robot_task(h)
        assert not h.rt.Synchronized and not h.rt.WarningID


# ---------------------------------------------------------------- lost connection / RC restart during a motion


@pytest.mark.parametrize(
    "variant",
    [
        pytest.param("unplugged-same-rc", id="unplugged-same-rc"),
        pytest.param("unplugged-restarted-rc", id="unplugged-restarted-rc"),
        pytest.param("restarted-rc", id="restarted-rc"),
    ],
)
def test_connection_lost_during_a_motion(sdk: SdkSimulator, clock: FakeClock, variant: str) -> None:
    """Connection lost or RC restarted during a motion: the motion ends without Done, the robot can be restarted.

    While the motion is active the cable is pulled (and plugged again into the same or a restarted
    RC) or the RC restarts. The motion block leaves Busy without Done, the RobotTask reports an error
    and loses Initialized. After the acknowledgement of the RobotTask, GroupReset, EnableRobot and
    GroupContinue end successfully and a new motion reaches its target.
    """
    sdk.set_move_cycles(300)
    cable = _Cable(sdk)
    h = RobotTaskHarness(cable, advance=clock.advance)
    _initialized(h)
    enable(h)
    mv = move_axes(h, 50.0)
    mv.Execute = True
    h.run(60)
    assert mv.Active and cable.sdk.joints[0] > 0.0, state(mv)
    if variant.startswith("unplugged"):
        cable.connected = False
    else:
        cable.plug(SdkSimulator())
    seen = watch(h, [mv], 300, lambda: bool(h.rt.Error and not mv.Busy))[0]
    assert h.rt.Error and not h.rt.Initialized, h.history
    assert not mv.Busy and not mv.Done and "Done" not in seen.flags, state(mv)
    if variant == "unplugged-restarted-rc":
        cable.plug(SdkSimulator())
    cable.connected = True
    mv.Execute = False
    _restart_robot_task(h)
    cable.sdk.set_move_cycles(50)
    _ready_to_move(h)


# ---------------------------------------------------------------- several RobotTasks


class _SecondTask:
    """A second RobotTask in the same PLC program, with its own or shared AxesGroup / telegram buffers."""

    def __init__(self, h: RobotTaskHarness, ag: AxesGroup, rin: bytearray, rout: bytearray) -> None:
        self.rt = MC_RobotTaskFB()
        self.h, self.ag, self.rin, self.rout = h, ag, rin, rout

    def __call__(self) -> None:
        h = self.h
        self.rt(
            Enable=True,
            RobotName="Robot2",
            SystemTime=system_time_now(),
            AxesGroupID=1,
            ParCfg=h.cfg,
            RobotInData=self.rin,
            RobotOutData=self.rout,
            UserData=h.user_data,
            ToolData=h.tools,
            FrameData=h.frames,
            LoadData=h.loads,
            WorkAreas=h.areas,
            SWLimits=h.sw_limits,
            DefaultDynamics=h.default_dynamics,
            ReferenceDynamics=h.reference_dynamics,
            SystemLog=h.system_log,
            MessageLog=h.message_log,
            AxesGroup=self.ag,
        )


def _two_tasks(
    sdk: SdkSimulator, clock: FakeClock, same_group: bool, same_buffers: bool
) -> tuple[RobotTaskHarness, Any]:
    h = RobotTaskHarness(sdk_transport(sdk, SIZE, SIZE), advance=clock.advance)
    _initialized(h)
    second = _SecondTask(
        h,
        h.ag if same_group else AxesGroup(),
        h.rin if same_buffers else bytearray(SIZE),
        h.rout if same_buffers else bytearray(SIZE),
    )
    h.fbs.append(second)  # called in the same cycle, before the first RobotTask
    h.run(300, until=lambda: bool(second.rt.Error))
    return h, second.rt


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F132: no check that an AxesGroup is used by one RobotTask only - ERR_AXESGROUP_INVALID (16#8007) "
    "is defined but never set (MC_RobotTaskFB)",
)
@pytest.mark.parametrize("same_buffers", [True, False], ids=["same-telegrams", "other-telegrams"])
def test_second_robot_task_on_the_same_axes_group(
    sdk: SdkSimulator, clock: FakeClock, same_buffers: bool
) -> None:
    """A second RobotTask with the same AxesGroup is rejected with 16#8007; the first one stays initialized."""
    h, second = _two_tasks(sdk, clock, same_group=True, same_buffers=same_buffers)
    assert second.Error and second.ErrorID == E.ERR_AXESGROUP_INVALID, hex(second.ErrorID)
    assert h.rt.Initialized and not h.rt.Error


@pytest.mark.xfail(
    strict=True,
    reason="LIB-BUG F132: no check that the telegram buffers (periphery) are used by one RobotTask only - "
    "ERR_PERIPHERY_INVALID (16#8008) is defined but never set (MC_RobotTaskFB)",
)
def test_second_robot_task_on_the_same_telegrams(sdk: SdkSimulator, clock: FakeClock) -> None:
    """A second RobotTask with other AxesGroup but the same telegram buffers is rejected with 16#8008."""
    h, second = _two_tasks(sdk, clock, same_group=False, same_buffers=True)
    assert second.Error and second.ErrorID == E.ERR_PERIPHERY_INVALID, hex(second.ErrorID)
    assert not second.Initialized and not second.Synchronized
    assert h.rt.Initialized and not h.rt.Error


# ---------------------------------------------------------------- blending between different motion commands


def test_blending_between_direct_and_linear_motions(robot: RobotTaskHarness, sdk: SdkSimulator) -> None:
    """Direct and linear motions with blending, started together, all end with Done at the last target.

    MoveDirectAbsolute with RAMP_OVERLAP 100 % and MoveLinearAbsolute with MAX_CORNER_DEVIATION 50 mm,
    alternating (direct, linear, direct, linear). Each block shows Busy, CommandBuffered, Active, Done;
    the robot ends at the last target. (The simulator accepts the blending modes but does not report
    IsBlending, so the blending itself is not observed.)
    """
    enable(robot)
    targets = [(10.0, 0.0, 0.0), (20.0, 5.0, 0.0), (30.0, 5.0, 0.0), (40.0, 10.0, 0.0)]
    blocks = []
    for i, target in enumerate(targets):
        linear = i % 2 == 1
        b = fb(robot, "MC_MoveLinearAbsoluteFB" if linear else "MC_MoveDirectAbsoluteFB")
        cartesian(b, *target)
        b.ParCmd.VelocityRate = 100.0
        b.ParCmd.AccelerationRate = 100.0
        b.ParCmd.BlendingMode = BlendingMode.MAX_CORNER_DEVIATION if linear else BlendingMode.RAMP_OVERLAP
        b.ParCmd.BlendingParameter[0] = 50.0 if linear else 100.0
        blocks.append(b)
    for b in blocks:
        b.Execute = True
    seen = watch(robot, blocks, 2000, lambda: all(b.Done or b.Error for b in blocks))
    for s in seen:
        assert order(s, "Busy", "CommandBuffered", "Active", "Done"), s.flags
        assert "Error" not in s.flags
    assert sdk.joints[:3] == pytest.approx([40.0, 10.0, 0.0])


# ---------------------------------------------------------------- Done after a short Execute


def test_done_is_shown_after_a_short_execute(robot: RobotTaskHarness) -> None:
    """A read command with an Execute pulse of one cycle still shows Done (for one cycle) when it has finished.

    ReadActualPosition (PARALLEL, no sequence): Execute TRUE for one cycle only. The block shows Busy
    and then Done without error (the simulator answers the read at once, so CommandBuffered /
    ParameterAccepted are not visible); Done stays for exactly one cycle because Execute is already FALSE.
    """
    rd = fb(robot, "MC_ReadActualPositionFB", ProcessingMode=ProcessingMode.PARALLEL)
    rd.Execute = True
    robot.run(1)
    rd.Execute = False
    seen = watch(robot, [rd], 200, lambda: bool(rd.Done or rd.Error))[0]
    assert order(seen, "Busy", "Done") and "Error" not in seen.flags, seen.flags
    done_cycles = 0
    for _ in range(5):
        robot.run(1)
        done_cycles += bool(rd.Done)
    assert done_cycles == 0 and not rd.Busy, state(rd)
