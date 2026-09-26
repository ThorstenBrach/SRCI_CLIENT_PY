# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.fb._internal.Send.RobotLibrarySendDataFB
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    RobotLibrarySendDataFB - writes the telegram to ``RobotOutData``.
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

"""RobotLibrarySendDataFB - writes the telegram to ``RobotOutData``."""

# ST-Source: POUs/_internal/Send/RobotLibrarySendDataFB.st  sha256: c756d6f937661664

from __future__ import annotations

from srci.fb._internal.Send.RobotLibrarySendDataBaseFB import RobotLibrarySendDataBaseFB

__all__ = ["RobotLibrarySendDataFB"]


class RobotLibrarySendDataFB(RobotLibrarySendDataBaseFB):
    """Writes into an external buffer (ST: ``Payload : POINTER TO BYTE``, ``PayLoadSize``)."""

    def __init__(self) -> None:
        super().__init__()
        # VAR_INPUT
        self.Payload: bytearray | None = None
        self.PayLoadSize: int = 0

    def __call__(self, Payload: bytearray, PayLoadSize: int | None = None) -> None:
        self.Payload = Payload
        self.PayLoadSize = len(Payload) if PayLoadSize is None else PayLoadSize
        if self.PayLoadSize > len(Payload):
            raise ValueError(f"PayLoadSize {self.PayLoadSize} > buffer size {len(Payload)}")

    def Reset(self) -> None:
        super().Reset()
        if self.Payload is not None:
            self.Payload[: self.PayLoadSize] = bytes(self.PayLoadSize)

    def SetLifeSignFooter(self, LifeSign: int) -> None:
        """Write the footer byte (last byte of the telegram)."""
        if self.Payload is None or self.PayLoadSize < 1:
            return
        self.Payload[self.PayLoadSize - 1] = LifeSign & 0xFF

    def UpdatePointer(self) -> None:
        self._pPayload = self.Payload

    def _payload_size(self, buf: bytearray) -> int:
        return min(len(buf), self.PayLoadSize)
