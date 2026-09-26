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
