"""FRAGMENT_ACTION_TO_STRING

ST-Source: Functions/Convert/TO_STRING/FRAGMENT_ACTION_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.rt import CONCAT, bit, trunc_str

__all__ = ['FRAGMENT_ACTION_TO_STRING']


def FRAGMENT_ACTION_TO_STRING(*, FragmentAction: int = 0) -> str:
    FRAGMENT_ACTION_TO_STRING: str = ''

    if bit(FragmentAction, 0):
        FRAGMENT_ACTION_TO_STRING = trunc_str(CONCAT(FRAGMENT_ACTION_TO_STRING, ' Complete (Bit 0)'), 80)

    if bit(FragmentAction, 1):
        FRAGMENT_ACTION_TO_STRING = trunc_str(CONCAT(FRAGMENT_ACTION_TO_STRING, ' Reset (Bit 1)'), 80)

    if bit(FragmentAction, 2):
        FRAGMENT_ACTION_TO_STRING = trunc_str(CONCAT(FRAGMENT_ACTION_TO_STRING, ' Clear (Bit 2)'), 80)
    return FRAGMENT_ACTION_TO_STRING
