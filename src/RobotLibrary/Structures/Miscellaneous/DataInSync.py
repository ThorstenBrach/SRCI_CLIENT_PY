"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      DataInSync
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

from RobotLibrary.IEC_Types import IEC_Struct, BYTE

class DataInSync(IEC_Struct):
    ToolsInSync: bool
    """TRUE, if no tool has been modified"""

    FramesInSync: bool
    """TRUE, if no frame has been modified"""

    LoadsInSync: bool
    """TRUE, if no load has been modified"""

    WorkAreasInSync: bool
    """TRUE, if no work area has been modified"""

    SoftwareLimitsInSync: bool
    """TRUE, if no software limit has been modified"""

    DefaultDynamicsInSync: bool
    """TRUE, if no default dynamic parameter has been modified"""

    ReferenceDynamicsInSync: bool
    """TRUE, if no reference dynamic parameter has been modified"""
    
    #-------------------------------
    # Constructor
    #-------------------------------
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        
        self.ToolsInSync = False
        self.FramesInSync = False
        self.LoadsInSync = False
        self.WorkAreasInSync = False
        self.SoftwareLimitsInSync = False
        self.DefaultDynamicsInSync = False
        self.ReferenceDynamicsInSync = False
    
    
    #-------------------------------
    # Override String Method
    #-------------------------------
    def __str__(self) -> str:
        
        value = BYTE(0)
        value.Bit[0] = self.ToolsInSync
        value.Bit[1] = self.FramesInSync  
        value.Bit[2] = self.LoadsInSync
        value.Bit[3] = self.WorkAreasInSync
        value.Bit[4] = self.SoftwareLimitsInSync
        value.Bit[5] = self.DefaultDynamicsInSync
        value.Bit[6] = self.ReferenceDynamicsInSync

        return f"{int(value):08b}"    