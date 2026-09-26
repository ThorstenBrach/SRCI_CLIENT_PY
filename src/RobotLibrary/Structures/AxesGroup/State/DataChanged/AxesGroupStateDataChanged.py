"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupStateDataChanged
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

from RobotLibrary.IEC_Types import ARRAY,IEC_Struct 
from RobotLibrary.Parameter import TOOL_MAX,FRAME_MAX,LOAD_MAX,WORK_AREAS_MAX

class AxesGroupStateDataChanged(IEC_Struct):
    
    Tool              : ARRAY[bool] = ARRAY(0, TOOL_MAX-1, bool)
    """indicates that tool data has changed"""
    
    Frame             : ARRAY[bool] = ARRAY(0, FRAME_MAX-1, bool)
    """ indicates that frame data has changed"""

    Load              : ARRAY[bool] = ARRAY(0, LOAD_MAX-1, bool)
    """indicates that load data has changed"""

    WorkArea          : ARRAY[bool] = ARRAY(0, WORK_AREAS_MAX-1, bool)
    """ indicates that work area has changed"""

    DefaultDynamics   : bool
    """indicates that default dynamic has changed"""

    ReferenceDynamics : bool
    """ indicates that reference dynamic has changed"""

    SwLimits          : bool
    """indicates that software limits has changed"""