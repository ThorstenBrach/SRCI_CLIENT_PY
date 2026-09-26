"""PATH_CHOICE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/PATH_CHOICE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import BYTE_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import PathChoice

__all__ = ['PATH_CHOICE_TO_STRING']


def PATH_CHOICE_TO_STRING(*, Value: PathChoice = PathChoice.CLOCKWISE) -> str:
    PATH_CHOICE_TO_STRING: str = ''

    match Value:
        case PathChoice.CLOCKWISE:
            PATH_CHOICE_TO_STRING = trunc_str(StrReplace(Str='CLOCKWISE ({0})', SubStr1='{0}', SubStr2=BYTE_TO_STRING(Value)), 80)
        case PathChoice.COUNTERCLOCKWISE:
            PATH_CHOICE_TO_STRING = trunc_str(StrReplace(Str='COUNTERCLOCKWISE ({0})', SubStr1='{0}', SubStr2=BYTE_TO_STRING(Value)), 80)
        case _:
            PATH_CHOICE_TO_STRING = trunc_str(CONCAT('PATH_CHOICE_TO_STRING Function: Error -> no parsing for value ', BYTE_TO_STRING(Value)), 80)
    return PATH_CHOICE_TO_STRING
