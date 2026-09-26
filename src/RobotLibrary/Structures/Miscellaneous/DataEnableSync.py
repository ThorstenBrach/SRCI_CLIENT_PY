"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DataEnableSync
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
from RobotLibrary.IEC_Types import BYTE, IEC_Struct


class DataEnableSync(IEC_Struct):

    EnableSyncTool : bool = True 
    """ 
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for tool data
    """

    EnableSyncFrame : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for frame data
    """

    EnableSyncLoad : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for load data
    """

    EnableSyncWorkArea : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for work area data
    """

    EnableSyncSWLimits : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for software limits
    """

    EnableSyncDefaultDynamics : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for default dynamics
    """

    EnableSyncReferenceDynamics : bool = True 
    """
    Set TRUE (default), to activate the synchronizationrelated comparison mechanism for reference dynamics
    """
    
    #-------------------------------
    # Override String Method
    #-------------------------------
    def __str__(self) -> str:
        
        value = BYTE(0)
        value.Bit[0] = self.EnableSyncTool
        value.Bit[1] = self.EnableSyncFrame  
        value.Bit[2] = self.EnableSyncLoad
        value.Bit[3] = self.EnableSyncWorkArea
        value.Bit[4] = self.EnableSyncSWLimits
        value.Bit[5] = self.EnableSyncDefaultDynamics
        value.Bit[6] = self.EnableSyncReferenceDynamics

        return f"{int(value):08b}"