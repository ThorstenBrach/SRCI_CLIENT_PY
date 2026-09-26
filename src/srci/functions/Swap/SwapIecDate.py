# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      SwapIecDate
#  Author:      Thorsten Brach
#  Date:        2024-06-09
#
#  Description:
#
#
#  Copyright:
#    (C) 2024 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""SwapIecDate

ST-Source: Functions/Swap/SwapIecDate.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
from srci.functions.Swap.SwapBytes import SwapBytes
from srci.iec.rt import ADR_VALUE

__all__ = ['SwapIecDate']


def SwapIecDate(*, Value: int = 0) -> int:
    SwapIecDate: int = 0

    _adr_Value = ADR_VALUE(Value, _iec.UINT)  # ADR(Value)
    SwapBytes(pValue=_adr_Value, Size=2)
    Value = _adr_Value.value

    SwapIecDate = Value
    return SwapIecDate
