"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupStateSyncStatePlc
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

from RobotLibrary.IEC_Types import IEC_Struct 
from RobotLibrary.Structures.AxesGroup.State.SyncState.AxesGroupStateSyncState import AxesGroupStateSyncState
from RobotLibrary.Structures.AxesGroup.State.SyncState.AxesGroupStateSyncStateNo import AxesGroupStateSyncStateNo

class AxesGroupStateSyncStatePlc(IEC_Struct):
    InSync: AxesGroupStateSyncState
    """Synchronization state of the datasets"""

    UnSyncNo: AxesGroupStateSyncStateNo
    """Number of the dataset which has been changed locally"""