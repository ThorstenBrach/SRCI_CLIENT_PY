"""EXECUTION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/EXECUTION_MODE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import USINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import ExecutionMode

__all__ = ['EXECUTION_MODE_TO_STRING']


def EXECUTION_MODE_TO_STRING(*, Value: ExecutionMode = ExecutionMode.SEQUENCE_PRIMARY) -> str:
    EXECUTION_MODE_TO_STRING: str = ''

    match Value:
        case ExecutionMode.SEQUENCE_PRIMARY:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='SEQUENCE_PRIMARY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.SEQUENCE_ABORT_OTHERS_PRIMARY:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='SEQUENCE_ABORT_OTHERS_PRIMARY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.PARALLEL:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='PARALLEL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.CONTINUOUS:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='CONTINUOUS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.TRIGGER_MULTIPLE:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_MULTIPLE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.SEQUENCE_SECONDARY:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='SEQUENCE_SECONDARY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.SEQUENCE_ABORT_OTHERS_SECONDARY:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='SEQUENCE_ABORT_OTHERS_SECONDARY ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ExecutionMode.STOP_PARALLEL_CONTINUOUS_TRIGGER:
            EXECUTION_MODE_TO_STRING = trunc_str(StrReplace(Str='STOP_PARALLEL_CONTINUOUS_TRIGGER ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            EXECUTION_MODE_TO_STRING = trunc_str(CONCAT('EXECUTION_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return EXECUTION_MODE_TO_STRING
