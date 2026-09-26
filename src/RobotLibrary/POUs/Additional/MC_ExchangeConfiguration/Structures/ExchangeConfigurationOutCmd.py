"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ExchangeConfigurationOutCmd
Author:      Thorsten Brach
Date:        2025-12-23

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
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync as DataInSyncStruct
    
class ExchangeConfigurationOutCmd(IEC_Struct):
  
    LengthACR: int
    """Returns a metric of how many CMDs it can receive and manage at the same time"""

    HighestToolIndex: int
    """Highest index of available tools on the RC"""

    HighestFrameIndex: int
    """Highest index of available frames on the RC"""

    HighestLoadIndex: int
    """Highest index of available loads on the RC"""

    HighestWorkAreaIndex: int
    """Highest index of available work areas on the RC"""

    DataInSync: DataInSyncStruct
    """Datas which are synchronized"""

    ChangeIndexTool: int
    """Index of tool changed on RC"""

    ChangeIndexFrame: int
    """Index of frame changed on RC"""

    ChangeIndexLoad: int
    """Index of load changed on RC"""

    ChangeIndexWorkArea: int
    """Index of work area changed on RC"""

    RAWorkingHours: int
    """Working hours of an RA connected to the RC"""

    BrakeTestRequired: bool
    """Signals that a brake test is required in the defined monitoring time"""

    StepModeExactStopActive: bool
    """StepMode is active and set to ExactStop"""

    StepModeBlendingActive: bool
    """StepMode is active and set to Blending"""

    PathAccuracyMode: bool
    """PathAccuracyMode is active"""

    AvoidSingularity: bool
    """AvoidSingularity is active"""

    CollisionDetectionEnabled: bool
    """CollisionDetection is active"""

    AcceleratingSupported: bool
    """Cyclic dynamics status bit Accelerating is supported by RC"""

    DecceleratingSupported: bool
    """Cyclic dynamics status bit Decelerating is supported by RC"""

    ConstantVelocitySupported: bool
    """Cyclic dynamics status bit ConstantVelocity is supported by RC"""

    RCWorkingHours: int
    """
    Total system hours of an RA connected to the RC.
    0: Invalid
    >1: Total system hours
    """
    
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)
        
        # Initialize numeric fields
        self.LengthACR = 0
        self.HighestToolIndex = 0
        self.HighestFrameIndex = 0
        self.HighestLoadIndex = 0
        self.HighestWorkAreaIndex = 0
        
        # Initialize nested structs and flags
        self.DataInSync = DataInSyncStruct()
        self.ChangeIndexTool = 0
        self.ChangeIndexFrame = 0
        self.ChangeIndexLoad = 0
        self.ChangeIndexWorkArea = 0
        self.RAWorkingHours = 0
        self.BrakeTestRequired = False
        self.StepModeExactStopActive = False
        self.StepModeBlendingActive = False
        self.PathAccuracyMode = False
        self.AvoidSingularity = False
        self.CollisionDetectionEnabled = False
        self.AcceleratingSupported = False
        self.DecceleratingSupported = False
        self.ConstantVelocitySupported = False
        self.RCWorkingHours = 0
    