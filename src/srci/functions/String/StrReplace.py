"""Returns a given string where a given substing is replaced by another substring

ST-Source: Functions/String/StrReplace.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.rt import FIND, LEN, REPLACE

__all__ = ['StrReplace']


def StrReplace(*, Str: str = '', SubStr1: str = '', SubStr2: str = '') -> str:
    """Returns a given string where a given substing is replaced by another substring"""
    StrReplace: str = ''

    while FIND(Str, SubStr1) > 0:
        Str = REPLACE(Str, SubStr2, LEN(SubStr1), FIND(Str, SubStr1))

    StrReplace = Str
    return StrReplace
