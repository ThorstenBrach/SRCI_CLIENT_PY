# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return.io
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    SDK return, group IO: registers, analog IO, WriteSystemVariable
#    (10_Application_Registers.cpp).
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

"""SDK return, group IO: registers, analog IO, WriteSystemVariable (10_Application_Registers.cpp)."""

from __future__ import annotations

from typing import Any

ADDED = (5206, 6102, 6103, 6105, 6106, 6107, 6108, 6109)

RSP_VALUES: dict[str, dict[str, object]] = {
    "MC_ReadAnalogInputFB": {"Unit": 1},
    "MC_ReadAnalogOutputFB": {"Unit": 1},
}

_ZERO7 = tuple((f"Index[{i}]", 0) for i in range(7))
# ReadAnalogInput / WriteAnalogOutput Index 0 / > 32: checked by the client (not sent)
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = [
    ("MC_ReadIntegersFB", (("Index[0]", 1), ("Index[1]", 1)), 0x8D48, 0),
    ("MC_ReadIntegersFB", _ZERO7, 0x8D50, 0),
    ("MC_ReadIntegersFB", (("Index[0]", 21),), 0x8D47, 0),
    ("MC_ReadRealsFB", (("Index[2]", 4), ("Index[5]", 4)), 0x8D48, 0),
    ("MC_ReadRealsFB", _ZERO7, 0x8D50, 0),
    ("MC_WriteIntegersFB", (("Index[0]", 2), ("Index[6]", 2)), 0x8D48, 0),
    ("MC_WriteIntegersFB", (*_ZERO7[1:], ("Index[0]", 3), ("Values[1]", 5)), 0, 0x6D51),
    ("MC_WriteRealsFB", (("Index[3]", 99),), 0x8D47, 0),
]
