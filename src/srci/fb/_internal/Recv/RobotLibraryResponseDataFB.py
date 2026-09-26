# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.fb._internal.Recv.RobotLibraryResponseDataFB
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    RobotLibraryResponseDataFB - payload buffer of one command response.
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

"""RobotLibraryResponseDataFB - payload buffer of one command response."""

# ST-Source: POUs/_internal/Recv/RobotLibraryResponseDataFB.st  sha256: 66823e78d3169e59

from __future__ import annotations

from srci.fb._internal.Recv.RobotLibraryRecvDataBaseFB import RobotLibraryRecvDataBaseFB
from srci.types import RobotLibraryParameter

__all__ = ["RobotLibraryResponseDataFB"]


class RobotLibraryResponseDataFB(RobotLibraryRecvDataBaseFB):
    """Owns ``Payload : ARRAY[0..RESPONSE_PAYLOAD_MAX] OF BYTE``."""

    def __init__(self) -> None:
        super().__init__()
        # VAR_INPUT
        self.Payload = bytearray(RobotLibraryParameter.RESPONSE_PAYLOAD_MAX + 1)

    @property
    def IsPayloadRemaining(self) -> bool:
        return self.PayloadPtr < self.PayloadLen

    def Reset(self) -> None:
        super().Reset()
        self.Payload[:] = bytes(len(self.Payload))

    def UpdatePointer(self) -> None:
        self._pPayload = self.Payload
