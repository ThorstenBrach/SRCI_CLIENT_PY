"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TelegramPlcToRobFooter
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
#region Imports
from RobotLibrary.IEC_Types import BYTE, IEC_Struct
#endregion

#------------------------------------------------------------
# TelegramPlcToRobFooter - Footer
#------------------------------------------------------------
class TelegramPlcToRobFooter(IEC_Struct):
  
    LifeSign : BYTE
    """ Life Sign"""
    
    Reserve  : BYTE
    """ Reserve"""