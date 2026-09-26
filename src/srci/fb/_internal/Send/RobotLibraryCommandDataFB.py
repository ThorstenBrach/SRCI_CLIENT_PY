# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.fb._internal.Send.RobotLibraryCommandDataFB
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    RobotLibraryCommandDataFB - payload buffer of one command.
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
