# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.functions.Common
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Functions/Common of the PLC library.
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

"""Functions/Common of the PLC library."""

from __future__ import annotations

from srci.iec.standard import TON
from srci.types import RobotLibraryConstants

__all__ = ["CheckTimeout", "SetTimeout"]


# ST-Source: Functions/Common/SetTimeout.st  sha256: e5d7a45d2b226e4e
def SetTimeout(PT: int, rTimer: TON) -> int:
    """(Re)start ``rTimer`` with ``PT`` milliseconds."""
    rTimer(IN=False)  # Reset timer
    rTimer(PT=PT, IN=True)  # Start timer
    return RobotLibraryConstants.OK


# ST-Source: Functions/Common/CheckTimeout.st  sha256: 72b89563167c79a3
def CheckTimeout(rTimer: TON) -> int:
    """``OK`` when the timer elapsed, otherwise ``RUNNING``."""
    rTimer()
    return RobotLibraryConstants.OK if rTimer.Q else RobotLibraryConstants.RUNNING
