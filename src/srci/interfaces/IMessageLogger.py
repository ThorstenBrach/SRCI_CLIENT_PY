# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      IMessageLogger
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""IMessageLogger

ST-Source: Interfaces/IMessageLogger.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing import Protocol

if TYPE_CHECKING:
    from srci.types import AlarmMessage

__all__ = ['IMessageLogger']


class IMessageLogger(Protocol):
    def AddMessageLog(self, *, MessageLog: AlarmMessage | None = None) -> None: ...
    def AddSystemLog(self, *, SystemLog: str = '') -> None: ...
