"""RobotLibraryRecvDataFB - reads the telegram from ``RobotInData``."""

# ST-Source: POUs/_internal/Recv/RobotLibraryRecvDataFB.st  sha256: 4292dfb1b8940091

from __future__ import annotations

from srci.fb._internal.Recv.RobotLibraryRecvDataBaseFB import RobotLibraryRecvDataBaseFB
from srci.functions.Convert.Misc import GetHalfeByteHi

__all__ = ["RobotLibraryRecvDataFB"]


class RobotLibraryRecvDataFB(RobotLibraryRecvDataBaseFB):
    """Reads from an external buffer (ST: ``Payload : POINTER TO BYTE``, ``PayLoadSize``)."""

    def __init__(self) -> None:
        super().__init__()
        # VAR_INPUT
        self.Payload: bytearray | bytes | None = None
        self.PayLoadSize: int = 0

    def __call__(self, Payload: bytearray | bytes, PayloadSize: int | None = None) -> None:
        self.Payload = Payload
        self.PayLoadSize = len(Payload) if PayloadSize is None else PayloadSize
        if self.PayLoadSize > len(Payload):
            raise ValueError(f"PayloadSize {self.PayLoadSize} > buffer size {len(Payload)}")

    def GetLifeSignFooter(self) -> int:
        """LifeSign in the high nibble of the last telegram byte."""
        if self.Payload is None or self.PayLoadSize < 1:
            return 0
        return GetHalfeByteHi(self.Payload[self.PayLoadSize - 1])

    def UpdatePointer(self) -> None:
        self._pPayload = self.Payload

    def _payload_size(self, buf: bytearray | bytes) -> int:
        return min(len(buf), self.PayLoadSize)
