"""Shared test helpers."""

from __future__ import annotations

from typing import Any

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB_Telegram import MC_RobotTaskFB_Telegram
from srci.types import AxesGroup, SystemTime, TelegramRobToPlcFragment


class FakeACR:
    def __init__(self) -> None:
        self.responses: list[tuple[int, bytes]] = []

    def AddRsp(self, Rsp: TelegramRobToPlcFragment) -> int:
        start = Rsp.Header.PayloadPointer
        self.responses.append(
            (Rsp.Header.CmdID, bytes(Rsp.Command.Payload[start : start + Rsp.Header.PayloadLength]))
        )
        return 0


class Host(MC_RobotTaskFB_Telegram):
    def __init__(self) -> None:
        super().__init__()
        self.SystemTime = SystemTime()
        self.logs: list[dict[str, Any]] = []
        self._parCfg.Com.TelegramLengthPlcToRob = 64
        self._parCfg.Com.TelegramLengthRobToPlc = 128

    def _log(self, **kw: Any) -> None:
        self.logs.append(kw)

    CreateLogMessagePara1 = CreateLogMessagePara2 = CreateLogMessagePara3 = _log
    CreateLogMessagePara4 = CreateLogMessagePara5 = _log


def new_axes_group() -> tuple[AxesGroup, FakeACR]:
    ag = AxesGroup()
    acr = FakeACR()
    ag.Acyclic.ActiveCommandRegister = acr
    return ag, acr
