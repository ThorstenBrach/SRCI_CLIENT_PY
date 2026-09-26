"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      IEC_TIMESTAMP
Author:      Thorsten Brach
Date:        2025-12-18

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
from RobotLibrary.Structures.DatenAndTime.IEC_DATE import IEC_DATE
from RobotLibrary.Structures.DatenAndTime.IEC_TIME import IEC_TIME  


class IEC_TIMESTAMP(IEC_Struct):
    """
    IEC_TIMESTAMP structure representing date and time.
    """

    IEC_DATE: IEC_DATE
    """
    Date part of the timestamp.
    """

    IEC_TIME: IEC_TIME
    """
    Time part of the timestamp.
    """
    
    #-------------------------------------------------------------------------
    # GetBytes - returns the byte representation of the structure
    #-------------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytearray:

        bytes = bytearray()
        
        # command data
        bytes.extend(self.IEC_DATE.GetBytes(order))
        bytes.extend(self.IEC_TIME.GetBytes(order))
        return bytes    