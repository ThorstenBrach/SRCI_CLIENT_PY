"""SENSOR_CONNECTION_MODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/SENSOR_CONNECTION_MODE_TO_STRING.st
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
from srci.types import SensorConnectionMode

__all__ = ['SENSOR_CONNECTION_MODE_TO_STRING']


def SENSOR_CONNECTION_MODE_TO_STRING(*, Value: SensorConnectionMode = SensorConnectionMode.RC_SENSOR_ALGORITHM) -> str:
    SENSOR_CONNECTION_MODE_TO_STRING: str = ''

    match Value:
        case SensorConnectionMode.RC_SENSOR_ALGORITHM:
            SENSOR_CONNECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='RC_SENSOR_ALGORITHM ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case SensorConnectionMode.PLC_SENSOR_RC_ALGORITHM:
            SENSOR_CONNECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='PLC_SENSOR_RC_ALGORITHM ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case SensorConnectionMode.PLC_SENSOR_ALGORITHM:
            SENSOR_CONNECTION_MODE_TO_STRING = trunc_str(StrReplace(Str='PLC_SENSOR_ALGORITHM ({0})', SubStr1='{0}', SubStr2=USINT_TO_STRING(Value)), 80)
        case _:
            SENSOR_CONNECTION_MODE_TO_STRING = trunc_str(CONCAT('SENSOR_CONNECTION_MODE_TO_STRING Function: Error -> no parsing for value ', USINT_TO_STRING(Value)), 80)
    return SENSOR_CONNECTION_MODE_TO_STRING
