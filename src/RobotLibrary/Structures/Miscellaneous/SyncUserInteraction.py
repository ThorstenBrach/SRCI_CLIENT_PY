"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SyncUserInteraction
Author:      Thorsten Brach
Date:        2025-12-18

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
from RobotLibrary.IEC_Types import BOOL, IEC_Struct


class SyncUserInteraction(IEC_Struct):

    Tool: BOOL
    """Synchronization of tool needs user interaction"""

    Frame: BOOL
    """Synchronization of frame needs user interaction"""

    Load: BOOL
    """Synchronization of load needs user interaction"""

    WorkAreas: BOOL
    """Synchronization of work areas needs user interaction"""

    SwLimits: BOOL
    """Synchronization of SW limits needs user interaction"""

    DefaultDynamics: BOOL
    """Synchronization of default dynamics needs user interaction"""

    ReferenceDynamics: BOOL
    """Synchronization of reference dynamics needs user interaction"""