# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      IEC_TIME_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-01-24
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

"""IEC_TIME_TO_STRING

ST-Source: Functions/Convert/TO_STRING/IEC_TIME_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.DT import IEC_TIME_TO_TIME
from srci.iec.conv import TOD_TO_STRING
from srci.iec.rt import trunc_str

__all__ = ['IEC_TIME_TO_STRING']


def IEC_TIME_TO_STRING(*, Value: int = 0) -> str:
    IEC_TIME_TO_STRING: str = ''
    # temporary date
    _tmpData: int = 0

    IEC_TIME_TO_STRING = trunc_str(TOD_TO_STRING(IEC_TIME_TO_TIME(Value=Value)), 80)
    return IEC_TIME_TO_STRING
