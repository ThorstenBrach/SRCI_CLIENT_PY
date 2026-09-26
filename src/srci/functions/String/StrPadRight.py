# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      StrPadRight
#  Author:      Thorsten Brach
#  Date:        2024-12-18
#
#  Description:
#    Returns the given string, filled up on the right side to the given total length with the
#    given substring
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

"""Returns the given string, filled up on the right side to the given total length with the given substring

ST-Source: Functions/String/StrPadRight.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.rt import CONCAT, LEN

__all__ = ['StrPadRight']


def StrPadRight(*, Str: str = '', SubStr: str = '', Length: int = 0) -> str:
    """Returns the given string, filled up on the right side to the given total length with the given substring"""
    StrPadRight: str = ''

    while LEN(Str) < Length:
        Str = CONCAT(Str, SubStr)

    StrPadRight = Str
    return StrPadRight
