"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ConnectionMode
Author:      Thorsten Brach
Date:        2025-12-14

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import SINT, SINTEnum

class ConnectionMode(SINTEnum):
    RC_CONNECTED = 0
    """
    Encoder is connected to RC
    """

    PLC_CONNECTED = 1
    """
    Encoder is connected to PLC
    """
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    