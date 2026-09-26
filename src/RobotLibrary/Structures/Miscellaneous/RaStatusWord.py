"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RaStatusWord
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
from RobotLibrary.IEC_Types import BOOL,IEC_Struct
from RobotLibrary.Enumerations.Mode.OperationMode import OperationMode
from RobotLibrary.Enumerations.State.RaSequenceState  import RaSequenceState

class RaStatusWord(IEC_Struct):
    IsMoving: BOOL
    """
    Bit 00:
    TRUE, when robot's axes values change due to physical movement of axes
    """

    PrimarySequencePaused: BOOL
    """
    Bit 01:
    TRUE, when move commands buffered by the primary sequence are currently not processed
    """

    InPrimaryPos: BOOL
    """
    Bit 02:
    TRUE, when robot is moving in the primary sequence, FALSE when robot leaves its position by other means
    Switches back to TRUE in the following two scenarios:
    1. During a change to the primary sequence the current TCP position is equal to
       - position when the primary sequence was left
       - target position of an interrupted move command of the primary sequence
         (see "ReturnToPrimary": "ReturnMode" "End position" chapter 6.3.11)
    2. The primary sequence is active, and the buffer is empty while a new command is buffered
       by the primary sequence
    Independent of RA state
    """

    SecondarySequenceActive: BOOL
    """
    Bit 03:
    Secondary sequence is active, either by user selection or by implicit behavior
    """

    IsBlending: BOOL
    """
    Bit 04:
    TRUE, when robot is currently blending between two move commands
    """

    ErrorPending: BOOL
    """
    Bit 05:
    Shows that an error acknowledgement by the client is necessary
    """

    RestartInProgress: BOOL
    """
    Bit 06:
    RC is restarting
    """

    Enabled: BOOL
    """
    Bit 07:
    RA power state
    """

    RaSequenceState: RaSequenceState
    """
    Bit 08 - Bit 09:
    RA sequence states: Idle, Interrupt active, Axes controlled
    """

    OperationMode: OperationMode
    """
    Bit 10 - Bit 12:
    Operation Mode: T1 Local, T2 Local, Auto, Auto Ext, T1 Ext, T2 Ext
    """

    CollisionDetectedEnabled: BOOL
    """
    Bit 13:
    TRUE, while CollisionDetection is enabled (see chapter 6.5.35)
    """

    CollisionDetected: BOOL
    """
    Bit 14:
    TRUE, when a collision was detected while CollisionDetection is enabled
    """

    RestartRequested: BOOL
    """
    Bit 15:
    TRUE, when the RC request a restart of the RC induced through the functions
    "WriteRobotSWLimits" or "WriteSystemVariable"
    """

    Accelerating: BOOL
    """
    Bit 16:
    RA is currently accelerating.
    Support of this value is returned via exchangeConfig.
    """

    Decelerating: BOOL
    """
    Bit 17:
    RA is currently decelerating.
    Support of this value is returned via exchangeConfig.
    """

    ConstantVelocity: BOOL
    """
    Bit 18:
    RA is currently not accelerating nor decelerating.
    Support of this value is returned via exchangeConfig.
    """

    Bit19: BOOL
    """Bit 19"""

    Bit20: BOOL
    """Bit 20"""

    Bit21: BOOL
    """Bit 21"""

    Bit22: BOOL
    """Bit 22"""

    Bit23: BOOL
    """Bit 23"""

    Bit24: BOOL
    """Bit 24"""

    Bit25: BOOL
    """Bit 25"""

    Bit26: BOOL
    """Bit 26"""

    Bit27: BOOL
    """Bit 27"""

    Bit28: BOOL
    """Bit 28"""

    Bit29: BOOL
    """Bit 29"""

    Bit30: BOOL
    """Bit 30"""

    Bit31: BOOL
    """Bit 31"""