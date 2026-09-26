"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ReadRobotReferenceDynamicsRecvData
Author:      Thorsten Brach
Date:        2026-01-20

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

from RobotLibrary.IEC_Types import UINT, BOOL
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Structures.DatenAndTime.IEC_TIMESTAMP import IEC_TIMESTAMP



class ReadRobotReferenceDynamicsRecvData(RspHeader):
    """Structure for received data from ReadRobotReferenceDynamics command."""
    
    Timestamp             : IEC_TIMESTAMP
    """Timestamp"""

    VelocityReference     : UINT
    """
    Path velocity [mm/s](tangent) at 100%\n
     • <0: (default) - Do not change values\n
     • ≥0: Change values according to input value\n
    """
    AccelerationReference : UINT
    """
    Path acceleration [mm/s2] at 100%\n
     • <0: (default) - Do not change values\n
     • ≥0: Change values according to input value\n
    """

    DecelerationReference : UINT
    """
    Path deceleration [mm/s2] at 100%\n
     • <0: (default) - Do not change values\n
     • ≥0: Change values according to input value\n
    """
    
    JerkReference        : UINT
    """
    Jerk [mm/s3] at 100%\n
     • <0: (default) - Do not change values\n
     • ≥0: Change values according to input value\n
    """

    DataChanged          : BOOL
    """The status bit "DataChanged" represents the modification state"""


    #------------------------------------------------------------
    # Constructor + Initialization
    #------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.Timestamp       = IEC_TIMESTAMP()
        self.VelocityReference     = UINT(0)
        self.AccelerationReference = UINT(0)
        self.DecelerationReference = UINT(0)
        self.JerkReference         = UINT(0)
        self.DataChanged           = BOOL(False)