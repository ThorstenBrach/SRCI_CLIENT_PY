"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_RobotTaskFB
Author:      Thorsten Brach
Date:        2026-01-06

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
#region Imports

import copy
from RobotLibrary.Enumerations.State.BufferStateCmd import BufferStateCmd
from RobotLibrary.Functions.ToString import ( 
    INT_TO_STRING,
    UINT_TO_STRING,
    FRAGMENT_ACTION_TO_STRING,
    WORD_TO_STRING_BIN
    ) 
from RobotLibrary.Functions.Check import (
    IsFrameDataEqual, 
    IsLoadDataEqual, 
    IsToolDataEqual,
    IsWorkAreaEqual,
    IsDefaultDynamicsEqual,
    IsReferenceDynamicsEqual,
    IsSwLimitsEqual
    )

from RobotLibrary.Functions.Convert import (
    BYTE_TO_SINT,
    DwordToRaStatusWord,
    GetHalfeByteHi,
    GetHalfeByteLo,
    WordToArmConfigShoulder,
    WordToArmConfigElbow,
    WordToArmConfigWrist,
    VersionToByte,
    CombineHalfBytes,
    PlcOptionalCyclicToUint,
    RobOptionalCyclicToUint,
    SINT_TO_BYTE,
    CombineBytesToUint,
    FragmentActionToByte,
    DATE_TO_IEC_DATE,
    TIME_TO_IEC_TIME,
    PERCENT_UINT_TO_REAL,
    SyncModesToDataEnableSync,
    ByteToVersion
)

from RobotLibrary.IEC_Types import BYTE, TIME, STRING, ARRAY, UINT, WORD, UDINT

from RobotLibrary.IEC_Standard import R_TRIG, F_TRIG, TON, SetTimeout, CheckTimeout, CONCAT, LIMIT

from RobotLibrary.Constants import (
    OK, 
    RUNNING, 
    ACTIVE_CMD, 
    AXES_GROUP_ID_MIN, 
    AXES_GROUP_ID_MAX,
    PRIMARY_SEQUENCE,
    SECONDARY_SEQUENCE,
    SRCIVersion,
    PLCLibraryVersion
)

from RobotLibrary.Parameter import (
    MESSAGE_LOG_MAX,
    SYSTEM_LOG_MAX,
    MESSAGE_TEXT_LEN,
    TOOL_MAX,
    FRAME_MAX,
    LOAD_MAX,
    WORK_AREAS_MAX,
    FRAGMENT_MAX,
    ACTIVE_CMD_REGISTER_ENTRIES_MAX,
    INVALID_FRAMES_CHECK_TIMEOUT,
    ACR_USAGE_WARNING_LIMIT,
    RESPONSE_PAYLOAD_MAX
)

from RobotLibrary.Structures.Miscellaneous.FragmentAction import FragmentAction
from RobotLibrary.Structures.Telegram.PlcToRob.TelegramPlcToRob import TelegramPlcToRob

from RobotLibrary.POUs._internal.Send.RobotLibrarySendDataFB import RobotLibrarySendDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryRecvDataFB import RobotLibraryRecvDataFB

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from RobotLibrary.POUs.Read.MC_ReadRobotData.MC_ReadRobotDataFB import MC_ReadRobotDataFB
from RobotLibrary.POUs.Read.MC_ReadMessages.MC_ReadMessagesFB import MC_ReadMessagesFB
from RobotLibrary.POUs.Read.MC_ReadFrameData.MC_ReadFrameDataFB import MC_ReadFrameDataFB
from RobotLibrary.POUs.Write.MC_WriteFrameData.MC_WriteFrameDataFB import MC_WriteFrameDataFB

from RobotLibrary.POUs.Read.MC_ReadLoadData.MC_ReadLoadDataFB import MC_ReadLoadDataFB
from RobotLibrary.POUs.Write.MC_WriteLoadData.MC_WriteLoadDataFB import MC_WriteLoadDataFB

from RobotLibrary.POUs.Read.MC_ReadToolData.MC_ReadToolDataFB import MC_ReadToolDataFB
from RobotLibrary.POUs.Write.MC_WriteToolData.MC_WriteToolDataFB import MC_WriteToolDataFB

from RobotLibrary.POUs.WorkAreas.MC_ReadWorkArea.MC_ReadWorkAreaFB import MC_ReadWorkAreaFB
from RobotLibrary.POUs.WorkAreas.MC_WriteWorkArea.MC_WriteWorkAreaFB import MC_WriteWorkAreaFB

from RobotLibrary.POUs.Read.MC_ReadRobotDefaultDynamics.MC_ReadRobotDefaultDynamicsFB import MC_ReadRobotDefaultDynamicsFB
from RobotLibrary.POUs.Write.MC_WriteRobotDefaultDynamics.MC_WriteRobotDefaultDynamicsFB import MC_WriteRobotDefaultDynamicsFB

from RobotLibrary.POUs.Read.MC_ReadRobotReferenceDynamics.MC_ReadRobotReferenceDynamicsFB import MC_ReadRobotReferenceDynamicsFB
from RobotLibrary.POUs.Write.MC_WriteRobotReferenceDynamics.MC_WriteRobotReferenceDynamicsFB import MC_WriteRobotReferenceDynamicsFB


from RobotLibrary.POUs.Read.MC_ReadRobotSwLimits.MC_ReadRobotSwLimitsFB import MC_ReadRobotSwLimitsFB
from RobotLibrary.POUs.Write.MC_WriteRobotSwLimits.MC_WriteRobotSwLimitsFB import MC_WriteRobotSwLimitsFB


from RobotLibrary.POUs.Additional.MC_ExchangeConfiguration.MC_ExchangeConfigurationFB import MC_ExchangeConfigurationFB


from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Mode.SyncMode import SyncMode
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode as ExecutionModeEnum
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Enumerations.State.RaSequenceState import RaSequenceState
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotLibraryErrorIdEnum
from RobotLibrary.Enumerations.Events.WarningIdEnum import WarningIdEnum as RobotLibraryWarningIdEnum
from RobotLibrary.Enumerations.Events.InfoIdEnum import InfoIdEnum as RobotLibraryInfoIdEnum
from RobotLibrary.Enumerations.State.TelegramState import TelegramState
from RobotLibrary.Enumerations.Miscellaneous.ControlHalfByte import ControlHalfByte
from RobotLibrary.Enumerations.Miscellaneous.ComDirection import ComDirection
from RobotLibrary.Enumerations.Flag.SequenceFlag import SequenceFlag
from RobotLibrary.Enumerations.Miscellaneous.SyncTime import SyncTime
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode


from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime as SystemTimeStruct
from RobotLibrary.Structures.Data.Tool.Tool import Tool
from RobotLibrary.Structures.Data.Load.Load import Load
from RobotLibrary.Structures.Data.Frame.Frame import Frame
from RobotLibrary.Structures.Data.WorkArea.RobotWorkArea import RobotWorkArea
from RobotLibrary.Structures.Data.User.UserData import UserData as UserDataStruct

from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits, SWLimits as SWLimitsStruct
from RobotLibrary.Structures.Dynamics.DefaultDynamics import DefaultDynamics, DefaultDynamics as DefaultDynamicsStruct
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import ReferenceDynamics, ReferenceDynamics as ReferenceDynamicsStruct
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage
from RobotLibrary.Structures.Telegram.PlcToRob.Fragment.TelegramPlcToRobFragment import TelegramPlcToRobFragmentHeader
from RobotLibrary.Structures.Telegram.PlcToRob.Command.TelegramPlcToRobCommand import TelegramPlcToRobCommandHeader

# Use explicit class import to avoid importing the module object
from RobotLibrary.Structures.Telegram.Telegram import Telegram as TelegramStruct
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup

from RobotLibrary.Structures.AxesGroup.State.DataChanged.AxesGroupStateDataChanged import AxesGroupStateDataChanged

from RobotLibrary.Structures.Telegram.RobToPlc.TelegramRobToPlc import TelegramRobToPlc

from .Structures.RobotTaskParCfg import RobotTaskParCfg


    
#endregion    

# ------------------------------------------------------------
# Vollständiger Funktionsbaustein
# ------------------------------------------------------------
class MC_RobotTaskFB(RobotLibraryLogFB):
    
        
    #region VAR_INPUT
    Enable            : bool
    """Set TRUE (default) to initialize the interface"""
    
    RobotName         : str
    """User defined robot name"""
    
    SystemTime        : SystemTimeStruct
    """Current System Time"""
    
    OnlineChange      : bool
    """Online Change detected"""
    
    AxesGroupID       : int = 0 # ToDo: Mistake in specification : ID should start with 1, but must start with 0 !  
    """
    Axes Group ID -> is used to uniquely identify each RA on a per RC basis.\n
    For convenience, an RC with only one RA must assign ID 1 to this RA.    \n
    An RC with multiple RAs must assign numeric values 1-15 to those RAs.   \n
    """
    
    ParCfg            : RobotTaskParCfg
    """Configuration parameter"""
    #endregion



    #region VAR_OUTPUT
    
    Busy              : bool
    """FB is being processed"""

    Initialized       : bool
    """
    Interface is initialized (RI state: "Initialized").\n
    For more information on RI states refer to chapter 5.5.3.1.
    """

    Synchronized      : bool
    """
    Server and client were successfully synchronized (RI state: "Synchronized"). \n
    For more information on the synchronization mechanism refer to chapter 5.6.7.
    """

    Error             : bool
    """An error occurred"""

    ErrorID           : int
    """ ErrorID reported by RC for error identification according to Table 7-1"""
    ErrorIdEnum       : RobotLibraryErrorIdEnum  
    """ ErrorID reported by RC for error identification according to Table 7-1"""
    ErrorAddTxt       : str
    """ Additional error text provided by RC"""
    
    
    WarningID         : int
    """ WarningID for warning identification reported during execution of command according to Table 7-3"""
    WarningIdEnum     : RobotLibraryWarningIdEnum  
    """ WarningID for warning identification reported during execution of command according to Table 7-3"""

    InfoID            : int    
    """ InfoID for info identification reported during execution of command according to Table 7-5"""
    InfoIdEnum        : RobotLibraryInfoIdEnum    
    """ InfoID for info identification reported during execution of command according to Table 7-5"""

    #endregion

    #region VAR
    _parCfg                       : RobotTaskParCfg
    """ internal copy of configuration parameter"""

    _toolData                     : list[Tool]
    """ internal ToolData for comparation to user ToolData"""

    _frameData                    : list[Frame]
    """ internal FrameData for comparation to user FrameData"""

    _loadData                     : list[Load]
    """ internal LoadData for comparation to user LoadData"""

    _workAreas                    : list[RobotWorkArea]
    """ internal WorkAreas for comparation to user WorkAreas"""

    _swLimits                     : SWLimitsStruct
    """ internal Software limits for comparation to user Software limit"""

    _defaultDynamics              : DefaultDynamicsStruct
    """ internal default dynamics for comparation to user default dynamics"""

    _referenceDynamics            : ReferenceDynamicsStruct
    """internal reference dynamics for comparation to user reference dynamics"""

    _exchangeConfiguration        : MC_ExchangeConfigurationFB
    """FB for exchange configuration"""
    
    _readRobotData                : MC_ReadRobotDataFB
    """FB for read robot data"""

    _readMessages                 : MC_ReadMessagesFB  
    """FB for read messaged"""

    _readToolData                 : MC_ReadToolDataFB  
    """FB for read tool data"""

    _readFrameData                : MC_ReadFrameDataFB  
    """FB for read frame data"""

    _readLoadData                 : MC_ReadLoadDataFB  
    """FB for read load data"""

    _readWorkArea                 : MC_ReadWorkAreaFB  
    """FB for read work area"""

    _readRobotSwLimits            : MC_ReadRobotSwLimitsFB  
    """FB for read robot software limits"""

    _readRobotDefaultDynamics     : MC_ReadRobotDefaultDynamicsFB  
    """FB for read robot default dynamics"""

    _readRobotReferenceDynamics   : MC_ReadRobotReferenceDynamicsFB  
    """FB for read robot reference dynamics"""

    _writeToolData                : MC_WriteToolDataFB  
    """FB for write tool data"""
    
    _writeFrameData               : MC_WriteFrameDataFB  
    """FB for write frame data"""
    
    _writeLoadData                : MC_WriteLoadDataFB  
    """FB for write load data"""
    
    _writeWorkArea                : MC_WriteWorkAreaFB  
    """FB for write work area"""
    
    _writeRobotSwLimits           : MC_WriteRobotSwLimitsFB  
    """FB for write robot software limits"""
    
    _writeRobotDefaultDynamics    : MC_WriteRobotDefaultDynamicsFB  
    """FB for write robot default dynamics"""
    
    _writeRobotReferenceDynamics  : MC_WriteRobotReferenceDynamicsFB  
    """FB for write robot reference dynamics"""
    
    SendData                      : RobotLibrarySendDataFB
    """Send Buffer"""

    RecvData                      : RobotLibraryRecvDataFB
    """Recv Buffer"""

    Telegram                      : TelegramStruct 
    """Telegram """
    
    _stepCmd                      : int
    """internal step counter for command"""

    _timerCmd                     : TON
    """internal timer for command """

    _timeoutCmd                   : TIME = TIME(5000) 
    """internal timeout for command"""
    
    _stepSyncFrameData            : int
    """internal step counter for synchronisation of frame data"""

    _timerSyncFrameData           : TON
    """internal timer for synchronisation of frame data"""

    _timeoutSyncFrameData         : TIME = TIME(5000)
    """internal timeout for synchronisation of frame data"""

    _syncIdxFrameData             : int
    """internal index for frame data synchronisation"""

    _syncIdxMaxFrameData          : int
    """internal index for maximal amount of frames data( MIN(PLC,RC) ) """
    
    _stepSyncLoadData             : int
    """internal step counter for synchronisation of load data"""

    _timerSyncLoadData             : TON
    """internal timer for synchronisation of load data"""

    _timeoutSyncLoadData           : TIME = TIME(5000)
    """internal timeout for synchronisation of load data"""

    _syncIdxLoadData               : int
    """internal index for load data synchronisation"""

    _syncIdxMaxLoadData            : int
    """internal index for maximal amount of load data ( MIN(PLC,RC) ) """

    _stepSyncToolData              : int
    """internal step counter for synchronisation of tool data"""

    _timerSyncToolData             : TON
    """internal timer for synchronisation of tool data"""

    _timeoutSyncToolData           : TIME = TIME(5000) 
    """internal timeout for synchronisation of tool data"""

    _syncIdxToolData               : int
    """internal index for tool data synchronisation"""

    _syncIdxMaxToolData            : int
    """internal index for maximal amount of tool data ( MIN(PLC,RC) ) """

    _stepSyncWorkArea            : int
    """internal step counter for synchronisation of work areas"""

    _timerSyncWorkArea           : TON
    """internal timer for synchronisation of work areas"""

    _timeoutSyncWorkArea         : TIME = TIME(5000)
    """internal timeout for synchronisation of work areas"""

    _syncIdxWorkArea             : int
    """internal index for WorkArea synchronisation"""

    _syncIdxMaxWorkArea          : int
    """internal index for maximal amount of Work Area( MIN(PLC,RC) ) """
    
    _stepSyncSWLimits            : int
    """internal step counter for synchronisation of software limits"""

    _timerSyncSWLimits           : TON
    """internal timer for synchronisation of software limits"""

    _timeoutSyncSWLimits         : TIME = TIME(5000)
    """internal timeout for synchronisation of software limits"""

    _stepSyncDefaultDynamics      : int
    """internal step counter for synchronisation of default dynamics"""

    _timerSyncDefaultDynamics     : TON
    """internal timer for synchronisation of default dynamics"""

    _timeoutSyncDefaultDynamics   : TIME = TIME(5000)
    """internal timeout for synchronisation of default dynamics"""
    
    _stepSyncReferenceDynamics    : int
    """internal step counter for synchronisation of reference dynamics"""

    _timerSyncReferenceDynamics   : TON
    """internal timer for synchronisation of reference dynamics"""

    _timeoutSyncReferenceDynamics : TIME = TIME(5000)
    """internal timeout for synchronisation of reference dynamics"""

    _enable_R                    : R_TRIG
    """Rising edge for enable"""

    _enable_F                    : F_TRIG
    """Falling edge for enable"""

    _aliveBit                    : bool
    """Flag that indicated the the connection is alive (data exchange)"""

    _aliveValue                  : int
    """last lifesign counter value"""

    _aliveCheck                  : TON
    """timer for detecting alive state"""

    _alive_R                     : R_TRIG
    """rising edge for connection is alive"""

    _alive_F                     : F_TRIG
    """falling edge for connection is alive"""

    _lastTelegramState           : TelegramState   = TelegramState.UNDEFINED
    """last telegram state"""

    _lastTelegramControl         : ControlHalfByte = ControlHalfByte.NONE
    """last telegram control"""

    _first                       : bool = True
    """First cycle """

    _invalidFrameCounterCheck_D : TON
    """Timeout for invalid frames counter check"""
 
    _lastInvalidFrames          : int
    """last count of invalid frames"""

    #endregion

    #region VAR // CONSTANT

    ROBOT_IN_DATA_MIN   : int
    """Lower array dimension of RobotInData"""

    ROBOT_IN_DATA_MAX   : int
    """Upper array dimension of RobotInData"""

    ROBOT_IN_DATA_SIZE  : int
    """Size of RobotInData"""

    ROBOT_OUT_DATA_MIN  : int
    """Lower array dimension of RobotOutData"""

    ROBOT_OUT_DATA_MAX  : int
    """Upper array dimension of RobotOutData"""

    ROBOT_OUT_DATA_SIZE : int
    """Size of RobotOutData"""

    #endregion

    #region VAR CONSTANT
    FRAGMENT_HEADER_SIZE : int = TelegramPlcToRobFragmentHeader.sizeof()
    """Size of the fragment header"""

    COMMAND_HEADER_SIZE  : int = TelegramPlcToRobCommandHeader.sizeof()
    """Size of the command header"""

    FOOTER_SIZE          : int = 1
    """Size of the footer"""

    MIN_PAYLOAD_SIZE     : int = 1
    """Minimal payload size for telegram"""

    ACTIVE_CMD           : int = 1
    """Active command"""

    BUFFER_CMD           : int = 2
    """Buffered command"""

    LIFESIGN_BIT_MASK    : BYTE = BYTE(int(0b0001111))
    """bitmask to mask the LifeSign out of the halfbyte"""

    PRIMARY_SEQUENCE     : int = 0
    """Primary sequence"""

    SECONDARY_SEQUENCE   : int = 1  
    """Secondary sequence"""

    EMPTY_EOL_ENTRY      : int = 0
    """Empty Execution-Order-List entry"""

    #endregion


    #------------------------------------------------------------
    # Constructor
    #------------------------------------------------------------
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # Set type name
        self.MyType = self.__class__.__name__

        #region VAR_INPUT
        self.Enable            = False
        self.RobotName         = ''
        self.SystemTime        = SystemTimeStruct()
        self.OnlineChange      = False
        self.AxesGroupID       = 0 
        self.ParCfg            = RobotTaskParCfg()
        #endregion

        #region VAR_OUTPUT
        self.Busy              = False
        self.Initialized       = False
        self.Synchronized      = False
        self.Error             = False
        self.ErrorID           = 0
        self.ErrorIdEnum       = RobotLibraryErrorIdEnum.NO_ERROR
        self.ErrorAddTxt       = ''
        self.WarningID         = 0
        self.WarningIdEnum     = RobotLibraryWarningIdEnum.NO_WARNING
        self.InfoID            = 0
        self.InfoIdEnum        = RobotLibraryInfoIdEnum.NO_INFO
        #endregion

        #region VAR

        # first cycle flag
        self._first                        = True

        # Initialize structures and lists
        self. ParCfg                       = RobotTaskParCfg()
        self._parCfg                       = RobotTaskParCfg()
        self._toolData                     = [Tool()          for _ in range(TOOL_MAX      )]
        self._frameData                    = [Frame()         for _ in range(FRAME_MAX     )]
        self._loadData                     = [Load()          for _ in range(LOAD_MAX      )]
        self._workAreas                    = [RobotWorkArea() for _ in range(WORK_AREAS_MAX)]
        self._swLimits                     = SWLimitsStruct()
        self._defaultDynamics              = DefaultDynamicsStruct()
        self._referenceDynamics            = ReferenceDynamicsStruct()

        # Initialize telegram variables
        self.Telegram                      = TelegramStruct()
        self._lastTelegramState            = TelegramState.UNDEFINED
        self._lastTelegramControl          = ControlHalfByte.NONE


        # Initialize function blocks
        self._enable_R                     = R_TRIG()
        self._enable_F                     = F_TRIG()
        self._exchangeConfiguration        = MC_ExchangeConfigurationFB()
        self._readRobotData                = MC_ReadRobotDataFB()
        self._readMessages                 = MC_ReadMessagesFB()
        self._readToolData                 = MC_ReadToolDataFB()
        self._readFrameData                = MC_ReadFrameDataFB()
        self._readLoadData                 = MC_ReadLoadDataFB()
        self._readWorkArea                 = MC_ReadWorkAreaFB()
        self._readRobotSwLimits            = MC_ReadRobotSwLimitsFB()
        self._readRobotDefaultDynamics     = MC_ReadRobotDefaultDynamicsFB()
        self._readRobotReferenceDynamics   = MC_ReadRobotReferenceDynamicsFB()
        self._writeToolData                = MC_WriteToolDataFB()
        self._writeFrameData               = MC_WriteFrameDataFB()
        self._writeLoadData                = MC_WriteLoadDataFB()
        self._writeWorkArea                = MC_WriteWorkAreaFB()
        self._writeRobotSwLimits           = MC_WriteRobotSwLimitsFB()
        self._writeRobotDefaultDynamics    = MC_WriteRobotDefaultDynamicsFB()
        self._writeRobotReferenceDynamics  = MC_WriteRobotReferenceDynamicsFB()
        self.SendData                      = RobotLibrarySendDataFB()
        self.RecvData                      = RobotLibraryRecvDataFB()

        # Initialize alive variables
        self._alive_R    = R_TRIG()
        self._alive_F    = F_TRIG()
        self._aliveCheck = TON()
        self._aliveBit   = False
        self._aliveValue = 0

        # Initialize timers used early
        self._invalidFrameCounterCheck_D = TON()
        self._lastInvalidFrames = 0

        # Initialize step counters
        self._stepCmd                   = 0
        self._stepSyncFrameData         = 0
        self._stepSyncLoadData          = 0
        self._stepSyncDefaultDynamics   = 0
        self._stepSyncReferenceDynamics = 0
        self._stepSyncSWLimits          = 0
        self._stepSyncToolData          = 0
        self._stepSyncWorkArea          = 0

        # Initialize timers
        self._timerCmd                   = TON()
        self._timerSyncFrameData         = TON()
        self._timerSyncLoadData          = TON()
        self._timerSyncToolData          = TON()
        self._timerSyncWorkArea          = TON()
        self._timerSyncSWLimits          = TON()
        self._timerSyncDefaultDynamics   = TON()
        self._timerSyncReferenceDynamics = TON()

        # Initialize sync indices
        self._syncIdxFrameData      = 0
        self._syncIdxMaxFrameData   = 0
        self._syncIdxLoadData       = 0
        self._syncIdxMaxLoadData    = 0
        self._syncIdxToolData       = 0
        self._syncIdxMaxToolData    = 0
        self._syncIdxWorkArea       = 0
        self._syncIdxMaxWorkArea    = 0

        #endregion

        # Create log entry
        self.CreateLogMessage ( 
            Timestamp   = self.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'PLC started / restarted'
        )

    #------------------------------------------------------------
    # Cyclic operation ( FB body )
    #------------------------------------------------------------
    def __call__(self,  RobotName         : str,
                        AxesGroupID       : int,
                        OnlineChange      : bool,
                        RobotInData       : bytearray,
                        RobotOutData      : bytearray,
                        UserData          : UserDataStruct,
                        AxesGroup         : AxesGroup,
                        ToolData          : list[Tool],
                        FrameData         : list[Frame],
                        LoadData          : list[Load],
                        WorkAreas         : list[RobotWorkArea],
                        SWLimits          : SWLimits,
                        DefaultDynamics   : DefaultDynamics,
                        ReferenceDynamics : ReferenceDynamics,
                        SystemLog         : ARRAY[STRING] = ARRAY(0, SYSTEM_LOG_MAX,  STRING(MESSAGE_TEXT_LEN)),
                        MessageLog        : ARRAY[AlarmMessage] = ARRAY (0, MESSAGE_LOG_MAX,  AlarmMessage) ) -> None:

        # apply parameter
        self.RobotName  = RobotName
        self.AxesGroupID = AxesGroupID
        self.OnlineChange = OnlineChange
        

        """Robot assignment of function"""

        # Get array dimension of RobotInData
        self.ROBOT_IN_DATA_MIN  = 0
        self.ROBOT_IN_DATA_MAX  = len( RobotInData) -1
        self.ROBOT_IN_DATA_SIZE = ( self.ROBOT_IN_DATA_MAX - self.ROBOT_IN_DATA_MIN + 1)

        # Get array dimension of RobotInData
        self.ROBOT_OUT_DATA_MIN  = 0
        self.ROBOT_OUT_DATA_MAX  = len( RobotOutData) -1
        self.ROBOT_OUT_DATA_SIZE = ( self.ROBOT_OUT_DATA_MAX - self.ROBOT_OUT_DATA_MIN + 1)


        self.HandleAxesGroup          ( AxesGroup         = AxesGroup,
                                        ToolData          = ToolData, 
                                        FrameData         = FrameData, 
                                        LoadData          = LoadData, 
                                        WorkAreas         = WorkAreas, 
                                        SWLimits          = SWLimits, 
                                        DefaultDynamics   = DefaultDynamics, 
                                        ReferenceDynamics = ReferenceDynamics)
                                    
        self.HandleLifeSign               ( AxesGroup         = AxesGroup)
        self.HandleLogMessagesAck         ( AxesGroup         = AxesGroup)
        self.HandleInvalidFrames          ( AxesGroup         = AxesGroup, RobotInData = RobotInData)
        self.HandleTelegramStateCtrl      (                              )
        self.HandleAliveBit               ( RobotInData[1]               )
        self.HandleSeqAck                 ( AxesGroup         = AxesGroup)
        self.HandleUserData               ( AxesGroup         = AxesGroup, UserData = UserData )

        self.HandleSync                   ( AxesGroup         = AxesGroup,
                                            ToolData          = ToolData,
                                            FrameData         = FrameData,
                                            LoadData          = LoadData,
                                            WorkAreas         = WorkAreas,
                                            SWLimits          = SWLimits,
                                            DefaultDynamics   = DefaultDynamics,
                                            ReferenceDynamics = ReferenceDynamics)

        self.OnCall                       ( AxesGroup         = AxesGroup)
        self.OnExecRun                    ( AxesGroup         = AxesGroup)

        self.AxesGroupToTelegram          ( AxesGroup         = AxesGroup )

        self.CreateSendPayload            ( AxesGroup         = AxesGroup, RobotOutData = RobotOutData )
        self.ParseRecvPayload             ( AxesGroup         = AxesGroup, RobotInData  = RobotInData)

        self.AxesGroupFromTelegram        ( AxesGroup         = AxesGroup)


        # call internal functionblocks
        self._exchangeConfiguration      ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readRobotData              ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readMessages               ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readToolData               ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readFrameData              ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readLoadData               ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readWorkArea               ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readRobotSwLimits          ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readRobotDefaultDynamics   ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._readRobotReferenceDynamics ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeToolData              ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeFrameData             ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeLoadData              ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeWorkArea              ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeRobotSwLimits         ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeRobotDefaultDynamics  ( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )
        self._writeRobotReferenceDynamics( Name = RobotName, ExecMode = ExecutionMode.PARALLEL, Priority = PriorityLevel.NORMAL, AxesGroup = AxesGroup )


        # Update SystemLog and MessageLog
        SystemLog  = AxesGroup.MessageLog.SystemLogs 
        MessageLog = AxesGroup.MessageLog.Messages   


    #------------------------------------------------------------
    # Extract AxesGroup information from received telegram
    #------------------------------------------------------------        
    def AxesGroupFromTelegram(self, AxesGroup : AxesGroup) -> None :
        """Extract AxesGroup information from received telegram."""
        
        self.AxesGroupFromTelegramCyclic         (AxesGroup = AxesGroup)
        self.AxesGroupFromTelegramCyclicOptional (AxesGroup = AxesGroup)


    #------------------------------------------------------------
    # Extract AxesGroup cyclic information from received telegram
    #------------------------------------------------------------
    def AxesGroupFromTelegramCyclic(self, AxesGroup : AxesGroup) -> None :
        """Extract AxesGroup cyclic information from received telegram."""
        
        AxesGroup.Cyclic.RobToPlc.SRCIVersion    = self.Telegram.RobToPlc.Header.SRCIVersion
        AxesGroup.Cyclic.RobToPlc.LifeSign       = self.Telegram.RobToPlc.Header.LifeSign
        AxesGroup.Cyclic.RobToPlc.TelegramState  = self.Telegram.RobToPlc.Header.TelegramState
        AxesGroup.Cyclic.RobToPlc.StatusRobotArm = DwordToRaStatusWord(self.Telegram.RobToPlc.Header.StatusRobotArm)
        AxesGroup.Cyclic.RobToPlc.Override       = self.Telegram.RobToPlc.Header.Override

    #------------------------------------------------------------
    # Extract AxesGroup cyclic optional information from received telegram
    #------------------------------------------------------------
    def AxesGroupFromTelegramCyclicOptional(self, AxesGroup : AxesGroup) -> None :
        
        #region Sub ProgramData 
        AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Data = self.Telegram.RobToPlc.CyclicOptional.SubProgramData.Data
        #endregion

        #region Cartesian position
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active                   =                                      AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.X                        =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.X.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Y                        =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Y.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Z                        =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Z.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rx                       =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rx.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Ry                       =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Ry.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rz                       =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rz.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Shoulder          =              WordToArmConfigShoulder(self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Elbow             =              WordToArmConfigElbow   (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Wrist             =              WordToArmConfigWrist   (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J1Turns       = BYTE_TO_SINT(GetHalfeByteLo         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J2_J1))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J2Turns       = BYTE_TO_SINT(GetHalfeByteHi         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J2_J1))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J3Turns       = BYTE_TO_SINT(GetHalfeByteLo         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J4_J3))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J4Turns       = BYTE_TO_SINT(GetHalfeByteHi         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J4_J3))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J5Turns       = BYTE_TO_SINT(GetHalfeByteLo         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J6_J5))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J6Turns       = BYTE_TO_SINT(GetHalfeByteHi         (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J6_J5))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.E1Turns       = BYTE_TO_SINT                        (self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_E1)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.E1                       =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.E1.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.ToolNo  =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedToolNo
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.FrameNo =                                      self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedFrameNo
        #endregion

        #region Joint position
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active = AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J1     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J1.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J2     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J2.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J3     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J3.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J4     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J4.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J5     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J5.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J6     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.J6.value
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.E1     =  self.Telegram.RobToPlc.CyclicOptional.JointPosition.E1.value
        #endregion

        #region Force
        AxesGroup.CyclicOptional.RobToPlc.Force.Active          = AxesGroup.CyclicOptional.RobToPlc.Force.Active
        AxesGroup.CyclicOptional.RobToPlc.Force.X               = self.Telegram.RobToPlc.CyclicOptional.Force.X
        AxesGroup.CyclicOptional.RobToPlc.Force.Y               = self.Telegram.RobToPlc.CyclicOptional.Force.Y
        AxesGroup.CyclicOptional.RobToPlc.Force.Z               = self.Telegram.RobToPlc.CyclicOptional.Force.Z
        AxesGroup.CyclicOptional.RobToPlc.Force.Rx              = self.Telegram.RobToPlc.CyclicOptional.Force.Rx
        AxesGroup.CyclicOptional.RobToPlc.Force.Ry              = self.Telegram.RobToPlc.CyclicOptional.Force.Ry
        AxesGroup.CyclicOptional.RobToPlc.Force.Rz              = self.Telegram.RobToPlc.CyclicOptional.Force.Rz
        #endregion


        #region Current
        AxesGroup.CyclicOptional.RobToPlc.Current.Active        =      AxesGroup.CyclicOptional.RobToPlc.Current.Active
        AxesGroup.CyclicOptional.RobToPlc.Current.J1            = self.Telegram.RobToPlc.CyclicOptional.Current.J1.value
        AxesGroup.CyclicOptional.RobToPlc.Current.J2            = self.Telegram.RobToPlc.CyclicOptional.Current.J2.value
        AxesGroup.CyclicOptional.RobToPlc.Current.J3            = self.Telegram.RobToPlc.CyclicOptional.Current.J3.value
        AxesGroup.CyclicOptional.RobToPlc.Current.J4            = self.Telegram.RobToPlc.CyclicOptional.Current.J4.value
        AxesGroup.CyclicOptional.RobToPlc.Current.J5            = self.Telegram.RobToPlc.CyclicOptional.Current.J5.value
        AxesGroup.CyclicOptional.RobToPlc.Current.J6            = self.Telegram.RobToPlc.CyclicOptional.Current.J6.value
        #endregion


        #region Two Sequences
        
        #endregion

        #region Cartesian Position Extended
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active =      AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E2     = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E2.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E3     = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E3.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E4     = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E4.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E5     = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E5.value
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E6     = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E6.value
        #endregion

        #region Joint Position Extended
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active     = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E2         = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E2.value
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E3         = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E3.value
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E4         = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E4.value
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E5         = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E5.value
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E6         = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E6.value
        #endregion

        #region Force Extended
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active             = AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E1                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E1
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E2                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E2
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E3                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E3
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E4                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E4
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E5                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E5
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E6                 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E6
        #endregion

        #region Current Extended
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active           = AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E1               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E1.value
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E2               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E2.value
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E3               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E3.value
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E4               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E4.value
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E5               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E5.value
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E6               = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E6.value
        #endregion

    #------------------------------------------------------------
    # Convert AxesGroup information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegram(self, AxesGroup : AxesGroup) -> int :
        
        if ( AxesGroup.State.NewSEQ[0]):  #ToDo Handle 2nd sequence
        
            # delete old telegram data 
            self.Telegram.PlcToRob = TelegramPlcToRob()

        self.AxesGroupToTelegramHeader        (AxesGroup = AxesGroup)
        self.AxesGroupToTelegramCyclic        (AxesGroup = AxesGroup)
        self.AxesGroupToTelegramCyclicOptional(AxesGroup = AxesGroup)
        self.AxesGroupToTelegramSequence      (AxesGroup = AxesGroup)
        self.AxesGroupToTelegramFooter        (AxesGroup = AxesGroup)
        self.AxesGroupToTelegramLogging       (AxesGroup = AxesGroup)

        return OK


    #------------------------------------------------------------
    # Convert AxesGroup information to telegram header
    #------------------------------------------------------------
    def AxesGroupToTelegramHeader(self, AxesGroup : AxesGroup) -> int :

        self.Telegram.PlcToRob.Header.SRCIVersion                  = VersionToByte(AxesGroup.Cyclic.PlcToRob.SRCIVersion)
        self.Telegram.PlcToRob.Header.FastStop_LifeSign.value      = CombineHalfBytes( HalfByteHi = AxesGroup.Cyclic.PlcToRob.FastStop, HalfByteLo = AxesGroup.Cyclic.PlcToRob.LifeSign ).value
        self.Telegram.PlcToRob.Header.TelegramLengthPlcToRob.value = self.ParCfg.Com.TelegramLengthPlcToRob
        self.Telegram.PlcToRob.Header.TelegramLengthRobToPlc.value = self.ParCfg.Com.TelegramLengthRobToPlc
        self.Telegram.PlcToRob.Header.AxesGroupID_Control.value    = CombineHalfBytes(HalfByteHi = AxesGroup.Cyclic.PlcToRob.AxesGroupID, HalfByteLo = AxesGroup.Cyclic.PlcToRob.Control.TypeValue).value
        self.Telegram.PlcToRob.Header.Reserved.value               = 0
        self.Telegram.PlcToRob.Header.TelegramNumberPlcToRob       = PlcOptionalCyclicToUint(AxesGroup.Parameter.Plc.OptionalCyclic)
        self.Telegram.PlcToRob.Header.TelegramNumberRobToPlc       = RobOptionalCyclicToUint(AxesGroup.Parameter.Rob.OptionalCyclic)
        self.Telegram.PlcToRob.Header.ClientDate                   = AxesGroup.Cyclic.PlcToRob.ClientDate
        self.Telegram.PlcToRob.Header.ClientTime                   = AxesGroup.Cyclic.PlcToRob.ClientTime

        return OK


    #------------------------------------------------------------
    # Convert AxesGroup cyclic information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegramCyclic(self, AxesGroup : AxesGroup) -> int :

        if (AxesGroup.Cyclic.PlcToRob.ToolNo == -1 ):
        
            self.Telegram.PlcToRob.Cyclic.ToolNo.value  = 0xFF
        else:
            self.Telegram.PlcToRob.Cyclic.ToolNo.value  = AxesGroup.Cyclic.PlcToRob.ToolNo.value


        if (AxesGroup.Cyclic.PlcToRob.FrameNo == -1 ):
        
            self.Telegram.PlcToRob.Cyclic.FrameNo.value  = 0xFF
        else:
            self.Telegram.PlcToRob.Cyclic.FrameNo.value  = AxesGroup.Cyclic.PlcToRob.FrameNo.value


        return OK


    #------------------------------------------------------------
    # Convert AxesGroup cyclic optional information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegramCyclicOptional(self, AxesGroup : AxesGroup) -> int :
        
        #region AxesGroup.CyclicOptional.PlcToRob.SubProgramData
        if (AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active) : 

            self.Telegram.PlcToRob.CyclicOptional.SubProgramData.Data = AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Data

        #endregion

        #region AxesGroup.CyclicOptional.PlcToRob.CartesianPosition 
        if (AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Active) : 
        
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.X.value           =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.X  
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Y.value           =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Y  
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Z.value           =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Z
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rx.value          =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Rx  
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Ry.value          =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Ry  
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rz.value          =                  AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Rz
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J2_J1.value = CombineHalfBytes(AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J2Turns, 
                                                                                                    AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J1Turns).value
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J4_J3.value = CombineHalfBytes(AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J4Turns, 
                                                                                                    AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J3Turns).value
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J6_J5.value = CombineHalfBytes(AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J6Turns, 
                                                                                                    AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J5Turns).value
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_E1          = SINT_TO_BYTE    (AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.E1Turns)
        
        #endregion
        
        #region AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt {{{ 
        if ( AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active) :
            
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E2.value = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E2
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E3.value = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E3
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E4.value = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E4
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E5.value = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E5
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E6.value = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E6

        #endregion

        #region AxesGroup.CyclicOptional.PlcToRob.JointPosition
        if ( AxesGroup.CyclicOptional.PlcToRob.JointPosition.Active) :
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J1.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J1
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J2.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J2
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J3.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J3
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J4.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J4
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J5.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J5
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J6.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J6
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.E1.value = AxesGroup.CyclicOptional.PlcToRob.JointPosition.E1

        #endregion

        #region AxesGroup.CyclicOptional.PlcToRob.JointPositionExt
        if ( AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.Active) :
            
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E2.value = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E2
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E3.value = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E3  
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E4.value = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E4
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E5.value = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E5
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E6.value = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E6

        #endregion
            
        #region AxesGroup.CyclicOptional.PlcToRob.Force
        if ( AxesGroup.CyclicOptional.PlcToRob.Force.Active) :
            
            self.Telegram.PlcToRob.CyclicOptional.Force.X  = AxesGroup.CyclicOptional.PlcToRob.Force.X
            self.Telegram.PlcToRob.CyclicOptional.Force.Y  = AxesGroup.CyclicOptional.PlcToRob.Force.Y
            self.Telegram.PlcToRob.CyclicOptional.Force.Z  = AxesGroup.CyclicOptional.PlcToRob.Force.Z
            self.Telegram.PlcToRob.CyclicOptional.Force.Rx = AxesGroup.CyclicOptional.PlcToRob.Force.Rx
            self.Telegram.PlcToRob.CyclicOptional.Force.Ry = AxesGroup.CyclicOptional.PlcToRob.Force.Ry
            self.Telegram.PlcToRob.CyclicOptional.Force.Rz = AxesGroup.CyclicOptional.PlcToRob.Force.Rz
        #endregion
                            
        #region AxesGroup.CyclicOptional.PlcToRob.ForceExt
        if ( AxesGroup.CyclicOptional.PlcToRob.ForceExt.Active) :
            
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E1 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E1
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E2 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E2
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E3 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E3
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E4 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E4
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E5 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E5
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E6 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E6
        #endregion
        
        return OK
    
    #------------------------------------------------------------
    # Convert AxesGroup sequence information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegramSequence(self, AxesGroup : AxesGroup) -> int :

        #region Local Variables
        
        # internal index
        _idx                       : int = 0
        # internal sequence index
        _seqIdx                    : int = 0
        # Amount of sequences
        _seqCount                  : int = 0
        # internal fragment index
        _fragIdx                   : int = 0
        # internal register index
        _regIdx                    : int = 0
        # internal execution order list index
        _listIdx                   : int = 1
        # internal payload pointer
        _payLoadPtr                : int = 0
        # internal fragment action
        _fragmentAction            : FragmentAction = FragmentAction()
        # internal fragment action as string
        _fragmentActionString      : STRING
        # current length of telegram 
        _telegramLengthCurrent    : int = 0
        # temporary byte variable
        _tmpByte                  : BYTE = BYTE(0)

        # maximount amount of bytes per sequence
        SEQUENCE_MAX_PAYLOAD_SIZE : int = 0
        
        #endregion


        # Check 2nd sequence active ? 
        if ( self._parCfg.Com.TwoSequences ) :
        
            # inc sequence counter
            _seqCount += 1
        
            SEQUENCE_MAX_PAYLOAD_SIZE = self.CalculateSequencePayloadMax(AxesGroup = AxesGroup, 
                                                                         Direction = ComDirection.PLC_TO_ROB, 
                                                                         Sequence  = SequenceFlag.SECONDARY_SEQUENCE ) - self.FOOTER_SIZE
        else:
            SEQUENCE_MAX_PAYLOAD_SIZE = self.CalculateSequencePayloadMax(AxesGroup = AxesGroup, 
                                                                         Direction = ComDirection.PLC_TO_ROB, 
                                                                         Sequence  = SequenceFlag.PRIMARY_SEQUENCE   ) - self.FOOTER_SIZE

        # dummy for compiler warning
        SEQUENCE_MAX_PAYLOAD_SIZE = SEQUENCE_MAX_PAYLOAD_SIZE


        for _seqIdx  in range(0, _seqCount) :
        
            # set current SEQ / ACk index
            self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK.value = AxesGroup.State.CurrentSEQ[_seqIdx]

            # only update telegram content if a new sequence SEQ is set
            if ( AxesGroup.State.NewSEQ[_seqIdx] ) :
            
                # only reset counters in case of new telegram to send  
                AxesGroup.State.SequenceCountSend = 0
                AxesGroup.State.FragmentCountSend[_seqIdx] = 0
                
                # calc current telegram payload length
                _telegramLengthCurrent = self.CalculateTelegramLengthPlcToRob(AxesGroup = AxesGroup)
                
                # Bedingung anpassen und TWO_SEQUENCES berücksichtigen
                while (( self._parCfg.Com.TelegramLengthPlcToRob - _telegramLengthCurrent ) >= self.FRAGMENT_HEADER_SIZE + self.MIN_PAYLOAD_SIZE ) :
                
                    # Check command in Execution-Order-List available ?
                    if ( AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx].value > self.EMPTY_EOL_ENTRY) :
                    
                        # set current SEQ / ACk index
                        self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK.value = AxesGroup.State.CurrentSEQ[_seqIdx]
                        
                        # get active command register index
                        _regIdx = AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx].value
                    
                        # check State of the current ACR entry ?
                        if (( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State >= BufferStateCmd.CREATED  ) and
                            ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State <= BufferStateCmd.SENDING  )):
                        
                            # add size of fragement header      
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength.value = ( self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength.value 
                                                                                                  + self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.sizeof())
                            
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID          = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].UniqueID
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.Reserve.value  = 0
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction.value = 0 # will be set below
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr
                        
                            # The 1st message resets the ACR entry on the server side  
                            _fragmentAction.Reset.value = (( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State      == BufferStateCmd.CREATED ) and
                                                           ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr == 0                      ))
                                                    
                            # Update messages must clear the ACR entry on the server side  
                            _fragmentAction.Clear.value = (( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State      == BufferStateCmd.UPDATE_AVAILABLE  ) and
                                                           ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr == 0                                )) 

                            #region fill telegramm header - just for later debugging ( the header is part of the command payload itselfy )
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.CmdType     = CmdType          (CombineBytesToUint ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[0],
                                                                                                                                                       AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[1]).value)
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode    = ExecutionModeEnum(GetHalfeByteLo     ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[2]).value)
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio        = PriorityLevel    (GetHalfeByteLo     ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[3]).value)
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence =                  (GetHalfeByteHi     ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[3]))
                            #endregion
                            
                            
                            # loop through the payload
                            for _payLoadPtr in range( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr.value, AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayloadLen.value -1  ) :
                            
                                # copy payload
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[_payLoadPtr] = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].Payload[_payLoadPtr]
                            
                                # inc current sequence payload length
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength.value += 1
                                
                                # inc current fragment payload length
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value += 1
                            
                                # inc payload pointer in active command register
                                AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr.value += 1
                            
                                # set command state
                                if ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr.value >= AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayloadLen.value) :
                                
                                    AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State = BufferStateCmd.PROCESSED
                                else:
                                    AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].State = BufferStateCmd.SENDING

                        
                                # calc current telegram payload length
                                _telegramLengthCurrent = self.CalculateTelegramLengthPlcToRob(AxesGroup = AxesGroup)
                        
                                # check limit reached ?
                                if ( _telegramLengthCurrent >= self._parCfg.Com.TelegramLengthPlcToRob) :
                                
                                    break # -> abort for loop 


                            # check payload complete ?
                            _fragmentAction.Complete.value = ( AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr.value 
                                                            >= AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[ACTIVE_CMD].PayloadLen.value)
                        
                            # just for brakepoint
                            if (_fragmentAction.Complete.value):
                            
                                _fragmentAction.Complete = _fragmentAction.Complete

                            # set fragment action
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction = FragmentActionToByte(_fragmentAction)

                    
                    # inc execution order list index 
                    _listIdx += 1
                    # inc fragment index 
                    _fragIdx += 1
                
                    # check abort conditions
                    if (( _telegramLengthCurrent                                                      >= self._parCfg.Com.TelegramLengthPlcToRob ) or  # Payload limit reached 
                        ( _fragIdx                                                                    >= FRAGMENT_MAX                            ) or  # Max fragment limit reached
                        (  AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx].value == self.EMPTY_EOL_ENTRY                    )) :  # No entry in ExecutionOrderList left
                    
                        break # -> Abort while loop

                AxesGroup.State.SequenceCountSend          = _seqIdx
                AxesGroup.State.FragmentCountSend[_seqIdx] = _fragIdx

        return OK


    #------------------------------------------------------------
    # Convert AxesGroup footer information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegramFooter(self, AxesGroup : AxesGroup) -> int :

        self.Telegram.PlcToRob.Footer.LifeSign = GetHalfeByteLo(self.Telegram.PlcToRob.Header.FastStop_LifeSign)  

        return OK


    #------------------------------------------------------------
    # Convert AxesGroup logging information to telegram
    #------------------------------------------------------------
    def AxesGroupToTelegramLogging(self, AxesGroup : AxesGroup) -> int :
        
        # region Local Variables
        
        # internal sequence index
        _seqIdx : int = 0
        # internal fragment index
        _fragIdx : int = 0
        
        # endregion


        for _seqIdx in range( 0, AxesGroup.State.SequenceCountSend ):
            
            # check new data ? 
            if ( AxesGroup.State.NewSEQ[_seqIdx] ) :

                if ( self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength.value > 0 ) :

                    # Create log entry
                    self.CreateLogMessage ( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SendData: SEQ = {1}, added Sequence [{2}] with PayloadLength = {3}, HeaderLength = {4}',
                        Para1       =  UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK),
                        Para2       =   INT_TO_STRING(_seqIdx),
                        Para3       =  UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength),
                        Para4       =   INT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.sizeof())
                    )
                    
                    for _fragIdx in range( 0, AxesGroup.State.FragmentCountSend[_seqIdx] ) :
                    
                        if ( self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > 0 ) :

                            # Create log entry
                            self.CreateLogMessage ( 
                                Timestamp   = self.SystemTime,
                                MessageType = MessageType.CMD,
                                Severity    = Severity.DEBUG,
                                MessageCode = 0,
                                MessageText = 'SendData: added Fragment [{1}] with PayloadLength = {2}, HeaderLength = {3}, CmdID <{4}>, Cmd <{5}> Fragment-Action Bits:{6}' ,
                                Para1       = INT_TO_STRING(_fragIdx),
                                Para2       = UINT_TO_STRING            (self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength),
                                Para3       = INT_TO_STRING(            (self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.sizeof())),
                                Para4       = UINT_TO_STRING            (self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID),
                                Para5       =                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.CmdType.toString(),
                                Para6       = FRAGMENT_ACTION_TO_STRING (self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction)
                            ) 

                            # Create log entry
                            self.CreateLogMessage ( 
                                Timestamp   = self.SystemTime,
                                MessageType = MessageType.CMD,
                                Severity    = Severity.DEBUG,
                                MessageCode = 0,
                                MessageText = 'SendData: added Fragment [{1}] will be executed with ExecMode = [{2}]' ,
                                Para1       = INT_TO_STRING(_fragIdx),
                                Para2       = self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode.toString()
                            )                            

        return OK

    
    #------------------------------------------------------------
    # Calculate length of telegram PLC to ROB
    #------------------------------------------------------------
    def CalculateTelegramLengthPlcToRob(self, AxesGroup : AxesGroup) -> int :
        
        _cyclicDataLength = self.CalculateCyclicDataLength(AxesGroup = AxesGroup, Direction = ComDirection.PLC_TO_ROB) 

        #return value of function
        CalculateTelegramLengthPlcToRob : int = 0 

        if ( self._parCfg.Com.TwoSequences ):
        
            CalculateTelegramLengthPlcToRob = ( _cyclicDataLength
                                                + self.Telegram.PlcToRob.Sequence[  PRIMARY_SEQUENCE].Header.sizeof()
                                                + self.Telegram.PlcToRob.Sequence[  PRIMARY_SEQUENCE].Header.PayloadLength.value
                                                + self.Telegram.PlcToRob.Sequence[SECONDARY_SEQUENCE].Header.sizeof()
                                                + self.Telegram.PlcToRob.Sequence[SECONDARY_SEQUENCE].Header.PayloadLength.value
                                                + self.Telegram.PlcToRob.Footer.sizeof()
                                            )   
        else:
            CalculateTelegramLengthPlcToRob = ( _cyclicDataLength
                                                + self.Telegram.PlcToRob.Sequence[PRIMARY_SEQUENCE].Header.sizeof()
                                                + self.Telegram.PlcToRob.Sequence[PRIMARY_SEQUENCE].Header.PayloadLength.value
                                                + self.Telegram.PlcToRob.Footer.sizeof()
                                            )


        return CalculateTelegramLengthPlcToRob


    #------------------------------------------------------------
    # Calculate length of cyclic data
    #------------------------------------------------------------
    def CalculateCyclicDataLength(self, AxesGroup : AxesGroup, Direction : ComDirection) -> int :
        
        #return value of function
        CalculateCyclicDataLength : int = 0
        
        # Size of the header
        ROB_TO_PLC_HEADER_SIZE : int = 10

        
        # ------------------------------------
        # PLC -> ROB
        # ------------------------------------
        if (Direction == ComDirection.PLC_TO_ROB) :
        
            # Add Header size 
            CalculateCyclicDataLength += self.Telegram.PlcToRob.Header.sizeof()
            # Add Cyclic size 
            CalculateCyclicDataLength += self.Telegram.PlcToRob.Cyclic.sizeof()
        
            # Check SubProgramData active ? 
            if ( AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active ) :
                # Add SubProgramData size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.SubProgramData.sizeof()
                
            # Check CartesianPosition active ? 
            if ( AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Active ) :
                # Add CartesianPosition size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.sizeof()
            
            # Check JointPosition active ? 
            if ( AxesGroup.CyclicOptional.PlcToRob.JointPosition.Active ) :
                # Add JointPosition size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.JointPosition.sizeof()
                
            # Check Force active ? 
            if ( AxesGroup.CyclicOptional.PlcToRob.Force.Active ) :
                # Add Force size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.Force.sizeof()
                
            # Check CartesianPositionExt acive ? 
            if ( AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active ) :
                # Add CartesianPositionExt size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.sizeof()

            # Check JointPositionExt active ?
            if ( AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.Active ) :
                # Add JointPositionExt size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.sizeof()
                    
            # Check ForceExt active ?
            if ( AxesGroup.CyclicOptional.PlcToRob.ForceExt.Active ) :
                # Add ForceExt size 
                CalculateCyclicDataLength += self.Telegram.PlcToRob.CyclicOptional.ForceExt.sizeof()
                
                
        # ------------------------------------
        # ROB -> PLC
        # ------------------------------------
        if (Direction == ComDirection.ROB_TO_PLC) :
            # Add Header size 
            CalculateCyclicDataLength += CalculateCyclicDataLength + ROB_TO_PLC_HEADER_SIZE
            # ToDo: Used a constant because SizeOf(Telegram.RobToPlc.Header) return a wrong value,  because of VersionStruct instead of Byte
            
            # Check SubProgramData active ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Active ) :
                # Add SubProgramData size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.SubProgramData.sizeof()

            # Check CartesianPosition active ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active ) :
                # Add CartesianPosition size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.sizeof()

            # Check JointPosition active ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active ) :
                # Add JointPosition size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.JointPosition.sizeof()

            # Check Force active ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.Force.Active ) :
                # Add Force size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.Force.sizeof()

            # Check Current acive ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.Current.Active ) :
                # Add Current size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.Current.sizeof()

            # Check CartesianPositionExt acive ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active ) :
                # Add CartesianPositionExt size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.sizeof()

            # Check JointPositionExt active ?
            if ( AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active ) :
                # Add JointPositionExt size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.sizeof()

            # Check ForceExt active ?
            if ( AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active ) :
                # Add ForceExt size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.ForceExt.sizeof()

            # Check CurrentExt active ? 
            if ( AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active ) :
                # Add CurrentExt size 
                CalculateCyclicDataLength += self.Telegram.RobToPlc.CyclicOptional.CurrentExt.sizeof()

        return CalculateCyclicDataLength


    #------------------------------------------------------------
    # Calculate maximum payload size 
    #------------------------------------------------------------
    def CalculateSequencePayloadMax(self, AxesGroup : AxesGroup, Direction : ComDirection, Sequence : SequenceFlag) -> int :
        
        # return value of function
        CalculateSequencePayloadMax : int = 0
        
        
        # calculate cyclic header length
        _cyclicDataLength = self.CalculateCyclicDataLength(AxesGroup = AxesGroup, Direction = Direction)


        match (Sequence) :

            case SequenceFlag.PRIMARY_SEQUENCE   : 

                if (Direction == ComDirection.PLC_TO_ROB) : 

                    # calculate sequence payload length
                    CalculateSequencePayloadMax = ( self._parCfg.Com.TelegramLengthPlcToRob - _cyclicDataLength )

                if (Direction == ComDirection.ROB_TO_PLC) :
                
                    # calculate sequence payload length
                    CalculateSequencePayloadMax = ( self._parCfg.Com.TelegramLengthRobToPlc - _cyclicDataLength )


            case SequenceFlag.SECONDARY_SEQUENCE :
            
                if (Direction == ComDirection.PLC_TO_ROB) :
                
                    # calculate sequence payload length
                    CalculateSequencePayloadMax = int (( self._parCfg.Com.TelegramLengthPlcToRob - _cyclicDataLength ) / 2 )


                if (Direction == ComDirection.ROB_TO_PLC) :
                
                    # calculate sequence payload length
                    CalculateSequencePayloadMax = int (( self._parCfg.Com.TelegramLengthRobToPlc - _cyclicDataLength ) / 2 )
                
        return CalculateSequencePayloadMax


    #------------------------------------------------------------
    # Calculate start address of sequence payload
    #------------------------------------------------------------
    def CalculateSequencePayloadStartAdr(self, AxesGroup : AxesGroup, Direction : ComDirection, Sequence : SequenceFlag) -> int :
        
        # return value of function
        CalculateSequencePayloadStartAdr : int = 0
        
        
        # calculate cyclic header length
        _cyclicDataLength = self.CalculateCyclicDataLength(AxesGroup = AxesGroup, Direction = Direction)

        match Sequence :


            case SequenceFlag.PRIMARY_SEQUENCE : 

                # return start address
                CalculateSequencePayloadStartAdr = _cyclicDataLength


            case SequenceFlag.SECONDARY_SEQUENCE :

                # calculate sequence payload max
                _sequencePayloadLength = self.CalculateSequencePayloadMax( AxesGroup = AxesGroup, 
                                                                           Direction = Direction, 
                                                                           Sequence  = Sequence )

                # return start address
                CalculateSequencePayloadStartAdr = _cyclicDataLength + _sequencePayloadLength



        return CalculateSequencePayloadStartAdr
    
    
    #------------------------------------------------------------
    # Check if parameter changed
    #------------------------------------------------------------
    def CheckParameterChanged(self, AxesGroup : AxesGroup) -> bool :    
        
        # internal index for loops
        _idx : int = 0

        # Check initialization is already done ?
        if ( not self.Initialized ) :

            CheckParameterChanged = False
            return CheckParameterChanged

        # compare memory 
        CheckParameterChanged = ( self.ParCfg != self._parCfg)

        for _idx in range( SyncTime.DURING_START_UP, SyncTime.AFTER_START_UP) :

            # Check Tool SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.Tool[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[_idx] ) :

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage(
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.Tool[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.Tool[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.Tool[_idx].toString()
                )


            # Check Frame SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.Frame[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[_idx] ):

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite =  True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.Frame[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.Frame[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.Frame[_idx].toString()
                )


            # Check Load SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.Load[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Load[_idx] ):

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.Load[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.Load[_idx].toString() ,
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.Load[_idx].toString()
                )   


            # Check WorkAreas SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx] ):

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_WORK_AREA_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.WorkAreas[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx].toString()
                )   


            # Check SWLimits SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.SwLimits[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[_idx] ) :

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.SwLimits[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.SwLimits[_idx].toString()
                )


            # Check DefaultDynamics SyncMode changed ? 
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx] ) :

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.DefaultDynamics[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx].toString()
                )


            # Check ReferenceDynamics SyncMode changed ?
            if ( self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx] ) :

                # Set info
                self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite = True)

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.INFO,
                    MessageCode = 0,
                    MessageText = 'SyncMode.ReferenceDynamics[{1}] changed from {2} to {3}, but this is only allowed at PLC start',
                    Para1       = INT_TO_STRING(_idx),
                    Para2       = self. ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx].toString(),
                    Para3       = self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx].toString()
                )


        # Check Plc.OptionalCyclic changed ? 
        if ( PlcOptionalCyclicToUint(self._parCfg.Plc.OptionalCyclic) != PlcOptionalCyclicToUint(self.ParCfg.Plc.OptionalCyclic )) :

            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT, Overwrite = True )

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = 0,
                MessageText = 'ParCfg.Plc.OptionalCyclic changed after initialization from {1} to {2} -> Reinitialize by disabling and enabling the RobotTask',
                Para1       = WORD_TO_STRING_BIN(PlcOptionalCyclicToUint(self._parCfg.Plc.OptionalCyclic)),
                Para2       = WORD_TO_STRING_BIN(PlcOptionalCyclicToUint(self. ParCfg.Plc.OptionalCyclic))
            )


        # Check Rob.OptionalCyclic changed ? 
        if ( RobOptionalCyclicToUint(self._parCfg.Rob.OptionalCyclic) != RobOptionalCyclicToUint(self.ParCfg.Rob.OptionalCyclic )) :

            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT, Overwrite = True )

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = 0,
                MessageText = 'ParCfg.Rob.OptionalCyclic changed after initialization from {1} to {2} -> Reinitialize by disabling and enabling the RobotTask',
                Para1       = WORD_TO_STRING_BIN(RobOptionalCyclicToUint(self._parCfg.Rob.OptionalCyclic)),
                Para2       = WORD_TO_STRING_BIN(RobOptionalCyclicToUint(self. ParCfg.Rob.OptionalCyclic))
            )


        return CheckParameterChanged


    def CheckParameterValid(self, AxesGroup : AxesGroup) -> bool :    
        
        # return value of function
        CheckParameterValid : bool = True


        # Check ParCfg.Com.TelegramLengthPlcToRob
        if ( self.ParCfg.Com.TelegramLengthPlcToRob < 128 ) : 
        
            # Set Warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_PLC_TO_ROB_VERY_SMALL, Overwrite = True )

        # Check ParCfg.Com.TelegramLengthRobToPlc
        if ( self.ParCfg.Com.TelegramLengthRobToPlc < 128 ) :

            # Set Warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_ROB_TO_PLC_VERY_SMALL, Overwrite = True )


        # region ParCfg.Com

        # Check LifeSignTimeout
        if ( self.ParCfg.Com.LifeSignTimeOut < 10 ) : # ms

            # set to valid min value
            self.ParCfg.Com.LifeSignTimeOut = 10

            # Set info
            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'LifeSignTimeout to small and set from {1}ms to 10ms',
                Para1       = str(self.ParCfg.Com.LifeSignTimeOut)
            )                          


        # Check ParCfg.Com.TelegramLengthPlcToRob
        if (( self.ParCfg.Com.TelegramLengthPlcToRob < 64                       ) or
            ( self.ParCfg.Com.TelegramLengthPlcToRob > self.ROBOT_OUT_DATA_SIZE )) : 

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =         'ParCfg.Com.TelegramLengthPlcToRob {1} invalid',
                Para1       = str(self.ParCfg.Com.TelegramLengthPlcToRob)
            )
            # no further validation                          
            return CheckParameterValid

        # Check ParCfg.Com.TelegramLengthRobToPlc
        if (( self.ParCfg.Com.TelegramLengthRobToPlc < 64                      ) or
            ( self.ParCfg.Com.TelegramLengthRobToPlc > self.ROBOT_IN_DATA_SIZE )) :
        
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =         'ParCfg.Com.TelegramLengthRobToPlc {1} invalid',
                Para1       = str(self.ParCfg.Com.TelegramLengthRobToPlc)
            )
            # no further validation                          
            return CheckParameterValid

        #endregion

        # Region ParCfg.Rob.OptionalCyclic

        # Check configuration if optional cyclic CartesianPosition valid ?
        if ( self.ParCfg.Rob.OptionalCyclic.UseCartesianPosition and self.ParCfg.Rob.OptionalCyclic.UseCartesianPositionExt ) :

            # set to valid configuration
            self.ParCfg.Rob.OptionalCyclic.UseCartesianPosition.value   = True
            self.ParCfg.Rob.OptionalCyclic.UseCartesianPositionExt.value = False
            
            # Set info
            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_RECV_EXT_CART_POS_NOT_USABLE_WITH_RECV_CART_POS, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'UseCartesianPosition and UseCartesianPositionExt cannot be configured together -> UseCartesianPosition is automatically activated'
            )


        # Check configuration if optional cyclic JointPosition valid ?
        if ( self.ParCfg.Rob.OptionalCyclic.UseJointPosition.value and self.ParCfg.Rob.OptionalCyclic.UseJointPositionExt.value ) and False : #ToDo: Yaskawa need this combination for debugging via JointPosExt

            # set to valid configuration
            self.ParCfg.Rob.OptionalCyclic.UseJointPosition.value    = True
            self.ParCfg.Rob.OptionalCyclic.UseJointPositionExt.value = False

            # Set info
            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_RECV_EXT_JOINT_POS_NOT_USABLE_WITH_RECV_JOINT_POS, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'UseJointPosition and UseJointPositionExt cannot be configured together -> UseJointPosition is automatically activated'
            )

        #endRegion


        # region ParCfg.Parameter.SynchronizationModes

        # Check ToolData synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )) : # Automatic is not allowed during startup
        
            # parameter(s) not valid
            CheckParameterValid = False
            
            #/ Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID             , Overwrite = True ) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_DATA_SYNC_MODE_INVALID, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid


        # Check ToolData synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )) :

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID             , Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_DATA_SYNC_MODE_INVALID, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString()
            )

            # no further validation
            return CheckParameterValid


        # Check FrameData synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )) : # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID              , Overwrite = True)# own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_DATA_SYNC_MODE_INVALID, Overwrite = False)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid                                                   


        # Check FrameData synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )) :

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID              , Overwrite = True)# own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_DATA_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid


        # Check LoadData synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )) : # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError   ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID             , Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_DATA_SYNC_MODE_INVALID, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid                          


        # Check LoadData synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )):

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError   ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID             , Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_DATA_SYNC_MODE_INVALID, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString()
            )
            # no further validation
            return CheckParameterValid


        # Check WorkAreas synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )) : # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False
        
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,              Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP].toString()
            )
            
            # no further validation                          
            return CheckParameterValid                          


        # Check WorkAreas synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )) :

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,              Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString()
            )

            # no further validation                          
            return CheckParameterValid


        # Check SWLimits synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )): # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,              Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid                          


        # Check SWLimits synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )) : 

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,              Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString()
            )
            # no further validation                          
            return CheckParameterValid                          


        # Check DefaultDynamics synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC          )): # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,                     Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP].toString()
            )
            
            # no further validation                          
            return CheckParameterValid                          


        # Check DefaultDynamics synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )) : 

            # parameter(s) not valid
            CheckParameterValid = False
            
            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,                     Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID, Overwrite = True)
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString()
            )

            # no further validation                          
            return CheckParameterValid                         


        # Check ReferenceDynamics synchronisation mode during startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP].value <  SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP].value >= SyncMode.AUTOMATIC          )): # Automatic is not allowed during startup

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,                       Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID, Overwrite = True)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] invalid SyncMode {1}',
                Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP].toString()
            )

            # no further validation                          
            return CheckParameterValid                        


        # Check ReferenceDynamics synchronisation mode after startup
        if (( self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].value < SyncMode.NO_SYNCHRONIZATION ) or
            ( self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].value > SyncMode.AUTOMATIC          )):

            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError  ( ErrorID   = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID,                       Overwrite = True) # own defined error - not in specification
            # Set warning
            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID, Overwrite = True)

        # Create log entry
        self.CreateLogMessage( 
            Timestamp   = self.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.INFO,
            MessageCode = 0,
            MessageText =     'ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] invalid SyncMode {1}',
            Para1       = self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString()
        )

        # no further validation                          
        return CheckParameterValid

        # endRegion



        return CheckParameterValid


    def CreateSendPayload(self, AxesGroup    : AxesGroup,
                                RobotOutData : bytearray) -> int:
        """Create the send payload based on the current state of the RobotTask."""

        # Call SendData FB, update payload and size 
        self.SendData( Payload = RobotOutData, PayLoadSize = UDINT(self.ROBOT_OUT_DATA_SIZE))
        # reset all variables and payload
        self.SendData.Reset()

        self.CreateSendPayloadHeader        ( AxesGroup = AxesGroup )
        self.CreateSendPayloadCyclic        ( AxesGroup = AxesGroup )
        self.CreateSendPayloadCyclicOptional( AxesGroup = AxesGroup )
        self.CreateSendPayloadSequence      ( AxesGroup = AxesGroup )
        self.CreateSendPayloadFooter        ( AxesGroup = AxesGroup )
        self.CreateSendPayloadLogging       ( AxesGroup = AxesGroup )

        # reset NewSEQ flag
        AxesGroup.State.NewSEQ[0] = False  # warning 'Test'

        return OK

    #------------------------------------------------------------
    # CreateSendPayloadHeader - create send payload header
    #------------------------------------------------------------
    def CreateSendPayloadHeader(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload header."""
        
        self.SendData.AddByte(self.Telegram.PlcToRob.Header.SRCIVersion           )
        self.SendData.AddByte(self.Telegram.PlcToRob.Header.FastStop_LifeSign     ) 
        self.SendData.AddUint(self.Telegram.PlcToRob.Header.TelegramLengthPlcToRob)
        self.SendData.AddUint(self.Telegram.PlcToRob.Header.TelegramLengthRobToPlc)
        self.SendData.AddByte(self.Telegram.PlcToRob.Header.AxesGroupID_Control   )
        self.SendData.AddByte(self.Telegram.PlcToRob.Header.Reserved              )
        self.SendData.AddUint(self.Telegram.PlcToRob.Header.TelegramNumberPlcToRob)
        self.SendData.AddUint(self.Telegram.PlcToRob.Header.TelegramNumberRobToPlc)
        self.SendData.AddUint(self.Telegram.PlcToRob.Header.ClientDate            ) 
        self.SendData.AddTime(self.Telegram.PlcToRob.Header.ClientTime            )  
        
        return OK


    #------------------------------------------------------------
    # CreateSendPayloadCyclic - create send payload cyclic data
    #------------------------------------------------------------
    def CreateSendPayloadCyclic(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload cyclic data."""
        
        self.SendData.AddByte(self.Telegram.PlcToRob.Cyclic.ToolNo)
        self.SendData.AddByte(self.Telegram.PlcToRob.Cyclic.FrameNo)
        
        return OK


    #------------------------------------------------------------
    # CreateSendPayloadCyclicOptional - create send payload optional cyclic data
    #------------------------------------------------------------
    def CreateSendPayloadCyclicOptional(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload optional cyclic data."""

        #region local variables

        # temporary byte
        _tmpByte   : BYTE = BYTE(0)
        
        #endregion


        # Telegram.PlcToRob.CyclicOptional.SubProgramData
        if ( AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active ) : 

            self.SendData.AddDataBlock( pValue=     self.Telegram.PlcToRob.CyclicOptional.SubProgramData.Data , 
                                          Size= len(self.Telegram.PlcToRob.CyclicOptional.SubProgramData.Data))

            
        # Telegram.PlcToRob.CyclicOptional.CartesianPos
        if ( AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Active.value) :

            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.X )
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Y )
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Z )
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rx)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Ry)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rz)

            _tmpByte = BYTE(0)
            _tmpByte.Bit[0] = self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.Bit[0]
            _tmpByte.Bit[1] = self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.Bit[1]
            _tmpByte.Bit[2] = self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.Bit[2]
            
            self.SendData.AddByte(_tmpByte)
                    
            self.SendData.AddByte (self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J2_J1 )
            self.SendData.AddByte (self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J4_J3 )
            self.SendData.AddByte (self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J6_J5 )
            self.SendData.AddByte (self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_E1    )
            self.SendData.AddReal (self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.E1          )


        # Telegram.PlcToRob.CyclicOptional.JointPosition
        if ( AxesGroup.CyclicOptional.PlcToRob.JointPosition.Active.value) :

            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J1)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J2)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J3)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J4)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J5)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.J6)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPosition.E1)


        # Telegram.PlcToRob.CyclicOptional.Force
        if ( AxesGroup.CyclicOptional.PlcToRob.Force.Active.value) :
        
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.X)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.Y)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.Z)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.Rx)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.Ry)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.Force.Rz)


        # Telegram.PlcToRob.CyclicOptional.TwoSequences {{{
        # }}}

        # AxesGroup.OptionalCyclic.PlcToRob.CartesianPosExt
        if ( AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active) :
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E2)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E3)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E4)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E5)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E6)


        # AxesGroup.OptionalCyclic.PlcToRob.JointPositionExt
        if ( AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.Active) :
            
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E2)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E3)  
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E4)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E5)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E6)


        # Telegram.PlcToRob.CyclicOptional..CartesianForceExt
        if ( AxesGroup.CyclicOptional.PlcToRob.ForceExt.Active) :

            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E1)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E2)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E3)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E4)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E5)
            self.SendData.AddReal(self.Telegram.PlcToRob.CyclicOptional.ForceExt.E6)


        return OK


    #------------------------------------------------------------
    # CreateSendPayloadSequence - create send payload sequence data
    #------------------------------------------------------------
    def CreateSendPayloadSequence(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload sequence data."""

        #region local variables
        
        # internal sequence index
        _seqIdx  : int = 0
        # internal fragment index
        _fragIdx : int = 0 

        #endregion



        for _seqIdx in range( 0, AxesGroup.State.SequenceCountSend ) :

            # Check 2nd sequence ? -> goto 2nd sequence payload address  
            if ( _seqIdx == SECONDARY_SEQUENCE ) :

                self.SendData.PayloadPtr.value = self.CalculateSequencePayloadStartAdr(AxesGroup = AxesGroup, 
                                                                                       Direction = ComDirection.PLC_TO_ROB,
                                                                                       Sequence  = SequenceFlag.SECONDARY_SEQUENCE)


            # Telegram.PlcToRob.Sequence[x].Header
            self.SendData.AddUint(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK)
            self.SendData.AddUint(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength)
            

            # check limit reachted ?
            if ( self.SendData.PayloadPtr.value + self.FOOTER_SIZE >= self.Telegram.PlcToRob.Header.TelegramLengthPlcToRob.value) :

                break


            # PlcToRob.Sequence[x].Fragment[x] {{{
            for _fragIdx in range( 0,  AxesGroup.State.FragmentCountSend[_seqIdx]  ) : 


                if (self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > 0) :
                    
                    # PlcToRob.Sequence[x].Fragment[x].Header
                    self.SendData.AddUint(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID)
                    self.SendData.AddByte(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.Reserve)
                    self.SendData.AddByte(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction)
                    self.SendData.AddUint(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer)
                    self.SendData.AddUint(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength)

                    # PlcToRob.Sequence[x].Fragment[x].Command

                    # Hint: the command header is part of the fragment payload  
                    if ( self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > 0 ) : 


                        Ptr : int = self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer.value

                        self.SendData.AddDataBlock( pValue =  self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[Ptr:],
                                                    Size   =  self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value)


        return OK


    #------------------------------------------------------------
    # CreateSendPayloadFooter - create send payload footer
    #------------------------------------------------------------
    def CreateSendPayloadFooter(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload footer."""

        self.SendData.SetLifeSignFooter( LifeSign =  AxesGroup.Cyclic.PlcToRob.LifeSign)

        return OK


    #------------------------------------------------------------
    # CreateSendPayloadLogging - create send payload logging data
    #------------------------------------------------------------
    def CreateSendPayloadLogging(self, AxesGroup : AxesGroup) -> int:
        """Create the send payload logging data."""

        if  ((( self.Telegram.PlcToRob.Sequence[PRIMARY_SEQUENCE  ].Header.PayloadLength.value > 0 ) and (AxesGroup.State.NewSEQ[PRIMARY_SEQUENCE  ] )) or
             (( self.Telegram.PlcToRob.Sequence[SECONDARY_SEQUENCE].Header.PayloadLength.value > 0 ) and (AxesGroup.State.NewSEQ[SECONDARY_SEQUENCE] ))) :

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'SendData: Bytes send in total: {1}',
                Para1       =  INT_TO_STRING(self.SendData.PayloadLen.value)
            )

        return OK

    #------------------------------------------------------------
    # HandleAliveBit - handle the alive bit
    #------------------------------------------------------------
    def HandleAliveBit(self, LifeSign : int) :
        """Handle the alive bit in the LifeSign byte."""

        if (self._first and LifeSign > 0) : 
        
            # init alive value
            self._aliveValue = LifeSign
            # reset first flag
            self._first = False


        self._aliveCheck ( IN  = (self._aliveValue == LifeSign) , PT = TIME(self.ParCfg.Com.LifeSignTimeOut + self.ParCfg.Plc.CycleTime))
        self._alive_R    ( CLK = self._aliveBit)
        self._alive_F    ( CLK = self._aliveBit)

        # check life sign has changed
        if ( self._aliveValue != LifeSign) : 

            self._aliveValue = LifeSign
            self._aliveBit   = True

        # check alive timeout
        if (self._aliveCheck.Q):

            self._aliveBit = False


        # log alive bit rising edge
        if (self._alive_R.Q):
        
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'Data Exchange is running (Alive-Bit)'
            )


        # log alive bit falling edge
        if (self._alive_F.Q):
        
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'Data Exchange has stopped (Alive-Bit)'
            )


    #------------------------------------------------------------
    # HandleAxesGroup - handle axes group 
    #------------------------------------------------------------
    def HandleAxesGroup(self,
                        AxesGroup         : AxesGroup,
                        ToolData          : list[Tool],
                        FrameData         : list[Frame],
                        LoadData          : list[Load],
                        WorkAreas         : list[RobotWorkArea],
                        SWLimits          : SWLimits,
                        DefaultDynamics   : DefaultDynamics,
                        ReferenceDynamics : ReferenceDynamics    ) -> None:
        """Handle the axes group specific tasks."""

        self.HandleAxesGroupAcyclic       ( AxesGroup         = AxesGroup )
        self.HandleAxesGroupCyclic        ( AxesGroup         = AxesGroup )
        self.HandleAxesGroupCyclicOptional( AxesGroup         = AxesGroup )
        self.HandleAxesGroupMessageLog    ( AxesGroup         = AxesGroup )
        self.HandleAxesGroupParameter     ( AxesGroup         = AxesGroup )
        self.HandleAxesGroupState         ( AxesGroup         = AxesGroup )
        self.HandleAxesGroupSystemData    ( AxesGroup         = AxesGroup, 
                                            ToolData          = ToolData, 
                                            FrameData         = FrameData, 
                                            LoadData          = LoadData, 
                                            WorkAreas         = WorkAreas, 
                                            SWLimits          = SWLimits, 
                                            DefaultDynamics   = DefaultDynamics, 
                                            ReferenceDynamics = ReferenceDynamics)


    #------------------------------------------------------------
    # HandleAxesGroupAcyclic - handle axes group acyclic data
    #------------------------------------------------------------
    def HandleAxesGroupAcyclic(self, AxesGroup : AxesGroup) -> None:
        """Handle the axes group acyclic data."""

        # Call active command register FB
        AxesGroup.Acyclic.ActiveCommandRegister(SystemTime     = self.SystemTime,
                                                RegisterSize   = min( ACTIVE_CMD_REGISTER_ENTRIES_MAX, AxesGroup.Parameter.Rob.Parameter.LengthACR),
                                                InternalLogger = AxesGroup.MessageLog, 
                                                ExternalLogger = AxesGroup.MessageLog.ExternalLogger,
                                                LogLevel       = AxesGroup.MessageLog.LogLevel)

    #------------------------------------------------------------
    # HandleAxesGroupCyclic - handle axes group cyclic data
    #------------------------------------------------------------
    def HandleAxesGroupCyclic(self, AxesGroup : AxesGroup) -> None:
        """Handle the axes group cyclic data."""

        # set instance AxesGroupID
        AxesGroup.Cyclic.PlcToRob.AxesGroupID.value = self.AxesGroupID
        # Set Version
        AxesGroup.Cyclic.PlcToRob.SRCIVersion = SRCIVersion

        AxesGroup.Cyclic.PlcToRob.TelegramLengthPlcToRob.value = self._parCfg.Com.TelegramLengthPlcToRob
        AxesGroup.Cyclic.PlcToRob.TelegramLengthRobToPlc.value = self._parCfg.Com.TelegramLengthRobToPlc

        AxesGroup.Cyclic.PlcToRob.TelegramNumberPlcToRob = PlcOptionalCyclicToUint(AxesGroup.Parameter.Plc.OptionalCyclic)
        AxesGroup.Cyclic.PlcToRob.TelegramNumberRobToPlc = RobOptionalCyclicToUint(AxesGroup.Parameter.Rob.OptionalCyclic)

        # Set Date + Time
        AxesGroup.Cyclic.PlcToRob.ClientDate = DATE_TO_IEC_DATE(self.SystemTime.SystemDate)
        AxesGroup.Cyclic.PlcToRob.ClientTime = TIME_TO_IEC_TIME(self.SystemTime.SystemTime)


    #------------------------------------------------------------
    # HandleAxesGroupCyclicOptional - handle axes group cyclic optional data
    #------------------------------------------------------------
    def HandleAxesGroupCyclicOptional(self, AxesGroup : AxesGroup) -> None:
        """Handle the axes group cyclic optional data."""

        # PlcToRob
        AxesGroup.CyclicOptional.PlcToRob.SubProgramData      .Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCallSubprogram
        AxesGroup.CyclicOptional.PlcToRob.CartesianPosition   .Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCartesianPosition
        AxesGroup.CyclicOptional.PlcToRob.JointPosition       .Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseJointPosition
        AxesGroup.CyclicOptional.PlcToRob.Force               .Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseForce
        AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCartesianPositionExt
        AxesGroup.CyclicOptional.PlcToRob.JointPositionExt    .Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseJointPositionExt


        # RobToPlc
        AxesGroup.CyclicOptional.RobToPlc.SubProgramData      .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCallSubprogram
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition   .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCartesianPosition
        AxesGroup.CyclicOptional.RobToPlc.JointPosition       .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseJointPosition
        AxesGroup.CyclicOptional.RobToPlc.Force               .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseForce
        AxesGroup.CyclicOptional.RobToPlc.Current             .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCurrent
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCartesianPositionExt
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt    .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseJointPositionExt
        AxesGroup.CyclicOptional.RobToPlc.ForceExt            .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseForceExt    
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt          .Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCurrentExt


    #------------------------------------------------------------
    # HandleAxesGroupMessageLog - handle axes group message log
    #------------------------------------------------------------
    def HandleAxesGroupMessageLog(self, AxesGroup : AxesGroup) -> None:

        # Set External logger 
        AxesGroup.MessageLog.ExternalLogger = self.ExternalLogger
        AxesGroup.MessageLog.LogLevel       = self.LogLevel


        if (AxesGroup.State.GroupReset_R.Q) : 

            AxesGroup.MessageLog.DeleteMessages()
            AxesGroup.MessageLog.DeleteSystemLogs()


    #------------------------------------------------------------
    # HandleAxesGroupParameter - handle axes group parameter data
    #------------------------------------------------------------
    def HandleAxesGroupParameter(self, AxesGroup : AxesGroup) -> None:
        """Handle the axes group parameter data."""
        
        if (self._exchangeConfiguration.Enabled) : 

            AxesGroup.Parameter.Plc.Parameter                           = self._parCfg.Plc.Parameter
            AxesGroup.Parameter.Plc.OptionalCyclic                      = self._parCfg.Plc.OptionalCyclic
            AxesGroup.Parameter.Rob.OptionalCyclic                      = self._parCfg.Rob.OptionalCyclic
            
            AxesGroup.Parameter.Rob.Parameter.LengthACR                 = self._exchangeConfiguration.OutCmd.LengthACR
            AxesGroup.Parameter.Rob.Parameter.HighestToolIndex          = self._exchangeConfiguration.OutCmd.HighestToolIndex
            AxesGroup.Parameter.Rob.Parameter.HighestFrameIndex         = self._exchangeConfiguration.OutCmd.HighestFrameIndex
            AxesGroup.Parameter.Rob.Parameter.HighestLoadIndex          = self._exchangeConfiguration.OutCmd.HighestLoadIndex
            AxesGroup.Parameter.Rob.Parameter.HighestWorkAreaIndex      = self._exchangeConfiguration.OutCmd.HighestWorkAreaIndex
            AxesGroup.Parameter.Rob.Parameter.DataInSync                = self._exchangeConfiguration.OutCmd.DataInSync
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexTool           = self._exchangeConfiguration.OutCmd.ChangeIndexTool
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexFrame          = self._exchangeConfiguration.OutCmd.ChangeIndexFrame
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexLoad           = self._exchangeConfiguration.OutCmd.ChangeIndexLoad
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexWorkArea       = self._exchangeConfiguration.OutCmd.ChangeIndexWorkArea
            AxesGroup.Parameter.Rob.Parameter.RAWorkingHours            = self._exchangeConfiguration.OutCmd.RAWorkingHours
            AxesGroup.Parameter.Rob.Parameter.BrakeTestRequired         = self._exchangeConfiguration.OutCmd.BrakeTestRequired
            AxesGroup.Parameter.Rob.Parameter.StepModeExactStopActive   = self._exchangeConfiguration.OutCmd.StepModeExactStopActive
            AxesGroup.Parameter.Rob.Parameter.StepModeBlendingActive    = self._exchangeConfiguration.OutCmd.StepModeBlendingActive
            AxesGroup.Parameter.Rob.Parameter.PathAccuracyMode          = self._exchangeConfiguration.OutCmd.PathAccuracyMode
            AxesGroup.Parameter.Rob.Parameter.AvoidSingularity          = self._exchangeConfiguration.OutCmd.AvoidSingularity
            AxesGroup.Parameter.Rob.Parameter.CollisionDetectionEnabled = self._exchangeConfiguration.OutCmd.CollisionDetectionEnabled
            AxesGroup.Parameter.Rob.Parameter.AcceleratingSupported     = self._exchangeConfiguration.OutCmd.AcceleratingSupported
            AxesGroup.Parameter.Rob.Parameter.DecceleratingSupported    = self._exchangeConfiguration.OutCmd.DecceleratingSupported
            AxesGroup.Parameter.Rob.Parameter.ConstantVelocitySupported = self._exchangeConfiguration.OutCmd.ConstantVelocitySupported
            AxesGroup.Parameter.Rob.Parameter.RCWorkingHours            = self._exchangeConfiguration.OutCmd.RCWorkingHours
        else:
            AxesGroup.Parameter.Plc.Parameter                           = self.ParCfg.Plc.Parameter
            AxesGroup.Parameter.Plc.OptionalCyclic                      = self.ParCfg.Plc.OptionalCyclic
            AxesGroup.Parameter.Rob.OptionalCyclic                      = self.ParCfg.Rob.OptionalCyclic

    #------------------------------------------------------------
    # HandleAxesGroupState - handle axes group state data
    #------------------------------------------------------------
    def HandleAxesGroupState(self, AxesGroup : AxesGroup) -> None:
            
        AxesGroup.State.AliveOk      = self._aliveBit
        AxesGroup.State.Initialized  = self.Initialized  and AxesGroup.State.AliveOk
        AxesGroup.State.Synchronized = self.Synchronized and AxesGroup.State.AliveOk
        AxesGroup.State.CMDsEnabled  = AxesGroup.State.Initialized or AxesGroup.State.Synchronized
                                        
        AxesGroup.State.StatusRobotArm  = AxesGroup.Cyclic.RobToPlc.StatusRobotArm
        AxesGroup.State.ConfigExchanged = self._exchangeConfiguration.Enabled

        AxesGroup.State.UnifiedFrameIndex                    = ( min( min(AxesGroup.SystemData.FrameDataMax, FRAME_MAX     ), self._exchangeConfiguration.OutCmd.HighestFrameIndex   ))
        AxesGroup.State.UnifiedToolIndex                     = ( min( min(AxesGroup.SystemData.ToolDataMax , TOOL_MAX      ), self._exchangeConfiguration.OutCmd.HighestToolIndex    ))
        AxesGroup.State.UnifiedLoadIndex                     = ( min( min(AxesGroup.SystemData.LoadDataMax , LOAD_MAX      ), self._exchangeConfiguration.OutCmd.HighestLoadIndex    ))
        AxesGroup.State.UnifiedWorkAreaIndex                 = ( min( min(AxesGroup.SystemData.WorkAreasMax, WORK_AREAS_MAX), self._exchangeConfiguration.OutCmd.HighestWorkAreaIndex))

        AxesGroup.State.DataEnableSync                       = self._exchangeConfiguration.ParCmd.DataEnableSync
        AxesGroup.State.SyncStateRc.InSync.Frame             = self._exchangeConfiguration.OutCmd.DataInSync.FramesInSync
        AxesGroup.State.SyncStateRc.InSync.Tool              = self._exchangeConfiguration.OutCmd.DataInSync.ToolsInSync
        AxesGroup.State.SyncStateRc.InSync.Load              = self._exchangeConfiguration.OutCmd.DataInSync.LoadsInSync
        AxesGroup.State.SyncStateRc.InSync.WorkArea          = self._exchangeConfiguration.OutCmd.DataInSync.WorkAreasInSync
        AxesGroup.State.SyncStateRc.InSync.SwLimits          = self._exchangeConfiguration.OutCmd.DataInSync.SoftwareLimitsInSync
        AxesGroup.State.SyncStateRc.InSync.DefaultDynamics   = self._exchangeConfiguration.OutCmd.DataInSync.DefaultDynamicsInSync
        AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics = self._exchangeConfiguration.OutCmd.DataInSync.ReferenceDynamicsInSync

        AxesGroup.State.SyncStateRc.UnSyncNo.Frame           = self._exchangeConfiguration.OutCmd.ChangeIndexFrame
        AxesGroup.State.SyncStateRc.UnSyncNo.Tool            = self._exchangeConfiguration.OutCmd.ChangeIndexTool
        AxesGroup.State.SyncStateRc.UnSyncNo.Load            = self._exchangeConfiguration.OutCmd.ChangeIndexLoad
        AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea        = self._exchangeConfiguration.OutCmd.ChangeIndexWorkArea

        # Update internal data
        AxesGroup.State.SystemTime   = self.SystemTime
        AxesGroup.State.OnlineChange = self.OnlineChange
        AxesGroup.State.Initialized  = self.Initialized

        # Create rising and falling edges for Online Change
        AxesGroup.State.OnlineChange_R(CLK = self.OnlineChange)
        AxesGroup.State.OnlineChange_F(CLK = self.OnlineChange)

        # Create rising and falling edges for GroupReset
        AxesGroup.State.GroupReset_R(CLK = AxesGroup.State.GroupReset)
        AxesGroup.State.GroupReset_F(CLK = AxesGroup.State.GroupReset)

        # Copy function block results 
        AxesGroup.State.RobotData         = self._readRobotData.OutCmd
        AxesGroup.State.ConfigurationData = self._exchangeConfiguration.OutCmd


    #------------------------------------------------------------
    # HandleAxesGroupSystemData - handle axes group system data
    #------------------------------------------------------------
    def HandleAxesGroupSystemData(self,
                                  AxesGroup         : AxesGroup, 
                                  ToolData          : list[Tool],
                                  FrameData         : list[Frame],
                                  LoadData          : list[Load],
                                  WorkAreas         : list[RobotWorkArea],
                                  SWLimits          : SWLimits,
                                  DefaultDynamics   : DefaultDynamics,
                                  ReferenceDynamics : ReferenceDynamics    ) -> None:

        # Update ToolData                    
        AxesGroup.SystemData.ToolDataPtr       = ToolData
        AxesGroup.SystemData.ToolDataMin       = 0
        AxesGroup.SystemData.ToolDataMax       = len(ToolData) - 1
        AxesGroup.SystemData.ToolDataCount     = len(ToolData)

        # Update LoadData                    
        AxesGroup.SystemData.LoadDataPtr       = LoadData
        AxesGroup.SystemData.LoadDataMin       = 0
        AxesGroup.SystemData.LoadDataMax       = len(LoadData) - 1
        AxesGroup.SystemData.LoadDataCount     = len(LoadData)

        # Update FrameData       
        AxesGroup.SystemData.FrameDataPtr      = FrameData
        AxesGroup.SystemData.FrameDataMin      = 0
        AxesGroup.SystemData.FrameDataMax      = len(FrameData) - 1
        AxesGroup.SystemData.FrameDataCount    = len(FrameData)

        # Update WorkAreas 
        AxesGroup.SystemData.WorkAreasPtr      = WorkAreas
        AxesGroup.SystemData.WorkAreasMin      = 0
        AxesGroup.SystemData.WorkAreasMax      = len(WorkAreas) - 1
        AxesGroup.SystemData.WorkAreasCount    = len(WorkAreas)

        # Update SoftwareLimits 
        AxesGroup.SystemData.SWLimits          = SWLimits
        # Update DefaultDynamics 
        AxesGroup.SystemData.DefaultDynamics   = DefaultDynamics
        # Update ReferenceDynamics 
        AxesGroup.SystemData.ReferenceDynamics = ReferenceDynamics


    #------------------------------------------------------------
    # HandleInvalidFrames - handle invalid frames
    #------------------------------------------------------------
    def HandleInvalidFrames(self, AxesGroup   : AxesGroup,
                                  RobotInData : bytearray) -> None:
        """Handle invalid frames in the axes group."""
        
        # Value of lifesign in header
        _lifeSignHeader    : int = 0 
        # Value of lifesign in footer
        _lifeSignFooter    : int = 0


        if ( AxesGroup.Cyclic.RobToPlc.TelegramState == TelegramState.INITIALIZED ) :
        
            # Get lifesign values
            _lifeSignHeader = GetHalfeByteHi( RobotInData[self.ROBOT_IN_DATA_MIN + 1]).value
            _lifeSignFooter = GetHalfeByteHi( RobotInData[self.ROBOT_IN_DATA_MAX + 0]).value

        # Timer for invalid frame(s) message
        self._invalidFrameCounterCheck_D( IN = True , PT = INVALID_FRAMES_CHECK_TIMEOUT)

        # Check Frame is valid : 
        # ----------------------
        if ( _lifeSignHeader != _lifeSignFooter ) :
        
            AxesGroup.State.InvalidFrames += 1


        # Check timeout for invalid frame message
        if ( self._invalidFrameCounterCheck_D.Q ) : 

            # reset timer
            self._invalidFrameCounterCheck_D( IN = False, PT = INVALID_FRAMES_CHECK_TIMEOUT)

        # compare invalid frame(s) counter
        if ( AxesGroup.State.InvalidFrames != self._lastInvalidFrames) : 

            # store last invalid frame(s) counter value
            self._lastInvalidFrames = AxesGroup.State.InvalidFrames
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.WARNING,
                MessageCode = 0,
                MessageText = 'Detected invalid frames {1} in total',
                Para1       =  str(AxesGroup.State.InvalidFrames)
            )


        # Reset invalid frames counter with rising edge of group reset
        if ( AxesGroup.State.GroupReset_R.Q) : 
        
            AxesGroup.State.InvalidFrames = 0
            self._lastInvalidFrames = 0

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'Reset invalid frames counter by executing GroupReset'
            )


    #------------------------------------------------------------
    # HandleLifeSign - handle the life sign
    #------------------------------------------------------------
    def HandleLifeSign(self, AxesGroup : AxesGroup) -> None:
        """Handle the life sign."""

        if ( self._first ) or ( not self.Enable ) :
        
            # init LifeSign 
            AxesGroup.Cyclic.PlcToRob.LifeSign.value = 0
            # reset first flag
            self._first = False
            # prevent inc LifeSign in the 1st cycle (Code below)
            return

        # Increment LifeSign
        AxesGroup.Cyclic.PlcToRob.LifeSign.value += 1
        
        if ( AxesGroup.Cyclic.PlcToRob.LifeSign.value > 15 ) :
        
            AxesGroup.Cyclic.PlcToRob.LifeSign.value = 1 # 0 is only in the very 1st cycle to indicate the system start in logging


        if ( self.Enable ) and ( self._alive_F.Q ) :
        
            # Reset initialized flag
            self.Initialized = False
            # Reset Synchronized flag
            self.Synchronized = False
            
            # Set error 
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_CONNECTION_LOST, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.FATAL_ERROR,
                MessageCode = 0,
                MessageText = 'LifeSign timeout -> Reinitialization required !'
            )

        # Reset connection lost error
        if ( not self.Enable ) and ( self._aliveBit ) and ( self.ErrorID == RobotLibraryErrorIdEnum.ERR_CONNECTION_LOST ) :

            self.ErrorID = 0


    #------------------------------------------------------------
    # HandleLogMessagesAck - handle the log messages acknowledgment
    #------------------------------------------------------------
    def HandleLogMessagesAck(self, AxesGroup : AxesGroup) -> None:
        """Handle the log messages acknowledgment."""

        if ( self._readMessages.Enabled ) :
        
            # Set Message ID as Acknowlege ID  
            self._readMessages.ParCmd.MsgID = self._readMessages.OutCmd.MsgId
        else:
            
            # Reset Acknowlege ID  
            self._readMessages.ParCmd.MsgID = 0


    #------------------------------------------------------------
    # HandleSeqAck - handle the sequence acknowledgment
    #------------------------------------------------------------
    def HandleSeqAck(self, AxesGroup : AxesGroup) -> None:
        """Handle the sequence acknowledgment."""
        
        #region local variables
        
        # internal index for loops
        _idx : int = 0
        
        #endregion


        for _idx in range(0, AxesGroup.State.SequenceCountSend) :


            AxesGroup.State.CurrentACK[_idx] = self.Telegram.RobToPlc.Sequence[_idx].Header.SEQ_ACK.value

            if (not self.Enable) :
            
                AxesGroup.State.CurrentSEQ[0] = 0
                AxesGroup.State.CurrentSEQ[1] = 0

            # Check Seq/Ack : 
            # ----------------------
            if ( AxesGroup.State.CurrentACK[_idx] == AxesGroup.State.CurrentSEQ[_idx] ) :
            
                AxesGroup.State.CurrentSEQ[_idx] = max(AxesGroup.State.CurrentSEQ[0],AxesGroup.State.CurrentSEQ[1]) +1

                if (AxesGroup.State.CurrentSEQ[_idx] >= 255): # warning 'ToDo: Test for Yaskawa'
                
                    AxesGroup.State.CurrentSEQ[_idx] = 0


                AxesGroup.State.NewSEQ[_idx] = True


    #------------------------------------------------------------
    # HandleSync - handle data synchronisation
    #------------------------------------------------------------
    def HandleSync(self,
                   AxesGroup         : AxesGroup, 
                   ToolData          : list[Tool],
                   FrameData         : list[Frame],
                   LoadData          : list[Load],
                   WorkAreas         : list[RobotWorkArea],
                   SWLimits          : SWLimits,
                   DefaultDynamics   : DefaultDynamics,
                   ReferenceDynamics : ReferenceDynamics ) -> None:


        #region local variables
        
        # flag that indicates at least any iten has enabled synchronisation
        _dataEnableSyncAny        : bool
        # flag that indicates that the frame datas are synchronized or deactivated 
        _inSyncFrameOk            : bool
        # flag that indicates that the tool datas are synchronized or deactivated 
        _inSyncToolOk             : bool
        # flag that indicates that the load datas are synchronized or deactivated 
        _inSyncLoadOk             : bool
        # flag that indicates that the work areas are synchronized or deactivated 
        _inSyncWorkAreaOk         : bool
        # flag that indicates that the SW limits are synchronized or deactivated 
        _inSyncSwLimitsOk         : bool
        # flag that indicates that the default dynamice are synchronized or deactivated 
        _inSyncDefaultDynamicOk   : bool
        # flag that indicates that the reference dynamice are synchronized or deactivated 
        _InSyncReferenceDynamicOk : bool 
        #endregion


        self.HandleSyncToolData              ( AxesGroup = AxesGroup, ToolData          = ToolData         )
        self.HandleSyncFrameData             ( AxesGroup = AxesGroup, FrameData         = FrameData        )
        self.HandleSyncLoadData              ( AxesGroup = AxesGroup, LoadData          = LoadData         )
        self.HandleSyncRobotDefaultDynamics  ( AxesGroup = AxesGroup, DefaultDynamics   = DefaultDynamics  )
        self.HandleSyncRobotReferenceDynamics( AxesGroup = AxesGroup, ReferenceDynamics = ReferenceDynamics)
        self.HandleSyncRobotSWLimits         ( AxesGroup = AxesGroup, SWLimits          = SWLimits         )
        self.HandleSyncToolData              ( AxesGroup = AxesGroup, ToolData          = ToolData         )
        self.HandleSyncWorkArea              ( AxesGroup = AxesGroup, WorkAreas         = WorkAreas        )


        # check any synchronisation activated ?
        _dataEnableSyncAny =         ((     AxesGroup.State.DataEnableSync.EnableSyncFrame             )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncTool              )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncLoad              )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncWorkArea          )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncSWLimits          )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics   )  or
                                      (     AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics ))
                            
        _inSyncFrameOk =            (((     AxesGroup.State.SyncStatePlc     .InSync.Frame             )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.Frame             )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncFrame             ))
                                                                                            
        _inSyncToolOk =             (((     AxesGroup.State.SyncStatePlc     .InSync.Tool              )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.Tool              )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncTool              )) 
                                                                                                
        _inSyncLoadOk =             (((     AxesGroup.State.SyncStatePlc     .InSync.Load              )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.Load              )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncLoad              ))
                                                                                                
        _inSyncWorkAreaOk =         (((     AxesGroup.State.SyncStatePlc     .InSync.WorkArea          )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.WorkArea          )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncWorkArea          ))
                                                                                                
        _inSyncSwLimitsOk =         (((     AxesGroup.State.SyncStatePlc    .InSync.SwLimits           )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.SwLimits          )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncSWLimits          ))
                            
        _inSyncDefaultDynamicOk =   (((     AxesGroup.State.SyncStatePlc     .InSync.DefaultDynamics   )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.DefaultDynamics   )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics   ))
  
        _inSyncReferenceDynamicOk = (((     AxesGroup.State.SyncStatePlc     .InSync.ReferenceDynamics )  and 
                                      (     AxesGroup.State.SyncStateRc      .InSync.ReferenceDynamics )) or
                                      ( not AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics ))


        self.Synchronized = (( _inSyncFrameOk            ) and
                             ( _inSyncToolOk             ) and
                             ( _inSyncLoadOk             ) and
                             ( _inSyncWorkAreaOk         ) and
                             ( _inSyncSwLimitsOk         ) and
                             ( _inSyncDefaultDynamicOk   ) and
                             ( _inSyncReferenceDynamicOk ) and
                             ( _dataEnableSyncAny        ))


        # Update exchange configuration parameter
        self._exchangeConfiguration.ParCmd.DataInSync.FramesInSync            = AxesGroup.State.SyncStatePlc.InSync.Frame
        self._exchangeConfiguration.ParCmd.DataInSync.ToolsInSync             = AxesGroup.State.SyncStatePlc.InSync.Tool
        self._exchangeConfiguration.ParCmd.DataInSync.LoadsInSync             = AxesGroup.State.SyncStatePlc.InSync.Load
        self._exchangeConfiguration.ParCmd.DataInSync.WorkAreasInSync         = AxesGroup.State.SyncStatePlc.InSync.WorkArea
        self._exchangeConfiguration.ParCmd.DataInSync.SoftwareLimitsInSync    = AxesGroup.State.SyncStatePlc.InSync.SwLimits
        self._exchangeConfiguration.ParCmd.DataInSync.DefaultDynamicsInSync   = AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics
        self._exchangeConfiguration.ParCmd.DataInSync.ReferenceDynamicsInSync = AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics


    #------------------------------------------------------------
    # HandleSyncFrameData - handle frame data synchronisation
    #------------------------------------------------------------
    def HandleSyncFrameData(self, AxesGroup : AxesGroup, FrameData : list[Frame]) -> None:
        """Handle frame data synchronisation."""

        #region local variables
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx             : int

        #endregion

        # Set internal references 
        _stepName    =   '_stepSyncFrameData = '
        _rStep       = self._stepSyncFrameData
        _rTimer      = self._timerSyncFrameData
        _rTimeout    = self._timeoutSyncFrameData
        _rSyncIdx    = self._syncIdxFrameData


        match _rStep : 
        
            case 0: 
                
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    return

                # wait for initialisation done
                if ((     AxesGroup.State.RobotData.RCSupportedFunctions. ReadFrameData ) and
                    (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteFrameData ) and
                    (     AxesGroup.State.Initialized                                   ) and 
                    ( not self.Error                                                    )) :

                    # Check PLC frames < RC frames and SyncFrame enabled ?    
                    if (( AxesGroup.State.DataEnableSync.EnableSyncFrame                                            )  and
                        ( AxesGroup.Parameter.Rob.Parameter.HighestFrameIndex > AxesGroup.SystemData.FrameDataCount )) :
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_TOO_SHORT, Overwrite = True)

                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Start initial reading of FrameData from RC',
                        Para1       =  ''
                    )
                    
                    # init frame number
                    _rSyncIdx = AxesGroup.SystemData.FrameDataMin
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1:

                # Start read FrameData
                if (( not self._readFrameData.Busy  ) and 
                    ( not self._readFrameData.Error ) and
                    ( not self._readFrameData.Done  )) :

                    # set command parameter
                    self._readFrameData.ParCmd.FrameNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if ( self._readFrameData.Error ) :
                    
                        self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2:

                # Wait Framedata read
                if (( not self._readFrameData.Busy  ) and
                    ( not self._readFrameData.Error ) and
                    (     self._readFrameData.Done  )):
                    
                    # reset execution
                    self._readFrameData.Execute = False
                    # set available bit
                    self._frameData[_rSyncIdx].Available = True
                    FrameData[_rSyncIdx].Available = True
                    # Copy data
                    self._frameData[_rSyncIdx].Data = copy.deepcopy(self._readFrameData.OutCmd.FrameData)

                    # Check frame data is equal ? 
                    if ( not IsFrameDataEqual( Data1 = self._frameData[_rSyncIdx].Data, Data2 = FrameData[_rSyncIdx].Data, IgnoreTimestamp = True)) :
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Frame = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Frame[_rSyncIdx] = True
                        # inc count of unsynchronised plc frames
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame += 1
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncFrameData: Detected a difference in Frame[{1}] between PLC and RC',
                            Para1       =  str(_rSyncIdx)
                        )

                        # Check synchronisation is enabled ? 
                        if ( not AxesGroup.State.DataEnableSync.EnableSyncFrame ) : 

                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_FRAME_DATA_DISABLED, Overwrite = False)

                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Frame ) :

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_NUMBER_SYNC_ERROR, Overwrite = False)                    

                    # Check all frames read ? 
                    if ( _rSyncIdx < AxesGroup.State.UnifiedFrameIndex ) : 

                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc frame index
                        _rSyncIdx +=1
                        # dec step counter
                        _rStep -=1
                    else:
                        #set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc step counter
                        _rStep += 1

                else:
                    # check error ? 
                    if (self._readFrameData.Error) :

                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)                    
                        # reset available bit
                        FrameData[_rSyncIdx].Available = False
                        self._frameData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3:
                
                # Check synchronisation state ? 
                if (( AxesGroup.State.SyncStatePlc.UnSyncNo.Frame                                            == 0                           ) or 
                    ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Frame = (AxesGroup.State.SyncStatePlc.UnSyncNo.Frame == 0)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )
                    
                else: 
                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Frame ) :
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] :

                            case SyncMode.SERVER_TO_CLIENT : 

                                for _idx in range(AxesGroup.SystemData.FrameDataMin, AxesGroup.SystemData.FrameDataMax) : 

                                    # Overwrite PLC data with RC data
                                    FrameData[_idx] = copy.deepcopy(self._frameData[_idx])

                                # Reset data changed flags
                                AxesGroup.State.DataChanged.Frame = _dataChangedNone.Frame
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Frame = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Frame = True
                                # Reset count of unsynchronised plc frames
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncFrameData: Synchronization of Frames triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                                    Para1       =  str(_rSyncIdx),
                                    Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP].toString(),
                                    Para3       =  SyncTime.DURING_START_UP.toString()
                                )
                                
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncFrameData: Applied the initial read frame data from RC',
                                    Para1       =  '' 
                                )


                            case SyncMode.CLIENT_TO_SERVER :

                                # Check conflicts to solve ? 
                                for _rSyncIdx in range(0, AxesGroup.State.UnifiedFrameIndex):
                            
                                    if ( AxesGroup.State.DataChanged.Frame[_rSyncIdx] ) :
                                    
                                        _found = True
                                        break

                                if ( _found ) :
                                
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Frame = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Frame = True
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = _rStep +1  # -> write PLC data to RC                  
                                    # Create log entry
                                    self.CreateLogMessage( 
                                        Timestamp   = self.SystemTime,
                                        MessageType = MessageType.CMD,
                                        Severity    = Severity.DEBUG,
                                        MessageCode = 0,
                                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                                        Para1       = str(_rSyncIdx),
                                        Para2       = AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP].toString(),
                                        Para3       = SyncTime.DURING_START_UP.toString()
                                    )
                                    
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.Frame = _dataChangedNone.Frame
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Frame = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Frame = True
                                    # Reset count of unsynchronised frames
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )


            case 4:

                # Start write frame data  
                if (( not self._writeFrameData.Busy  ) and 
                    ( not self._writeFrameData.Error )):
                
                    # set command parameter
                    self._writeFrameData.ParCmd.FrameNo   = copy.deepcopy(_rSyncIdx) 
                    self._writeFrameData.ParCmd.FrameData = copy.deepcopy(FrameData[_rSyncIdx].Data)
                    # execute command
                    self._writeFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeFrameData.Error) : 

                        self.ErrorID     = self._writeFrameData.ErrorID
                        self.ErrorAddTxt = self._writeFrameData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5:
                # Wait frame data written ?   
                if (( not self._writeFrameData.Busy  ) and
                    ( not self._writeFrameData.Error ) and
                    (     self._writeFrameData.Done  )):
                
                    # execute command
                    self._writeFrameData.Execute = False
                    # apply frame data to internal frame data
                    self._frameData[_rSyncIdx] = copy.deepcopy(FrameData[_rSyncIdx])
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.Frame[_rSyncIdx] = False
                    # dec count of unsynchronised frames
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame -= 1
                    # set timeout        
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= - 2
                else:
                    # check error ? 
                    if (self._writeFrameData.Error) : 
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           
                    
                    
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------                    
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION) :
                
                    return                

                # reset count of unsynchronised frames
                AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0

                # Check all frame datas
                for _rSyncIdx in range(0, AxesGroup.State.UnifiedFrameIndex):
                
                    # compare frame data
                    AxesGroup.State.DataChanged.Frame[_rSyncIdx] = not IsFrameDataEqual( Data1 = FrameData[_rSyncIdx].Data, Data2 = self._frameData[_rSyncIdx].Data, IgnoreTimestamp = False)

                    # Check Frame data changed ? 
                    if (AxesGroup.State.DataChanged.Frame[_rSyncIdx]) : 
                        # inc count of unsynchronised plc frames
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame += 1
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncFrameData: Detected a local change of Frame[{1}] on PLC, SyncTime = {2}',
                            Para1       =  str(_rSyncIdx),    
                            Para2       =  SyncTime.AFTER_START_UP.toString()
                        )

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Frame = (AxesGroup.State.SyncStatePlc.UnSyncNo.Frame == 0)


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.Frame ) ^ # ^ = xor
                    ( not AxesGroup.State.SyncStateRc .InSync.Frame )):
                
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] :

                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass  # no further action 

                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11

                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12

                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13

                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.Frame ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.Frame )):
 
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Frame ):

                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedFrameIndex):
                    
                        if ( AxesGroup.State.DataChanged.Frame[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Frame ) : 

                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10

                
            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Frame ) : 
                
                    # search for changed index  
                    for _rSyncIdx in range(0 , AxesGroup.State.UnifiedFrameIndex ) : 
                    
                        if ( AxesGroup.State.DataChanged.Frame[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 20 # -> read RC data and write it to PLC
                            break

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Frame ) : 
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Frame ) :
                
                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedFrameIndex):
                    
                        if ( AxesGroup.State.DataChanged.Frame[_rSyncIdx] ) : 
                        
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC                  
                            
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Frame ) :
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return
                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                # _rStep := 10;


            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readFrameData.Busy  ) and
                    ( not self._readFrameData.Error )):
                    # set command parameter
                    self._readFrameData.ParCmd.FrameNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readFrameData.Error):
                        
                        self.ErrorID     = self._readFrameData.ErrorID
                        self.ErrorAddTxt = self._readFrameData.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 21 : 
                
                if (( not self._readFrameData.Busy  ) and
                    ( not self._readFrameData.Error ) and
                    (     self._readFrameData.Done  )):
                
                    # reset execution
                    self._readFrameData.Execute = False
                    # update internal frame data
                    FrameData[_rSyncIdx].Data = copy.deepcopy( self._readFrameData.OutCmd.FrameData)
                    self._frameData[_rSyncIdx].Data = copy.deepcopy( self._readFrameData.OutCmd.FrameData)
                    # set available bit
                    FrameData[_rSyncIdx].Available = True                    
                    self._frameData[_rSyncIdx].Available = True
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readFrameData.Error):
                        
                        self.ErrorID     = self._readFrameData.ErrorID
                        self.ErrorAddTxt = self._readFrameData.ErrorAddTxt
                        # reset available bit
                        FrameData[_rSyncIdx].Available = False
                        self._frameData[_rSyncIdx].Available = False
                    
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeFrameData.Busy  ) and 
                    ( not self._writeFrameData.Error )):

                    # set command parameter
                    self._writeFrameData.ParCmd.FrameNo   = copy.deepcopy(_rSyncIdx)
                    self._writeFrameData.ParCmd.FrameData = copy.deepcopy(FrameData[_rSyncIdx].Data)
                    # execute command
                    self._writeFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeFrameData.Error):
                    
                        self.ErrorID     = self._writeFrameData.ErrorID
                        self.ErrorAddTxt = self._writeFrameData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 :
               
                if (( not self._writeFrameData.Busy  ) and
                    ( not self._writeFrameData.Error ) and
                    (     self._writeFrameData.Done  )):
                   
                    # execute command
                    self._writeFrameData.Execute = False      
                    # update internal frame data
                    self._frameData[_rSyncIdx] = copy.deepcopy(FrameData[_rSyncIdx])
                    # set available bit
                    FrameData[_rSyncIdx].Available = True 
                    self._frameData[_rSyncIdx].Available = True         
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup;           

                else:

                    # check error ? 
                    if (self._writeFrameData.Error):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    
                        # reset available bit
                        FrameData[_rSyncIdx].Available = False
                        self._frameData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                
                
            case _:
                
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleSyncLoadData - handle load data synchronisation
    #------------------------------------------------------------
    def HandleSyncLoadData(self, AxesGroup : AxesGroup, LoadData : list[Load]) -> None:
        """Handle load data synchronisation."""

        #region local variables
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx             : int
        # internal Start index for loops
        _idxStart        : int

        #endregion

        # Set internal references 
        _stepName    =   '_stepSyncLoadData = '
        _rStep       = self._stepSyncLoadData
        _rTimer      = self._timerSyncLoadData
        _rTimeout    = self._timeoutSyncLoadData
        _rSyncIdx    = self._syncIdxLoadData


        match _rStep : 
        
            case 0: 
                
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    return

                # wait for initialisation done
                if ((     AxesGroup.State.RobotData.RCSupportedFunctions. ReadLoadData ) and
                    (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteLoadData ) and
                    (     AxesGroup.State.Initialized                                   ) and 
                    ( not self.Error                                                    )) :

                    # Check PLC loads < RC loads and SyncLoad enabled ?    
                    if (( AxesGroup.State.DataEnableSync.EnableSyncLoad                                           )  and
                        ( AxesGroup.Parameter.Rob.Parameter.HighestLoadIndex > AxesGroup.SystemData.LoadDataCount )) :
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_DATA_ARRAY_TOO_SHORT, Overwrite = True)

                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Start initial reading of LoadData from RC',
                        Para1       =  ''
                    )
                    
                    # calculate start index !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    _rSyncIdx = LIMIT(1, AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex)
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1:

                # Start read LoasData
                if (( not self._readLoadData.Busy  ) and 
                    ( not self._readLoadData.Error ) and
                    ( not self._readLoadData.Done  )) :

                    # set command parameter
                    self._readLoadData.ParCmd.LoadNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if ( self._readLoadData.Error ) :
                    
                        self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2:

                # Wait Loaddata read
                if (( not self._readLoadData.Busy  ) and
                    ( not self._readLoadData.Error ) and
                    (     self._readLoadData.Done  )):
                    
                    # reset execution
                    self._readLoadData.Execute = False
                    # set available bit
                    self._loadData[_rSyncIdx].Available = True
                    LoadData[_rSyncIdx].Available = True
                    # Copy data
                    self._loadData[_rSyncIdx].Data = copy.deepcopy(self._readLoadData.OutCmd.LoadData)

                    # Check load data is equal ? 
                    if ( not IsLoadDataEqual( Data1 = self._loadData[_rSyncIdx].Data, Data2 = LoadData[_rSyncIdx].Data, IgnoreTimestamp = True)) :
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Load = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Load[_rSyncIdx] = True
                        # inc count of unsynchronised plc loads
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Load += 1
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncLoadData: Detected a difference in Load[{1}] between PLC and RC',
                            Para1       =  str(_rSyncIdx)
                        )

                        # Check synchronisation is enabled ? 
                        if ( not AxesGroup.State.DataEnableSync.EnableSyncLoad ) : 

                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_LOAD_DATA_DISABLED, Overwrite = False)

                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Load ) :

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_NUMBER_SYNC_ERROR, Overwrite = False)                    

                    # Check all loads read ? 
                    if ( _rSyncIdx < AxesGroup.State.UnifiedLoadIndex ) : 

                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc load index
                        _rSyncIdx +=1
                        # dec step counter
                        _rStep -=1
                    else:
                        #set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc step counter
                        _rStep += 1

                else:
                    # check error ? 
                    if (self._readLoadData.Error) :

                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)                    
                        # reset available bit
                        LoadData[_rSyncIdx].Available = False
                        self._loadData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3:
                
                # Check synchronisation state ? 
                if (( AxesGroup.State.SyncStatePlc.UnSyncNo.Load                                            == 0                            ) or 
                    ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Load = (AxesGroup.State.SyncStatePlc.UnSyncNo.Load == 0)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )
                    
                else: 
                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Load ) :
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] :

                            case SyncMode.SERVER_TO_CLIENT : 

                                for _idx in range(AxesGroup.SystemData.LoadDataMin, AxesGroup.SystemData.LoadDataMax) : 

                                    # Overwrite PLC data with RC data
                                    LoadData[_idx] = copy.deepcopy(self._loadData[_idx])

                                # Reset data changed flags
                                AxesGroup.State.DataChanged.Load = _dataChangedNone.Load
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Load = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Load = True
                                # Reset count of unsynchronised plc loads
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncLoadData: Synchronization of Loads triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                                    Para1       =  str(_rSyncIdx),
                                    Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP].toString(),
                                    Para3       =  SyncTime.DURING_START_UP.toString()
                                )
                                
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncLoadData: Applied the initial read load data from RC',
                                    Para1       =  '' 
                                )


                            case SyncMode.CLIENT_TO_SERVER :

                                #  calculate start index 
                                _idxStart = LIMIT(1 , AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex) 

                                # Check conflicts to solve ? 
                                for _rSyncIdx in range(_idxStart, AxesGroup.State.UnifiedLoadIndex): # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                            
                                    if ( AxesGroup.State.DataChanged.Load[_rSyncIdx] ) :
                                    
                                        _found = True
                                        break

                                if ( _found ) :
                                
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Load = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Load = True
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = _rStep + 1  # -> write PLC data to RC                  
                                    # Create log entry
                                    self.CreateLogMessage( 
                                        Timestamp   = self.SystemTime,
                                        MessageType = MessageType.CMD,
                                        Severity    = Severity.DEBUG,
                                        MessageCode = 0,
                                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                                        Para1       = str(_rSyncIdx),
                                        Para2       = AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP].toString(),
                                        Para3       = SyncTime.DURING_START_UP.toString()
                                    )
                                    
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.Load = _dataChangedNone.Load
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Load = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Load = True
                                    # Reset count of unsynchronised loads
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )


            case 4:

                # Start write load data  
                if (( not self._writeLoadData.Busy  ) and 
                    ( not self._writeLoadData.Error )):
                
                    # set command parameter
                    self._writeLoadData.ParCmd.LoadNo   = copy.deepcopy(_rSyncIdx) 
                    self._writeLoadData.ParCmd.LoadData = copy.deepcopy(LoadData[_rSyncIdx].Data)
                    # execute command
                    self._writeLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeLoadData.Error) : 

                        self.ErrorID     = self._writeLoadData.ErrorID
                        self.ErrorAddTxt = self._writeLoadData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5:
                # Wait load data written ?   
                if (( not self._writeLoadData.Busy  ) and
                    ( not self._writeLoadData.Error ) and
                    (     self._writeLoadData.Done  )):
                
                    # execute command
                    self._writeLoadData.Execute = False
                    # apply load data to internal load data
                    self._loadData[_rSyncIdx] = copy.deepcopy(LoadData[_rSyncIdx])
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.Load[_rSyncIdx] = False
                    # dec count of unsynchronised loads
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load -= 1
                    # set timeout        
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= - 2
                else:
                    # check error ? 
                    if (self._writeLoadData.Error) : 
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           
                    
                    
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------                    
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION) :
                
                    return

                # reset count of unsynchronised loads
                AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0

                #  calculate start index 
                _idxStart = LIMIT(1 , AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex)

                # Check all load datas
                for _rSyncIdx in range(_idxStart, AxesGroup.State.UnifiedLoadIndex): # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                
                    # compare load data
                    AxesGroup.State.DataChanged.Load[_rSyncIdx] = not IsLoadDataEqual( Data1 = LoadData[_rSyncIdx].Data, Data2 = self._loadData[_rSyncIdx].Data, IgnoreTimestamp = False)

                    # Check Load data changed ? 
                    if (AxesGroup.State.DataChanged.Load[_rSyncIdx]) : 
                        # inc count of unsynchronised plc loads
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Load += 1
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncLoadData: Detected a local change of Load[{1}] on PLC, SyncTime = {2}',
                            Para1       =  str(_rSyncIdx),    
                            Para2       =  SyncTime.AFTER_START_UP.toString()
                        )

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Load = (AxesGroup.State.SyncStatePlc.UnSyncNo.Load == 0)


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.Load ) ^ # ^ = xor
                    ( not AxesGroup.State.SyncStateRc .InSync.Load )):
                
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] :

                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass  # no further action 

                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11

                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12

                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13

                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.Load ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.Load )):
 
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Load ):

                    #  calculate start index 
                    _idxStart = LIMIT(1 , AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex) 

                    # search for changed index  
                    for _rSyncIdx in range(_idxStart, AxesGroup.State.UnifiedLoadIndex): # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    
                        if ( AxesGroup.State.DataChanged.Load[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Load ) : 

                    # get changed index 
                    _rSyncIdx = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex) # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10

                
            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Load ) : 
                
                    #  calculate start index 
                    _idxStart = LIMIT(1 , AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex)
                
                    # search for changed index  
                    for _rSyncIdx in range(_idxStart , AxesGroup.State.UnifiedLoadIndex ) : # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    
                        if ( AxesGroup.State.DataChanged.Load[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 20 # -> read RC data and write it to PLC
                            break

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Load ) : 
                
                    # get changed index 
                    _rSyncIdx = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex) # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Load ) :
                
                    #  calculate start index 
                    _idxStart = LIMIT(1 , AxesGroup.SystemData.LoadDataMin, AxesGroup.State.UnifiedLoadIndex)

                    # search for changed index  
                    for _rSyncIdx in range(_idxStart, AxesGroup.State.UnifiedLoadIndex): #!!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    
                        if ( AxesGroup.State.DataChanged.Load[_rSyncIdx] ) : 
                        
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC                  
                            
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Load ) :
                
                    # get changed index 
                    _rSyncIdx = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex) # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return
                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                # _rStep := 10;


            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readLoadData.Busy  ) and
                    ( not self._readLoadData.Error )):
                    # set command parameter
                    self._readLoadData.ParCmd.LoadNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readLoadData.Error):
                        
                        self.ErrorID     = self._readLoadData.ErrorID
                        self.ErrorAddTxt = self._readLoadData.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 21 : 
                
                if (( not self._readLoadData.Busy  ) and
                    ( not self._readLoadData.Error ) and
                    (     self._readLoadData.Done  )):
                
                    # reset execution
                    self._readLoadData.Execute = False
                    # update internal load data
                    LoadData[_rSyncIdx].Data = copy.deepcopy( self._readLoadData.OutCmd.LoadData)
                    self._loadData[_rSyncIdx].Data = copy.deepcopy( self._readLoadData.OutCmd.LoadData)
                    # set available bit
                    LoadData[_rSyncIdx].Available = True                    
                    self._loadData[_rSyncIdx].Available = True
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readLoadData.Error):
                        
                        self.ErrorID     = self._readLoadData.ErrorID
                        self.ErrorAddTxt = self._readLoadData.ErrorAddTxt
                        # reset available bit
                        LoadData[_rSyncIdx].Available = False
                        self._loadData[_rSyncIdx].Available = False
                    
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeLoadData.Busy  ) and 
                    ( not self._writeLoadData.Error )):

                    # set command parameter
                    self._writeLoadData.ParCmd.LoadNo   = copy.deepcopy(_rSyncIdx)
                    self._writeLoadData.ParCmd.LoadData = copy.deepcopy(LoadData[_rSyncIdx].Data)
                    # execute command
                    self._writeLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeLoadData.Error):
                    
                        self.ErrorID     = self._writeLoadData.ErrorID
                        self.ErrorAddTxt = self._writeLoadData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 :
               
                if (( not self._writeLoadData.Busy  ) and
                    ( not self._writeLoadData.Error ) and
                    (     self._writeLoadData.Done  )):
                   
                    # execute command
                    self._writeLoadData.Execute = False      
                    # update internal load data
                    self._loadData[_rSyncIdx] = copy.deepcopy(LoadData[_rSyncIdx])
                    # set available bit
                    LoadData[_rSyncIdx].Available = True 
                    self._loadData[_rSyncIdx].Available = True         
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup;           

                else:

                    # check error ? 
                    if (self._writeLoadData.Error):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    
                        # reset available bit
                        LoadData[_rSyncIdx].Available = False
                        self._loadData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                
                
            case _:
                
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleSyncRobotDefaultDynamics - handle robot default dynamics synchronisation
    #------------------------------------------------------------
    def HandleSyncRobotDefaultDynamics(self, AxesGroup : AxesGroup, DefaultDynamics : DefaultDynamics) -> None:

        #region local variables
        
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME 
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        
        #endregion

        # Set internal references 
        _stepName      =   '_stepSyncDefaultDynamics = '
        _rStep         =    self._stepSyncDefaultDynamics
        _rTimer        =   self._timerSyncDefaultDynamics
        _rTimeout      = self._timeoutSyncDefaultDynamics

        match _rStep :
        
            case 0: 
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    return

                # wait for initialisation done
                if  ((     AxesGroup.State.RobotData.RCSupportedFunctions .ReadRobotDefaultDynamics ) and
                     (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotDefaultDynamics ) and
                     (     AxesGroup.State.Initialized                                              ) and 
                     ( not self.Error                                                                    )):

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Start initial reading of DefaultDynamics from RC',
                        Para1       =  ''
                    )

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1: 

                # Start read DefaultDynamics
                if (( not self._readRobotDefaultDynamics.Busy  ) and 
                    ( not self._readRobotDefaultDynamics.Error ) and
                    ( not self._readRobotDefaultDynamics.Done  )):

                    # execute command
                    self._readRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:

                    # check error ? 
                    if ( self._readRobotDefaultDynamics.Error ) :
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False )

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2: 
            
                # Wait DefaultDynamics read
                if (( not self._readRobotDefaultDynamics.Busy  ) and
                    ( not self._readRobotDefaultDynamics.Error ) and
                    (     self._readRobotDefaultDynamics.Done  )):

                    # reset execution
                    self._readRobotDefaultDynamics.Execute = False
                    # Copy data
                    _defaultDynamics = copy.deepcopy(self._readRobotDefaultDynamics.OutCmd.DynamicValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                    # inc step counter
                    _rStep += 1

                    # Check DefaultDynamics data is equal ? 
                    if ( not IsDefaultDynamicsEqual( Data1 = _defaultDynamics, Data2 = DefaultDynamics, IgnoreTimestamp = True)):

                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.DefaultDynamics = True
                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncDefaultDynamics: Detected a difference in DefaultDynamics between PLC and RC',
                            Para1       =  ''
                        )

                        # Check synchronisation is enabled ? 
                        if ( not  AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics ):
                        
                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_DEFAULT_DYNAMICS_DISABLED, Overwrite = False)


                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.DefaultDynamics ):

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_ERROR, Overwrite = False)


                else:
                    # check error ? 
                    if (self._readRobotDefaultDynamics.Error):
                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3: 
                # Check synchronisation state ? 
                if ((  not AxesGroup.State.DataChanged.DefaultDynamics                                                                                     ) or 
                    (      AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = not AxesGroup.State.DataChanged.DefaultDynamics
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )

                else:

                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.DefaultDynamics ):
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] :

                            case SyncMode.SERVER_TO_CLIENT : 

                                # Overwrite PLC data with RC data
                                DefaultDynamics = copy.deepcopy(self._defaultDynamics)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.DefaultDynamics = _dataChangedNone.DefaultDynamics
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.DefaultDynamics = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                                    Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP].toString(),
                                    Para2       =  SyncTime.DURING_START_UP.toString()
                                )
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncDefaultDynamics: Applied the initial read DefaultDynamics from RC',
                                    Para1       =  '' 
                                )

                            case SyncMode.CLIENT_TO_SERVER :

                                    if ( AxesGroup.State.DataChanged.DefaultDynamics ) :

                                        # Reset plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = False
                                        # Set Synchronizing flag
                                        AxesGroup.State.Synchronizing.DefaultDynamics = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep += 1 # -> write PLC data to RC                  
                                        # Create log entry
                                        self.CreateLogMessage( 
                                            Timestamp   = self.SystemTime,
                                            MessageType = MessageType.CMD,
                                            Severity    = Severity.DEBUG,
                                            MessageCode = 0,
                                            MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                                            Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP].toString(),
                                            Para2       =  SyncTime.DURING_START_UP.toString()
                                        )
                                    else:
                                    # Reset data changed flags
                                        AxesGroup.State.DataChanged.DefaultDynamics = _dataChangedNone.DefaultDynamics
                                        # Reset Synchronizing flag
                                        AxesGroup.State.Synchronizing.DefaultDynamics = False
                                        # Set plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )

            
                    
            case 4:
            
                # Start write DefaultDynamics data  
                if (( not self._writeRobotDefaultDynamics.Busy  ) and 
                    ( not self._writeRobotDefaultDynamics.Error )):
                    # set command parameter
                    self._writeRobotDefaultDynamics.ParCmd.DynamicValues =  copy.deepcopy(DefaultDynamics)
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeRobotDefaultDynamics.Error) :

                        self.ErrorID     = self._writeRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5: 
                
                # Wait DefaultDynamics data written ?   
                if (( not self._writeRobotDefaultDynamics.Busy  ) and
                    ( not self._writeRobotDefaultDynamics.Error ) and
                    (     self._writeRobotDefaultDynamics.Done  )) :

                    # execute command
                    self._writeRobotDefaultDynamics.Execute = False
                    # apply DefaultDynamics data to internal DefaultDynamics data
                    self._defaultDynamics = copy.deepcopy(DefaultDynamics)
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.DefaultDynamics = False
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= 2 
                else:
                    # check error ? 
                    if (self._writeRobotDefaultDynamics.Error):

                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

            
            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION):

                    return

                # compare DefaultDynamics data
                AxesGroup.State.DataChanged.DefaultDynamics = not IsDefaultDynamicsEqual( Data1 = DefaultDynamics, Data2 = self._defaultDynamics, IgnoreTimestamp = False)

                # Check DefaultDynamics data changed ? 
                if (AxesGroup.State.DataChanged.DefaultDynamics):
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Detected a local change of DefaultDynamics on PLC, SyncTime = {1}',
                        Para1       =  SyncTime.AFTER_START_UP.toString()
                    )

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = not AxesGroup.State.DataChanged.DefaultDynamics 


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics ) ^
                    ( not AxesGroup.State.SyncStateRc .InSync.DefaultDynamics )):

                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] :
                             
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass # no further action 
                    
                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11
            
                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12
            
                        # AUTOMATIC
                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13
                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.DefaultDynamics )):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics ):
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC                  

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return
            
                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics ):
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                #_rStep = 10;

            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readRobotDefaultDynamics.Busy  ) and
                    ( not self._readRobotDefaultDynamics.Error )):
                
                    # execute command
                    self._readRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readRobotDefaultDynamics.Error):
                    
                        self.ErrorID     = self._readRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

        
            case 21 :
                
                if (( not self._readRobotDefaultDynamics.Busy  ) and
                    ( not self._readRobotDefaultDynamics.Error ) and
                    (     self._readRobotDefaultDynamics.Done  )):
                
                    # reset execution
                    self._readRobotDefaultDynamics.Execute = False
                    # update internal DefaultDynamics data
                    DefaultDynamics = copy.deepcopy(self._readRobotDefaultDynamics.OutCmd.DynamicValues)         
                    _defaultDynamics = copy.deepcopy(self._readRobotDefaultDynamics.OutCmd.DynamicValues)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readRobotDefaultDynamics.Error):
                        
                        self.ErrorID     = self._readRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotDefaultDynamics.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeRobotDefaultDynamics.Busy  ) and 
                    ( not self._writeRobotDefaultDynamics.Error )) :
                
                    # set command parameter
                    self._writeRobotDefaultDynamics.ParCmd.DynamicValues = copy.deepcopy(DefaultDynamics)
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep +=1
                else:
                    
                    # check error ? 
                    if (self._writeRobotDefaultDynamics.Error):
                        
                        self.ErrorID     = self._writeRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 : 

                if (( not self._writeRobotDefaultDynamics.Busy  ) and
                    ( not self._writeRobotDefaultDynamics.Error ) and
                    (     self._writeRobotDefaultDynamics.Done  )):

                    # execute command
                    self._writeRobotDefaultDynamics.Execute = False
                    # update internal DefaultDynamics data
                    _defaultDynamics = copy.deepcopy(DefaultDynamics)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup;

                else:
                    # check error ? 
                    if (self._writeRobotDefaultDynamics.Error):
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case _:
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleSyncRobotReferenceDynamics - handle robot reference dynamics synchronisation
    #------------------------------------------------------------
    def HandleSyncRobotReferenceDynamics(self, AxesGroup : AxesGroup, ReferenceDynamics : ReferenceDynamics) -> None:

        #region local variables
        
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME 
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        
        #endregion

        # Set internal references 
        _stepName      =   '_stepSyncReferenceDynamics = '
        _rStep         =    self._stepSyncReferenceDynamics
        _rTimer        =   self._timerSyncReferenceDynamics
        _rTimeout      = self._timeoutSyncReferenceDynamics

        match _rStep :
        
            case 0: 
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    return

                # wait for initialisation done
                if  ((     AxesGroup.State.RobotData.RCSupportedFunctions .ReadRobotReferenceDynamics ) and
                     (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotReferenceDynamics ) and
                     (     AxesGroup.State.Initialized                                                ) and 
                     ( not self.Error                                                                 )):

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Start initial reading of ReferenceDynamics from RC',
                        Para1       =  ''
                    )

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1: 

                # Start read ReferenceDynamics
                if (( not self._readRobotReferenceDynamics.Busy  ) and 
                    ( not self._readRobotReferenceDynamics.Error ) and
                    ( not self._readRobotReferenceDynamics.Done  )):

                    # execute command
                    self._readRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:

                    # check error ? 
                    if ( self._readRobotReferenceDynamics.Error ) :
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False )

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2: 
            
                # Wait ReferenceDynamics read
                if (( not self._readRobotReferenceDynamics.Busy  ) and
                    ( not self._readRobotReferenceDynamics.Error ) and
                    (     self._readRobotReferenceDynamics.Done  )):

                    # reset execution
                    self._readRobotReferenceDynamics.Execute = False
                    # Copy data
                    _referenceDynamics = copy.deepcopy(self._readRobotReferenceDynamics.OutCmd.DynamicValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                    # inc step counter
                    _rStep += 1

                    # Check ReferenceDynamics data is equal ? 
                    if ( not IsReferenceDynamicsEqual( Data1 = _referenceDynamics, Data2 = ReferenceDynamics, IgnoreTimestamp = True)):

                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.ReferenceDynamics = True
                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncReferenceDynamics: Detected a difference in ReferenceDynamics between PLC and RC',
                            Para1       =  ''
                        )

                        # Check synchronisation is enabled ? 
                        if ( not  AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics ):
                        
                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_REFERENCE_DYNAMICS_DISABLED, Overwrite = False)


                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.ReferenceDynamics ):

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_ERROR, Overwrite = False)


                else:
                    # check error ? 
                    if (self._readRobotReferenceDynamics.Error):
                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3: 
                # Check synchronisation state ? 
                if ((  not AxesGroup.State.DataChanged.ReferenceDynamics                                                                                     ) or 
                    (      AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = not AxesGroup.State.DataChanged.ReferenceDynamics
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )

                else:

                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.ReferenceDynamics ):
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] :

                            case SyncMode.SERVER_TO_CLIENT : 

                                # Overwrite PLC data with RC data
                                ReferenceDynamics = copy.deepcopy(self._referenceDynamics)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.ReferenceDynamics = _dataChangedNone.ReferenceDynamics
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.ReferenceDynamics = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                                    Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP].toString(),
                                    Para2       =  SyncTime.DURING_START_UP.toString()
                                )
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncReferenceDynamics: Applied the initial read ReferenceDynamics from RC',
                                    Para1       =  '' 
                                )

                            case SyncMode.CLIENT_TO_SERVER :

                                    if ( AxesGroup.State.DataChanged.ReferenceDynamics ) :

                                        # Reset plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False
                                        # Set Synchronizing flag
                                        AxesGroup.State.Synchronizing.ReferenceDynamics = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep += 1 # -> write PLC data to RC                  
                                        # Create log entry
                                        self.CreateLogMessage( 
                                            Timestamp   = self.SystemTime,
                                            MessageType = MessageType.CMD,
                                            Severity    = Severity.DEBUG,
                                            MessageCode = 0,
                                            MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                                            Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP].toString(),
                                            Para2       =  SyncTime.DURING_START_UP.toString()
                                        )
                                    else:
                                    # Reset data changed flags
                                        AxesGroup.State.DataChanged.ReferenceDynamics = _dataChangedNone.ReferenceDynamics
                                        # Reset Synchronizing flag
                                        AxesGroup.State.Synchronizing.ReferenceDynamics = False
                                        # Set plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )

            
                    
            case 4:
            
                # Start write ReferenceDynamics data  
                if (( not self._writeRobotReferenceDynamics.Busy  ) and 
                    ( not self._writeRobotReferenceDynamics.Error )):
                    # set command parameter
                    self._writeRobotReferenceDynamics.ParCmd.DynamicValues =  copy.deepcopy(ReferenceDynamics)
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeRobotReferenceDynamics.Error) :

                        self.ErrorID     = self._writeRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5: 
                
                # Wait ReferenceDynamics data written ?   
                if (( not self._writeRobotReferenceDynamics.Busy  ) and
                    ( not self._writeRobotReferenceDynamics.Error ) and
                    (     self._writeRobotReferenceDynamics.Done  )) :

                    # execute command
                    self._writeRobotReferenceDynamics.Execute = False
                    # apply ReferenceDynamics data to internal ReferenceDynamics data
                    self._referenceDynamics = copy.deepcopy(ReferenceDynamics)
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.ReferenceDynamics = False
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= 2 
                else:
                    # check error ? 
                    if (self._writeRobotReferenceDynamics.Error):

                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

            
            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION):

                    return

                # compare ReferenceDynamics data
                AxesGroup.State.DataChanged.ReferenceDynamics = not IsReferenceDynamicsEqual( Data1 = ReferenceDynamics, Data2 = self._referenceDynamics, IgnoreTimestamp = False)

                # Check ReferenceDynamics data changed ? 
                if (AxesGroup.State.DataChanged.ReferenceDynamics):
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Detected a local change of ReferenceDynamics on PLC, SyncTime = {1}',
                        Para1       =  SyncTime.AFTER_START_UP.toString()
                    )

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = not AxesGroup.State.DataChanged.ReferenceDynamics 


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics ) ^
                    ( not AxesGroup.State.SyncStateRc .InSync.ReferenceDynamics )):

                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] :
                             
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass # no further action 
                    
                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11
            
                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12
            
                        # AUTOMATIC
                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13
                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.ReferenceDynamics )):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics ):
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC                  

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return
            
                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics ):
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                #_rStep = 10;

            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readRobotReferenceDynamics.Busy  ) and
                    ( not self._readRobotReferenceDynamics.Error )):
                
                    # execute command
                    self._readRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readRobotReferenceDynamics.Error):
                    
                        self.ErrorID     = self._readRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

        
            case 21 :
                
                if (( not self._readRobotReferenceDynamics.Busy  ) and
                    ( not self._readRobotReferenceDynamics.Error ) and
                    (     self._readRobotReferenceDynamics.Done  )):
                
                    # reset execution
                    self._readRobotReferenceDynamics.Execute = False
                    # update internal ReferenceDynamics data
                    ReferenceDynamics = copy.deepcopy(self._readRobotReferenceDynamics.OutCmd.DynamicValues)         
                    _referenceDynamics = copy.deepcopy(self._readRobotReferenceDynamics.OutCmd.DynamicValues)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readRobotReferenceDynamics.Error):
                        
                        self.ErrorID     = self._readRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotReferenceDynamics.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeRobotReferenceDynamics.Busy  ) and 
                    ( not self._writeRobotReferenceDynamics.Error )) :
                
                    # set command parameter
                    self._writeRobotReferenceDynamics.ParCmd.DynamicValues = copy.deepcopy(ReferenceDynamics)
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep +=1
                else:
                    
                    # check error ? 
                    if (self._writeRobotReferenceDynamics.Error):
                        
                        self.ErrorID     = self._writeRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 : 

                if (( not self._writeRobotReferenceDynamics.Busy  ) and
                    ( not self._writeRobotReferenceDynamics.Error ) and
                    (     self._writeRobotReferenceDynamics.Done  )):

                    # execute command
                    self._writeRobotReferenceDynamics.Execute = False
                    # update internal ReferenceDynamics data
                    _referenceDynamics = copy.deepcopy(ReferenceDynamics)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup;

                else:
                    # check error ? 
                    if (self._writeRobotReferenceDynamics.Error):
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case _:
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleSyncRobotSwLimits - handle robot software limits synchronisation
    #------------------------------------------------------------
    def HandleSyncRobotSWLimits(self, AxesGroup : AxesGroup, SWLimits : SWLimits) -> None:

        #region local variables
        
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME 
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        
        #endregion

        # Set internal references 
        _stepName      =   '_stepSyncSWLimits = '
        _rStep         =    self._stepSyncSWLimits
        _rTimer        =   self._timerSyncSWLimits
        _rTimeout      = self._timeoutSyncSWLimits

        match _rStep :
        
            case 0: 
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    return

                # wait for initialisation done
                if  ((     AxesGroup.State.RobotData.RCSupportedFunctions .ReadRobotSWLimits ) and
                     (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotSWLimits ) and
                     (     AxesGroup.State.Initialized                                                ) and 
                     ( not self.Error                                                                 )):

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Start initial reading of SWLimits from RC',
                        Para1       =  ''
                    )

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1: 

                # Start read SWLimits
                if (( not self._readRobotSwLimits.Busy  ) and 
                    ( not self._readRobotSwLimits.Error ) and
                    ( not self._readRobotSwLimits.Done  )):

                    # execute command
                    self._readRobotSwLimits.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:

                    # check error ? 
                    if ( self._readRobotSwLimits.Error ) :
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False )

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2: 
            
                # Wait SWLimits read
                if (( not self._readRobotSwLimits.Busy  ) and
                    ( not self._readRobotSwLimits.Error ) and
                    (     self._readRobotSwLimits.Done  )):

                    # reset execution
                    self._readRobotSwLimits.Execute = False
                    # Copy data
                    _swLimits = copy.deepcopy(self._readRobotSwLimits.OutCmd.LimitValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                    # inc step counter
                    _rStep += 1

                    # Check SWLimits data is equal ? 
                    if ( not IsSwLimitsEqual( Data1 = _swLimits, Data2 = SWLimits, IgnoreTimestamp = True)):

                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.SwLimits = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.SwLimits = True
                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncSWLimits: Detected a difference in SWLimits between PLC and RC',
                            Para1       =  ''
                        )

                        # Check synchronisation is enabled ? 
                        if ( not  AxesGroup.State.DataEnableSync.EnableSyncSWLimits ):
                        
                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_REFERENCE_DYNAMICS_DISABLED, Overwrite = False)


                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.SwLimits ):

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_ERROR, Overwrite = False)


                else:
                    # check error ? 
                    if (self._readRobotSwLimits.Error):
                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3: 
                # Check synchronisation state ? 
                if ((  not AxesGroup.State.DataChanged.SwLimits                                                                                     ) or 
                    (      AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = not AxesGroup.State.DataChanged.SwLimits
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )

                else:

                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.SwLimits ):
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP] :

                            case SyncMode.SERVER_TO_CLIENT : 

                                # Overwrite PLC data with RC data
                                SWLimits = copy.deepcopy(self._swLimits)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.SwLimits = _dataChangedNone.SwLimits
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.SwLimits = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncSWLimits: Synchronization of SWLimits triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                                    Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP].toString(),
                                    Para2       =  SyncTime.DURING_START_UP.toString()
                                )
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncSWLimits: Applied the initial read SWLimits from RC',
                                    Para1       =  '' 
                                )

                            case SyncMode.CLIENT_TO_SERVER :

                                    if ( AxesGroup.State.DataChanged.SwLimits ) :

                                        # Reset plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.SwLimits = False
                                        # Set Synchronizing flag
                                        AxesGroup.State.Synchronizing.SwLimits = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep += 1 # -> write PLC data to RC                  
                                        # Create log entry
                                        self.CreateLogMessage( 
                                            Timestamp   = self.SystemTime,
                                            MessageType = MessageType.CMD,
                                            Severity    = Severity.DEBUG,
                                            MessageCode = 0,
                                            MessageText = 'SyncSWLimits: Synchronization of SWLimits triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                                            Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.DURING_START_UP].toString(),
                                            Para2       =  SyncTime.DURING_START_UP.toString()
                                        )
                                    else:
                                    # Reset data changed flags
                                        AxesGroup.State.DataChanged.SwLimits = _dataChangedNone.SwLimits
                                        # Reset Synchronizing flag
                                        AxesGroup.State.Synchronizing.SwLimits = False
                                        # Set plc in sync flag
                                        AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                                        # set timeout
                                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                        # inc step counter
                                        _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )

            
                    
            case 4:
            
                # Start write SWLimits data  
                if (( not self._writeRobotSwLimits.Busy  ) and 
                    ( not self._writeRobotSwLimits.Error )):
                    # set command parameter
                    self._writeRobotSwLimits.ParCmd.DynamicValues =  copy.deepcopy(SWLimits)
                    # execute command
                    self._writeRobotSwLimits.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeRobotSwLimits.Error) :

                        self.ErrorID     = self._writeRobotSwLimits.ErrorID
                        self.ErrorAddTxt = self._writeRobotSwLimits.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5: 
                
                # Wait SWLimits data written ?   
                if (( not self._writeRobotSwLimits.Busy  ) and
                    ( not self._writeRobotSwLimits.Error ) and
                    (     self._writeRobotSwLimits.Done  )) :

                    # execute command
                    self._writeRobotSwLimits.Execute = False
                    # apply SWLimits data to internal SWLimits data
                    self._swLimits = copy.deepcopy(SWLimits)
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.SWLimits = False
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= 2 
                else:
                    # check error ? 
                    if (self._writeRobotSwLimits.Error):

                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

            
            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION):

                    return

                # compare SWLimits data
                AxesGroup.State.DataChanged.SwLimits = not IsSwLimitsEqual( Data1 = SWLimits, Data2 = self._swLimits, IgnoreTimestamp = False)

                # Check SWLimits data changed ? 
                if (AxesGroup.State.DataChanged.SwLimits):
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Detected a local change of SWLimits on PLC, SyncTime = {1}',
                        Para1       =  SyncTime.AFTER_START_UP.toString()
                    )

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.SwLimits = not AxesGroup.State.DataChanged.SwLimits 


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.SwLimits ) ^
                    ( not AxesGroup.State.SyncStateRc .InSync.SwLimits )):

                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP] :
                             
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass # no further action 
                    
                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11
            
                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12
            
                        # AUTOMATIC
                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13
                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.SwLimits ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.SwLimits )):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.SwLimits ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.SwLimits ):
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.SwLimits ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC                  

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return
            
                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.SwLimits ) :
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 :
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.SwLimits ):
                
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC                  
                    
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.SwLimits ) :

                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncSWLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC',
                        Para1       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SwLimits[SyncTime.AFTER_START_UP].toString(),
                        Para2       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                #_rStep = 10;

            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readRobotSwLimits.Busy  ) and
                    ( not self._readRobotSwLimits.Error )):
                
                    # execute command
                    self._readRobotSwLimits.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readRobotSwLimits.Error):
                    
                        self.ErrorID     = self._readRobotSwLimits.ErrorID
                        self.ErrorAddTxt = self._readRobotSwLimits.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))

        
            case 21 :
                
                if (( not self._readRobotSwLimits.Busy  ) and
                    ( not self._readRobotSwLimits.Error ) and
                    (     self._readRobotSwLimits.Done  )):
                
                    # reset execution
                    self._readRobotSwLimits.Execute = False
                    # update internal SwLimits data
                    SWLimits = copy.deepcopy(self._readRobotSwLimits.OutCmd.LimitValues)         
                    _swLimits = copy.deepcopy(self._readRobotSwLimits.OutCmd.LimitValues)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readRobotSwLimits.Error):
                        
                        self.ErrorID     = self._readRobotSwLimits.ErrorID
                        self.ErrorAddTxt = self._readRobotSwLimits.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeRobotSwLimits.Busy  ) and 
                    ( not self._writeRobotSwLimits.Error )) :
                
                    # set command parameter
                    self._writeRobotSwLimits.ParCmd.DynamicValues = copy.deepcopy(SWLimits)
                    # execute command
                    self._writeRobotSwLimits.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep +=1
                else:
                    
                    # check error ? 
                    if (self._writeRobotSwLimits.Error):
                        
                        self.ErrorID     = self._writeRobotSwLimits.ErrorID
                        self.ErrorAddTxt = self._writeRobotSwLimits.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 : 

                if (( not self._writeRobotSwLimits.Busy  ) and
                    ( not self._writeRobotSwLimits.Error ) and
                    (     self._writeRobotSwLimits.Done  )):

                    # execute command
                    self._writeRobotSwLimits.Execute = False
                    # update internal SWLimits data
                    _swLimits = copy.deepcopy(SWLimits)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup;

                else:
                    # check error ? 
                    if (self._writeRobotSwLimits.Error):
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case _:
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleSyncToolData - handle tool data synchronisation
    #------------------------------------------------------------
    def HandleSyncToolData(self, AxesGroup : AxesGroup, ToolData : list[Tool]) -> None:
        """Handle tool data synchronisation."""

        #region local variables
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx             : int

        #endregion

        # Set internal references 
        _stepName    =   '_stepSyncToolData = '
        _rStep       = self._stepSyncToolData
        _rTimer      = self._timerSyncToolData
        _rTimeout    = self._timeoutSyncToolData
        _rSyncIdx    = self._syncIdxToolData


        match _rStep : 
        
            case 0: 
                
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    return

                # wait for initialisation done
                if ((     AxesGroup.State.RobotData.RCSupportedFunctions. ReadToolData ) and
                    (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteToolData ) and
                    (     AxesGroup.State.Initialized                                  ) and 
                    ( not self.Error                                                   )) :

                    # Check PLC tools < RC tools and SyncTool enabled ?    
                    if (( AxesGroup.State.DataEnableSync.EnableSyncTool                                           )  and
                        ( AxesGroup.Parameter.Rob.Parameter.HighestToolIndex > AxesGroup.SystemData.ToolDataCount )) :
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_TOO_SHORT, Overwrite = True)

                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Start initial reading of ToolData from RC',
                        Para1       =  ''
                    )
                    
                    # init tool number
                    _rSyncIdx = AxesGroup.SystemData.ToolDataMin
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1:

                # Start read ToolData
                if (( not self._readToolData.Busy  ) and 
                    ( not self._readToolData.Error ) and
                    ( not self._readToolData.Done  )) :

                    # set command parameter
                    self._readToolData.ParCmd.ToolNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readToolData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if ( self._readToolData.Error ) :
                    
                        self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2:

                # Wait ToolData read
                if (( not self._readToolData.Busy  ) and
                    ( not self._readToolData.Error ) and
                    (     self._readToolData.Done  )):
                    
                    # reset execution
                    self._readToolData.Execute = False
                    # set available bit
                    self._toolData[_rSyncIdx].Available = True
                    ToolData[_rSyncIdx].Available = True
                    # Copy data
                    self._toolData[_rSyncIdx].Data = copy.deepcopy(self._readToolData.OutCmd.ToolData)

                    # Check tool data is equal ? 
                    if ( not IsToolDataEqual( Data1 = self._toolData[_rSyncIdx].Data, Data2 = ToolData[_rSyncIdx].Data, IgnoreTimestamp = True)) :
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Tool = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Tool[_rSyncIdx] = True
                        # inc count of unsynchronised plc tools
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool += 1
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncToolData: Detected a difference in Tool[{1}] between PLC and RC',
                            Para1       =  str(_rSyncIdx)
                        )

                        # Check synchronisation is enabled ? 
                        if ( not AxesGroup.State.DataEnableSync.EnableSyncTool ) : 

                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_TOOL_DATA_DISABLED, Overwrite = False)

                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Tool ) :

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_NUMBER_SYNC_ERROR, Overwrite = False)                    

                    # Check all tools read ? 
                    if ( _rSyncIdx < AxesGroup.State.UnifiedToolIndex ) : 

                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc tool index
                        _rSyncIdx +=1
                        # dec step counter
                        _rStep -=1
                    else:
                        #set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc step counter
                        _rStep += 1

                else:
                    # check error ? 
                    if (self._readToolData.Error) :

                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)                    
                        # reset available bit
                        ToolData[_rSyncIdx].Available = False
                        self._toolData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3:
                
                # Check synchronisation state ? 
                if (( AxesGroup.State.SyncStatePlc.UnSyncNo.Tool                                            == 0                           ) or 
                    ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Tool = (AxesGroup.State.SyncStatePlc.UnSyncNo.Tool == 0)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )
                    
                else: 
                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Tool ) :
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] :
                            
                            case SyncMode.SERVER_TO_CLIENT : 

                                for _idx in range(AxesGroup.SystemData.ToolDataMin, AxesGroup.SystemData.ToolDataMax) : 

                                    # Overwrite PLC data with RC data
                                    ToolData[_idx] = copy.deepcopy(self._toolData[_idx])

                                # Reset data changed flags
                                AxesGroup.State.DataChanged.Tool = _dataChangedNone.Tool
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Tool = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Tool = True
                                # Reset count of unsynchronised plc tools
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncToolData: Synchronization of Tools triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                                    Para1       =  str(_rSyncIdx),
                                    Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP].toString(),
                                    Para3       =  SyncTime.DURING_START_UP.toString()
                                )
                                
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncToolData: Applied the initial read tool data from RC',
                                    Para1       =  '' 
                                )


                            case SyncMode.CLIENT_TO_SERVER :

                                # Check conflicts to solve ? 
                                for _rSyncIdx in range(0, AxesGroup.State.UnifiedToolIndex):
                            
                                    if ( AxesGroup.State.DataChanged.Tool[_rSyncIdx] ) :
                                    
                                        _found = True
                                        break

                                if ( _found ) :
                                
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Tool = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Tool = True
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = _rStep + 1  # -> write PLC data to RC                  
                                    # Create log entry
                                    self.CreateLogMessage( 
                                        Timestamp   = self.SystemTime,
                                        MessageType = MessageType.CMD,
                                        Severity    = Severity.DEBUG,
                                        MessageCode = 0,
                                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                                        Para1       = str(_rSyncIdx),
                                        Para2       = AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP].toString(),
                                        Para3       = SyncTime.DURING_START_UP.toString()
                                    )
                                    
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.Tool = _dataChangedNone.Tool
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Tool = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Tool = True
                                    # Reset count of unsynchronised tools
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )


            case 4:

                # Start write tool data  
                if (( not self._writeToolData.Busy  ) and 
                    ( not self._writeToolData.Error )):
                
                    # set command parameter
                    self._writeToolData.ParCmd.ToolNo   = copy.deepcopy(_rSyncIdx) 
                    self._writeToolData.ParCmd.ToolData = copy.deepcopy(ToolData[_rSyncIdx].Data)
                    # execute command
                    self._writeToolData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeToolData.Error) : 

                        self.ErrorID     = self._writeToolData.ErrorID
                        self.ErrorAddTxt = self._writeToolData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5:
                # Wait tool data written ?   
                if (( not self._writeToolData.Busy  ) and
                    ( not self._writeToolData.Error ) and
                    (     self._writeToolData.Done  )):
                
                    # execute command
                    self._writeToolData.Execute = False
                    # apply tool data to internal tool data
                    self._toolData[_rSyncIdx] = copy.deepcopy(ToolData[_rSyncIdx])
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.Tool[_rSyncIdx] = False
                    # dec count of unsynchronised tools
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool -= 1
                    # set timeout        
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= - 2
                else:
                    # check error ? 
                    if (self._writeToolData.Error) : 
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           
                    
                    
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------                    
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION) :
                
                    return                

                # reset count of unsynchronised tools
                AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0

                # Check all tool datas
                for _rSyncIdx in range(0, AxesGroup.State.UnifiedToolIndex):
                
                    # compare tool data
                    AxesGroup.State.DataChanged.Tool[_rSyncIdx] = not IsToolDataEqual( Data1 = ToolData[_rSyncIdx].Data, Data2 = self._toolData[_rSyncIdx].Data, IgnoreTimestamp = False)

                    # Check Tool data changed ? 
                    if (AxesGroup.State.DataChanged.Tool[_rSyncIdx]) : 
                        # inc count of unsynchronised plc tools
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool += 1
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncToolData: Detected a local change of Tool[{1}] on PLC, SyncTime = {2}',
                            Para1       =  str(_rSyncIdx),    
                            Para2       =  SyncTime.AFTER_START_UP.toString()
                        )

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Tool = (AxesGroup.State.SyncStatePlc.UnSyncNo.Tool == 0)


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.Tool ) ^ # ^ = xor
                    ( not AxesGroup.State.SyncStateRc .InSync.Tool )):
                
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] :

                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass  # no further action 

                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11

                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12

                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13

                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.Tool ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.Tool )):
 
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Tool ):

                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedToolIndex):
                    
                        if ( AxesGroup.State.DataChanged.Tool[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Tool ) : 

                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10

                
            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Tool ) : 
                
                    # search for changed index  
                    for _rSyncIdx in range(0 , AxesGroup.State.UnifiedToolIndex ) : 
                    
                        if ( AxesGroup.State.DataChanged.Tool[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 20 # -> read RC data and write it to PLC
                            break

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Tool ) : 
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.Tool ) :
                
                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedToolIndex):
                    
                        if ( AxesGroup.State.DataChanged.Tool[_rSyncIdx] ) : 
                        
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC                  
                            
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.Tool ) :
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return
                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                # _rStep := 10;


            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readToolData.Busy  ) and
                    ( not self._readToolData.Error )):
                    # set command parameter
                    self._readToolData.ParCmd.ToolNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readToolData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readToolData.Error):
                        
                        self.ErrorID     = self._readToolData.ErrorID
                        self.ErrorAddTxt = self._readToolData.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 21 : 
                
                if (( not self._readToolData.Busy  ) and
                    ( not self._readToolData.Error ) and
                    (     self._readToolData.Done  )):
                
                    # reset execution
                    self._readToolData.Execute = False
                    # update internal tool data
                    ToolData[_rSyncIdx].Data = copy.deepcopy( self._readToolData.OutCmd.ToolData)
                    self._toolData[_rSyncIdx].Data = copy.deepcopy( self._readToolData.OutCmd.ToolData)
                    # set available bit
                    ToolData[_rSyncIdx].Available = True                    
                    self._toolData[_rSyncIdx].Available = True
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readToolData.Error):
                        
                        self.ErrorID     = self._readToolData.ErrorID
                        self.ErrorAddTxt = self._readToolData.ErrorAddTxt
                        # reset available bit
                        ToolData[_rSyncIdx].Available = False
                        self._toolData[_rSyncIdx].Available = False
                    
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeToolData.Busy  ) and 
                    ( not self._writeToolData.Error )):

                    # set command parameter
                    self._writeToolData.ParCmd.ToolNo   = copy.deepcopy(_rSyncIdx)
                    self._writeToolData.ParCmd.ToolData = copy.deepcopy(ToolData[_rSyncIdx].Data)
                    # execute command
                    self._writeToolData.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeToolData.Error):
                    
                        self.ErrorID     = self._writeToolData.ErrorID
                        self.ErrorAddTxt = self._writeToolData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 :
               
                if (( not self._writeToolData.Busy  ) and
                    ( not self._writeToolData.Error ) and
                    (     self._writeToolData.Done  )):
                   
                    # execute command
                    self._writeToolData.Execute = False      
                    # update internal tool data
                    self._toolData[_rSyncIdx] = copy.deepcopy(ToolData[_rSyncIdx])
                    # set available bit
                    ToolData[_rSyncIdx].Available = True 
                    self._toolData[_rSyncIdx].Available = True         
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup;           

                else:

                    # check error ? 
                    if (self._writeToolData.Error):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    
                        # reset available bit
                        ToolData[_rSyncIdx].Available = False
                        self._toolData[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                
                
            case _:
                
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))
    

    #------------------------------------------------------------
    # HandleSyncWorkArea - handle work area synchronisation
    #------------------------------------------------------------
    def HandleSyncWorkArea(self, AxesGroup : AxesGroup, WorkAreas : list[RobotWorkArea]) -> None:
        """Handle work area synchronisation."""

        #region local variables
        
        # Internal step counter name
        _stepName        : str
        # Internal reference to step counter
        _rStep           : int
        # Internal reference to timer
        _rTimer          : TON
        # Internal reference to timeout
        _rTimeout        : TIME
        # Internal reference to synchroniztion index
        _rSyncIdx        : int
        # internal bit for condition found
        _found           : bool
        # empty data set to reset all DataChanged bits
        _dataChangedNone : AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx             : int

        #endregion

        # Set internal references 
        _stepName    =   '_stepSyncWorkArea = '
        _rStep       = self._stepSyncWorkArea
        _rTimer      = self._timerSyncWorkArea
        _rTimeout    = self._timeoutSyncWorkArea
        _rSyncIdx    = self._syncIdxWorkArea

        match _rStep : 
        
            case 0: 
                
                # Check initialisation configured ?
                if (( self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION ) and
                    ( self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime. AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION )) : 

                    return

                # wait for initialisation done
                if ((     AxesGroup.State.RobotData.RCSupportedFunctions. ReadWorkArea ) and
                    (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteWorkArea ) and
                    (     AxesGroup.State.Initialized                                  ) and 
                    ( not self.Error                                                   )) :

                    # Check PLC work areas < RC work areas and SyncWorkArea enabled ?    
                    if (( AxesGroup.State.DataEnableSync.EnableSyncWorkArea                                            )  and
                        ( AxesGroup.Parameter.Rob.Parameter.HighestWorkAreaIndex > AxesGroup.SystemData.WorkAreasCount )) :
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_ARRAY_TOO_SHORT, Overwrite = True)

                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Start initial reading of WorkArea from RC',
                        Para1       =  ''
                    )
                    
                    # init work area number
                    _rSyncIdx = AxesGroup.SystemData.WorkAreasMin
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1


            case 1:

                # Start read WorkArea
                if (( not self._readWorkArea.Busy  ) and 
                    ( not self._readWorkArea.Error ) and
                    ( not self._readWorkArea.Done  )) :

                    # set command parameter
                    self._readWorkArea.ParCmd.WorkAreaNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if ( self._readWorkArea.Error ) :
                    
                        self.SetWarning ( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = False)           

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) : 

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 2:

                # Wait WorkArea read
                if (( not self._readWorkArea.Busy  ) and
                    ( not self._readWorkArea.Error ) and
                    (     self._readWorkArea.Done  )):
                    
                    # reset execution
                    self._readWorkArea.Execute = False
                    # set available bit
                    self._workAreas[_rSyncIdx].Available = True
                    WorkAreas[_rSyncIdx].Available = True
                    # Copy data
                    self._workAreas[_rSyncIdx].Data = copy.deepcopy(self._readWorkArea.OutCmd.WorkAreaData)

                    # Check work area data is equal ? 
                    if ( not IsWorkAreaEqual( Data1 = self._workAreas[_rSyncIdx].Data, Data2 = WorkAreas[_rSyncIdx].Data, IgnoreTimestamp = True)) :
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.WorkArea = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] = True
                        # inc count of unsynchronised plc work areas
                        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea += 1
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncWorkArea: Detected a difference in WorkArea[{1}] between PLC and RC',
                            Para1       =  str(_rSyncIdx)
                        )

                        # Check synchronisation is enabled ? 
                        if ( not AxesGroup.State.DataEnableSync.EnableSyncWorkArea ) : 

                            self.SetInfo( InfoID = RobotLibraryInfoIdEnum.INFO_SYNC_WORK_AREA_DISABLED, Overwrite = False)

                        # Check user interaction needed ?  
                        if ( AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.WorkAreas ) :

                            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_NUMBER_SYNC_ERROR, Overwrite = False)                    

                    # Check all work areas read ? 
                    if ( _rSyncIdx < AxesGroup.State.UnifiedWorkAreaIndex ) : 

                        # set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc work area index
                        _rSyncIdx +=1
                        # dec step counter
                        _rStep -=1
                    else:
                        #set timeout
                        SetTimeout(PT = _rTimeout, Timer = _rTimer)
                        # inc step counter
                        _rStep += 1

                else:
                    # check error ? 
                    if (self._readWorkArea.Error) :

                        # Set warning
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)                    
                        # reset available bit
                        WorkAreas[_rSyncIdx].Available = False
                        self._workAreas[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 3:
                
                # Check synchronisation state ? 
                if (( AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea                                             == 0                           ) or 
                    ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION )):

                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = (AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea == 0)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup
                            
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization Startup Phase done',
                        Para1       =  '' 
                    )
                    
                else: 
                    # Check user interaction needed ? 
                    if ( not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.WorkAreas ) :
                    
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] :
                            
                            case SyncMode.SERVER_TO_CLIENT : 

                                for _idx in range(AxesGroup.SystemData.WorkAreasMin, AxesGroup.SystemData.WorkAreasMax) : 

                                    # Overwrite PLC data with RC data
                                    WorkAreas[_idx] = copy.deepcopy(self._workAreas[_idx])

                                # Reset data changed flags
                                AxesGroup.State.DataChanged.WorkArea = _dataChangedNone.WorkArea
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.WorkArea = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.WorkArea = True
                                # Reset count of unsynchronised plc work areas
                                AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                                # set timeout
                                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                # inc step counter
                                _rStep = 10 # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncWorkArea: Synchronization of WorkArea triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                                    Para1       =  str(_rSyncIdx),
                                    Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP].toString(),
                                    Para3       =  SyncTime.DURING_START_UP.toString()
                                )
                                
                                # Create log entry
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'SyncWorkArea: Applied the initial read work area data from RC',
                                    Para1       =  '' 
                                )


                            case SyncMode.CLIENT_TO_SERVER :

                                # Check conflicts to solve ? 
                                for _rSyncIdx in range(0, AxesGroup.State.UnifiedWorkAreaIndex):
                            
                                    if ( AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] ) :
                                    
                                        _found = True
                                        break

                                if ( _found ) :
                                
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.WorkArea = True
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = _rStep + 1  # -> write PLC data to RC                  
                                    # Create log entry
                                    self.CreateLogMessage( 
                                        Timestamp   = self.SystemTime,
                                        MessageType = MessageType.CMD,
                                        Severity    = Severity.DEBUG,
                                        MessageCode = 0,
                                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                                        Para1       = str(_rSyncIdx),
                                        Para2       = AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP].toString(),
                                        Para3       = SyncTime.DURING_START_UP.toString()
                                    )
                                    
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.WorkArea = _dataChangedNone.WorkArea
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.WorkArea = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = True
                                    # Reset count of unsynchronised work areas
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                                    # set timeout
                                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                                    # inc step counter
                                    _rStep = 10 # -> jump to after startup                  


                            case _:
                                # invalid sync mode for startup
                                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite = True )


            case 4:

                # Start write work area data  
                if (( not self._writeWorkArea.Busy  ) and 
                    ( not self._writeWorkArea.Error )):
                
                    # set command parameter
                    self._writeWorkArea.ParCmd.WorkAreaNo   = copy.deepcopy(_rSyncIdx) 
                    self._writeWorkArea.ParCmd.WorkAreaData = copy.deepcopy(WorkAreas[_rSyncIdx].Data)
                    # execute command
                    self._writeWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeWorkArea.Error) : 

                        self.ErrorID     = self._writeWorkArea.ErrorID
                        self.ErrorAddTxt = self._writeWorkArea.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 5:
                # Wait work area data written ?   
                if (( not self._writeWorkArea.Busy  ) and
                    ( not self._writeWorkArea.Error ) and
                    (     self._writeWorkArea.Done  )):
                
                    # execute command
                    self._writeWorkArea.Execute = False
                    # apply work area data to internal work area data
                    self._workAreas[_rSyncIdx] = copy.deepcopy(WorkAreas[_rSyncIdx])
                    # reset data changed bit 
                    AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] = False
                    # dec count of unsynchronised work areas
                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea -= 1
                    # set timeout        
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # dec step counter
                    _rStep -= - 2
                else:
                    # check error ? 
                    if (self._writeWorkArea.Error) : 
                    
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)           
                    
                    
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                    
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            # --------------------------------------------
            # SyncMode after startup : 
            # --------------------------------------------                    
            case 10 :
                # check synchronisation active ? 
                if ( AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION) :
                
                    return                

                # reset count of unsynchronised work areas
                AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0

                # Check all work area datas
                for _rSyncIdx in range(0, AxesGroup.State.UnifiedWorkAreaIndex):
                
                    # compare work area data
                    AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] = not IsWorkAreaEqual( Data1 = WorkAreas[_rSyncIdx].Data, Data2 = self._workAreas[_rSyncIdx].Data, IgnoreTimestamp = False)

                    # Check WorkArea data changed ? 
                    if (AxesGroup.State.DataChanged.WorkArea[_rSyncIdx]) : 
                        # inc count of unsynchronised plc work areas
                        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea += 1
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'SyncWorkArea: Detected a local change of WorkArea[{1}] on PLC, SyncTime = {2}',
                            Para1       =  str(_rSyncIdx),    
                            Para2       =  SyncTime.AFTER_START_UP.toString()
                        )

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = (AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea == 0)


                # Check synchronization is needed ? 
                if (( not AxesGroup.State.SyncStatePlc.InSync.WorkArea ) ^ # ^ = xor
                    ( not AxesGroup.State.SyncStateRc .InSync.WorkArea )):
                
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] :

                        case SyncMode.NO_SYNCHRONIZATION : 
                            pass  # no further action 

                        case SyncMode.CLIENT_TO_SERVER :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 11

                        case SyncMode.SERVER_TO_CLIENT :
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 12

                        case SyncMode.AUTOMATIC : 
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 13

                else:
                    # datas changeḍ on both sides ? -> Warning 
                    if (( not AxesGroup.State.SyncStatePlc.InSync.WorkArea ) and  
                        ( not AxesGroup.State.SyncStateRc .InSync.WorkArea )):
 
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_BOTH_SIDES_CHANGED, Overwrite = True)


            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER 
            # ------------------------------------------  
            case 11 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.WorkArea ):

                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedWorkAreaIndex):
                    
                        if ( AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.WorkArea ) : 

                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 30 # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return

                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10

                
            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT 
            # ------------------------------------------
            case 12 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.WorkArea ) : 
                
                    # search for changed index  
                    for _rSyncIdx in range(0 , AxesGroup.State.UnifiedWorkAreaIndex ) : 
                    
                        if ( AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] ):
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 20 # -> read RC data and write it to PLC
                            break

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.WorkArea ) : 
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                _rStep = 10


            # ------------------------------------------
            # SyncMode : AUTOMATIC 
            # ------------------------------------------
            case 13 : 
                
                # Conflict triggerd by PLC ?  
                if ( not AxesGroup.State.SyncStatePlc.InSync.WorkArea ) :
                
                    # search for changed index  
                    for _rSyncIdx in range(0, AxesGroup.State.UnifiedWorkAreaIndex):
                    
                        if ( AxesGroup.State.DataChanged.WorkArea[_rSyncIdx] ) : 
                        
                            # set timeout
                            SetTimeout(PT = _rTimeout, Timer = _rTimer)
                            # inc step counter
                            _rStep = 30 # -> write PLC data to RC                  
                            
                            break


                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    return


                # Conflict triggered by RC ?
                if ( not AxesGroup.State.SyncStateRc.InSync.WorkArea ) :
                
                    # get changed index 
                    _rSyncIdx = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 20 # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC',
                        Para1       =  str(_rSyncIdx),
                        Para2       =  AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP].toString(),
                        Para3       =  SyncTime.AFTER_START_UP.toString()
                    )
                    
                    return
                
                # set timeout
                SetTimeout(PT = _rTimeout, Timer = _rTimer)
                # jump back
                # _rStep := 10;


            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20 :
                
                if (( not self._readWorkArea.Busy  ) and
                    ( not self._readWorkArea.Error )):
                    # set command parameter
                    self._readWorkArea.ParCmd.WorkAreaNo = copy.deepcopy(_rSyncIdx)
                    # execute command
                    self._readWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._readWorkArea.Error):
                        
                        self.ErrorID     = self._readWorkArea.ErrorID
                        self.ErrorAddTxt = self._readWorkArea.ErrorAddTxt
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 21 : 
                
                if (( not self._readWorkArea.Busy  ) and
                    ( not self._readWorkArea.Error ) and
                    (     self._readWorkArea.Done  )):
                
                    # reset execution
                    self._readWorkArea.Execute = False
                    # update internal work area data
                    WorkAreas[_rSyncIdx].Data = copy.deepcopy( self._readWorkArea.OutCmd.WorkAreaData)
                    self._workAreas[_rSyncIdx].Data = copy.deepcopy( self._readWorkArea.OutCmd.WorkAreaData)
                    # set available bit
                    WorkAreas[_rSyncIdx].Available = True                    
                    self._workAreas[_rSyncIdx].Available = True
                    
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10  # -> jump to after startup           
                else:
                    # check error ? 
                    if (self._readWorkArea.Error):
                        
                        self.ErrorID     = self._readWorkArea.ErrorID
                        self.ErrorAddTxt = self._readWorkArea.ErrorAddTxt
                        # reset available bit
                        WorkAreas[_rSyncIdx].Available = False
                        self._workAreas[_rSyncIdx].Available = False
                    
                
                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                


            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30 :
                
                if (( not self._writeWorkArea.Busy  ) and 
                    ( not self._writeWorkArea.Error )):

                    # set command parameter
                    self._writeWorkArea.ParCmd.WorkAreaNo   = copy.deepcopy(_rSyncIdx)
                    self._writeWorkArea.ParCmd.WorkAreaData = copy.deepcopy(WorkAreas[_rSyncIdx].Data)
                    # execute command
                    self._writeWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep += 1
                else:
                    # check error ? 
                    if (self._writeWorkArea.Error):
                    
                        self.ErrorID     = self._writeWorkArea.ErrorID
                        self.ErrorAddTxt = self._writeWorkArea.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))


            case 31 :
               
                if (( not self._writeWorkArea.Busy  ) and
                    ( not self._writeWorkArea.Error ) and
                    (     self._writeWorkArea.Done  )):
                   
                    # execute command
                    self._writeWorkArea.Execute = False      
                    # update internal work area data
                    self._workAreas[_rSyncIdx] = copy.deepcopy(WorkAreas[_rSyncIdx])
                    # set available bit
                    WorkAreas[_rSyncIdx].Available = True 
                    self._workAreas[_rSyncIdx].Available = True         
                    # set timeout
                    SetTimeout(PT = _rTimeout, Timer = _rTimer)
                    # inc step counter
                    _rStep = 10 # -> jump to after startup;           

                else:

                    # check error ? 
                    if (self._writeWorkArea.Error):
                        
                        self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite = True)    
                        # reset available bit
                        WorkAreas[_rSyncIdx].Available = False
                        self._workAreas[_rSyncIdx].Available = False


                    # timeout exceeded ? 
                    if (CheckTimeout(_rTimer) == OK):
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT(_stepName, str(_rStep))
                
                
            case _:
                
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT(_stepName , str(_rStep))


    #------------------------------------------------------------
    # HandleTelegramStateCtrl - handle telegram state and control changes
    #------------------------------------------------------------
    def HandleTelegramStateCtrl(self) -> None:
        """Handle Telegram State Control"""

        # Telegram Control
        # ----------------
        if ( self._lastTelegramControl != GetHalfeByteLo(self.Telegram.PlcToRob.Header.AxesGroupID_Control)):
        
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'SRCI Interface control changed from {1} to {2}',
                Para1       = self._lastTelegramControl.toString(),
                Para2       = str(ControlHalfByte(GetHalfeByteLo(self.Telegram.PlcToRob.Header.AxesGroupID_Control.value).value).toString())
            )


            self._lastTelegramControl = ControlHalfByte(GetHalfeByteLo(self.Telegram.PlcToRob.Header.AxesGroupID_Control).value)


        # Telegram State
        # ----------------
        if ( self._lastTelegramState != self.Telegram.RobToPlc.Header.TelegramState):
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.INFO,
                MessageCode = 0,
                MessageText = 'SRCI Interface state changed from {1} to {2}',
                Para1       = self._lastTelegramState.toString(),
                Para2       = self.Telegram.RobToPlc.Header.TelegramState.toString()
        )


        # Check Interface changed after being initialized ?  
        if ((  self.Initialized or self.Synchronized                                                 ) and
            (  self._lastTelegramState                     == TelegramState.INITIALIZED              ) and  
           ((  self.Telegram.RobToPlc.Header.TelegramState == TelegramState.READY_FOR_INITIALIZATION ) or
            (  self.Telegram.RobToPlc.Header.TelegramState == TelegramState.READY_TO_RESUME          ))) :

            # ToDo 
            #SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7  , Overwrite := TRUE );
            # apply new telegram state
            self._lastTelegramState = self.Telegram.RobToPlc.Header.TelegramState


    #------------------------------------------------------------
    # HandleUserData - handle user data
    #------------------------------------------------------------
    def HandleUserData(self, AxesGroup : AxesGroup, UserData : UserDataStruct) -> None: #noqa: F811

        # Common
        UserData.LogLevel                                = self.LogLevel

        UserData.PLCManufacturedID                       = self._parCfg.Plc.Parameter.ManufacturedID.value
        UserData.PLCOrderID                              = self._parCfg.Plc.Parameter.OrderID.toString()
        UserData.PLCSerialNumber                         = self._parCfg.Plc.Parameter.SerialNumber.toString()
        UserData.PLCFirmwareVersion                      = self._parCfg.Plc.Parameter.FirmwareVersion.toString()
        UserData.PLCInterfaceVersion                     = self._parCfg.Plc.Parameter.InterfaceVersion.toString() 
        UserData.PLCLibraryVersion                       = PLCLibraryVersion

        # Communication                                 
        UserData.LifeSignTimeOut                         = self._parCfg.Com.LifeSignTimeOut

        # Plc Parameter                                 
        UserData.SynchronizationModes                    = self._parCfg.Plc.Parameter.SynchronizationModes
        UserData.EnableSync                              =  SyncModesToDataEnableSync(Value = self._parCfg.Plc.Parameter.SynchronizationModes)

        # Robot Parameter                               
        UserData.DelayTime                               = self._parCfg.Rob.Parameter.DelayTime
        UserData.WaitForNrOfCmd                          = self._parCfg.Rob.Parameter.WaitForNrOfCmd
        UserData.WaitAtBlendingZone                      = self._parCfg.Rob.Parameter.WaitAtBlendingZone
        UserData.AllowSecSeqWhileSubprogram              = self._parCfg.Rob.Parameter.AllowSecSeqWhileSubprogram
        UserData.AllowDynamicBlending                    = self._parCfg.Rob.Parameter.AllowDynamicBlending
        UserData.SyncReaction                            = self._parCfg.Rob.Parameter.SyncReaction
        UserData.SyncDelay                               = self._parCfg.Rob.Parameter.SyncDelay
        UserData.MessageLevel                            = self._parCfg.Rob.Parameter.MessageLevel

        # ReadRobotData      
        UserData.RCManufacturer                          = AxesGroup.State.RobotData.RCManufacturer.toString()
        UserData.RCOrderID                               = AxesGroup.State.RobotData.RCOrderID.toString()
        UserData.RCSerialNumber                          = AxesGroup.State.RobotData.RCSerialNumber.toString()
        UserData.RASerialNumber                          = AxesGroup.State.RobotData.RASerialNumber.toString()
        UserData.RCFirmwareVersion                       = AxesGroup.State.RobotData.RCFirmwareVersion.toString()

        _ver = AxesGroup.State.RobotData.RCInterpreterVersion.toString()
        _maj = int(_ver[0]) if len(_ver) >= 1 and _ver[0].isdigit() else 0
        _min = int(_ver[1]) if len(_ver) >= 2 and _ver[1].isdigit() else 0
        _pat = int(_ver[2]) if len(_ver) >= 3 and _ver[2].isdigit() else 0
        UserData.RCInterpreterVersion.MajorVersion.value = _maj
        UserData.RCInterpreterVersion.MinorVersion.value = _min
        UserData.RCInterpreterVersion.PatchVersion.value = _pat

        UserData.AxisJointUsed                           = AxesGroup.State.RobotData.AxisJointUsed
        UserData.AxisExternalUsed                        = AxesGroup.State.RobotData.AxisExternalUsed
        UserData.AxisJointUnit                           = AxesGroup.State.RobotData.AxisJointUnit
        UserData.AxisExternalUnit                        = AxesGroup.State.RobotData.AxisExternalUnit
        UserData.RCSupportedFunctions                    = AxesGroup.State.RobotData.RCSupportedFunctions

        UserData.BrakeTestRequired                       = AxesGroup.State.ConfigurationData.BrakeTestRequired
        UserData.PathAccuracyMode                        = AxesGroup.State.ConfigurationData.PathAccuracyMode
        UserData.AvoidSingularity                        = AxesGroup.State.ConfigurationData.AvoidSingularity
        UserData.ConstantVelocitySupported               = AxesGroup.State.ConfigurationData.ConstantVelocitySupported
        UserData.StepModeExactStopActive                 = AxesGroup.State.ConfigurationData.StepModeExactStopActive
        UserData.StepModeBlendingActive                  = AxesGroup.State.ConfigurationData.StepModeBlendingActive
        UserData.AcceleratingSupported                   = AxesGroup.State.ConfigurationData.AcceleratingSupported
        UserData.DeceleratingSupported                   = AxesGroup.State.ConfigurationData.DecceleratingSupported
      
        UserData.Initialized                             = self.Initialized
        UserData.Synchronized                            = self.Synchronized

        # Cyclic data                             
        UserData.RCSRCIVersion                           = AxesGroup.Cyclic.RobToPlc.SRCIVersion
        UserData.IsMoving                                = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.IsMoving.value
        UserData.PrimarySequencePaused                   = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.PrimarySequencePaused.value
        UserData.InPrimaryPos                            = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.InPrimaryPos.value
        UserData.SecondarySequenceActive                 = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.SecondarySequenceActive.value
        UserData.ErrorPending                            = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.ErrorPending.value
        UserData.RestartInProgress                       = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RestartInProgress.value
        UserData.Enabled                                 = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Enabled.value
        UserData.Idle                                    = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.IDLE
        UserData.Executing                               = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.EXECUTING
        UserData.Interrupted                             = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.INTERRUPTED
        UserData.IsBlending                              = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.IsBlending.value  
        UserData.OperationMode                           = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.OperationMode
        UserData.CollisionDetectionEnabled               = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.CollisionDetectedEnabled.value
        UserData.CollisionDetected                       = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.CollisionDetected.value
        UserData.RestartRequested                        = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RestartRequested.value
        UserData.Accelerating                            = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Accelerating.value
        UserData.Decelerating                            = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Decelerating.value
        UserData.ConstantVelocity                        = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.ConstantVelocity.value
        UserData.ActualOverride                          = PERCENT_UINT_TO_REAL( Value = AxesGroup.Cyclic.RobToPlc.Override, IsOptional = False).value

        # Cyclic optional data
        UserData.CartesianPosition                       = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition
        UserData.ExtCartesianPosition                    = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt
        UserData.JointPosition                           = AxesGroup.CyclicOptional.RobToPlc.JointPosition
        UserData.ExtJointPosition                        = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt

        # Synchronizing
        UserData.ToolDataSynchronizing                   = AxesGroup.State.Synchronizing.Tool
        UserData.FrameDataSynchronizing                  = AxesGroup.State.Synchronizing.Frame
        UserData.LoadDataSynchronizing                   = AxesGroup.State.Synchronizing.Load
        UserData.WorkAreaDataSynchronizing               = AxesGroup.State.Synchronizing.WorkAreas
        UserData.SWLimitsSynchronizing                   = AxesGroup.State.Synchronizing.SwLimits
        UserData.DefaultDynamicsSynchronizing            = AxesGroup.State.Synchronizing.DefaultDynamics
        UserData.ReferenceDynamicsSynchronizing          = AxesGroup.State.Synchronizing.ReferenceDynamics


        UserData.ActivateTwoSequences                    = self._parCfg.Com.TwoSequences
        UserData.ReadingCartesianPosition                = AxesGroup.State.ReadingCartesianPosition
        UserData.ReadingExtCartesianPosition             = AxesGroup.State.ReadingCartesianPositionExt
        UserData.ReadingJointPosition                    = AxesGroup.State.ReadingJointPosition
        UserData.ReadingExtJointPosition                 = AxesGroup.State.ReadingJointPositionExt


    #------------------------------------------------------------
    # HasError - check for error
    #------------------------------------------------------------
    @property
    def HasError(self) -> bool:
        """Returns TRUE if an error is present."""
        return self.ErrorID != OK


    #------------------------------------------------------------
    # HasWarning - check for warning    
    #------------------------------------------------------------
    @property
    def HasWarning(self) -> bool:
        """Returns TRUE if a warning is present."""
        return self.WarningID != OK


    #------------------------------------------------------------
    # HasInfo - check for info    
    #------------------------------------------------------------
    @property
    def HasInfo(self) -> bool:
        """Returns TRUE if an info is present."""
        return self.InfoID != OK


    # --------------------------------------------------------------
    # OnCall - cyclic method
    # ---------------------------------------------------------------
    def OnCall(self, AxesGroup: AxesGroup) -> None:
        """OnCall method called cyclically"""
        
        # map numeric value to enum, so that the corresponding message text is directly shown by the tooltip
        self.ErrorIdEnum   = RobotLibraryErrorIdEnum  (self.ErrorID  )
        self.WarningIdEnum = RobotLibraryWarningIdEnum(self.WarningID)
        self.InfoIdEnum    = RobotLibraryInfoIdEnum   (self.InfoID   )

        self.Error = self.HasError

        # Check Payload and In/Out data size
        if (( self.ROBOT_IN_DATA_SIZE  < 64 ) or
            ( self.ROBOT_OUT_DATA_SIZE < 64 )) : 

            self.SetError(ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_LIBRARY_PARA, Overwrite = True )
            return


        # Check AxesGroupID valid
        if (( self.AxesGroupID < AXES_GROUP_ID_MIN ) or
            ( self.AxesGroupID > AXES_GROUP_ID_MAX )):
            
            self.SetError(ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_AXES_GROUP_ID, Overwrite = True )
            return


        # Reset flag for initialization / Synchronization
        if ( self.Initialized or self.Synchronized) and ( AxesGroup.Cyclic.RobToPlc.TelegramState != TelegramState.INITIALIZED):

            # Reset initialized flag
            self.Initialized = False
            # Reset Synchronized flag
            self.Synchronized = False
            # Set error 
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0x80A2, Overwrite = True )


        # Warning for ACR Registers running low
        if ( AxesGroup.Acyclic.ActiveCommandRegister.CurrentAcrUsagePercent > ACR_USAGE_WARNING_LIMIT ) :

            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_ACR_FREE_ENTRIES_LOW, Overwrite = True)  


        # Check ToolData boundary
        if ( AxesGroup.SystemData.ToolDataMin  != 0 ) :

            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite = False )


        # Check FrameData boundary
        if ( AxesGroup.SystemData.FrameDataMin != 0 ) and ( not self.HasWarning ) :

            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite = False )


        # Check WorkAreas boundary
        if ( AxesGroup.SystemData.WorkAreasMin != 0 ) and ( not self.HasWarning ) :

            self.SetWarning( WarningID = RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite = False )


        # Check configuration parameter changed ? 
        self.CheckParameterChanged(AxesGroup := AxesGroup)


    # --------------------------------------------------------------
    # OnExecRun - cyclic method in RUN state
    # ---------------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup) -> int:
        """OnExecRun method called cyclically when in RUN state"""

        # building rising and falling edges
        self._enable_R( CLK = self.Enable)
        self._enable_F( CLK = self.Enable)

        if ( self._enable_F.Q):
        
            self.Reset(AxesGroup = AxesGroup)


        OnExecRun = RUNNING


        match self._stepCmd :
        
            case 0:
                
                if ( self._enable_R.Q ) : 
                
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.INFO,
                        MessageCode = 0,
                        MessageText = 'Robot Task Enabled'
                    )

                    # reset the rising edge
                    self._enable_R()
                    # set busy flag
                    self.Busy = True
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # Reset FastStop       
                    AxesGroup.Cyclic.PlcToRob.FastStop.value = 0
                    # Reset Active command register
                    AxesGroup.Acyclic.ActiveCommandRegister.Reset()
                
                    # check parameter valid
                    if ( self.CheckParameterValid(AxesGroup = AxesGroup) ):
                        # take configuration parameter if not yet enabled
                        self._parCfg = copy.deepcopy(self.ParCfg)
                        # inc step counter
                        self._stepCmd += 1


            case 1:

                match AxesGroup.Cyclic.RobToPlc.TelegramState :

                    case TelegramState.UNDEFINED : 
                        pass

                    case ( TelegramState.ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE |
                           TelegramState.ERROR_162_INIT_LOST_UNKNOWN                        |
                           TelegramState.ERROR_163_TELEGRAM_LENGTH_MISMATCH                 |
                           TelegramState.ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE          |
                           TelegramState.ERROR_165_LIFESIGN_TIMEOUT                         |
                           TelegramState.ERROR_166_CYCLIC_DATA_TOO_LARGE                    |
                           TelegramState.ERROR_167_INTERFACE_WAS_RESET_AFTER_INIT           |
                           TelegramState.ERROR_168_TELEGRAM_SEQ_TIMEOUT                     |
                           TelegramState.ERROR_169_TELEGRAM_NO_CHANGED_AFTER_INIT           |
                           TelegramState.ERROR_170_AXESGROUP_ID_INVALID                     |
                           TelegramState.ERROR_171_TELEGRAM_NUMBER_INVALID                  |
                           TelegramState.ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED            ) :

                        # clear error
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.ACK_ERROR
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESET # always a reset, so that on the robot side the ACR is reseted

                    case TelegramState.ERROR_173_SERVER_CONNECTION_LOST:

                        # Reset interface including the ACR register on server side
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESET

                    case TelegramState.READY_TO_RESUME :

                        # Resume
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESUME

                    case TelegramState.READY_FOR_INITIALIZATION: 

                        # Request initialization
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.INITIALIZE

                    case TelegramState.INITIALIZED: 

                        # Reset Telegram Control 
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.NONE

                        # Check SRCI Version is compatible ? 
                        if ( AxesGroup.Cyclic.RobToPlc.SRCIVersion.MajorVersion == SRCIVersion.MajorVersion ):

                            # set timeout
                            SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                            # inc step counter
                            self._stepCmd += 1
                        else:
                            # set error 
                            self.SetError(ErrorID = RobotLibraryErrorIdEnum.ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0x80A4, Overwrite = True)
                            self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))
                            return OnExecRun

                    case _:
                        # TelegrammState in error
                        self.SetError(ErrorID = RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0xA2, Overwrite = True)
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))
                        return


                # timeout exceeded ? 
                if (CheckTimeout(self._timerCmd) == OK) :
                
                    # Check Telegram State error ? 
                    if (( AxesGroup.Cyclic.RobToPlc.TelegramState >= TelegramState.ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE ) or
                        ( AxesGroup.Cyclic.RobToPlc.TelegramState <= TelegramState.ERROR_173_SERVER_CONNECTION_LOST                   )) : 

                        self.ErrorID     = AxesGroup.Cyclic.RobToPlc.TelegramState
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))
                    else:
                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))

            case 2: 

                if (( not self._readMessages.Busy  ) and 
                    ( not self._readMessages.Error )) :

                    # start function block
                    self._readMessages.Enable = True
                    self._readMessages.ParCmd.MsgID = 0
                    self._readMessages.ParCmd.MessageLevel = self._parCfg.Rob.Parameter.MessageLevel

                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1
                else:
                    # check error ? 
                    if (self._readMessages.Error):

                        self.ErrorID     = self._readMessages.ErrorID
                        self.ErrorAddTxt = self._readMessages.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))
            
            case 3: 

                if ((     self._readMessages.Enabled ) and
                    ( not self._readMessages.Error   )):

                    # --------------------------------------------------------------- 
                    # ReadMessages must stay active for the Message mechanism !!!
                    # --------------------------------------------------------------- 
                    # ReadMessages.Enable := FALSE;  
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1
                else:
                    # check error ? 
                    if (self._readMessages.Error):

                        self.ErrorID     = self._readMessages.ErrorID
                        self.ErrorAddTxt = self._readMessages.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


            case 4:
                
                if (( not self._exchangeConfiguration.Busy  ) and
                    ( not self._exchangeConfiguration.Error )) :
                
                    # set command parameter
                    self._exchangeConfiguration.ParCmd.LogLevel                           = self.LogLevel 
                    self._exchangeConfiguration.ParCmd.WaitAtBlendingZone                 = self._parCfg.Rob.Parameter.WaitAtBlendingZone
                    self._exchangeConfiguration.ParCmd.AllowSecSeqWhileSubprogram         = self._parCfg.Rob.Parameter.AllowSecSeqWhileSubprogram
                    self._exchangeConfiguration.ParCmd.AllowDynamicBlending               = self._parCfg.Rob.Parameter.AllowDynamicBlending
                    self._exchangeConfiguration.ParCmd.DelayTime                          = self._parCfg.Rob.Parameter.DelayTime
                    self._exchangeConfiguration.ParCmd.WaitForNrOfCmd                     = self._parCfg.Rob.Parameter.WaitForNrOfCmd
                    self._exchangeConfiguration.ParCmd.LifeSignTimeOut                    = self._parCfg.Com.LifeSignTimeOut
                    self._exchangeConfiguration.ParCmd.SyncDelay                          = self._parCfg.Rob.Parameter.SyncDelay
                    self._exchangeConfiguration.ParCmd.SyncReaction                       = self._parCfg.Rob.Parameter.SyncReaction
                    self._exchangeConfiguration.ParCmd.DataEnableSync                     = SyncModesToDataEnableSync(Value = self._parCfg.Plc.Parameter.SynchronizationModes)
                    self._exchangeConfiguration.ParCmd.DataInSync.ToolsInSync             = False
                    self._exchangeConfiguration.ParCmd.DataInSync.FramesInSync            = False
                    self._exchangeConfiguration.ParCmd.DataInSync.LoadsInSync             = False
                    self._exchangeConfiguration.ParCmd.DataInSync.WorkAreasInSync         = False
                    self._exchangeConfiguration.ParCmd.DataInSync.SoftwareLimitsInSync    = False
                    self._exchangeConfiguration.ParCmd.DataInSync.DefaultDynamicsInSync   = False
                    self._exchangeConfiguration.ParCmd.DataInSync.ReferenceDynamicsInSync = False

                    # start function block
                    self._exchangeConfiguration.Enable = True
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1
                else:
                    # check error ? 
                    if (self._exchangeConfiguration.Error):
                        
                        self.ErrorID     = self._exchangeConfiguration.ErrorID
                        self.ErrorAddTxt = self._exchangeConfiguration.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


            case 5: 

                if ((     self._exchangeConfiguration.Enabled ) and
                    ( not self._exchangeConfiguration.Error   )) :

                    # --------------------------------------------------------------------- 
                    # ExchangeConfiguration must stay active for the Sync mechanism !!!
                    # --------------------------------------------------------------------- 
                    # ExchangeConfiguration.Enable := FALSE;  
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1

                else:

                    # check error ? 
                    if (self._exchangeConfiguration.Error) :

                        self.ErrorID     = self._exchangeConfiguration.ErrorID
                        self.ErrorAddTxt = self._exchangeConfiguration.ErrorAddTxt


                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK) :

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


            case 6: 

                if (( not self._readRobotData.Busy  ) and 
                    ( not self._readRobotData.Error )) :
                    # start function block
                    self._readRobotData.Execute = True
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1       
                else:

                    # check error ? 
                    if (self._readRobotData.Error):

                        self.ErrorID     = self._readRobotData.ErrorID
                        self.ErrorAddTxt = self._readRobotData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


            case 7: 

                if ((     self._readRobotData.Done  ) and
                    ( not self._readRobotData.Busy  ) and
                    ( not self._readRobotData.Error )) :

                    # set initialized flag
                    self.Initialized = True       
                    # start function block
                    self._readRobotData.Execute = False
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1
                else:

                    # check error ? 
                    if (self._readRobotData.Error):

                        self.ErrorID     = self._readRobotData.ErrorID
                        self.ErrorAddTxt = self._readRobotData.ErrorAddTxt

                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerCmd) == OK):

                        self.ErrorID     = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


            case 8:
                
                # Update Initialized state
                self.Initialized = not self.Error and not self.Synchronized

                # Wait for task disable
                if ( not self.Enable):
                    # Reset active command register
                    AxesGroup.Acyclic.ActiveCommandRegister.Reset()
                    # reset internal variables
                    self.Reset(AxesGroup = AxesGroup)
                    # Reset step counter
                    self._stepCmd = 0        
                    # finished okay
                    OnExecRun = OK


            case _:
                # invalid step
                self.ErrorID     = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = CONCAT('_stepCmd = ' , str(self._stepCmd))


        return OnExecRun



    # --------------------------------------------------------------
    # ParseRecvPayload - parse received payload
    # ---------------------------------------------------------------
    def ParseRecvPayload(self, AxesGroup: AxesGroup, RobotInData : bytearray) -> None:

        # reset all variables and payload
        self.RecvData.Reset()
        # Call RecvData FB, update payload and size 
        self.RecvData(Payload = RobotInData, PayloadSize = UDINT(self.ROBOT_IN_DATA_SIZE))

        # check new data to receive ? 
        if ( self.Telegram.RobToPlc.Sequence[0].Header.SEQ_ACK != AxesGroup.State.LastACK[0]) : #ToDo: handle 2nd sequence

            # delete old telegram data 
            self.Telegram.RobToPlc = TelegramRobToPlc()


        self.ParseRecvPayloadHeader        ( AxesGroup := AxesGroup)
        self.ParseRecvPayloadCyclic        ( AxesGroup := AxesGroup)
        self.ParseRecvPayloadCyclicOptional( AxesGroup := AxesGroup)
        self.ParseRecvPayloadSequence      ( AxesGroup := AxesGroup)
        self.ParseRecvPayloadFooter        ( AxesGroup := AxesGroup)
        self.ParseRecvPayloadLogging       ( AxesGroup := AxesGroup)

        AxesGroup.State.LastACK[0] = int(self.Telegram.RobToPlc.Sequence[0].Header.SEQ_ACK)
        AxesGroup.State.LastACK[1] = int(self.Telegram.RobToPlc.Sequence[1].Header.SEQ_ACK)


    # --------------------------------------------------------------
    # ParseRecvPayloadCyclic - parse received cyclic payload
    # ---------------------------------------------------------------
    def ParseRecvPayloadCyclic(self, AxesGroup: AxesGroup) -> None:
        """Parse received cyclic payload"""


    #------------------------------------------------------------
    # ParseRecvPayloadCyclicOptional - parse received cyclic optional payload
    #------------------------------------------------------------
    def ParseRecvPayloadCyclicOptional(self, AxesGroup: AxesGroup) -> None:
        """Parse received cyclic optional payload"""

        #region internal variables
        
        # internal index for loops
        _idx : int = 0
        
        #endregion


        #region AxesGroup.OptionalCyclic.RobToPlc.SubProgramData
        if ( AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Active ) :

            for _idx in  range(0,25) : # ToDo: Add contant for DataMax
            
                self.Telegram.RobToPlc.CyclicOptional.SubProgramData.Data[_idx] = self.RecvData.GetByte().value

        #endregion
        
        #region AxesGroup.OptionalCyclic.RobToPlc.CartesianPos
        if ( AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active ) :
            
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.X                    = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Y                    = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Z                    = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rx                   = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Ry                   = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rz                   = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config               = self.RecvData.GetWord()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J2_J1          = self.RecvData.GetByte()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J4_J3          = self.RecvData.GetByte()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J6_J5          = self.RecvData.GetByte()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_E1             = self.RecvData.GetByte()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.E1                   = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.ToolNo               = self.RecvData.GetUsint()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.FrameNo              = self.RecvData.GetUsint()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedToolNo  = self.RecvData.GetUsint()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedFrameNo = self.RecvData.GetUsint()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Reserve_1            = self.RecvData.GetByte()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Reserve_2            = self.RecvData.GetByte()
        #endregion

        #region AxesGroup.OptionalCyclic.RobToPlc.JointPosition
        if ( AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active ) :
            
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J1         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J2         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J3         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J4         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J5         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.J6         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.E1         = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPosition.E1_Reserve = self.RecvData.GetWord()
        #endregion

        #region AxesGroup.OptionalCyclic.RobToPlc.CartesianForce
        if ( AxesGroup.CyclicOptional.RobToPlc.Force.Active ) :
            
            self.Telegram.RobToPlc.CyclicOptional.Force.X  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Force.Y  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Force.Z  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Force.Rx = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Force.Ry = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Force.Rz = self.RecvData.GetReal()
        #endregion
        
        #region AxesGroup.OptionalCyclic.RobToPlc.Current
        if ( AxesGroup.CyclicOptional.RobToPlc.Current.Active ) :
        
            self.Telegram.RobToPlc.CyclicOptional.Current.J1  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Current.J2  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Current.J3  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Current.J4  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Current.J5  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.Current.J6  = self.RecvData.GetReal()
        #endregion

        #region AxesGroup.OptionalCyclic.RobToPlc.CartesianPosExt
        if ( AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active ) :
            
            self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E2 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E3 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E4 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E5 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E6 = self.RecvData.GetReal()
        #endregion
        
        #region AxesGroup.OptionalCyclic.RobToPlc.JointPosition
        if ( AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active ) :
            self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E2 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E3 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E4 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E5 = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E6 = self.RecvData.GetReal()
        #endregion
            
        #region AxesGroup.OptionalCyclic.RobToPlc.CartesianForceExt
        if ( AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active ) :
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E1  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E2  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E3  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E4  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E5  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.ForceExt.E6  = self.RecvData.GetReal()
        #endregion
        
        #region AxesGroup.OptionalCyclic.RobToPlc.CurrentExt
        if ( AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active ) :
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E1  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E2  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E3  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E4  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E5  = self.RecvData.GetReal()
            self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E6  = self.RecvData.GetReal()
        #endregion


    # --------------------------------------------------------------
    # ParseRecvPayloadFooter - parse received payload footer
    # ---------------------------------------------------------------
    def ParseRecvPayloadFooter(self, AxesGroup: AxesGroup) -> None:
        """Parse received payload footer"""

        self.Telegram.RobToPlc.Footer.LifeSign = self.RecvData.GetLifeSignFooter() 


    # --------------------------------------------------------------
    # ParseRecvPayloadHeader - parse received payload header
    # ---------------------------------------------------------------
    def ParseRecvPayloadHeader(self, AxesGroup: AxesGroup) -> None:
        """Parse received payload header"""

        # Version
        self.Telegram.RobToPlc.Header.SRCIVersion    = ByteToVersion(self.RecvData.GetByte())
        # Connection alive signal
        self.Telegram.RobToPlc.Header.LifeSign       = self.RecvData.GetHalfeByte2(IncPayloadPtr = True)
        # Reserved byte
        self.Telegram.RobToPlc.Header.Reserved       = self.RecvData.GetByte()
        # Initialization and Telegram control state
        self.Telegram.RobToPlc.Header.TelegramState  = TelegramState(self.RecvData.GetUsint().value)
        # Combination of various RA related states.
        self.Telegram.RobToPlc.Header.StatusRobotArm = self.RecvData.GetDword()
        # Actual override in percentage encoding 
        self.Telegram.RobToPlc.Header.Override       = self.RecvData.GetUint()


    # --------------------------------------------------------------
    # ParseRecvPayloadSequence - parse received payload sequence
    # ---------------------------------------------------------------
    def ParseRecvPayloadLogging(self, AxesGroup: AxesGroup) -> None:
        """Parse received payload logging data"""

        #region internal variables

        # internal sequence index for loops
        _seqIdx : int = 0
        # internal fragment index for loops
        _fragIdx : int = 0

        #endregion


        return

        for _seqIdx in range(0, AxesGroup.State.SequenceCountRecv):
            # check new data to receive ? 
            if ( self.Telegram.RobToPlc.Sequence[_seqIdx].Header.SEQ_ACK != AxesGroup.State.LastACK[_seqIdx]) :

                # Check sequence payload > 0 ?    
                if (self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength.value > 0):
                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = 'RecvData: ACK = {1}, received Sequence [{2}] with PayloadLength = {3}, Lifesign = {4}',
                        Para1       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Header.SEQ_ACK),
                        Para2       =  str(_seqIdx),
                        Para3       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength),
                        Para4       =  str(self.Telegram.RobToPlc.Header.LifeSign)
                    )

                for _fragIdx in range ( 0,  AxesGroup.State.FragmentCountRecv[_seqIdx] ) :

                    # Check fragment payload > 0 ?    
                    if ( self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > 0 ) :

                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'RecvData: received Fragment [{1}] with PayloadLength = {2}, CmdID <{3}> , CmdState: {4}, Fragment-Action Bits: {5}',
                            Para1       =  str(0), #ToDo 'Add seqIdx'
                            Para2       =  str                      (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength),
                            Para3       =  str                      (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID),
                            Para4       =                            self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.State.toString(),
                            Para5       = FRAGMENT_ACTION_TO_STRING (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction)
                        )

    # --------------------------------------------------------------
    # ParseRecvPayloadSequence - parse received payload sequence
    # ---------------------------------------------------------------
    def ParseRecvPayloadSequence(self, AxesGroup: AxesGroup) -> None:
        """Parse received payload sequence"""

        #region internal variables

        # internal index
        _idx              : int = 0
        # index for sequence
        _seqIdx           : int = 0
        # index for fragment
        _fragIdx          : int = 0
        # current payload pointer for current fragment
        _payLoadPtr       : int = 0
        # Amount of sequences
        _seqCount         : int = 0
        # current payload pointer of the current sequence
        _seqPayloadPtr    : int = 0

        #endregion


        # Check 2nd sequence active ? 
        if ( self._parCfg.Com.TwoSequences ) : 
        
            _seqCount += 1


        for _seqIdx in range ( 0,  _seqCount ) :

            # Check 2nd sequence ? -> goto 2nd sequence payload address  
            if ( _seqIdx == SECONDARY_SEQUENCE ) :
            
                self.RecvData.PayloadPtr.value = self.CalculateSequencePayloadStartAdr(AxesGroup = AxesGroup, 
                                                                                       Direction = ComDirection.ROB_TO_PLC,
                                                                                       Sequence  = SequenceFlag.SECONDARY_SEQUENCE)

            # parste sequence header
            self.Telegram.RobToPlc.Sequence[_seqIdx].Header.SEQ_ACK       = self.RecvData.GetUint()
            self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength = self.RecvData.GetUint()

            # check new data available ? 
            if ( self.Telegram.RobToPlc.Sequence[_seqIdx].Header.SEQ_ACK != AxesGroup.State.LastACK[_seqIdx]) :

                # Check sequence payload available ? 
                if (self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength.value > 0):

                    # Check sequence payload length is valid ? 
                    if ( self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength.value > self._parCfg.Com.TelegramLengthRobToPlc ) :
                    
                        # Create log entry for payload not valid 
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'Invalid sequence payload length, Sequence = {1}, PayloadLength = {2} ',
                            Para1       =  str(_seqIdx),
                            Para2       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength)
                        )
                        return
                    else:
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'RecvData: ACK = {1}, received Sequence [{2}] with PayloadLength = {3}, Lifesign = {4}',
                            Para1       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Header.SEQ_ACK),
                            Para2       =  str(_seqIdx),
                            Para3       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength),
                            Para4       =  str(self.Telegram.RobToPlc.Header.LifeSign)
                        )

                    # processing sequence payload                                  
                    while ( _seqPayloadPtr < self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength.value ) : 

                        # parse header
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID          = self.RecvData.GetUint()
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.Reserve        = self.RecvData.GetByte()
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction = self.RecvData.GetByte()
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer = self.RecvData.GetUint()
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength  = self.RecvData.GetUint()

                        # add header size to payload pointer 
                        _seqPayloadPtr = _seqPayloadPtr + self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.sizeof()

                        # Check fragment payload available ? 
                        if (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > 0) :

                            # Check fragment payload length is valid ? 
                            if ( self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value > self._parCfg.Com.TelegramLengthRobToPlc ) : 

                                # Create log entry for payload not valid 
                                self.CreateLogMessage( 
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'Invalid fragment payload length, Sequence = {1}, PayloadLength = {2} ',
                                    Para1       =  str(_seqIdx),
                                    Para2       =  str(self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength)
                                )
                                return


                        # Fill Response payload
                        for _idx in range( 0, self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength.value -1 ) : 
                        
                            # calculate payload pointer
                            _payLoadPtr = self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer.value + _idx
                        
                            if (( _payLoadPtr >= 0                    ) and
                                ( _payLoadPtr <= RESPONSE_PAYLOAD_MAX )) : 

                                self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[_payLoadPtr] = self.RecvData.GetByte().value
                                # inc payload pointer
                                _seqPayloadPtr = _seqPayloadPtr + BYTE.sizeof()
                            else:
                                # Create log entry for payload pointer not valid 
                                self.CreateLogMessage(
                                    Timestamp   = self.SystemTime,
                                    MessageType = MessageType.CMD,
                                    Severity    = Severity.DEBUG,
                                    MessageCode = 0,
                                    MessageText = 'Invalid fragment payload pointer, Sequence = {1}, Fragment = {2}, PayloadPointer = {3} ',
                                    Para1       =  str(_seqIdx),
                                    Para2       =  str(_fragIdx),
                                    Para3       =  str(_payLoadPtr)
                                )
                                return


                        # Add Response to ACR
                        AxesGroup.Acyclic.ActiveCommandRegister.AddRsp(self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx])
                        
                        
                        
                        # Only for debugging - header is part of the payload itself
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.State                 =     CmdMessageState( GetHalfeByteLo( value  = self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[0]).value)
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSeq                =      GetHalfeByteHi(                 value  = self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[0])
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.AlarmMessageSeverity  =        BYTE_TO_SINT(                          self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[1])
                        self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.AlarmMessageCode      =  CombineBytesToUint(                 ByteHi = self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[2],
                                                                                                                                                                ByteLo = self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[3])
                        # Create log entry
                        self.CreateLogMessage(
                            Timestamp   = self.SystemTime,
                            MessageType = MessageType.CMD,
                            Severity    = Severity.DEBUG,
                            MessageCode = 0,
                            MessageText = 'RecvData: received Fragment [{1}] with PayloadLength = {2}, CmdID <{3}> , CmdState: {4}, Fragment-Action Bits: {5}',
                            Para1       =  str(_seqIdx),
                            Para2       =  str                      (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength),
                            Para3       =  str                      (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID),
                            Para4       =                           (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.State.toString()),
                            Para5       = FRAGMENT_ACTION_TO_STRING (self.Telegram.RobToPlc.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction)
                        )


                        # Check still payload left ? -> goto next fragment  
                        if ( _seqPayloadPtr < self.Telegram.RobToPlc.Sequence[_seqIdx].Header.PayloadLength.value ) :

                            _fragIdx += 1

                        # Check fragment index limit reached ? 
                        if ( _fragIdx > FRAGMENT_MAX ) :

                            # Create log entry
                            self.CreateLogMessage( 
                                Timestamp   = self.SystemTime,
                                MessageType = MessageType.CMD,
                                Severity    = Severity.DEBUG,
                                MessageCode = 0,
                                MessageText = 'Fragment index out of range, _fragIdx = {1} ',
                                Para1       =  str(_fragIdx)
                            )
                            return




    # --------------------------------------------------------------
    # Reset - reset internal variables
    # ---------------------------------------------------------------
    def Reset(self, AxesGroup: AxesGroup) -> None:
        """Reset internal variables"""
        
        # reset flags
        self.Busy              = False
        self.Initialized       = False
        self.Synchronized      = False
        self.Error             = False
        self.ErrorID           = 0
        self.ErrorAddTxt       = ''
        self.WarningID         = 0
        self.InfoID            = 0

        # Reset internal functon blocks
        self._exchangeConfiguration      .Enable  = False
        self._readRobotData              .Execute = False
        self._readMessages               .Enable  = False  
        self._readToolData               .Execute = False  
        self._readFrameData              .Execute = False  
        self._readLoadData               .Execute = False  
        self._readWorkArea               .Execute = False  
        self._readRobotSwLimits          .Execute = False  
        self._readRobotDefaultDynamics   .Execute = False  
        self._readRobotReferenceDynamics .Execute = False  
        self._writeToolData              .Execute = False   
        self._writeFrameData             .Execute = False   
        self._writeLoadData              .Execute = False   
        self._writeWorkArea              .Execute = False   
        self._writeRobotSwLimits         .Execute = False   
        self._writeRobotDefaultDynamics  .Execute = False   
        self._writeRobotReferenceDynamics.Execute = False   

        # Set Client error to force server error
        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.NONE

        # Reset synchronisation state variables
        AxesGroup.State.SyncStatePlc.InSync.Frame             = False
        AxesGroup.State.SyncStatePlc.InSync.Tool              = False
        AxesGroup.State.SyncStatePlc.InSync.Load              = False
        AxesGroup.State.SyncStatePlc.InSync.WorkArea          = False
        AxesGroup.State.SyncStatePlc.InSync.SwLimits          = False
        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics   = False
        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False

        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame    = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool     = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.Load     = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0

        AxesGroup.State.SyncStateRc .InSync.Frame             = False
        AxesGroup.State.SyncStateRc .InSync.Tool              = False
        AxesGroup.State.SyncStateRc .InSync.Load              = False
        AxesGroup.State.SyncStateRc .InSync.WorkArea          = False
        AxesGroup.State.SyncStateRc .InSync.SwLimits          = False
        AxesGroup.State.SyncStateRc .InSync.DefaultDynamics   = False
        AxesGroup.State.SyncStateRc .InSync.ReferenceDynamics = False

        AxesGroup.State.SyncStateRc .UnSyncNo.Frame    = 0
        AxesGroup.State.SyncStateRc .UnSyncNo.Tool     = 0
        AxesGroup.State.SyncStateRc .UnSyncNo.Load     = 0
        AxesGroup.State.SyncStateRc .UnSyncNo.WorkArea = 0

        # Reset active command register
        AxesGroup.Acyclic.ActiveCommandRegister.Reset()
            
        # reset step counters
        self._stepCmd                   = 0
        self._stepSyncFrameData         = 0
        self._stepSyncLoadData          = 0
        self._stepSyncDefaultDynamics   = 0
        self._stepSyncReferenceDynamics = 0
        self._stepSyncSWLimits          = 0
        self._stepSyncToolData          = 0
        self._stepSyncWorkArea          = 0

    # --------------------------------------------------------------
    # SetError - set error ID
    # ---------------------------------------------------------------
    def SetError(self, ErrorID: int | UINT | WORD, Overwrite: bool = False) -> None:

        """Set error ID"""
        if not self.HasError or Overwrite:

            if (isinstance(ErrorID, int)):
                self.ErrorID = ErrorID 

            if (isinstance(ErrorID, UINT)):
                self.ErrorID = ErrorID.value 

            if (isinstance(ErrorID, WORD)):
                self.ErrorID = ErrorID.value


    # --------------------------------------------------------------
    # SetWarning - set warning ID
    # ---------------------------------------------------------------
    def SetWarning(self, WarningID: int | UINT | WORD, Overwrite: bool = False) -> None:
        """Set warning ID"""

        if not self.HasWarning or Overwrite:

            if (isinstance(WarningID, int)):
                self.WarningID = WarningID 

            if (isinstance(WarningID, UINT)):
                self.WarningID = WarningID.value 

            if (isinstance(WarningID, WORD)):
                self.WarningID = WarningID.value


    # --------------------------------------------------------------
    # SetInfo - set info ID
    # ---------------------------------------------------------------
    def SetInfo(self, InfoID: int | UINT | WORD, Overwrite: bool = False) -> None:
        """Set info ID"""
        if not self.HasInfo or Overwrite:

            if (isinstance(InfoID, int)):
                self.InfoID = InfoID 

            if (isinstance(InfoID, UINT)):
                self.InfoID = InfoID.value 

            if (isinstance(InfoID, WORD)):
                self.InfoID = InfoID.value