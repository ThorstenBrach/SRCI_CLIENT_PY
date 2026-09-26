"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TriggerReactionMode
Author:      Thorsten Brach
Date:        2025-12-14

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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class TriggerReactionMode(SINTEnum):
    NO_REACTION = 0
    """
    No reaction (default)
    """

    INTERRUPT = 1
    """
    Interrupt\n
    Robot movement is paused.\n
    Movement can be continued by function GroupContinue
    """

    GROUP_STOP = 2
    """
    GroupStop\n
    Robot stops the movement and brings all axes to a halt.\n
    Movements aborted by this command cannot be continued
    """

    DISABLE_ROBOT = 3
    """
    Disable robot\n
    The robot's drives are disabled.\n
    This leads to the robot state \"Not enabled\" (see chapter 5.5.3)
    """

    STOP_ACTUAL_MOTION_COMMAND = 4
    """
    Stop actual motion command\n
    Robot movement is paused.\n
    Movement can be continued by the next motion command
    """
    
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    