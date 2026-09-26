# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      JOG_CONTROL_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-03-01
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

"""JOG_CONTROL_TO_STRING

ST-Source: Functions/Convert/TO_STRING/JOG_CONTROL_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.iec.rt import CONCAT, trunc_str
from srci.types import JogControl

__all__ = ['JOG_CONTROL_TO_STRING']


def JOG_CONTROL_TO_STRING(*, Value: JogControl | None = None) -> str:
    if Value is None:
        Value = JogControl()
    JOG_CONTROL_TO_STRING: str = ''

    JOG_CONTROL_TO_STRING = '2#'

    if Value.E6_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E6_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E5_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E5_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1_'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0_'), 80)

    if Value.E4_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E4_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E3_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E3_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '_'), 80)

    if Value.E2_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E2_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E1_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.E1_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Rz_J6_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Rz_J6_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Ry_J5_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Ry_J5_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '_'), 80)

    if Value.Rx_J4_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Rx_J4_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Z_J3_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Z_J3_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Y_J2_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.Y_J2_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.X_J1_Neg:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)

    if Value.X_J1_Pos:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '1'), 80)
    else:
        JOG_CONTROL_TO_STRING = trunc_str(CONCAT(JOG_CONTROL_TO_STRING, '0'), 80)
    return JOG_CONTROL_TO_STRING
