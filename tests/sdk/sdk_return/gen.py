"""SDK return, group GEN: general commands (11_Application_General.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (1005, 1006, 1101, 5101, 5110, 5111, 7005)

# ToolNoReturn / FrameNoReturn: the tool and frame of the command (filled by the SDK)
PARCMD: dict[str, dict[str, Any]] = {
    "MC_ReadActualTCPVelocityFB": {"ToolNo": 2, "FrameNo": 3},
}
RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_ReadActualTCPVelocityFB": {"ToolNoReturn": 2, "FrameNoReturn": 3},
}

# client checks (not sent): UserLogin Mode 3, ReadActualForce ReferenceType 2 (16#0008), ToolNo /
# FrameNo not available on the RC (16#8413 / 16#8415) - the SDK checks of these values are not
# reachable with the client. CalibrationData 20: valid for the client (LOAD_MAX = 20), the simulated
# RC has the loads 0..19.
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_WaitTimeFB", (("WaitTime", 0),), 0x8D34, 0),
    ("MC_ReadActualForceFB", (("CalibrationData", 20),), 0x8D17, 0),
]
