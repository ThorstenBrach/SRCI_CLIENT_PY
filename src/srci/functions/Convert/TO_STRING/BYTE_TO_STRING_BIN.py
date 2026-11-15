# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      BYTE_TO_STRING_BIN
#  Author:      Thorsten Brach
#  Date:        2025-01-20
#
#  Description:
#
#
#  Copyright:
#    (C) 2025 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""BYTE_TO_STRING_BIN

ST-Source: Functions/Convert/TO_STRING/BYTE_TO_STRING_BIN.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.conv import WORD_TO_STRING
from srci.iec.rt import CONCAT, bit, trunc_str

__all__ = ['BYTE_TO_STRING_BIN']


def BYTE_TO_STRING_BIN(*, Value: int = 0) -> str:
    BYTE_TO_STRING_BIN: str = ''

    BYTE_TO_STRING_BIN = '2#'

    if bit(Value, 7):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 6):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 5):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 4):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1_'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0_'), 80)

    if bit(Value, 3):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 2):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 1):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    if bit(Value, 0):
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '1'), 80)
    else:
        BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, '0'), 80)

    BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, ' ('), 80)
    BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, WORD_TO_STRING(Value)), 80)
    BYTE_TO_STRING_BIN = trunc_str(CONCAT(BYTE_TO_STRING_BIN, ')'), 80)
    return BYTE_TO_STRING_BIN
