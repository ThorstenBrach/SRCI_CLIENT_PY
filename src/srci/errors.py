# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.errors
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Exceptions of the srci package.
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

"""Exceptions of the srci package.

The PLC library silently writes/reads past buffer ends (``SysDepMemCpy``) - the Python
port raises instead, so that such situations are found by tests.
"""

from __future__ import annotations

__all__ = ["PayloadOverflowError", "PayloadUnderflowError", "SrciError", "ValueRangeError"]


class SrciError(Exception):
    """Base class of all srci exceptions."""


class PayloadOverflowError(SrciError, BufferError):
    """Writing would exceed the payload buffer."""


class PayloadUnderflowError(SrciError, BufferError):
    """Reading would exceed the received payload."""


class ValueRangeError(SrciError, ValueError):
    """A value does not fit into the IEC data type it is written as."""
