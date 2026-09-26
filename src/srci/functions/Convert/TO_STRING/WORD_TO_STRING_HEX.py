"""WORD_TO_STRING_HEX

ST-Source: Functions/Convert/TO_STRING/WORD_TO_STRING_HEX.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.conv import WORD_TO_BYTE
from srci.iec.rt import CONCAT, trunc_str

__all__ = ['WORD_TO_STRING_HEX']


def WORD_TO_STRING_HEX(*, Value: int = 0) -> str:
    WORD_TO_STRING_HEX: str = ''
    # high Byte
    _highByte: int = 0
    # low Byte
    _lowByte: int = 0
    # high Nibble
    _highNibble: int = 0
    # low Nibble
    _lowNibble: int = 0
    # single Hex char
    hexChar: str = ''
    # Hex chars
    hexChars: list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

    # get high and low byte from word
    _highByte = WORD_TO_BYTE(Value >> 8)
    _lowByte = WORD_TO_BYTE(Value & 255)

    # convert highest Byte to HEX
    _highNibble = _highByte >> 4
    _lowNibble = _highByte & 15
    WORD_TO_STRING_HEX = trunc_str(CONCAT(hexChars[_highNibble], hexChars[_lowNibble]), 80)

    # convert lowest Byte to HEX
    _highNibble = _lowByte >> 4
    _lowNibble = _lowByte & 15
    WORD_TO_STRING_HEX = trunc_str(CONCAT(WORD_TO_STRING_HEX, CONCAT(hexChars[_highNibble], hexChars[_lowNibble])), 80)
    return WORD_TO_STRING_HEX
