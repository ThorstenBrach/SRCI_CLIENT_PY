# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      TRIGGER_MODE_LIMIT_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-03-02
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

"""TRIGGER_MODE_LIMIT_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TRIGGER_MODE_LIMIT_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import SINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import TriggerModeLimit

__all__ = ['TRIGGER_MODE_LIMIT_TO_STRING']


def TRIGGER_MODE_LIMIT_TO_STRING(*, Value: TriggerModeLimit = TriggerModeLimit.INVALID) -> str:
    TRIGGER_MODE_LIMIT_TO_STRING: str = ''

    match Value:
        case TriggerModeLimit.INVALID:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(StrReplace(Str='INVALID ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeLimit.JOINT_CURRENT:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(StrReplace(Str='JOINT_CURRENT ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeLimit.FORCE:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(StrReplace(Str='FORCE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeLimit.FOLLOWING_ERROR:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(StrReplace(Str='FOLLOWING_ERROR ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeLimit.TEMPERATURE:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(StrReplace(Str='TEMPERATURE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TRIGGER_MODE_LIMIT_TO_STRING = trunc_str(CONCAT('TRIGGER_MODE_LIMIT_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TRIGGER_MODE_LIMIT_TO_STRING
