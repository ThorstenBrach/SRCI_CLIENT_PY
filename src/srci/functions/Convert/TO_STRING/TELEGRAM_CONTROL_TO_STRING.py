# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      TELEGRAM_CONTROL_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2024-11-16
#
#  Description:
#
#
#  Copyright:
#    (C) 2024 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""TELEGRAM_CONTROL_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TELEGRAM_CONTROL_TO_STRING.st
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
from srci.types import ControlHalfByte

__all__ = ['TELEGRAM_CONTROL_TO_STRING']


def TELEGRAM_CONTROL_TO_STRING(*, Control: ControlHalfByte = ControlHalfByte.NONE) -> str:
    TELEGRAM_CONTROL_TO_STRING: str = ''

    match Control:
        case ControlHalfByte.NONE:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='NONE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case ControlHalfByte.INITIALIZE:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='INITIALIZE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case ControlHalfByte.RESUME:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='RESUME ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case ControlHalfByte.RESET:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='RESET ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case ControlHalfByte.ACK_ERROR:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='ACK_ERROR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case ControlHalfByte.CLIENT_ERROR:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(StrReplace(Str='CLIENT_ERROR ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Control)), 80)
        case _:
            TELEGRAM_CONTROL_TO_STRING = trunc_str(CONCAT('TelegramControlToString-Function: Error -> no parsing for value ', USINT_TO_STRING(Control)), 80)
    return TELEGRAM_CONTROL_TO_STRING
