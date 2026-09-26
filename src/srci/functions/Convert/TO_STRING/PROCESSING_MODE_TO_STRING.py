"""PROCESSING_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/PROCESSING_MODE_TO_STRING.st
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
from srci.types import ProcessingMode

__all__ = ['PROCESSING_MODE_TO_STRING']


def PROCESSING_MODE_TO_STRING(*, Value: ProcessingMode = ProcessingMode.BUFFERED) -> str:
    PROCESSING_MODE_TO_STRING: str = ''

    match Value:
        case ProcessingMode.BUFFERED:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='BUFFERED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.ABORTING:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='ABORTING ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.PARALLEL:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='PARALLEL ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.CONTINUOUS:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='CONTINUOUS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.DEACTIVATE:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='DEACTIVATE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.TRIGGER_BUFFERED:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_BUFFERED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.TRIGGER_ABORTING:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_ABORTING ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.TRIGGER_ONCE:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_ONCE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.TRIGGER_CONTINUOUS:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_CONTINUOUS ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case ProcessingMode.TRIGGER_MULTIPLE:
            PROCESSING_MODE_TO_STRING = trunc_str(StrReplace(Str='TRIGGER_MULTIPLE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            PROCESSING_MODE_TO_STRING = trunc_str(CONCAT('PROCESSING_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return PROCESSING_MODE_TO_STRING
