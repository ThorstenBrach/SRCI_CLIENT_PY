# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      TELEGRAM_STATE_TO_STRING
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

"""TELEGRAM_STATE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TELEGRAM_STATE_TO_STRING.st
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
from srci.types import TelegramState

__all__ = ['TELEGRAM_STATE_TO_STRING']


def TELEGRAM_STATE_TO_STRING(*, State: TelegramState = TelegramState.UNDEFINED) -> str:
    TELEGRAM_STATE_TO_STRING: str = ''

    match State:
        case TelegramState.UNDEFINED:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='UNDEFINED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_162_INIT_LOST_UNKNOWN:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_162_INIT_LOST_UNKNOWN ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_163_TELEGRAM_LENGTH_MISMATCH:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_163_TELEGRAM_LENGTH_MISMATCH ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_165_LIFESIGN_TIMEOUT:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_165_LIFESIGN_TIMEOUT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_166_CYCLIC_DATA_TOO_LARGE:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_166_CYCLIC_DATA_TOO_LARGE ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_167_INTERFACE_WAS_RESET_AFTER_INIT:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_167_INTERFACE_WAS_RESET_AFTER_INIT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_168_TELEGRAM_SEQ_TIMEOUT:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_168_TELEGRAM_SEQ_TIMEOUT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_169_TELEGRAM_NO_CHANGED_AFTER_INIT:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_169_TELEGRAM_NO_CHANGED_AFTER_INIT ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_170_AXESGROUP_ID_INVALID:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_170_AXESGROUP_ID_INVALID ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_171_TELEGRAM_NUMBER_INVALID:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_171_TELEGRAM_NUMBER_INVALID ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.ERROR_173_SERVER_CONNECTION_LOST:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='ERROR_173_SERVER_CONNECTION_LOST ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.READY_TO_RESUME:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='READY_TO_RESUME ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.READY_FOR_INITIALIZATION:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='READY_FOR_INITIALIZATION ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case TelegramState.INITIALIZED:
            TELEGRAM_STATE_TO_STRING = trunc_str(StrReplace(Str='INITIALIZED ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(State)), 80)
        case _:
            TELEGRAM_STATE_TO_STRING = trunc_str(CONCAT('TELEGRAM_STATE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(State)), 80)
    return TELEGRAM_STATE_TO_STRING
