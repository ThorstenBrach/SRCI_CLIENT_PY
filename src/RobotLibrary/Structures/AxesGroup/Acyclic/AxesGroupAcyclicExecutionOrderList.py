"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupAcyclicExecutionOrderList
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

from RobotLibrary.IEC_Types import UINT, IEC_Struct, ARRAY 
from RobotLibrary.Parameter import ACTIVE_CMD_REGISTER_ENTRIES_MAX


class AxesGroupAcyclicExecutionOrderList(IEC_Struct):

    Command  : ARRAY[UINT] = ARRAY(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX, UINT) 
    """Command"""

    Response : ARRAY[UINT] = ARRAY(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX, UINT) 
    """ Response"""