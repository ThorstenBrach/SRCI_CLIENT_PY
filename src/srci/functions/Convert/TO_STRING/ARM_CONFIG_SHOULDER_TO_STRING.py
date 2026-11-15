# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      ARM_CONFIG_SHOULDER_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-02-04
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

"""ARM_CONFIG_SHOULDER_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ARM_CONFIG_SHOULDER_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import INT_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import ArmConfigShoulder

__all__ = ['ARM_CONFIG_SHOULDER_TO_STRING']


def ARM_CONFIG_SHOULDER_TO_STRING(*, Value: ArmConfigShoulder = ArmConfigShoulder.USE_CONFIG) -> str:
    ARM_CONFIG_SHOULDER_TO_STRING: str = ''

    match Value:
        case ArmConfigShoulder.USE_CONFIG:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(StrReplace(Str='Shoulder = USE_CONFIG ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigShoulder.SAME:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(StrReplace(Str='Shoulder = SAME ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigShoulder.FREE:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(StrReplace(Str='Shoulder = FREE ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigShoulder.BACK:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(StrReplace(Str='Shoulder = BACK ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case ArmConfigShoulder.FRONT:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(StrReplace(Str='Shoulder = FRONT ({0})', SubStr1='{0}', SubStr2=INT_TO_STRING(Value)), 80)
        case _:
            ARM_CONFIG_SHOULDER_TO_STRING = trunc_str(CONCAT('ARM_CONFIG_SHOULDER_TO_STRING Function: Error -> no parsing for value ', INT_TO_STRING(Value)), 80)
    return ARM_CONFIG_SHOULDER_TO_STRING
