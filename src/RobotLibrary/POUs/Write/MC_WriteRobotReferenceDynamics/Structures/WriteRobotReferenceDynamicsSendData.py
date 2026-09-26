"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotReferenceDynamicsSendData
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

from RobotLibrary.IEC_Types import REAL
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader



class WriteRobotReferenceDynamicsSendData(CmdHeader):
    """Structure for received data from WriteRobotReferenceDynamics command."""
    
    Timestamp        : IEC_TIMESTAMP
    """Timestamp of the reference dynamics."""
    
    VelocityReference     : REAL
    """
    Path velocity [mm/s](tangent) at 100%
     • <0: (default) - Do not change values
     • ≥0: Change values according to input value
    """
    
    AccelerationReference : REAL
    """    
    Path acceleration [mm/s2] at 100%
     • <0: (default) - Do not change values
     • ≥0: Change values according to input value
    """
    
    DecelerationReference : REAL
    """
    Path deceleration [mm/s2] at 100%
     • <0: (default) - Do not change values
     • ≥0: Change values according to input value
    """

    JerkReference         : REAL  
    """
    Jerk [mm/s3] at 100%
     • <0: (default) - Do not change values
     • ≥0: Change values according to input value
    """
    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.TimeStamp        = IEC_TIMESTAMP()
        self.VelocityReference     = REAL(0)
        self.AccelerationReference = REAL(0)
        self.DecelerationReference = REAL(0)
        self.JerkReference         = REAL(0)