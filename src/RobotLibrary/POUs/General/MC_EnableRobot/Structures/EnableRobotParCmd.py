"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      EnableRobotParCmd
Author:      Thorsten Brach
Date:        2025-12-22

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
from RobotLibrary.Enumerations.Mode.StepMode import StepMode

class EnableRobotParCmd(IEC_Struct):
  
    HoldToRun: bool
    """The robot will move while HoldToRun is set TRUE"""

    StepMode: StepMode
    """
    While activated the RI state switches to interrupted when a buffered command
    returns Done TRUE.
    At least one of the optional modes must be supported
    """

    ManualStep: bool
    """
    Relates to StepMode 1 (Blending) and 2 (Exact stop).
    Start the next buffered command with the rising edge
    in T1 External or T2 External
    """