"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RRobotJointPosition
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


class RobotJointPosition(IEC_Struct):
    J1: float
    """Position [°] of first joint of the robot"""

    J2: float
    """Position [°] of second joint of the robot"""

    J3: float
    """Position [°] of third joint of the robot"""

    J4: float
    """Position [°] of fourth joint of the robot"""

    J5: float
    """Position [°] of fifth joint of the robot"""

    J6: float
    """Position [°] of sixth joint of the robot"""

    E1: float
    """Position [°] of first external axis"""

    E2: float
    """Position [°] of second external axis"""

    E3: float
    """Position [°] of third external axis"""

    E4: float
    """Position [°] of fourth external axis"""

    E5: float
    """Position [°] of fifth external axis"""

    E6: float
    """Position [°] of sixth external axis"""
    
class RobotJointPositionExt(IEC_Struct):
    E2: float
    """Position of second external axis"""

    E3: float
    """Position of third external axis"""

    E4: float
    """Position of fourth external axis"""

    E5: float
    """Position of fifth external axis"""

    E6: float
    """Position of sixth external axis"""
    
class RobotJointPositionShort(IEC_Struct):
    J1: float
    """Position of first joint of the robot"""

    J2: float
    """Position of second joint of the robot"""

    J3: float
    """Position of third joint of the robot"""

    J4: float
    """Position of fourth joint of the robot"""

    J5: float
    """Position of fifth joint of the robot"""

    J6: float
    """Position of sixth joint of the robot"""

    E1: float
    """Position of first external axis"""
    
class RobotJointCurrent(IEC_Struct):
    J1: float
    """Current of first joint of the robot"""

    J2: float
    """Current of second joint of the robot"""

    J3: float
    """Current of third joint of the robot"""

    J4: float
    """Current of fourth joint of the robot"""

    J5: float
    """Current of fifth joint of the robot"""

    J6: float
    """Current of sixth joint of the robot"""

    E1: float
    """Current of first external joint of the robot"""

    E2: float
    """Current of second external axis"""

    E3: float
    """Current of third external axis"""

    E4: float
    """Current of fourth external axis"""

    E5: float
    """Current of fifth external axis"""

    E6: float
    """Current of sixth external axis"""    
    
class RobotJointCurrentExt(IEC_Struct):
    E1: float
    """Current of first external joint of the robot"""

    E2: float
    """Current of second external axis"""

    E3: float
    """Current of third external axis"""

    E4: float
    """Current of fourth external axis"""

    E5: float
    """Current of fifth external axis"""

    E6: float
    """Current of sixth external axis"""
    
class RobotJointCurrentShort(IEC_Struct):
    J1: float
    """Current of first joint of the robot"""

    J2: float
    """Current of second joint of the robot"""

    J3: float
    """Current of third joint of the robot"""

    J4: float
    """Current of fourth joint of the robot"""

    J5: float
    """Current of fifth joint of the robot"""

    J6: float
    """Current of sixth joint of the robot"""        