# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      SYNC_TIME_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-04-13
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

"""SYNC_TIME_TO_STRING

ST-Source: Functions/Convert/TO_STRING/SYNC_TIME_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import DINT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import SyncTime

__all__ = ['SYNC_TIME_TO_STRING']


def SYNC_TIME_TO_STRING(*, Value: SyncTime = SyncTime.DURING_START_UP) -> str:
    SYNC_TIME_TO_STRING: str = ''

    match Value:
        case SyncTime.DURING_START_UP:
            SYNC_TIME_TO_STRING = trunc_str(StrReplace(Str='DURING_START_UP ({0})', SubStr1='{0}', SubStr2=DINT_TO_STRING(Value)), 80)
        case SyncTime.AFTER_START_UP:
            SYNC_TIME_TO_STRING = trunc_str(StrReplace(Str='AFTER_START_UP ({0})', SubStr1='{0}', SubStr2=DINT_TO_STRING(Value)), 80)
        case _:
            SYNC_TIME_TO_STRING = trunc_str(CONCAT('SYNC_TIME_TO_STRING Function: Error -> no parsing for value ', DINT_TO_STRING(Value)), 80)
    return SYNC_TIME_TO_STRING
