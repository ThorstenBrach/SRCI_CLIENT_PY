# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.api
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    High level entry points.
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

"""High level entry points.

* :class:`RobotProgram` - RobotTask + user data + command function blocks (one PLC program)
* :class:`SrciClient` - drives a :class:`RobotProgram` from a sequential Python script
"""

from srci.api.client import CommandError, SrciClient, WaitTimeoutError
from srci.api.program import RobotProgram

__all__ = ["CommandError", "RobotProgram", "SrciClient", "WaitTimeoutError"]
