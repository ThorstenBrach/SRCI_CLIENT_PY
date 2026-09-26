"""Returns the given string, filled up on the right side to the given total length with the given substring

ST-Source: Functions/String/StrPadRight.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.rt import CONCAT, LEN

__all__ = ['StrPadRight']


def StrPadRight(*, Str: str = '', SubStr: str = '', Length: int = 0) -> str:
    """Returns the given string, filled up on the right side to the given total length with the given substring"""
    StrPadRight: str = ''

    while LEN(Str) < Length:
        Str = CONCAT(Str, SubStr)

    StrPadRight = Str
    return StrPadRight
