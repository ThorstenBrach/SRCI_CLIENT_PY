"""DATA_ENABLE_SYNC_TO_STRING

ST-Source: Functions/Convert/TO_STRING/DATA_ENABLE_SYNC_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.TO_STRING.BYTE_TO_STRING_BIN import BYTE_TO_STRING_BIN
from srci.iec.rt import bit, set_bit
from srci.types import DataEnableSync

__all__ = ['DATA_ENABLE_SYNC_TO_STRING']


def DATA_ENABLE_SYNC_TO_STRING(*, Value: DataEnableSync | None = None) -> str:
    if Value is None:
        Value = DataEnableSync()
    DATA_ENABLE_SYNC_TO_STRING: str = ''
    # temporary byte
    _tmpByte: int = 0

    _tmpByte = set_bit(_tmpByte, 0, Value.EnableSyncTool)
    _tmpByte = set_bit(_tmpByte, 1, Value.EnableSyncFrame)
    _tmpByte = set_bit(_tmpByte, 2, Value.EnableSyncLoad)
    _tmpByte = set_bit(_tmpByte, 3, Value.EnableSyncWorkArea)
    _tmpByte = set_bit(_tmpByte, 4, Value.EnableSyncSWLimits)
    _tmpByte = set_bit(_tmpByte, 5, Value.EnableSyncDefaultDynamics)
    _tmpByte = set_bit(_tmpByte, 6, Value.EnableSyncReferenceDynamics)

    DATA_ENABLE_SYNC_TO_STRING = BYTE_TO_STRING_BIN(Value=_tmpByte)
    return DATA_ENABLE_SYNC_TO_STRING
