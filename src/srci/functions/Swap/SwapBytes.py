# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      SwapBytes
#  Author:      Thorsten Brach
#  Date:        2024-06-01
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

"""SwapBytes

ST-Source: Functions/Swap/SwapBytes.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
from srci.iec.rt import ADR, SysDepMemCpy
from srci.types import RobotLibraryParameter

if TYPE_CHECKING:
    from srci.iec.rt import Ptr

__all__ = ['SwapBytes']


def SwapBytes(*, pValue: Ptr | None = None, Size: int = 0) -> None:
    # Pointer to low word low byte
    _pLwLb: Ptr | None = None
    # Pointer to low word high byte
    _pLwHb: Ptr | None = None
    # Pointer to high word low byte
    _pHwLb: Ptr | None = None
    # Pointer to high word high byte
    _pHwHb: Ptr | None = None
    # temporary bytes
    _tmpBytes: _iec.IecArray[int] = _iec.IecArray(1, [0] * 4)

    if RobotLibraryParameter.SWAP_BYTE_ORDER and Size == 2:
        _pLwLb = pValue + 0
        _pLwHb = pValue + 1

        # swap bytes
        _tmpBytes[1] = _pLwHb.deref(_iec.BYTE)
        _tmpBytes[2] = _pLwLb.deref(_iec.BYTE)

        # copy bytes to data type
        SysDepMemCpy(pDest=pValue, pSrc=ADR(_tmpBytes, None, _iec.ArrayType(1, 4, _iec.BYTE)), DataLen=Size)

    if RobotLibraryParameter.SWAP_BYTE_ORDER and Size == 4:
        _pLwLb = pValue + 0
        _pLwHb = pValue + 1
        _pHwLb = pValue + 2
        _pHwHb = pValue + 3

        # swap bytes
        _tmpBytes[1] = _pHwHb.deref(_iec.BYTE)
        _tmpBytes[2] = _pHwLb.deref(_iec.BYTE)
        _tmpBytes[3] = _pLwHb.deref(_iec.BYTE)
        _tmpBytes[4] = _pLwLb.deref(_iec.BYTE)

        # copy bytes to data type
        SysDepMemCpy(pDest=pValue, pSrc=ADR(_tmpBytes, None, _iec.ArrayType(1, 4, _iec.BYTE)), DataLen=Size)
