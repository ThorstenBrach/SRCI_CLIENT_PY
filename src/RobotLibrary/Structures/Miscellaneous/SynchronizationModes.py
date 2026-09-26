"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SynchronizationModes
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
from RobotLibrary.IEC_Types import IEC_Struct, ARRAY
from RobotLibrary.Enumerations.Mode.SyncMode import  SyncMode
from RobotLibrary.Enumerations.Miscellaneous.SyncTime import  SyncTime

class SynchronizationModes(IEC_Struct):
    

    Tool              : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for tool
    """

    Frame             : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for frame
    """

    Load              : ARRAY[SyncMode] = ARRAY(0,  SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for load
    """

    WorkAreas         : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode )
    """
    synchronization direction for work areas
    """

    SwLimits          : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for SW limits
    """

    DefaultDynamics   : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for defaul dynamics
    """
    
    ReferenceDynamics : ARRAY[SyncMode] = ARRAY(0, SyncTime.AFTER_START_UP, SyncMode)
    """
    synchronization direction for reference dynamics 
    """