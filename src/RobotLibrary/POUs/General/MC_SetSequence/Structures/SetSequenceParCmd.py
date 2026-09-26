"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SetSequenceParCmd
Author:      Thorsten Brach
Date:        2026-01-24

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

from RobotLibrary.Enumerations.Flag.SequenceFlag import SequenceFlag
from RobotLibrary.IEC_Types import IEC_Struct

class SetSequenceParCmd(IEC_Struct):
    TargetSequence  : SequenceFlag
    """Defines sequence to be activated when function is executed"""
