"""RobotLibraryCommandDataFB - payload buffer of one command."""

# ST-Source: POUs/_internal/Send/RobotLibraryCommandDataFB.st  sha256: cba0fa2ed29335f0

from __future__ import annotations

from srci.fb._internal.Send.RobotLibrarySendDataBaseFB import RobotLibrarySendDataBaseFB
from srci.types import RobotLibraryParameter

__all__ = ["RobotLibraryCommandDataFB"]


class RobotLibraryCommandDataFB(RobotLibrarySendDataBaseFB):
    """Owns ``Payload : ARRAY[0..PARAMETER_PAYLOAD_MAX] OF BYTE``."""

    def __init__(self) -> None:
        super().__init__()
        # VAR_INPUT
        self.Payload = bytearray(RobotLibraryParameter.PARAMETER_PAYLOAD_MAX + 1)

    def Reset(self) -> None:
        super().Reset()
        self.Payload[:] = bytes(len(self.Payload))

    def UpdatePointer(self) -> None:
        self._pPayload = self.Payload
