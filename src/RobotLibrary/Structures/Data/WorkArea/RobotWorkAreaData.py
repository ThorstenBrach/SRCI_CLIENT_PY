"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotWorkAreaData
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

from RobotLibrary.IEC_Types import USINT,REAL,BOOL,IEC_Struct 
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
from.RobotWorkAreaDataLimitCartesian import RobotWorkAreaDataLimitCartesian
from.RobotWorkAreaDataLimitJoint import RobotWorkAreaDataLimitJoint
from RobotLibrary.Enumerations.Type.AreaType import AreaType
from RobotLibrary.Enumerations.Mode.DefinitionMode import DefinitionMode
from RobotLibrary.Enumerations.Mode.WorkAreaReactionMode import WorkAreaReactionMode


class RobotWorkAreaData(IEC_Struct):
    Timestamp: IEC_TIMESTAMP
    """Timestamp"""

    AreaType: AreaType
    """Defines type of work area"""

    AreaMode: BOOL
    """
    Defines violation condition
    • FALSE (default) : Robot must not leave defined area
    • TRUE            : Robot must not enter defined area
    """

    ReactionMode: WorkAreaReactionMode
    """Defines RC's and robot's behavior when robot violates work area"""

    ActiveModification: BOOL
    """
    Specifies whether an active work area can be edited by function WriteWorkArea
     TRUE            : Modification of active work area possible
     FALSE (default) : Modification of active work areas not possible
    """

    DefinitionMode: DefinitionMode
    """Relates to AreaType Box, Cylinder and Sphere"""

    FrameNo: USINT
    """
    Relates to AreaType Box, Cylinder and Sphere.
    Index of reference frame
    • 0: WCS (default)
    • 1..254: User frames
    """

    ZeroPointX: REAL 
    """
    Relates to AreaType Box, Cylinder and Sphere.
    X-value of reference point in specified frame - Default: 0
    """

    ZeroPointY: REAL 
    """
    Relates to AreaType Box, Cylinder and Sphere.
    Y-value of reference point in specified frame - Default: 0
    """

    ZeroPointZ: REAL
    """
    Relates to AreaType Box, Cylinder and Sphere.
    Z-value of reference point in specified frame - Default: 0
    """

    X: RobotWorkAreaDataLimitCartesian
    """Limit for cartesian X"""

    Y: RobotWorkAreaDataLimitCartesian
    """Limit for cartesian Y"""

    Z: RobotWorkAreaDataLimitCartesian
    """Limit for cartesian Z"""

    Radius: REAL
    """
    Relates to AreaType Sphere.
    Radius of cylinder or sphere - Default: 0
    """

    J1Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J1"""

    J2Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J2"""

    J3Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J3"""

    J4Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J4"""

    J5Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J5"""

    J6Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint J6"""

    E1Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E1"""

    E2Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E2"""

    E3Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E3"""

    E4Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E4"""

    E5Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E5"""

    E6Limit: RobotWorkAreaDataLimitJoint
    """Limits for Joint E6"""