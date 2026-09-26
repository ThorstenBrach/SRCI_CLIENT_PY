"""WORD_TO_STRING_BIN

ST-Source: Functions/Convert/TO_STRING/WORD_TO_STRING_BIN.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.conv import WORD_TO_STRING
from srci.iec.rt import CONCAT, bit, trunc_str

__all__ = ['WORD_TO_STRING_BIN']


def WORD_TO_STRING_BIN(*, Value: int = 0) -> str:
    WORD_TO_STRING_BIN: str = ''

    WORD_TO_STRING_BIN = '2#'

    if bit(Value, 15):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 14):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 13):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 12):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1_'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0_'), 80)

    if bit(Value, 11):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 10):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 9):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 8):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1_'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0_'), 80)

    if bit(Value, 7):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 6):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 5):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 4):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1_'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0_'), 80)

    if bit(Value, 3):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 2):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 1):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    if bit(Value, 0):
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '1'), 80)
    else:
        WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, '0'), 80)

    WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, ' ('), 80)
    WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, WORD_TO_STRING(Value)), 80)
    WORD_TO_STRING_BIN = trunc_str(CONCAT(WORD_TO_STRING_BIN, ')'), 80)
    return WORD_TO_STRING_BIN
