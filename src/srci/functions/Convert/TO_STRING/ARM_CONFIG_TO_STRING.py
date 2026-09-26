"""ARM_CONFIG_TO_STRING

ST-Source: Functions/Convert/TO_STRING/ARM_CONFIG_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.Convert.TO_STRING.ARM_CONFIG_ELBOW_TO_STRING import ARM_CONFIG_ELBOW_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_SHOULDER_TO_STRING import ARM_CONFIG_SHOULDER_TO_STRING
from srci.functions.Convert.TO_STRING.ARM_CONFIG_WRIST_TO_STRING import ARM_CONFIG_WRIST_TO_STRING
from srci.iec.rt import CONCAT, trunc_str
from srci.types import ArmConfigParameter

__all__ = ['ARM_CONFIG_TO_STRING']


def ARM_CONFIG_TO_STRING(*, Value: ArmConfigParameter | None = None) -> str:
    if Value is None:
        Value = ArmConfigParameter()
    ARM_CONFIG_TO_STRING: str = ''
    # temporary byte
    _tmpByte: int = 0

    ARM_CONFIG_TO_STRING = ''
    ARM_CONFIG_TO_STRING = trunc_str(CONCAT(ARM_CONFIG_TO_STRING, ARM_CONFIG_SHOULDER_TO_STRING(Value=Value.Shoulder)), 80)
    ARM_CONFIG_TO_STRING = trunc_str(CONCAT(ARM_CONFIG_TO_STRING, ' ; '), 80)
    ARM_CONFIG_TO_STRING = trunc_str(CONCAT(ARM_CONFIG_TO_STRING, ARM_CONFIG_ELBOW_TO_STRING(Value=Value.Elbow)), 80)
    ARM_CONFIG_TO_STRING = trunc_str(CONCAT(ARM_CONFIG_TO_STRING, ' ; '), 80)
    ARM_CONFIG_TO_STRING = trunc_str(CONCAT(ARM_CONFIG_TO_STRING, ARM_CONFIG_WRIST_TO_STRING(Value=Value.Wrist)), 80)
    return ARM_CONFIG_TO_STRING
