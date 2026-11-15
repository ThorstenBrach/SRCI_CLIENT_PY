# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      LOGON_MODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-02-01
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

"""LOGON_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/LOGON_MODE_TO_STRING.st
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
from srci.types import LogonMode

__all__ = ['LOGON_MODE_TO_STRING']


def LOGON_MODE_TO_STRING(*, Value: LogonMode = LogonMode.PASSWORD_ONLY) -> str:
    LOGON_MODE_TO_STRING: str = ''

    match Value:
        case LogonMode.PASSWORD_ONLY:
            LOGON_MODE_TO_STRING = trunc_str(StrReplace(Str='PASSWORD_ONLY ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case LogonMode.USERNAME_AND_PASSWORD:
            LOGON_MODE_TO_STRING = trunc_str(StrReplace(Str='USERNAME_AND_PASSWORD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case LogonMode.LEVEL_ID_AND_PASSWORD:
            LOGON_MODE_TO_STRING = trunc_str(StrReplace(Str='LEVEL_ID_AND_PASSWORD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            LOGON_MODE_TO_STRING = trunc_str(CONCAT('LOGON_MODE_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return LOGON_MODE_TO_STRING
