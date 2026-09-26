# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SRCI client for Python.
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

"""SRCI client for Python.

Python port of the open SRCI PLC library (https://github.com/ThorstenBrach/SRCI),
based on the SRCI profile V1.5.9. The structure (function blocks, methods, step
numbers, error ids) mirrors the PLC library 1:1 so that fixes can be ported
between both implementations. See ``docs/PORTING.md``.
"""

from srci.library_parameters import configure, parameters

__version__ = "0.1.0.dev0"

SRCI_PROFILE_VERSION = "1.5.9"

__all__ = ["SRCI_PROFILE_VERSION", "__version__", "configure", "parameters"]
