# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      DATA_IN_SYNC_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-01-24
#
#  Description:
#
#
#  Copyright:
#    (C) 2025 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""DATA_IN_SYNC_TO_STRING

ST-Source: Functions/Convert/TO_STRING/DATA_IN_SYNC_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.iec.rt import bit, set_bit
from srci.types import DataInSync

__all__ = ['DATA_IN_SYNC_TO_STRING']


def DATA_IN_SYNC_TO_STRING(*, Value: DataInSync | None = None) -> str:
    if Value is None:
        Value = DataInSync()
    DATA_IN_SYNC_TO_STRING: str = ''
    # temporary byte
    _tmpByte: int = 0

    _tmpByte = set_bit(_tmpByte, 0, Value.ToolsInSync)
    _tmpByte = set_bit(_tmpByte, 1, Value.FramesInSync)
    _tmpByte = set_bit(_tmpByte, 2, Value.LoadsInSync)
    _tmpByte = set_bit(_tmpByte, 3, Value.WorkAreasInSync)
    _tmpByte = set_bit(_tmpByte, 4, Value.SoftwareLimitsInSync)
    _tmpByte = set_bit(_tmpByte, 5, Value.DefaultDynamicsInSync)
    _tmpByte = set_bit(_tmpByte, 6, Value.ReferenceDynamicsInSync)
    _tmpByte = set_bit(_tmpByte, 7, False)

    DATA_IN_SYNC_TO_STRING = BYTE_TO_STRING_BIN(Value=_tmpByte)
    return DATA_IN_SYNC_TO_STRING
