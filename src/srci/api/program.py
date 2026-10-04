# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.api.program
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    ``RobotProgram``: the "PLC program" around ``MC_RobotTaskFB``.
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

"""``RobotProgram``: the "PLC program" around ``MC_RobotTaskFB``.

In a PLC the user declares the RobotTask, its user data (tool, frame, load, ... arrays, log
buffers, configuration) and the command function blocks, and calls them once per cycle.
:class:`RobotProgram` does exactly that in Python::

    program = RobotProgram(send_size=256, recv_size=256)
    move = program.add(MC_MoveAxesAbsoluteFB())      # called in every cycle
    out = program.step(robot_in_data)                # one cycle: in -> out telegram

It is a :class:`srci.runtime.Program` (method ``cycle``) and runs with
:class:`srci.runtime.Runner` or :class:`srci.api.SrciClient`.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB import MC_RobotTaskFB
from srci.interfaces.IMessageLogger import IMessageLogger
from srci.runtime.runner import CycleContext
from srci.runtime.systemtime import system_time_now
from srci.types import (
    AlarmMessage,
    AxesGroup,
    DefaultDynamics,
    Frame,
    Load,
    ReferenceDynamics,
    RobotLibraryParameter,
    RobotTaskParCfg,
    RobotWorkArea,
    Severity,
    SWLimits,
    Tool,
    UserData,
)

__all__ = ["RobotProgram"]

FB = TypeVar("FB")


class RobotProgram:
    """RobotTask + user data + command function blocks, executed once per cycle.

    Order in a cycle (like a PLC program): the command function blocks in the order they were
    added, then ``MC_RobotTaskFB`` (which builds the telegram from the commands of this cycle).
    """

    def __init__(
        self,
        send_size: int = 256,
        recv_size: int = 256,
        *,
        robot_name: str = "Robot1",
        axes_group_id: int = 0,
        ParCfg: RobotTaskParCfg | None = None,  # input name of MC_RobotTaskFB
        external_logger: IMessageLogger | None = None,
        log_level: Severity = Severity.INFO,
    ) -> None:
        self.robot_name = robot_name
        self.axes_group_id = axes_group_id
        self.robot_task = MC_RobotTaskFB()
        self.axes_group = AxesGroup()
        # configuration of the RobotTask: input ParCfg of MC_RobotTaskFB (same name as in the PLC)
        self.ParCfg = ParCfg if ParCfg is not None else RobotTaskParCfg()
        self.ParCfg.Com.TelegramLengthPlcToRob = send_size
        self.ParCfg.Com.TelegramLengthRobToPlc = recv_size
        # user data of the RobotTask (the arrays of the PLC program)
        self.tools = [Tool() for _ in range(RobotLibraryParameter.TOOL_MAX)]
        self.frames = [Frame() for _ in range(RobotLibraryParameter.FRAME_MAX)]
        self.loads = [Load() for _ in range(RobotLibraryParameter.LOAD_MAX)]
        self.work_areas = [RobotWorkArea() for _ in range(RobotLibraryParameter.WORK_AREAS_MAX)]
        self.sw_limits = SWLimits()
        self.default_dynamics = DefaultDynamics()
        self.reference_dynamics = ReferenceDynamics()
        self.user_data = UserData()
        self.system_log = [""] * len(self.axes_group.MessageLog.SystemLogs)
        self.message_log = [AlarmMessage() for _ in range(len(self.axes_group.MessageLog.Messages))]
        self.external_logger = external_logger
        self.log_level = log_level
        self.enable = True
        self._in = bytearray(recv_size)
        self._out = bytearray(send_size)
        self._blocks: list[tuple[Any, Callable[[], None]]] = []

    # ------------------------------------------------------------------ function blocks

    def add(self, block: FB, **inputs: Any) -> FB:
        """Add a command function block; it is called with ``AxesGroup`` in every cycle.

        ``inputs`` are set as attributes (e.g. ``Enable=True``) before the first call.
        """
        for name, value in inputs.items():
            if not hasattr(block, name):
                raise AttributeError(f"{type(block).__name__} has no input {name!r}")
            setattr(block, name, value)
        call: Callable[..., None] = block  # type: ignore[assignment]
        kwargs: dict[str, Any] = {"AxesGroup": self.axes_group}
        if self.external_logger is not None:
            kwargs["ExternalLogger"] = self.external_logger
            kwargs["LogLevel"] = self.log_level
        self._blocks.append((block, lambda: call(**kwargs)))
        return block

    def remove(self, block: Any) -> None:
        """Remove a function block (it is no longer called)."""
        self._blocks = [(b, c) for b, c in self._blocks if b is not block]

    @property
    def blocks(self) -> list[Any]:
        return [b for b, _ in self._blocks]

    # ------------------------------------------------------------------ cycle

    def step(self, robot_in_data: bytes | bytearray) -> bytes:
        """One cycle: telegram of the robot in, telegram to the robot out."""
        self._in[:] = robot_in_data
        for _, call in self._blocks:
            call()
        rt_kwargs: dict[str, Any] = {}
        if self.external_logger is not None:
            rt_kwargs = {"ExternalLogger": self.external_logger, "LogLevel": self.log_level}
        self.robot_task(
            Enable=self.enable,
            RobotName=self.robot_name,
            SystemTime=system_time_now(),
            AxesGroupID=self.axes_group_id,
            ParCfg=self.ParCfg,
            RobotInData=self._in,
            RobotOutData=self._out,
            UserData=self.user_data,
            ToolData=self.tools,
            FrameData=self.frames,
            LoadData=self.loads,
            WorkAreas=self.work_areas,
            SWLimits=self.sw_limits,
            DefaultDynamics=self.default_dynamics,
            ReferenceDynamics=self.reference_dynamics,
            SystemLog=self.system_log,
            MessageLog=self.message_log,
            AxesGroup=self.axes_group,
            **rt_kwargs,
        )
        return bytes(self._out)

    def cycle(self, ctx: CycleContext) -> None:
        """:class:`srci.runtime.Program` interface (used by :class:`srci.runtime.Runner`)."""
        ctx.RobotOutData[:] = self.step(ctx.RobotInData)

    # ------------------------------------------------------------------ state

    @property
    def initialized(self) -> bool:
        return bool(self.robot_task.Initialized or self.robot_task.Synchronized)

    @property
    def commands_enabled(self) -> bool:
        """TRUE when commands can be sent (RobotTask initialized)."""
        return bool(self.axes_group.State.CMDsEnabled)

    @property
    def error(self) -> bool:
        return bool(self.robot_task.Error)
