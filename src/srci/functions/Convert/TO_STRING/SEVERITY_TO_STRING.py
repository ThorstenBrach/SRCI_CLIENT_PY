"""SEVERITY_TO_STRING

ST-Source: Functions/Convert/TO_STRING/SEVERITY_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import Severity

__all__ = ['SEVERITY_TO_STRING']


def SEVERITY_TO_STRING(*, Value: Severity = Severity.DEACTIVATE, AlignString: bool = False) -> str:
    SEVERITY_TO_STRING: str = ''

    if AlignString:
        match Value:
            case Severity.DEBUG:
                SEVERITY_TO_STRING = 'DEBUG      '
            case Severity.INFO:
                SEVERITY_TO_STRING = 'INFO       '
            case Severity.WARNING:
                SEVERITY_TO_STRING = 'WARNING    '
            case Severity.ERROR:
                SEVERITY_TO_STRING = 'ERROR      '
            case Severity.FATAL_ERROR:
                SEVERITY_TO_STRING = 'FATAL_ERROR'
            case _:
                SEVERITY_TO_STRING = 'UNKOWN     '
    else:
        match Value:
            case Severity.DEBUG:
                SEVERITY_TO_STRING = 'DEBUG'
            case Severity.INFO:
                SEVERITY_TO_STRING = 'INFO'
            case Severity.WARNING:
                SEVERITY_TO_STRING = 'WARNING'
            case Severity.ERROR:
                SEVERITY_TO_STRING = 'ERROR'
            case Severity.FATAL_ERROR:
                SEVERITY_TO_STRING = 'FATAL_ERROR'
            case _:
                SEVERITY_TO_STRING = 'UNKOWN'
    return SEVERITY_TO_STRING
