"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupCyclicOptionalData
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
#region Imports
from RobotLibrary.IEC_Types import IEC_Struct, BOOL
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPositionShort
from RobotLibrary.Structures.Common.RobotCoordinateSystemParameters import RobotCoordinateSystemParameters
from RobotLibrary.Structures.Cartesian.RobotCartesianPosition import RobotCartesianPositionExt
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointCurrentShort
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointCurrentExt
from RobotLibrary.Structures.Cartesian.RobotCartesianForce import RobotCartesianForceShort
from RobotLibrary.Structures.Cartesian.RobotCartesianForce import RobotCartesianForceExt
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPositionShort
from RobotLibrary.Structures.Joint.RobotJointPosition import RobotJointPositionExt
from RobotLibrary.Structures.Data.SubProgram.RobotSubProgramData import RobotSubProgramData
#endregion


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataCartesianPosition
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataCartesianPosition(RobotCartesianPositionShort):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""    
    
    CoordinateSystem : RobotCoordinateSystemParameters
    """ corresponding coordinate systems"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataCartesianPositionExt
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataCartesianPositionExt(RobotCartesianPositionExt):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataCurrent
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataCurrent(RobotJointCurrentShort):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataCurrentExt
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataCurrentExt(RobotJointCurrentExt):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataForce
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataForce(RobotCartesianForceShort):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataForceExt
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataForceExt(RobotCartesianForceExt):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataJointPosition
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataJointPosition(RobotJointPositionShort):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataJointPositionExt
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataJointPositionExt(RobotJointPositionExt):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""

#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataSubProgram
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataSubProgram(RobotSubProgramData):
  
    Active : BOOL
    """ indicates that this optional parameter will be used"""

#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataPlcToRob
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataPlcToRob(IEC_Struct):
  
    SubProgramData: AxesGroupCyclicOptionalDataSubProgram
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC
    called via the function “CallSubprogram”
    """

    CartesianPosition: AxesGroupCyclicOptionalDataCartesianPosition
    """
    Short cartesian position with TCP position (X, Y, Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1)
    and corresponding coordinate systems (ToolNo, FrameNo)
    """

    CartesianPositionExt: AxesGroupCyclicOptionalDataCartesianPositionExt
    """
    The external axis values for an extended cartesian position (E2, E3, E4, E5, E6).
    When selected, Tool and Frame will automatically cyclically be sent
    from client to server.
    """

    JointPosition: AxesGroupCyclicOptionalDataJointPosition
    """
    Short axes position with joint values (J1, J2, J3, J4, J5, J6)
    and position of first external axis (E1)
    """

    JointPositionExt: AxesGroupCyclicOptionalDataJointPositionExt
    """
    The external axis values for an extended joint position (E2, E3, E4, E5, E6)
    """

    Force: AxesGroupCyclicOptionalDataForce
    """
    Force with the divided forces in the individual directions
    (X, Y, Z, RX, RY, RZ)
    """

    ForceExt: AxesGroupCyclicOptionalDataForceExt
    """
    Current force for the external axes (E1, E2, E3, E4, E5, E6)
    """


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalDataRobToPlc
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalDataRobToPlc(IEC_Struct):
  
    SubProgramData : AxesGroupCyclicOptionalDataSubProgram
    """
    Transmit cyclic data from PLC to RC for the usage in a subprogram on the RC
    called via the function “CallSubprogram”
    """

    CartesianPosition: AxesGroupCyclicOptionalDataCartesianPosition
    """
    Short cartesian position with TCP position (X, Y, Z), rotation (RX, RY, RZ),
    configuration bytes (Config, TurnNumber), position of first external axis (E1)
    and corresponding coordinate systems (ToolNo, FrameNo)
    """

    CartesianPositionExt: AxesGroupCyclicOptionalDataCartesianPositionExt
    """
    The external axis values for an extended cartesian position (E2, E3, E4, E5, E6).
    When selected, Tool and Frame will automatically cyclically be sent
    from client to server.
    """

    JointPosition: AxesGroupCyclicOptionalDataJointPosition
    """
    Short axes position with joint values (J1, J2, J3, J4, J5, J6)
    and position of first external axis (E1)
    """

    JointPositionExt: AxesGroupCyclicOptionalDataJointPositionExt
    """
    The external axis values for an extended joint position (E2, E3, E4, E5, E6)
    """

    Force: AxesGroupCyclicOptionalDataForce
    """
    Force with the divided forces in the individual directions
    (X, Y, Z, RX, RY, RZ)
    """

    ForceExt: AxesGroupCyclicOptionalDataForceExt
    """
    Current force for the external axes (E1, E2, E3, E4, E5, E6)
    """

    Current: AxesGroupCyclicOptionalDataCurrent
    """
    Actual axes current of individual axes (J1, J2, J3, J4, J5, J6)
    """

    CurrentExt: AxesGroupCyclicOptionalDataCurrentExt
    """
    Actual current for the external axes (E1, E2, E3, E4, E5, E6)
    """    


#-------------------------------------------------------------------------
# AxesGroupCyclicOptionalData
#-------------------------------------------------------------------------
class AxesGroupCyclicOptionalData(IEC_Struct):
  
  PlcToRob : AxesGroupCyclicOptionalDataPlcToRob
  """ Optional cyclic data from PLC to Robot"""
  
  
  RobToPlc : AxesGroupCyclicOptionalDataRobToPlc
  """ Optional cyclic data from Robot to PLC"""