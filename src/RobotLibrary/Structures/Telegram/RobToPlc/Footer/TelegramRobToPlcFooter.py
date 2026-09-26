"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramRobToPlcFooter
Author:      Thorsten Brach
Date:        2025-12-21

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
#region imports
from RobotLibrary.IEC_Types import IEC_Struct, BYTE
#endregion

#-------------------------------------------------------------------------
# TelegramRobToPlcFooter
#-------------------------------------------------------------------------
class TelegramRobToPlcFooter(IEC_Struct):
  
    Reserve: BYTE
    """Reserve"""

    LifeSign: BYTE
    """Life sign"""