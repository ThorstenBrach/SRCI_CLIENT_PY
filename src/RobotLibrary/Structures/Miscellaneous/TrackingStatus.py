"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      TrackingStatus
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
from RobotLibrary.IEC_Types import BOOL, IEC_Struct


class TrackingStatus(IEC_Struct):

    ConveyorTrackingEnabled: BOOL
    """TRUE, while a "ConveyorTracking" function is enabled"""

    WaitingForSynchronization: BOOL
    """
    TRUE, while robot is waiting for condition defined by "SyncInMode"
    after "SyncToConveyor" has been executed
    """

    Synchronizing: BOOL
    """TRUE, while robot is matching the TCP's velocity to the conveyor's velocity"""

    Synchronous: BOOL
    """TRUE, while TCP is moving synchronously to conveyor"""

    Desynchronizing: BOOL
    """TRUE, while robot is terminating synchronous movement"""

    SyncOutZoneEntered: BOOL
    """TRUE, while assigned UCS is within "SyncOutZone"""

    SyncOutZoneLeft: BOOL
    """
    TRUE, when assigned UCS leaves "SyncOutZone"
    Reset, when robot's synchronous movement has been stopped
    """

    NotUsed: BOOL
    """Not used"""