"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroup
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
from RobotLibrary.Structures.AxesGroup.Parameter.AxesGroupParameter import AxesGroupParameter
from RobotLibrary.Structures.AxesGroup.State.AxesGroupState import AxesGroupState 
from RobotLibrary.Structures.AxesGroup.Cyclic.AxesGroupCyclic import AxesGroupCyclic
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclic import AxesGroupAcyclic
from RobotLibrary.Structures.AxesGroup.CyclicOptional.AxesGroupCyclicOptionalData import AxesGroupCyclicOptionalData
from RobotLibrary.POUs._internal.LogFBs.AxesGroupMessageLogFB import AxesGroupMessageLogFB
from RobotLibrary.POUs._internal.AxesGroupSystemDataFB import AxesGroupSystemDataFB

class AxesGroup(IEC_Struct):
    """
    Represents an axes group structure containing all relevant data for robot control.
    
    This class provides a comprehensive interface to robot axes group management,
    including parameter configuration, state monitoring, message logging, and 
    cyclic/acyclic data exchange between server and client.
    
    Attributes:
        Parameter (AxesGroupParameter): Configuration parameters for the axes group.
        State (AxesGroupState): Current state information of the robot interface (RI).
            See chapter 5.5.3 of the documentation.
        MessageLog (AxesGroupMessageLogFB): Logger for warnings and errors from RC 
            (Robot Control), RA (Robot Application), RI (Robot Interface), and CMD 
            (Command) modules. See chapter 5.5.11 of the documentation.
        Cyclic (AxesGroupCyclic): Cyclic data exchanged between server and client.
            See chapter 5.6.6.5 of the documentation.
        CyclicOptional (AxesGroupCyclicOptionalData): Optional cyclic data exchanged 
            between server and client. See chapter 5.6.6.2 of the documentation.
        Acyclic (AxesGroupAcyclic): Execution order list and ACR (Axis Control Record) 
            entries. See chapter 5.6.4.2 of the documentation.
        SystemData (AxesGroupSystemDataFB): System data including ToolData, FrameData, 
            LoadData, and other system-specific information.
    """
    
    Parameter: AxesGroupParameter
    """Parameter"""

    State: AxesGroupState
    """RI state information (see chapter 5.5.3)"""

    MessageLog: AxesGroupMessageLogFB
    """RC, RA, RI, and CMD warnings and errors (see chapter 5.5.11)"""

    Cyclic: AxesGroupCyclic
    """Cyclic data exchanged between server and client (see chapter 5.6.6.5)"""

    CyclicOptional: AxesGroupCyclicOptionalData
    """Optional cyclic data exchanged between server and client (see chapter 5.6.6.2)"""

    Acyclic: AxesGroupAcyclic
    """Execution order list and ACR entries (see chapter 5.6.4.2)"""

    SystemData: AxesGroupSystemDataFB
    """System data like ToolData, FrameData, LoadData etc."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure non-IEC_Struct fields are constructed
        if not isinstance(getattr(self, 'MessageLog', None), AxesGroupMessageLogFB):
            self.MessageLog = AxesGroupMessageLogFB()
        if getattr(self, 'SystemData', None) is None:
            self.SystemData = AxesGroupSystemDataFB()