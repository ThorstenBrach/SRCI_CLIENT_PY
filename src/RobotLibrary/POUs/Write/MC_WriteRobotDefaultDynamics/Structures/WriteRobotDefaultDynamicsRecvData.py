"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotDefaultDynamicsRecvData
Author:      Thorsten Brach
Date:        2026-01-22

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

from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.IEC_Types import UINT

class WriteRobotDefaultDynamicsRecvData(RspHeader):
    """Structure for received data from WriteRobotDefaultDynamics command."""
    
    VelocityRate     : UINT
    """
    Maximum velocity for the axes.\n
    Range [%]:\n
     •  <0% : Use default velocity given by the user\n
     •   0% : Use internal minimal velocity\n
     • 100% : Use the entire reference velocity, given by the user\n
    """
    
    AccelerationRate : UINT
    """
    Maximum acceleration.\n
    Range [%]:\n
     •  <0% : Use default acceleration given by the user\n
     •   0% : Use internal minimal acceleration\n
     • 100% : Use the entire reference acceleration, given by the user\n
    """
    
    
    DecelerationRate : UINT
    """
    Maximum deceleration.\n
    Range [%] :\n
     •  <0% : Use default deceleration given by the user\n
     •   0% : Use internal minimal deceleration\n
     • 100% : Use the entire reference deceleration, given by the user\n
    """

    JerkRate         : UINT
    """
    Maximum jerk\n
    Range [%] :\n
     •  <0% : Use default jerk given by the user\n
     •   0% : Use internal minimal jerk\n
     • 100% : Use the entire reference jerk, given by the user (Trapezoidal if possible) \n
    """


    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.VelocityRate     = UINT(0)
        self.AccelerationRate = UINT(0)
        self.DecelerationRate = UINT(0)
        self.JerkRate         = UINT(0)