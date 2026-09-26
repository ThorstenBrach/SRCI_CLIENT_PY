"""Test harness: MC_RobotTaskFB with user data arrays, driven cycle by cycle."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB import MC_RobotTaskFB
from srci.runtime.systemtime import system_time_now
from srci.transport import Transport
from srci.types import (
    AlarmMessage,
    AxesGroup,
    DefaultDynamics,
    Frame,
    Load,
    ReferenceDynamics,
    RobotTaskParCfg,
    RobotWorkArea,
    SWLimits,
    SyncMode,
    Tool,
    UserData,
)

SIZE = 128
SYNC_ITEMS = ("Tool", "Frame", "Load", "WorkAreas", "SWLimits", "DefaultDynamics", "ReferenceDynamics")


@dataclass
class RobotTaskHarness:
    """``MC_RobotTaskFB`` + the variables a PLC program would declare for it."""

    transport: Transport
    count: int = 20  # elements of ToolData/FrameData/LoadData (ARRAY[0..count-1])
    work_areas: int = 16
    size: int = SIZE
    advance: Callable[[float], None] | None = None  # FakeClock.advance
    cycle_time: float = 0.01
    rt: MC_RobotTaskFB = field(init=False)

    def __post_init__(self) -> None:
        self.rt = MC_RobotTaskFB()
        self.ag = AxesGroup()
        self.tools = [Tool() for _ in range(self.count)]
        self.frames = [Frame() for _ in range(self.count)]
        self.loads = [Load() for _ in range(self.count)]
        self.areas = [RobotWorkArea() for _ in range(self.work_areas)]
        self.sw_limits = SWLimits()
        self.default_dynamics = DefaultDynamics()
        self.reference_dynamics = ReferenceDynamics()
        self.user_data = UserData()
        self.system_log = [""] * len(self.ag.MessageLog.SystemLogs)
        self.message_log = [AlarmMessage() for _ in range(len(self.ag.MessageLog.Messages))]
        self.cfg = RobotTaskParCfg()
        self.cfg.Com.TelegramLengthPlcToRob = self.size
        self.cfg.Com.TelegramLengthRobToPlc = self.size
        self.rin = bytearray(self.size)
        self.rout = bytearray(self.size)
        self.enable = True
        self.cycles = 0
        self.history: list[tuple[int, bool, bool, bool, int]] = []
        # function blocks of the "PLC program", called before the RobotTask in every cycle
        self.fbs: list[Callable[[], None]] = []

    def sync(self, mode: SyncMode, *items: str, after_startup: bool = True) -> None:
        modes = self.cfg.Plc.Parameter.SynchronizationModes
        for item in items or SYNC_ITEMS:
            arr = getattr(modes, item)
            arr[0] = mode
            if after_startup:
                arr[1] = mode

    def call(self) -> None:
        self.rt(
            Enable=self.enable,
            RobotName="Robot1",
            SystemTime=system_time_now(),
            AxesGroupID=0,
            ParCfg=self.cfg,
            RobotInData=self.rin,
            RobotOutData=self.rout,
            UserData=self.user_data,
            ToolData=self.tools,
            FrameData=self.frames,
            LoadData=self.loads,
            WorkAreas=self.areas,
            SWLimits=self.sw_limits,
            DefaultDynamics=self.default_dynamics,
            ReferenceDynamics=self.reference_dynamics,
            SystemLog=self.system_log,
            MessageLog=self.message_log,
            AxesGroup=self.ag,
        )

    def cycle(self) -> None:
        """One PLC cycle: call the function blocks and the RobotTask, exchange the telegrams."""
        for fb in self.fbs:
            fb()
        self.call()
        self.rin[:] = self.transport.exchange(bytes(self.rout))
        self.cycles += 1
        if self.advance is not None:
            self.advance(self.cycle_time)
        state = (self.cycles, self.rt.Initialized, self.rt.Synchronized, self.rt.Error, int(self.rt.ErrorID))
        if not self.history or self.history[-1][1:] != state[1:]:
            self.history.append(state)

    def add(self, fb: Any, **inputs: Any) -> Any:
        """Call ``fb`` (with ``AxesGroup``) in every cycle; inputs are set as attributes."""
        for name, value in inputs.items():
            setattr(fb, name, value)
        self.fbs.append(lambda: fb(AxesGroup=self.ag))
        return fb

    def run(self, cycles: int, until: Callable[[], bool] | None = None) -> int:
        """Run ``cycles`` cycles (or until ``until()`` is true); returns the cycles run."""
        for n in range(1, cycles + 1):
            self.cycle()
            if until is not None and until():
                return n
        return cycles
