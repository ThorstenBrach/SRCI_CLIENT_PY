"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      GroupJogOutCmd
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

from RobotLibrary.IEC_Types import IEC_Struct

class GroupJogOutCmd(IEC_Struct):
  
    DistanceReached : bool
    """Relates to Incremental mode ON: TRUE, when robot's TCP or axes have traversed distance of "IncrementalTranslation" or "IncrementalRotation" """

    MotionActive    : bool
    """The command takes control of the motion of the according axis group"""
