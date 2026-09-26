"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupSystemDataFB
Author:      Thorsten Brach
Date:        2026-01-10

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.Data.Tool.Tool import Tool
from RobotLibrary.Structures.Data.Tool.ToolData import ToolData
from RobotLibrary.Structures.Data.Load.Load import Load
from RobotLibrary.Structures.Data.Load.LoadData import LoadData
from RobotLibrary.Structures.Data.Frame.Frame import Frame
from RobotLibrary.Structures.Data.Frame.FrameData import FrameData

from RobotLibrary.Structures.Data.WorkArea.RobotWorkArea import RobotWorkArea
from RobotLibrary.Structures.Data.WorkArea.RobotWorkAreaData import RobotWorkAreaData
from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits
from RobotLibrary.Structures.Dynamics.DefaultDynamics import DefaultDynamics as DefaultDynamicsStruct
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import ReferenceDynamics as ReferenceDynamicsStruct


class AxesGroupSystemDataFB(IEC_Struct):
    
    ToolDataPtr       : list[Tool]
    """Reference to ToolData array"""

    ToolDataMin       : int
    """Lower dimension of ToolData array"""

    ToolDataMax       : int
    """Lower dimension of ToolData array"""

    """Amount of ToolData elements in array"""
    ToolDataCount     : int

    LoadDataPtr       : list[Load]
    """Reference to LoadData array"""

    LoadDataMin       : int
    """Lower dimension of LoadData array"""

    LoadDataMax       : int
    """Lower dimension of LoadData array"""

    LoadDataCount     : int
    """Amount of Load elements in array"""

    FrameDataPtr      : list[Frame]
    """Reference to FrameData array"""

    FrameDataMin      : int
    """Lower dimension of FrameData array"""

    FrameDataMax      : int
    """Lower dimension of FrameData array"""

    FrameDataCount    : int
    """Amount of FrameData elements in array"""
    
    """Reference to WorkAreas array"""
    WorkAreasPtr      : list[RobotWorkArea]

    WorkAreasMin      : int
    """Lower dimension of WorkAreas array"""

    WorkAreasMax      : int
    """Lower dimension of WorkAreas array"""

    WorkAreasCount    : int
    """Amount of WorkAreas elements in array"""
    
    SwLimits          : SWLimits
    """Software limits stored on PLC"""

    DefaultDynamics   : DefaultDynamicsStruct
    """Default dynamics stored on PLC. For more information refer to 5.5.7"""

    ReferenceDynamics : ReferenceDynamicsStruct
    """Reference dynamics stored on PLC. For more information refer to 5.5.7"""
    
    
    #------------------------------------------------------------
    # Constructor + Initialization
    #------------------------------------------------------------
    def __init__(self) -> None:
        # Initialize array bounds and counts to safe defaults
        self.ToolDataPtr: list[Tool] 
        self.ToolDataMin: int = 0
        self.ToolDataMax: int = 0
        self.ToolDataCount: int = 0

        self.LoadDataPtr: list[Load] 
        self.LoadDataMin: int = 0
        self.LoadDataMax: int = 0
        self.LoadDataCount: int = 0

        self.FrameDataPtr: list[Frame] 
        self.FrameDataMin: int = 0
        self.FrameDataMax: int = 0
        self.FrameDataCount: int = 0

        self.WorkAreasPtr: list[RobotWorkArea]
        self.WorkAreasMin: int = 0
        self.WorkAreasMax: int = 0
        self.WorkAreasCount: int = 0

        # Initialize structures (can be overwritten later)
        self.SWLimits : SWLimits = SWLimits()
        self.DefaultDynamics : DefaultDynamicsStruct = DefaultDynamicsStruct()
        self.ReferenceDynamics : ReferenceDynamicsStruct = ReferenceDynamicsStruct()


    #--------------------------------------------------------
    # Update Frame Data
    #--------------------------------------------------------
    def UpdateFrameData(self,
                        Caller     : RobotLibraryBaseExecuteFB,
                        SystemTime : SystemTime,
                        FrameNo    : int,
                        FrameData  : FrameData)  -> None:

        pass # ToDo: implement frame data update logic

    
    #--------------------------------------------------------
    # Update Load Data
    #--------------------------------------------------------
    def UpdateLoadData(self,
                       Caller     : RobotLibraryBaseExecuteFB,
                       SystemTime : SystemTime,
                       LoadNo    : int,
                       LoadData  : LoadData)  -> None:

        pass # ToDo: implement load data update logic
    
    
    #--------------------------------------------------------
    # Update Default Dynamics
    #--------------------------------------------------------
    def UpdateDefaultDynamics(self, DynamicValues : DefaultDynamicsStruct) -> None:
        
        pass # ToDo: implement load data update logic
    
    
    #--------------------------------------------------------
    # Update Reference Dynamics
    #--------------------------------------------------------
    def UpdateReferenceDynamics(self, DynamicValues : ReferenceDynamicsStruct) -> None:
        
        pass # ToDo: implement load data update logic    
    
    #--------------------------------------------------------
    # Update SW Limits
    #--------------------------------------------------------
    def UpdateSWLimits(self, LimitValues : SWLimits):
        pass # ToDo: implement SW limits update logic
    
    #--------------------------------------------------------
    # Update Tool Data
    #--------------------------------------------------------
    def UpdateToolData(self,
                       Caller     : RobotLibraryBaseExecuteFB,
                       SystemTime : SystemTime,
                       ToolNo    : int,
                       ToolData  : ToolData)  -> None:

        pass # ToDo: implement load data update logic


    #--------------------------------------------------------
    # Update Work Area Data
    #--------------------------------------------------------
    def UpdateWorkAreas(self,
                       Caller       : RobotLibraryBaseExecuteFB,
                       SystemTime   : SystemTime,
                       WorkAreaNo   : int,
                       WorkAreaData : RobotWorkAreaData)  -> None:

            pass # ToDo: implement work area data update logic