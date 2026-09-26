"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupStateSyncStateNo
Author:      Thorsten Brach
Date:        2025-12-20

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

from RobotLibrary.IEC_Types import IEC_Struct 

class AxesGroupStateSyncStateNo(IEC_Struct):
    Tool: int
    """Amount of unsynchronized tool data"""

    Frame: int
    """Amount of unsynchronized frame data"""

    Load: int
    """Amount of unsynchronized load data"""

    WorkArea: int
    """Amount of unsynchronized work areas"""