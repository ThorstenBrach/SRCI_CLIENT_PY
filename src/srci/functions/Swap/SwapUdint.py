"""SwapUdint

ST-Source: Functions/Swap/SwapUdint.st
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

__all__ = ['SwapUdint']


def SwapUdint(*, Value: int = 0) -> int:
    SwapUdint: int = 0

    _adr_Value = ADR_VALUE(Value, _iec.UDINT)  # ADR(Value)
    SwapBytes(pValue=_adr_Value, Size=4)
    Value = _adr_Value.value

    SwapUdint = Value
    return SwapUdint
