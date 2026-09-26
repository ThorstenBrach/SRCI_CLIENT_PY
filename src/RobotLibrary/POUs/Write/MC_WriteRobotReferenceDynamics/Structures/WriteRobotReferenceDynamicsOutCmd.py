"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WriteRobotReferenceDynamicsOutCmd
Author:      Thorsten Brach
Date:        2026-01-12

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
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import ReferenceDynamics

class WriteRobotReferenceDynamicsOutCmd(IEC_Struct):
    
    ReferenceDynamicValues   : ReferenceDynamics
    """Commanded dynamics values according to Table 6-141."""
