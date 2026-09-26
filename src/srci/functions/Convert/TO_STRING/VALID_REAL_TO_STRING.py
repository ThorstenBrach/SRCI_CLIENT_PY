"""VALID_REAL_TO_STRING

ST-Source: Functions/Convert/TO_STRING/VALID_REAL_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.conv import REAL_TO_STRING
from srci.iec.rt import SysDepIsValidReal, trunc_str

__all__ = ['VALID_REAL_TO_STRING']


def VALID_REAL_TO_STRING(*, Value: float = 0.0) -> str:
    VALID_REAL_TO_STRING: str = ''

    if SysDepIsValidReal(Value=Value):
        VALID_REAL_TO_STRING = trunc_str(REAL_TO_STRING(Value), 80)
    else:
        VALID_REAL_TO_STRING = 'NaN'
    return VALID_REAL_TO_STRING
