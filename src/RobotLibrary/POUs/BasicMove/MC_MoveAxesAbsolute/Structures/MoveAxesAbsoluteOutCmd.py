"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MoveAxesAbsoluteOutCmd
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

from typing import Any
from RobotLibrary.IEC_Types import IEC_Struct


class MoveAxesAbsoluteOutCmd(IEC_Struct):

    Progress : float
    """
    Percentage of already traversed distance of current job.
    If not supported : • -1
    """

    FollowID : int
    """
    Unique system-generated ID of the trigger function when the function is called by the user.
    For more information see chapter 5.5.12.4.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        
        self.Progress = float(0)
        self.FollowID = int(0)
        