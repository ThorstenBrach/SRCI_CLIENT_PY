"""MESSAGE_TYPE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/MESSAGE_TYPE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import MessageType

__all__ = ['MESSAGE_TYPE_TO_STRING']


def MESSAGE_TYPE_TO_STRING(*, Value: MessageType = MessageType.RI, AlignString: bool = False) -> str:
    MESSAGE_TYPE_TO_STRING: str = ''

    if AlignString:
        match Value:

            case MessageType.RI:
                MESSAGE_TYPE_TO_STRING = 'RI '
            case MessageType.RC:
                MESSAGE_TYPE_TO_STRING = 'RC '
            case MessageType.RA:
                MESSAGE_TYPE_TO_STRING = 'RA '
            case MessageType.CMD:
                MESSAGE_TYPE_TO_STRING = 'CMD'
            case _:
                MESSAGE_TYPE_TO_STRING = '???'
    else:
        match Value:

            case MessageType.RI:
                MESSAGE_TYPE_TO_STRING = 'RI'
            case MessageType.RC:
                MESSAGE_TYPE_TO_STRING = 'RC'
            case MessageType.RA:
                MESSAGE_TYPE_TO_STRING = 'RA'
            case MessageType.CMD:
                MESSAGE_TYPE_TO_STRING = 'CMD'
            case _:
                MESSAGE_TYPE_TO_STRING = '???'
    return MESSAGE_TYPE_TO_STRING
