"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupState
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

from RobotLibrary.IEC_Types import IEC_Struct, BOOL, UINT, UDINT, USINT, DINT, ARRAY
from RobotLibrary.IEC_Standard import R_TRIG, F_TRIG
from RobotLibrary.POUs.Additional.ExchangeConfiguration.Structures.ExchangeConfigurationOutCmd import ExchangeConfigurationOutCmd
from RobotLibrary.POUs.Read.MC_ReadRobotData.Structures.ReadRobotDataOutCmd import ReadRobotDataOutCmd
from RobotLibrary.Structures.Miscellaneous.RaStatusWord import RaStatusWord
from RobotLibrary.Structures.Miscellaneous.DataEnableSync import DataEnableSync as DataEnableSyncStruct
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.AxesGroup.State.Synchronizing.AxesGroupStateSynchronizing import AxesGroupStateSynchronizing
from RobotLibrary.Structures.AxesGroup.State.DataChanged.AxesGroupStateDataChanged import AxesGroupStateDataChanged
from RobotLibrary.Structures.AxesGroup.State.SyncState.AxesGroupStateSyncStatePlc import AxesGroupStateSyncStatePlc
from RobotLibrary.Structures.AxesGroup.State.SyncState.AxesGroupStateSyncStateRob import AxesGroupStateSyncStateRob

class AxesGroupState(IEC_Struct):
    
    FatalErrorClient: bool
    """Client reports a fatal error"""

    InvalidFrames: int
    """Invalid frames counter"""

    Synchronized: bool
    """PLC and RC are synchronized"""

    Synchronizing: AxesGroupStateSynchronizing
    """Synchronizing is running"""

    AliveOk: bool
    """Data exchange is running (Life bit toggles)"""

    CMDsEnabled: bool
    """Bit that indicates that it is possible to execute commands"""

    ConfigExchanged: bool
    """Configuration is exchanged"""

    UnifiedToolIndex: int
    """Highest available tool index of RC and PLC in combination"""

    UnifiedFrameIndex: int
    """Highest available frame index of RC and PLC in combination"""

    UnifiedLoadIndex: int
    """Highest available load index of RC and PLC in combination"""

    UnifiedWorkAreaIndex: int
    """Highest available work area index of RC and PLC in combination"""

    DataEnableSync: DataEnableSyncStruct
    """Enable data sets to synchronize"""

    DataChanged: AxesGroupStateDataChanged
    """Flags that indicate which element has changed"""

    SyncStatePlc: AxesGroupStateSyncStatePlc
    """Synchronization state of the PLC"""

    SyncStateRc: AxesGroupStateSyncStateRob
    """Synchronization state of the RC"""

    SystemTime: SystemTime
    """Current system time"""

    RobotData: ReadRobotDataOutCmd
    """Read robot data"""

    StatusRobotArm: RaStatusWord
    """Status of robot arm"""

    ConfigurationData: ExchangeConfigurationOutCmd
    """Read configuration data"""

    ReadingCartesianPosition: bool
    """TRUE, while the CartesianPosition is returned cyclically"""

    ReadingCartesianPositionExt: bool
    """TRUE, while the ExtCartesianPosition is returned cyclically"""

    ReadingJointPosition: bool
    """TRUE, while the JointPosition is returned cyclically"""

    ReadingJointPositionExt: bool
    """TRUE, while the ExtJointPosition is returned cyclically"""

    Initialized: bool
    """Robot is initialized"""

    OnlineChange: bool
    """Online change detected"""

    OnlineChange_R: R_TRIG
    """Rising edge for online change detected"""

    OnlineChange_F: F_TRIG
    """Falling edge for online change detected"""

    GroupReset: bool
    """GroupReset active"""

    GroupReset_R: R_TRIG
    """Rising edge for GroupReset"""

    GroupReset_F: F_TRIG
    """Falling edge for GroupReset"""

    SequenceCountSend: int
    """Counter of sequences to send"""

    SequenceCountRecv: int
    """Counter of sequences received"""

    FragmentCountSend: ARRAY[int] = ARRAY(0, 1, int)
    """
    Counter of fragments to send
    Size: 0..1 (2 elements)
    """

    FragmentCountRecv: ARRAY[int] = ARRAY(0, 1, int)
    """
    Counter of fragments received
    Size: 0..1 (2 elements)
    """

    CurrentSEQ: ARRAY[int] = ARRAY(0, 1, int)
    """
    Current sequence ID
    Size: 0..1 (2 elements)
    """

    CurrentACK: ARRAY[int] = ARRAY(0, 1, int)
    """
    Current acknowledge ID
    Size: 0..1 (2 elements)
    """

    NewSEQ: ARRAY[bool] = ARRAY(0, 1, bool)
    """
    Current sequence ID has changed -> send new data
    Size: 0..1 (2 elements)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure trigger FBs are constructed
        if not isinstance(getattr(self, 'OnlineChange_R', None), R_TRIG):
            self.OnlineChange_R = R_TRIG()
        if not isinstance(getattr(self, 'OnlineChange_F', None), F_TRIG):
            self.OnlineChange_F = F_TRIG()
        # Ensure GroupReset triggers are constructed
        if not isinstance(getattr(self, 'GroupReset_R', None), R_TRIG):
            self.GroupReset_R = R_TRIG()
        if not isinstance(getattr(self, 'GroupReset_F', None), F_TRIG):
            self.GroupReset_F = F_TRIG()
        # Default boolean flags
        if getattr(self, 'GroupReset', None) is None:
            self.GroupReset = False
        if getattr(self, 'InvalidFrames', None) is None:
            self.InvalidFrames = 0
        # Initialize sequence/fragment counters
        if not hasattr(self, 'SequenceCountSend') or self.SequenceCountSend is None:
            self.SequenceCountSend = 0
        if not hasattr(self, 'SequenceCountRecv') or self.SequenceCountRecv is None:
            self.SequenceCountRecv = 0
        # Initialize reading flags
        if getattr(self, 'ReadingCartesianPosition', None) is None:
            self.ReadingCartesianPosition = False
        if getattr(self, 'ReadingCartesianPositionExt', None) is None:
            self.ReadingCartesianPositionExt = False
        if getattr(self, 'ReadingJointPosition', None) is None:
            self.ReadingJointPosition = False
        if getattr(self, 'ReadingJointPositionExt', None) is None:
            self.ReadingJointPositionExt = False

    LastACK: ARRAY = ARRAY(0, 1, UINT)
    """
    Last received acknowledge ID
    Size: 0..1 (2 elements)
    """