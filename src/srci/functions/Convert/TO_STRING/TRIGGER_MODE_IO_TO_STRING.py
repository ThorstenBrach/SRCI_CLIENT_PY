# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      TRIGGER_MODE_IO_TO_STRING
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

"""TRIGGER_MODE_IO_TO_STRING

ST-Source: Functions/Convert/TO_STRING/TRIGGER_MODE_IO_TO_STRING.st
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
from srci.types import TriggerModeIo

__all__ = ['TRIGGER_MODE_IO_TO_STRING']


def TRIGGER_MODE_IO_TO_STRING(*, Value: TriggerModeIo = TriggerModeIo.INVALID) -> str:
    TRIGGER_MODE_IO_TO_STRING: str = ''

    match Value:
        case TriggerModeIo.INVALID:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INVALID ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_INPUT_RISING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_INPUT_RISING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_INPUT_FALLING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_INPUT_FALLING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_INPUT_RISING_OR_FALLING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_INPUT_RISING_OR_FALLING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_INPUT_RISING_OR_FALLING_EDGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_INPUT_RISING_OR_FALLING_EDGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_OUTPUT_RISING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_OUTPUT_RISING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_OUTPUT_FALLING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_OUTPUT_FALLING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_EXCEEDING_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_EXCEEDING_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_ENTERING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_ENTERING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_EXCEEDING_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_EXCEEDING_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_ENTERING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_ENTERING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_EXCEEDING_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_EXCEEDING_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_VALUE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_VALUE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_ENTERING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_ENTERING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_EXCEEDING_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_EXCEEDING_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_ENTERING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_ENTERING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case TriggerModeIo.REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(StrReplace(Str='REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED ({0})', SubStr1='{0}', SubStr2=SINT_TO_STRING(Value)), 80)
        case _:
            TRIGGER_MODE_IO_TO_STRING = trunc_str(CONCAT('TRIGGER_MODE_IO_TO_STRING Function: Error -> no parsing for value ', SINT_TO_STRING(Value)), 80)
    return TRIGGER_MODE_IO_TO_STRING
