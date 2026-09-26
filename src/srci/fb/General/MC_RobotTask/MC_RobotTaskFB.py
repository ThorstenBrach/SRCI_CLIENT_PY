"""Handles multiple mechanisms required for operation of the interface. For maximal performance, this FB must be called after the function FB's, so that the data can be written to the fieldbus in the same cycle as the start of FB occours

ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.fb.Additional.MC_ExchangeConfiguration.MC_ExchangeConfigurationFB import MC_ExchangeConfigurationFB
from srci.fb.General.MC_RobotTask.MC_RobotTaskFB_Telegram import MC_RobotTaskFB_Telegram
from srci.fb.Read.MC_ReadFrameData.MC_ReadFrameDataFB import MC_ReadFrameDataFB
from srci.fb.Read.MC_ReadLoadData.MC_ReadLoadDataFB import MC_ReadLoadDataFB
from srci.fb.Read.MC_ReadMessages.MC_ReadMessagesFB import MC_ReadMessagesFB
from srci.fb.Read.MC_ReadRobotData.MC_ReadRobotDataFB import MC_ReadRobotDataFB
from srci.fb.Read.MC_ReadRobotDefaultDynamics.MC_ReadRobotDefaultDynamicsFB import MC_ReadRobotDefaultDynamicsFB
from srci.fb.Read.MC_ReadRobotReferenceDynamics.MC_ReadRobotReferenceDynamicsFB import MC_ReadRobotReferenceDynamicsFB
from srci.fb.Read.MC_ReadRobotSWLimits.MC_ReadRobotSWLimitsFB import MC_ReadRobotSWLimitsFB
from srci.fb.Read.MC_ReadToolData.MC_ReadToolDataFB import MC_ReadToolDataFB
from srci.fb.WorkAreas.MC_ReadWorkArea.MC_ReadWorkAreaFB import MC_ReadWorkAreaFB
from srci.fb.WorkAreas.MC_WriteWorkArea.MC_WriteWorkAreaFB import MC_WriteWorkAreaFB
from srci.fb.Write.MC_WriteFrameData.MC_WriteFrameDataFB import MC_WriteFrameDataFB
from srci.fb.Write.MC_WriteLoadData.MC_WriteLoadDataFB import MC_WriteLoadDataFB
from srci.fb.Write.MC_WriteRobotDefaultDynamics.MC_WriteRobotDefaultDynamicsFB import MC_WriteRobotDefaultDynamicsFB
from srci.fb.Write.MC_WriteRobotReferenceDynamics.MC_WriteRobotReferenceDynamicsFB import MC_WriteRobotReferenceDynamicsFB
from srci.fb.Write.MC_WriteRobotSWLimits.MC_WriteRobotSWLimitsFB import MC_WriteRobotSWLimitsFB
from srci.fb.Write.MC_WriteToolData.MC_WriteToolDataFB import MC_WriteToolDataFB
from srci.fb._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from srci.fb._internal.Recv.RobotLibraryRecvDataFB import RobotLibraryRecvDataFB
from srci.fb._internal.Send.RobotLibrarySendDataFB import RobotLibrarySendDataFB
from srci.functions.Check.IsDefaultDynamicsEqual import IsDefaultDynamicsEqual
from srci.functions.Check.IsFrameDataEqual import IsFrameDataEqual
from srci.functions.Check.IsLoadDataEqual import IsLoadDataEqual
from srci.functions.Check.IsReferenceDynamicsEqual import IsReferenceDynamicsEqual
from srci.functions.Check.IsSwLimitsEqual import IsSwLimitsEqual
from srci.functions.Check.IsToolDataEqual import IsToolDataEqual
from srci.functions.Check.IsWorkAreaEqual import IsWorkAreaEqual
from srci.functions.Common import CheckTimeout, SetTimeout
from srci.functions.Convert.DT import DATE_TO_IEC_DATE, TIME_TO_IEC_TIME
from srci.functions.Convert.Misc import CombineBytesToUint, CombineHalfBytes, CombineHalfSints, DwordToRaStatusWord, FragmentActionToByte, GetHalfeByteHi, GetHalfeByteLo, PERCENT_UINT_TO_REAL, PlcOptionalCyclicToUint, RobOptionalCyclicToUint, SyncModesToDataEnableSync, VersionToByte, WordToArmConfigElbow, WordToArmConfigShoulder, WordToArmConfigWrist
from srci.functions.Convert.TO_STRING.CMD_TYPE_TO_STRING import CMD_TYPE_TO_STRING
from srci.functions.Convert.TO_STRING.EXECUTION_MODE_TO_STRING import EXECUTION_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.FRAGMENT_ACTION_TO_STRING import FRAGMENT_ACTION_TO_STRING
from srci.functions.Convert.TO_STRING.SYNC_MODE_TO_STRING import SYNC_MODE_TO_STRING
from srci.functions.Convert.TO_STRING.SYNC_TIME_TO_STRING import SYNC_TIME_TO_STRING
from srci.functions.Convert.TO_STRING.TELEGRAM_CONTROL_TO_STRING import TELEGRAM_CONTROL_TO_STRING
from srci.functions.Convert.TO_STRING.TELEGRAM_STATE_TO_STRING import TELEGRAM_STATE_TO_STRING
from srci.functions.Convert.TO_STRING.WORD_TO_STRING_BIN import WORD_TO_STRING_BIN
from srci.iec.conv import BYTE_TO_SINT, DINT_TO_STRING, DINT_TO_UDINT, DINT_TO_USINT, INT_TO_BYTE, SINT_TO_BYTE, STRING_TO_USINT, TIME_TO_STRING, TIME_TO_UINT, UDINT_TO_STRING, UINT_TO_STRING
from srci.iec.rt import ADR, CONCAT, LIMIT, LOWER_BOUND, MAX, MID, MIN, SysDepMemCmp, SysDepMemSet, UPPER_BOUND, array_type, bit, copy_into, set_bit, st_for_end, trunc_str, type_size, wrap
from srci.iec.standard import F_TRIG, R_TRIG, TON
from srci.types import AxesGroupAcyclicAcrEntryCmdBuffer, AxesGroupStateDataChanged, BufferStateCmd, CmdType, ComDirection, ControlHalfByte, DefaultDynamics, ExecutionMode, FragmentAction, Frame, Load, MessageType, PriorityLevel, RaSequenceState, ReferenceDynamics, RobotLibraryConstants, RobotLibraryErrorIdEnum, RobotLibraryInfoIdEnum, RobotLibraryParameter, RobotLibraryWarningIdEnum, RobotTaskParCfg, RobotWorkArea, SWLimits, SequenceFlag, Severity, SyncMode, SyncTime, SystemTime, Telegram, TelegramPlcToRob, TelegramState, Tool

if TYPE_CHECKING:
    from srci.interfaces.IMessageLogger import IMessageLogger
    from srci.types import AlarmMessage, AxesGroup, UserData

__all__ = ['MC_RobotTaskFB']


class MC_RobotTaskFB(MC_RobotTaskFB_Telegram, RobotLibraryLogFB):
    """Handles multiple mechanisms required for operation of the interface. For maximal performance, this FB must be called after the function FB's, so that the data can be written to the fieldbus in the same cycle as the start of FB occours"""

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Set TRUE (default) to initialize the interface
        self.Enable: bool = False
        # User defined robot name
        self.RobotName: str = ''
        # Current System Time
        self.SystemTime: SystemTime = SystemTime()
        # Online Change detected
        self.OnlineChange: bool = False
        # Axes Group ID -> is used to uniquely identify each RA on a per RC basis.
        # 
        # For convenience, an RC with only one RA must assign ID 1 to this RA.
        # An RC with multiple RAs must assign numeric values 1-15 to those RAs.
        self.AxesGroupID: int = 0  #  ToDo: Mistake in specification : ID should start with 1, but must start with 0 !
        # Configuration parameter
        self.ParCfg: RobotTaskParCfg = RobotTaskParCfg()
        # VAR_IN_OUT
        # Inputs of PLC for communication from RC
        self.RobotInData: list[int] = None
        # Outputs of PLC for communication to RC
        self.RobotOutData: list[int] = None
        # User data stored on the PLC according to Table 6-10
        self.UserData: UserData = None
        # ToolData stored on PLC. For more information refer to 5.5.6.3
        self.ToolData: list[Tool] = None
        # LoadData stored on PLC.For more information refer to 5.5.6.4
        self.FrameData: list[Frame] = None
        # LoadData stored on PLC.For more information refer to 5.5.6.4
        self.LoadData: list[Load] = None
        # Work areas stored on PLC. For more information refer to 5.5.8
        self.WorkAreas: list[RobotWorkArea] = None
        # Software limits stored on PLC
        self.SWLimits: SWLimits = None
        # Default dynamics stored on PLC. For more information refer to 5.5.7
        self.DefaultDynamics: DefaultDynamics = None
        # Reference dynamics stored on PLC. For more information refer to 5.5.7
        self.ReferenceDynamics: ReferenceDynamics = None
        # System log on PLC
        self.SystemLog: list[str] = None
        # Message buffer on the PLC - For more information refer to 5.5.11
        self.MessageLog: list[AlarmMessage] = None
        # Robot assignment of function
        self.AxesGroup: AxesGroup = None
        # VAR_OUTPUT
        # FB is being processed
        self.Busy: bool = False
        # Interface is initialized (RI state: "Initialized").
        # For more information on RI states refer to chapter 5.5.3.1.
        self.Initialized: bool = False
        # Server and client were successfully synchronized (RI state: "Synchronized").
        # For more information on the synchronization mechanism refer to chapter 5.6.7.
        self.Synchronized: bool = False
        # An error occurred
        self.Error: bool = False
        # ErrorID reported by RC for error identification according to Table 7-1
        self.ErrorID: int = 0
        self.ErrorIdEnum: RobotLibraryErrorIdEnum = RobotLibraryErrorIdEnum.NO_ERROR
        self.ErrorAddTxt: str = ''
        # WarningID for warning identification reported during execution of command according to Table 7-3
        self.WarningID: int = 0
        self.WarningIdEnum: RobotLibraryWarningIdEnum = RobotLibraryWarningIdEnum.NO_WARNING
        # InfoID for info identification reported during execution of command according to Table 7-5
        self.InfoID: int = 0
        self.InfoIdEnum: RobotLibraryInfoIdEnum = RobotLibraryInfoIdEnum.NO_INFO
        # VAR
        # internal copy of configuration parameter
        self._parCfg: RobotTaskParCfg = RobotTaskParCfg()
        # internal ToolData for comparation to user ToolData
        self._toolData: list[Tool] = [Tool() for _ in range(_iec.array_len(0, _iec.Param('TOOL_MAX', -1)))]
        # internal FrameData for comparation to user FrameData
        self._frameData: list[Frame] = [Frame() for _ in range(_iec.array_len(0, _iec.Param('FRAME_MAX', -1)))]
        # internal LoadData for comparation to user LoadData
        self._loadData: list[Load] = [Load() for _ in range(_iec.array_len(0, _iec.Param('LOAD_MAX', -1)))]
        # internal WorkAreas for comparation to user WorkAreas
        self._workAreas: list[RobotWorkArea] = [RobotWorkArea() for _ in range(_iec.array_len(0, _iec.Param('WORK_AREAS_MAX', -1)))]
        # internal Software limits for comparation to user Software limit
        self._swLimits: SWLimits = SWLimits()
        # internal default dynamics for comparation to user default dynamics
        self._defaultDynamics: DefaultDynamics = DefaultDynamics()
        # internal reference dynamics for comparation to user reference dynamics
        self._referenceDynamics: ReferenceDynamics = ReferenceDynamics()
        # FB for exchange configuration
        self._exchangeConfiguration: MC_ExchangeConfigurationFB = MC_ExchangeConfigurationFB()
        # FB for read robot data
        self._readRobotData: MC_ReadRobotDataFB = MC_ReadRobotDataFB()
        # FB for read messaged
        self._readMessages: MC_ReadMessagesFB = MC_ReadMessagesFB()
        # FB for read tool data
        self._readToolData: MC_ReadToolDataFB = MC_ReadToolDataFB()
        # FB for read frame data
        self._readFrameData: MC_ReadFrameDataFB = MC_ReadFrameDataFB()
        # FB for read load data
        self._readLoadData: MC_ReadLoadDataFB = MC_ReadLoadDataFB()
        # FB for read work area
        self._readWorkArea: MC_ReadWorkAreaFB = MC_ReadWorkAreaFB()
        # FB for read robot software limits
        self._readRobotSWLimits: MC_ReadRobotSWLimitsFB = MC_ReadRobotSWLimitsFB()
        # FB for read robot default dynamics
        self._readRobotDefaultDynamics: MC_ReadRobotDefaultDynamicsFB = MC_ReadRobotDefaultDynamicsFB()
        # FB for read robot reference dynamics
        self._readRobotReferenceDynamics: MC_ReadRobotReferenceDynamicsFB = MC_ReadRobotReferenceDynamicsFB()
        # FB for write tool data
        self._writeToolData: MC_WriteToolDataFB = MC_WriteToolDataFB()
        # FB for write frame data
        self._writeFrameData: MC_WriteFrameDataFB = MC_WriteFrameDataFB()
        # FB for write load data
        self._writeLoadData: MC_WriteLoadDataFB = MC_WriteLoadDataFB()
        # FB for write work area
        self._writeWorkArea: MC_WriteWorkAreaFB = MC_WriteWorkAreaFB()
        # FB for write robot software limits
        self._writeRobotSWLimits: MC_WriteRobotSWLimitsFB = MC_WriteRobotSWLimitsFB()
        # FB for write robot default dynamics
        self._writeRobotDefaultDynamics: MC_WriteRobotDefaultDynamicsFB = MC_WriteRobotDefaultDynamicsFB()
        # FB for write robot reference dynamics
        self._writeRobotReferenceDynamics: MC_WriteRobotReferenceDynamicsFB = MC_WriteRobotReferenceDynamicsFB()
        # Send Buffer
        self.SendData: RobotLibrarySendDataFB = RobotLibrarySendDataFB()
        # Recv Buffer
        self.RecvData: RobotLibraryRecvDataFB = RobotLibraryRecvDataFB()
        # Telegram
        self.Telegram: Telegram = Telegram()
        # internal step counter for command
        self._stepCmd: int = 0
        # internal timer for command
        # {attribute 'hide'}
        self._timerCmd: TON = TON()
        # internal timeout for command
        # {attribute 'hide'}
        self._timeoutCmd: int = 5000
        # internal step counter for synchronisation of frame data
        self._stepSyncFrameData: int = 0
        # internal timer for synchronisation of frame data
        # {attribute 'hide'}
        self._timerSyncFrameData: TON = TON()
        # internal timeout for synchronisation of frame data
        # {attribute 'hide'}
        self._timeoutSyncFrameData: int = 5000
        # internal index for frame data synchronisation
        self._syncIdxFrameData: int = 0
        # internal index for maximal amount of frames data( MIN(PLC,RC) )
        self._syncIdxMaxFrameData: int = 0
        # internal step counter for synchronisation of load data
        self._stepSyncLoadData: int = 0
        # internal timer for synchronisation of load data
        # {attribute 'hide'}
        self._timerSyncLoadData: TON = TON()
        # internal timeout for synchronisation of load data
        # {attribute 'hide'}
        self._timeoutSyncLoadData: int = 5000
        # internal index for load data synchronisation
        self._syncIdxLoadData: int = 0
        # internal index for maximal amount of load data ( MIN(PLC,RC) )
        self._syncIdxMaxLoadData: int = 0
        # internal step counter for synchronisation of tool data
        self._stepSyncToolData: int = 0
        # internal timer for synchronisation of tool data
        # {attribute 'hide'}
        self._timerSyncToolData: TON = TON()
        # internal timeout for synchronisation of tool data
        # {attribute 'hide'}
        self._timeoutSyncToolData: int = 5000
        # internal index for tool data synchronisation
        self._syncIdxToolData: int = 0
        # internal index for maximal amount of tool data ( MIN(PLC,RC) )
        self._syncIdxMaxToolData: int = 0
        # internal step counter for synchronisation of work areas
        self._stepSyncWorkArea: int = 0
        # internal timer for synchronisation of work areas
        # {attribute 'hide'}
        self._timerSyncWorkArea: TON = TON()
        # internal timeout for synchronisation of work areas
        # {attribute 'hide'}
        self._timeoutSyncWorkArea: int = 5000
        # internal index for WorkArea synchronisation
        self._syncIdxWorkArea: int = 0
        # internal index for maximal amount of Work Area( MIN(PLC,RC) )
        self._syncIdxMaxWorkArea: int = 0
        # internal step counter for synchronisation of software limits
        self._stepSyncSWLimits: int = 0
        # internal timer for synchronisation of software limits
        # {attribute 'hide'}
        self._timerSyncSWLimits: TON = TON()
        # internal timeout for synchronisation of software limits
        # {attribute 'hide'}
        self._timeoutSyncSWLimits: int = 5000
        # internal step counter for synchronisation of default dynamics
        self._stepSyncDefaultDynamics: int = 0
        # internal timer for synchronisation of default dynamics
        # {attribute 'hide'}
        self._timerSyncDefaultDynamics: TON = TON()
        # internal timeout for synchronisation of default dynamics
        # {attribute 'hide'}
        self._timeoutSyncDefaultDynamics: int = 5000
        # internal step counter for synchronisation of reference dynamics
        self._stepSyncReferenceDynamics: int = 0
        # internal timer for synchronisation of reference dynamics
        # {attribute 'hide'}
        self._timerSyncReferenceDynamics: TON = TON()
        # internal timeout for synchronisation of reference dynamics
        # {attribute 'hide'}
        self._timeoutSyncReferenceDynamics: int = 5000
        # Rising edge for enable
        # {attribute 'hide'}
        self._enable_R: R_TRIG = R_TRIG()
        # Falling edge for enable
        # {attribute 'hide'}
        self._enable_F: F_TRIG = F_TRIG()
        # Flag that indicated the the connection is alive (data exchange)
        self._aliveBit: bool = False
        # last lifesign counter value
        self._aliveValue: int = 0
        # timer for detecting alive state
        self._aliveCheck: TON = TON()
        # rising edge for connection is alive
        # {attribute 'hide'}
        self._alive_R: R_TRIG = R_TRIG()
        # falling edge for connection is alive
        # {attribute 'hide'}
        self._alive_F: F_TRIG = F_TRIG()
        # last telegram state
        self._lastTelegramState: TelegramState = TelegramState.UNDEFINED
        # last telegram control
        self._lastTelegramControl: ControlHalfByte = ControlHalfByte.NONE
        # Lower array dimension of RobotInData
        self.ROBOT_IN_DATA_MIN: int = 0
        # Upper array dimension of RobotInData
        self.ROBOT_IN_DATA_MAX: int = 0
        # Size of RobotInData
        self.ROBOT_IN_DATA_SIZE: int = 0
        # Lower array dimension of RobotOutData
        self.ROBOT_OUT_DATA_MIN: int = 0
        # Upper array dimension of RobotOutData
        self.ROBOT_OUT_DATA_MAX: int = 0
        # Size of RobotOutData
        self.ROBOT_OUT_DATA_SIZE: int = 0
        # VAR CONSTANT
        # {attribute 'hide'}
        self.FRAGMENT_HEADER_SIZE: int = 8
        # Size of the comand header
        # {attribute 'hide'}
        self.COMMAND_HEADER_SIZE: int = 5
        # Size of the footer
        # {attribute 'hide'}
        self.FOOTER_SIZE: int = 1
        # Minimal payload size for telegram
        # {attribute 'hide'}
        self.MIN_PAYLOAD_SIZE: int = 1
        # Active command
        # {attribute 'hide'}
        self.ACTIVE_CMD: int = 1
        # Buffered command
        # {attribute 'hide'}
        self.BUFFER_CMD: int = 2
        # Empty command entry
        # {attribute 'hide'}
        self.EMPTY_CMD_ENTRY: AxesGroupAcyclicAcrEntryCmdBuffer = AxesGroupAcyclicAcrEntryCmdBuffer(State=BufferStateCmd.EMPTY)
        # bitmask to mask the LifeSign out of the halfbyte
        # {attribute 'hide'}
        self.LIFESIGN_BIT_MASK: int = 15
        # Primary sequence
        # {attribute 'hide'}
        self.PRIMARY_SEQUENCE: int = 0
        # Secondary sequence
        # {attribute 'hide'}
        self.SECONDARY_SEQUENCE: int = 1
        # Empty Execution-Order-List entry
        # {attribute 'hide'}
        self.EMPTY_EOL_ENTRY: int = 0
        # VAR_INST of HandleAliveBit
        self._HandleAliveBit_First: bool = True
        # VAR_INST of HandleInvalidFrames
        self._HandleInvalidFrames__invalidFrameCounterCheck_D: TON = TON()
        self._HandleInvalidFrames__lastInvalidFrames: int = 0
        # VAR_INST of HandleLifeSign
        self._HandleLifeSign__first: bool = True

    def __call__(self, *, Enable: bool | None = None, RobotName: str | None = None, SystemTime: SystemTime | None = None, OnlineChange: bool | None = None, AxesGroupID: int | None = None, ParCfg: RobotTaskParCfg | None = None, RobotInData: list[int] | None = None, RobotOutData: list[int] | None = None, UserData: UserData | None = None, ToolData: list[Tool] | None = None, FrameData: list[Frame] | None = None, LoadData: list[Load] | None = None, WorkAreas: list[RobotWorkArea] | None = None, SWLimits: SWLimits | None = None, DefaultDynamics: DefaultDynamics | None = None, ReferenceDynamics: ReferenceDynamics | None = None, SystemLog: list[str] | None = None, MessageLog: list[AlarmMessage] | None = None, AxesGroup: AxesGroup | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if Enable is not None:
            self.Enable = Enable
        if RobotName is not None:
            self.RobotName = trunc_str(RobotName, 20)
        if SystemTime is not None:
            copy_into(self.SystemTime, SystemTime)
        if OnlineChange is not None:
            self.OnlineChange = OnlineChange
        if AxesGroupID is not None:
            self.AxesGroupID = AxesGroupID
        if ParCfg is not None:
            copy_into(self.ParCfg, ParCfg)
        if RobotInData is not None:
            self.RobotInData = RobotInData
        if RobotOutData is not None:
            self.RobotOutData = RobotOutData
        if UserData is not None:
            self.UserData = UserData
        if ToolData is not None:
            self.ToolData = ToolData
        if FrameData is not None:
            self.FrameData = FrameData
        if LoadData is not None:
            self.LoadData = LoadData
        if WorkAreas is not None:
            self.WorkAreas = WorkAreas
        if SWLimits is not None:
            self.SWLimits = SWLimits
        if DefaultDynamics is not None:
            self.DefaultDynamics = DefaultDynamics
        if ReferenceDynamics is not None:
            self.ReferenceDynamics = ReferenceDynamics
        if SystemLog is not None:
            self.SystemLog = SystemLog
        if MessageLog is not None:
            self.MessageLog = MessageLog
        if AxesGroup is not None:
            self.AxesGroup = AxesGroup
        if InternalLogger is not None:
            self.InternalLogger = InternalLogger
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        self.__body()

    def __body(self) -> None:
        # Get array dimension of RobotInData
        self.ROBOT_IN_DATA_MIN = LOWER_BOUND(self.RobotInData)
        self.ROBOT_IN_DATA_MAX = UPPER_BOUND(self.RobotInData)
        self.ROBOT_IN_DATA_SIZE = DINT_TO_UDINT(self.ROBOT_IN_DATA_MAX - self.ROBOT_IN_DATA_MIN + 1)

        # Get array dimension of RobotInData
        self.ROBOT_OUT_DATA_MIN = LOWER_BOUND(self.RobotOutData)
        self.ROBOT_OUT_DATA_MAX = UPPER_BOUND(self.RobotOutData)
        self.ROBOT_OUT_DATA_SIZE = DINT_TO_UDINT(self.ROBOT_OUT_DATA_MAX - self.ROBOT_OUT_DATA_MIN + 1)

        self.HandleAxesGroup(AxesGroup=self.AxesGroup, ToolData=self.ToolData, FrameData=self.FrameData, LoadData=self.LoadData, WorkAreas=self.WorkAreas, SWLimits=self.SWLimits, DefaultDynamics=self.DefaultDynamics, ReferenceDynamics=self.ReferenceDynamics)

        self.HandleLifeSign(AxesGroup=self.AxesGroup)
        self.HandleLogMessagesAck(AxesGroup=self.AxesGroup)
        self.HandleInvalidFrames(AxesGroup=self.AxesGroup, RobotInData=self.RobotInData)
        self.HandleTelegramStateCtrl()
        self.HandleAliveBit(LifeSign=self.RobotInData[1])
        self.HandleSeqAck(AxesGroup=self.AxesGroup)
        self.HandleUserData(AxesGroup=self.AxesGroup, UserData=self.UserData)

        self.HandleSync(AxesGroup=self.AxesGroup, ToolData=self.ToolData, FrameData=self.FrameData, LoadData=self.LoadData, WorkAreas=self.WorkAreas, SWLimits=self.SWLimits, DefaultDynamics=self.DefaultDynamics, ReferenceDynamics=self.ReferenceDynamics)

        self.OnCall(AxesGroup=self.AxesGroup)
        self.OnExecRun(AxesGroup=self.AxesGroup)

        self.AxesGroupToTelegram(AxesGroup=self.AxesGroup)

        self.CreateSendPayload(AxesGroup=self.AxesGroup, RobotOutData=self.RobotOutData)
        self.ParseRecvPayload(AxesGroup=self.AxesGroup, RobotInData=self.RobotInData)

        self.AxesGroupFromTelegram(AxesGroup=self.AxesGroup)

        # call internal functionblocks
        self._exchangeConfiguration(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readRobotData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readMessages(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readToolData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readFrameData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readLoadData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readWorkArea(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readRobotSWLimits(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readRobotDefaultDynamics(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._readRobotReferenceDynamics(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeToolData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeFrameData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeLoadData(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeWorkArea(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeRobotSWLimits(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeRobotDefaultDynamics(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)
        self._writeRobotReferenceDynamics(Name=self.RobotName, ExecMode=ExecutionMode.PARALLEL, Priority=PriorityLevel.NORMAL, AxesGroup=self.AxesGroup)

        # Update SystemLog and MessageLog
        copy_into(self.SystemLog, self.AxesGroup.MessageLog.SystemLogs)
        copy_into(self.MessageLog, self.AxesGroup.MessageLog.Messages)

    def AxesGroupFromTelegram(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        self.AxesGroupFromTelegramCyclic(AxesGroup=AxesGroup)
        self.AxesGroupFromTelegramCyclicOptional(AxesGroup=AxesGroup)

    def AxesGroupFromTelegramCyclic(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # ---------------------------------
        # Mapp Telegramm to AxesGroup Data
        # ---------------------------------
        copy_into(AxesGroup.Cyclic.RobToPlc.SRCIVersion, self.Telegram.RobToPlc.Header.SRCIVersion)
        AxesGroup.Cyclic.RobToPlc.LifeSign = self.Telegram.RobToPlc.Header.LifeSign
        AxesGroup.Cyclic.RobToPlc.TelegramState = self.Telegram.RobToPlc.Header.TelegramState
        copy_into(AxesGroup.Cyclic.RobToPlc.StatusRobotArm, DwordToRaStatusWord(Value=self.Telegram.RobToPlc.Header.StatusRobotArm))
        AxesGroup.Cyclic.RobToPlc.Override = self.Telegram.RobToPlc.Header.Override

    def AxesGroupFromTelegramCyclicOptional(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # Sub ProgramData {{{
        copy_into(AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Data, self.Telegram.RobToPlc.CyclicOptional.SubProgramData.Data)

        # }}}
        # Cartesian position {{{
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active = AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.X = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.X
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Y = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Y
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Z = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Z
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rx = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rx
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Ry = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Ry
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Rz = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Rz
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Shoulder = WordToArmConfigShoulder(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Elbow = WordToArmConfigElbow(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Config.Wrist = WordToArmConfigWrist(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Config)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J1Turns = BYTE_TO_SINT(GetHalfeByteLo(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J2_J1))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J2Turns = BYTE_TO_SINT(GetHalfeByteHi(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J2_J1))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J3Turns = BYTE_TO_SINT(GetHalfeByteLo(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J4_J3))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J4Turns = BYTE_TO_SINT(GetHalfeByteHi(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J4_J3))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J5Turns = BYTE_TO_SINT(GetHalfeByteLo(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J6_J5))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.J6Turns = BYTE_TO_SINT(GetHalfeByteHi(Value=self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_J6_J5))
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.TurnNumber.E1Turns = BYTE_TO_SINT(self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.Turns_E1)
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.E1 = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.E1
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.ToolNo = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedToolNo
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.CoordinateSystem.FrameNo = self.Telegram.RobToPlc.CyclicOptional.CartesianPosition.CurrentlyUsedFrameNo

        # }}}
        # Joint position {{{
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active = AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J1 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J1
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J2 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J2
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J3 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J3
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J4 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J4
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J5 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J5
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.J6 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.J6
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.E1 = self.Telegram.RobToPlc.CyclicOptional.JointPosition.E1

        # }}}
        # Force {{{
        AxesGroup.CyclicOptional.RobToPlc.Force.Active = AxesGroup.CyclicOptional.RobToPlc.Force.Active
        AxesGroup.CyclicOptional.RobToPlc.Force.X = self.Telegram.RobToPlc.CyclicOptional.Force.X
        AxesGroup.CyclicOptional.RobToPlc.Force.Y = self.Telegram.RobToPlc.CyclicOptional.Force.Y
        AxesGroup.CyclicOptional.RobToPlc.Force.Z = self.Telegram.RobToPlc.CyclicOptional.Force.Z
        AxesGroup.CyclicOptional.RobToPlc.Force.Rx = self.Telegram.RobToPlc.CyclicOptional.Force.Rx
        AxesGroup.CyclicOptional.RobToPlc.Force.Ry = self.Telegram.RobToPlc.CyclicOptional.Force.Ry
        AxesGroup.CyclicOptional.RobToPlc.Force.Rz = self.Telegram.RobToPlc.CyclicOptional.Force.Rz

        # }}}
        # Current {{{
        AxesGroup.CyclicOptional.RobToPlc.Current.Active = AxesGroup.CyclicOptional.RobToPlc.Current.Active
        AxesGroup.CyclicOptional.RobToPlc.Current.J1 = self.Telegram.RobToPlc.CyclicOptional.Current.J1
        AxesGroup.CyclicOptional.RobToPlc.Current.J2 = self.Telegram.RobToPlc.CyclicOptional.Current.J2
        AxesGroup.CyclicOptional.RobToPlc.Current.J3 = self.Telegram.RobToPlc.CyclicOptional.Current.J3
        AxesGroup.CyclicOptional.RobToPlc.Current.J4 = self.Telegram.RobToPlc.CyclicOptional.Current.J4
        AxesGroup.CyclicOptional.RobToPlc.Current.J5 = self.Telegram.RobToPlc.CyclicOptional.Current.J5
        AxesGroup.CyclicOptional.RobToPlc.Current.J6 = self.Telegram.RobToPlc.CyclicOptional.Current.J6

        # }}}
        # Two Sequences {{{
        # }}}
        # Cartesian Position Extended
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active = AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E2 = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E2
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E3 = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E3
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E4 = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E4
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E5 = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E5
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.E6 = self.Telegram.RobToPlc.CyclicOptional.CartesianPositionExt.E6

        # Joint Position Extended
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active = AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E2 = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E2
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E3 = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E3
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E4 = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E4
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E5 = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E5
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.E6 = self.Telegram.RobToPlc.CyclicOptional.JointPositionExt.E6

        # Force Extended
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active = AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E1 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E1
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E2 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E2
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E3 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E3
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E4 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E4
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E5 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E5
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.E6 = self.Telegram.RobToPlc.CyclicOptional.ForceExt.E6

        # Current Extended
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active = AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E1 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E1
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E2 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E2
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E3 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E3
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E4 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E4
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E5 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E5
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.E6 = self.Telegram.RobToPlc.CyclicOptional.CurrentExt.E6

    def AxesGroupToTelegram(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegram: int = 0
        # internal index
        _idx: int = 0
        # internal sequence index
        _seqIdx: int = 0
        # internal fragment index
        _fragIdx: int = 0
        # internal register index
        _regIdx: int = 0
        # internal execution order list index
        _listIdx: int = 1
        # internal payload pointer
        _payLoadPtr: int = 0
        # internal fragment action
        _fragmentAction: FragmentAction = FragmentAction()
        # internal fragment action as string
        _fragmentActionString: str = ''
        # maximount amount of bytes per sequence
        SEQUENCE_MAX_PAYLOAD_SIZE: int = 0

        # {warning 'Handle 2nd sequence'}
        if AxesGroup.State.NewSEQ[0]:
            # delete old telegram data
            SysDepMemSet(pDest=ADR(self.Telegram, 'PlcToRob', _iec.StructType(TelegramPlcToRob)), Value=0, DataLen=type_size(_iec.StructType(TelegramPlcToRob)))

        self.AxesGroupToTelegramHeader(AxesGroup=AxesGroup)
        self.AxesGroupToTelegramCyclic(AxesGroup=AxesGroup)
        self.AxesGroupToTelegramCyclicOptional(AxesGroup=AxesGroup)
        self.AxesGroupToTelegramSequence(AxesGroup=AxesGroup)
        self.AxesGroupToTelegramFooter(AxesGroup=AxesGroup)
        self.AxesGroupToTelegramLogging(AxesGroup=AxesGroup)
        return AxesGroupToTelegram

    def AxesGroupToTelegramCyclic(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramCyclic: int = 0

        if AxesGroup.Cyclic.PlcToRob.ToolNo == -1:
            self.Telegram.PlcToRob.Cyclic.ToolNo = 255
        else:
            self.Telegram.PlcToRob.Cyclic.ToolNo = INT_TO_BYTE(AxesGroup.Cyclic.PlcToRob.ToolNo)

        if AxesGroup.Cyclic.PlcToRob.FrameNo == -1:
            self.Telegram.PlcToRob.Cyclic.FrameNo = 255
        else:
            self.Telegram.PlcToRob.Cyclic.FrameNo = INT_TO_BYTE(AxesGroup.Cyclic.PlcToRob.FrameNo)
        return AxesGroupToTelegramCyclic

    def AxesGroupToTelegramCyclicOptional(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramCyclicOptional: int = 0

        # AxesGroup.CyclicOptional.PlcToRob.SubProgramData {{{
        if AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active:
            copy_into(self.Telegram.PlcToRob.CyclicOptional.SubProgramData.Data, AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Data)

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.CartesianPosition  {{{
        if AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Active:
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.X = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.X
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Y = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Y
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Z = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Z
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rx = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Rx
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Ry = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Ry
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Rz = AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Rz
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J2_J1 = CombineHalfSints(HalfSintHi=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J2Turns, HalfSintLo=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J1Turns)
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J4_J3 = CombineHalfSints(HalfSintHi=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J4Turns, HalfSintLo=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J3Turns)
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_J6_J5 = CombineHalfSints(HalfSintHi=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J6Turns, HalfSintLo=AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.J5Turns)
            self.Telegram.PlcToRob.CyclicOptional.CartesianPosition.Turns_E1 = SINT_TO_BYTE(AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.TurnNumber.E1Turns)

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt {{{
        if AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active:
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E2 = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E2
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E3 = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E3
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E4 = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E4
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E5 = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E5
            self.Telegram.PlcToRob.CyclicOptional.CartesianPositionExt.E6 = AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.E6

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.JointPosition {{{
        if AxesGroup.CyclicOptional.PlcToRob.JointPosition.Active:
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J1 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J1
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J2 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J2
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J3 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J3
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J4 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J4
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J5 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J5
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.J6 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.J6
            self.Telegram.PlcToRob.CyclicOptional.JointPosition.E1 = AxesGroup.CyclicOptional.PlcToRob.JointPosition.E1

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.JointPositionExt {{{
        if AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.Active:
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E2 = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E2
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E3 = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E3
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E4 = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E4
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E5 = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E5
            self.Telegram.PlcToRob.CyclicOptional.JointPositionExt.E6 = AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.E6

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.Force {{{
        if AxesGroup.CyclicOptional.PlcToRob.Force.Active:
            self.Telegram.PlcToRob.CyclicOptional.Force.X = AxesGroup.CyclicOptional.PlcToRob.Force.X
            self.Telegram.PlcToRob.CyclicOptional.Force.Y = AxesGroup.CyclicOptional.PlcToRob.Force.Y
            self.Telegram.PlcToRob.CyclicOptional.Force.Z = AxesGroup.CyclicOptional.PlcToRob.Force.Z
            self.Telegram.PlcToRob.CyclicOptional.Force.Rx = AxesGroup.CyclicOptional.PlcToRob.Force.Rx
            self.Telegram.PlcToRob.CyclicOptional.Force.Ry = AxesGroup.CyclicOptional.PlcToRob.Force.Ry
            self.Telegram.PlcToRob.CyclicOptional.Force.Rz = AxesGroup.CyclicOptional.PlcToRob.Force.Rz

        # }}}
        # AxesGroup.CyclicOptional.PlcToRob.ForceExt {{{
        if AxesGroup.CyclicOptional.PlcToRob.ForceExt.Active:
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E1 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E1
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E2 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E2
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E3 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E3
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E4 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E4
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E5 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E5
            self.Telegram.PlcToRob.CyclicOptional.ForceExt.E6 = AxesGroup.CyclicOptional.PlcToRob.ForceExt.E6
        # }}}
        return AxesGroupToTelegramCyclicOptional

    def AxesGroupToTelegramFooter(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramFooter: int = 0

        self.Telegram.PlcToRob.Footer.LifeSign = GetHalfeByteLo(Value=self.Telegram.PlcToRob.Header.FastStop_LifeSign)
        return AxesGroupToTelegramFooter

    def AxesGroupToTelegramHeader(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramHeader: int = 0

        self.Telegram.PlcToRob.Header.SRCIVersion = VersionToByte(Value=AxesGroup.Cyclic.PlcToRob.SRCIVersion)
        self.Telegram.PlcToRob.Header.FastStop_LifeSign = CombineHalfBytes(HalfByteHi=AxesGroup.Cyclic.PlcToRob.FastStop, HalfByteLo=AxesGroup.Cyclic.PlcToRob.LifeSign)
        self.Telegram.PlcToRob.Header.TelegramLengthPlcToRob = self.ParCfg.Com.TelegramLengthPlcToRob
        self.Telegram.PlcToRob.Header.TelegramLengthRobToPlc = self.ParCfg.Com.TelegramLengthRobToPlc
        self.Telegram.PlcToRob.Header.AxesGroupID_Control = CombineHalfBytes(HalfByteHi=AxesGroup.Cyclic.PlcToRob.AxesGroupID, HalfByteLo=AxesGroup.Cyclic.PlcToRob.Control)
        self.Telegram.PlcToRob.Header.Reserved = 0
        self.Telegram.PlcToRob.Header.TelegramNumberPlcToRob = PlcOptionalCyclicToUint(OptionalCyclic=AxesGroup.Parameter.Plc.OptionalCyclic)
        self.Telegram.PlcToRob.Header.TelegramNumberRobToPlc = RobOptionalCyclicToUint(OptionalCyclic=AxesGroup.Parameter.Rob.OptionalCyclic)
        self.Telegram.PlcToRob.Header.ClientDate = AxesGroup.Cyclic.PlcToRob.ClientDate
        self.Telegram.PlcToRob.Header.ClientTime = AxesGroup.Cyclic.PlcToRob.ClientTime
        return AxesGroupToTelegramHeader

    def AxesGroupToTelegramLogging(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramLogging: int = 0
        # internal sequence index
        _seqIdx: int = 0
        # internal fragment index
        _fragIdx: int = 0

        for _seqIdx in range(0, AxesGroup.State.SequenceCountSend + 1):
            # check new data ?
            if AxesGroup.State.NewSEQ[_seqIdx]:
                if self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength > 0:
                    # Create log entry
                    self.CreateLogMessagePara4(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SendData: SEQ = {1}, added Sequence [{2}] with PayloadLength = {3}, HeaderLength = {4}', Para1=UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK), Para2=DINT_TO_STRING(_seqIdx), Para3=UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength), Para4=DINT_TO_STRING(4))

                for _fragIdx in range(0, AxesGroup.State.FragmentCountSend[_seqIdx] + 1):
                    if self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength > 0:
                        # Create log entry
                        self.CreateLogMessagePara6(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SendData: added Fragment [{1}] with PayloadLength = {2}, HeaderLength = {3}, CmdID <{4}>, Cmd <{5}> Fragment-Action Bits:{6}', Para1=DINT_TO_STRING(_fragIdx), Para2=UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength), Para3=DINT_TO_STRING(8), Para4=UINT_TO_STRING(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID), Para5=CMD_TYPE_TO_STRING(Value=self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.CmdType), Para6=FRAGMENT_ACTION_TO_STRING(FragmentAction=self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction))

                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SendData: added Fragment [{1}] will be executed with ExecMode = [{2}]', Para1=DINT_TO_STRING(_fragIdx), Para2=EXECUTION_MODE_TO_STRING(Value=self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode))
        return AxesGroupToTelegramLogging

    def AxesGroupToTelegramSequence(self, *, AxesGroup: _T.AxesGroup) -> int:  # PRIVATE
        AxesGroupToTelegramSequence: int = 0
        # internal index
        _idx: int = 0
        # internal sequence index
        _seqIdx: int = 0
        # Amount of sequences
        _seqCount: int = 0
        # internal fragment index
        _fragIdx: int = 0
        # internal register index
        _regIdx: int = 0
        # internal execution order list index
        _listIdx: int = 1
        # internal payload pointer
        _payLoadPtr: int = 0
        # internal fragment action
        _fragmentAction: FragmentAction = FragmentAction()
        # internal fragment action as string
        _fragmentActionString: str = ''
        # maximount amount of bytes per sequence
        SEQUENCE_MAX_PAYLOAD_SIZE: int = 0
        # current length of telegram
        _telegramLengthCurrent: int = 0

        # Check 2nd sequence active ?
        if self._parCfg.Com.TwoSequences:
            # inc sequence counter
            _seqCount = _seqCount + 1

            SEQUENCE_MAX_PAYLOAD_SIZE = wrap(self.CalculateSequencePayloadMax(AxesGroup=AxesGroup, Direction=ComDirection.PLC_TO_ROB, Sequence=SequenceFlag.SECONDARY_SEQUENCE) - self.FOOTER_SIZE, 'UDINT')
        else:
            SEQUENCE_MAX_PAYLOAD_SIZE = wrap(self.CalculateSequencePayloadMax(AxesGroup=AxesGroup, Direction=ComDirection.PLC_TO_ROB, Sequence=SequenceFlag.PRIMARY_SEQUENCE) - self.FOOTER_SIZE, 'UDINT')

        for _seqIdx in range(0, _seqCount + 1):
            # set current SEQ / ACk index
            self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK = AxesGroup.State.CurrentSEQ[_seqIdx]

            # only update telegram content if a new sequence SEQ is set
            if AxesGroup.State.NewSEQ[_seqIdx]:
                # only reset counters in case of new telegram to send
                AxesGroup.State.SequenceCountSend = 0
                AxesGroup.State.FragmentCountSend[_seqIdx] = 0

                # calc current telegram payload length
                _telegramLengthCurrent = self.CalculateTelegramLengthPlcToRob(AxesGroup=AxesGroup)

                # Bedingung anpassen und TWO_SEQUENCES berücksichtigen
                while self._parCfg.Com.TelegramLengthPlcToRob - _telegramLengthCurrent >= self.FRAGMENT_HEADER_SIZE + self.MIN_PAYLOAD_SIZE:
                    # Check command in Execution-Order-List available ?
                    if AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx] > self.EMPTY_EOL_ENTRY:
                        # set current SEQ / ACk index
                        self.Telegram.PlcToRob.Sequence[_seqIdx].Header.SEQ_ACK = AxesGroup.State.CurrentSEQ[_seqIdx]

                        # get active command register index
                        _regIdx = AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx]

                        # check State of the current ACR entry ?
                        if AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State >= BufferStateCmd.CREATED and AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State <= BufferStateCmd.SENDING:
                            # add size of fragement header
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength = wrap(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength + 8, 'UINT')

                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.CmdID = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].UniqueID
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.Reserve = 0
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction = 0  # will be set below
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadPointer = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr

                            # The 1st message resets the ACR entry on the server side
                            _fragmentAction.Reset = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State == BufferStateCmd.CREATED and AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr == 0

                            # Update messages must clear the ACR entry on the server side
                            _fragmentAction.Clear = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State == BufferStateCmd.UPDATE_AVAILABLE and AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr == 0

                            # fill telegramm header - just for later debugging ( the header is part of the command payload itselfy ) {{{
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.CmdType = CmdType(CombineBytesToUint(HiByte=AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[0], LoByte=AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[1]))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode, 0, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[2], 0))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode, 1, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[2], 1))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode, 2, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[2], 2))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ExecMode, 3, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[2], 3))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio, 0, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 0))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio, 1, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 1))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio, 2, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 2))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.Prio, 3, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 3))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence, 0, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 4))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence, 1, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 5))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence, 2, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 6))
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence = set_bit(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Header.ParSequence, 3, bit(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[3], 7))
                            # }}}
                            # loop through the payload
                            for _payLoadPtr in range(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr, AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayloadLen - 1 + 1):
                                # copy payload
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Command.Payload[_payLoadPtr] = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[_payLoadPtr]

                                # inc current sequence payload length
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength = wrap(self.Telegram.PlcToRob.Sequence[_seqIdx].Header.PayloadLength + 1, 'UINT')

                                # inc current fragment payload length
                                self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength = wrap(self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.PayloadLength + 1, 'UINT')

                                # inc payload pointer in active command register
                                AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr = wrap(AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr + 1, 'UINT')

                                # set command state
                                if AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr >= AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayloadLen:
                                    AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State = BufferStateCmd.PROCESSED
                                else:
                                    AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].State = BufferStateCmd.SENDING

                                # calc current telegram payload length
                                _telegramLengthCurrent = self.CalculateTelegramLengthPlcToRob(AxesGroup=AxesGroup)

                                # check limit reached ?
                                if _telegramLengthCurrent >= self._parCfg.Com.TelegramLengthPlcToRob:
                                    break  # -> abort for loop

                            # check payload complete ?
                            _fragmentAction.Complete = AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayLoadPtr >= AxesGroup.Acyclic.ActiveCommandRegister.Register[_regIdx].Command[self.ACTIVE_CMD].PayloadLen

                            # just for brakepoint
                            if _fragmentAction.Complete:
                                _fragmentAction.Complete = _fragmentAction.Complete

                            # set fragment action
                            self.Telegram.PlcToRob.Sequence[_seqIdx].Fragment[_fragIdx].Header.FragmentAction = FragmentActionToByte(FragmentAction=_fragmentAction)

                    # inc execution order list index
                    _listIdx = _listIdx + 1
                    # inc fragment index
                    _fragIdx = _fragIdx + 1

                    # check abort conditions
                    # Payload limit reached
                    # Max fragment limit reached
                    # No entry in ExecutionOrderList left
                    if (_telegramLengthCurrent >= self._parCfg.Com.TelegramLengthPlcToRob or _fragIdx >= RobotLibraryParameter.FRAGMENT_MAX) or AxesGroup.Acyclic.ActiveCommandRegister.ExecutionOrderList[_listIdx] == self.EMPTY_EOL_ENTRY:
                        break  # -> Abort while loop

                AxesGroup.State.SequenceCountSend = _seqIdx
                AxesGroup.State.FragmentCountSend[_seqIdx] = _fragIdx
        return AxesGroupToTelegramSequence

    def CheckParameterChanged(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterChanged: bool = False
        # internal index for loops
        _idx: int = 0

        # Check initialization is already done ?
        if not self.Initialized:
            CheckParameterChanged = False
            return CheckParameterChanged

        # compare memory
        CheckParameterChanged = SysDepMemCmp(pData1=ADR(self, 'ParCfg', _iec.StructType(RobotTaskParCfg)), pData2=ADR(self, '_parCfg', _iec.StructType(RobotTaskParCfg)), DataLen=135) != RobotLibraryConstants.OK

        for _idx in range(SyncTime.DURING_START_UP, SyncTime.AFTER_START_UP + 1):
            # Check Tool SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.Tool[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.Tool[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.Tool[_idx]))

            # Check Frame SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.Frame[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.Frame[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.Frame[_idx]))

            # Check Load SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.Load[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.Load[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.Load[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Load[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.Load[_idx]))

            # Check WorkAreas SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_WORK_AREA_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.WorkAreas[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[_idx]))

            # Check SWLimits SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.SWLimits[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[_idx]))

            # Check DefaultDynamics SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.DefaultDynamics[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[_idx]))

            # Check ReferenceDynamics SyncMode changed ?
            if self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx] != self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx]:
                # Set info
                self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED, Overwrite=True)

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SyncMode.ReferenceDynamics[{1}] changed from {2} to {3}, but this is only allowed at PLC start', Para1=SYNC_TIME_TO_STRING(Value=SyncTime(_idx)), Para2=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx]), Para3=SYNC_MODE_TO_STRING(Value=self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[_idx]))

        # Check Plc.OptionalCyclic changed ?
        if PlcOptionalCyclicToUint(OptionalCyclic=self._parCfg.Plc.OptionalCyclic) != PlcOptionalCyclicToUint(OptionalCyclic=self.ParCfg.Plc.OptionalCyclic):
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=0, MessageText='ParCfg.Plc.OptionalCyclic changed after initialization from {1} to {2} -> Reinitialize by disabling and enabling the RobotTask', Para1=WORD_TO_STRING_BIN(Value=PlcOptionalCyclicToUint(OptionalCyclic=self._parCfg.Plc.OptionalCyclic)), Para2=WORD_TO_STRING_BIN(Value=PlcOptionalCyclicToUint(OptionalCyclic=self.ParCfg.Plc.OptionalCyclic)))

        # Check Rob.OptionalCyclic changed ?
        if RobOptionalCyclicToUint(OptionalCyclic=self._parCfg.Rob.OptionalCyclic) != RobOptionalCyclicToUint(OptionalCyclic=self.ParCfg.Rob.OptionalCyclic):
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.ERROR, MessageCode=0, MessageText='ParCfg.Rob.OptionalCyclic changed after initialization from {1} to {2} -> Reinitialize by disabling and enabling the RobotTask', Para1=WORD_TO_STRING_BIN(Value=RobOptionalCyclicToUint(OptionalCyclic=self._parCfg.Rob.OptionalCyclic)), Para2=WORD_TO_STRING_BIN(Value=RobOptionalCyclicToUint(OptionalCyclic=self.ParCfg.Rob.OptionalCyclic)))
        return CheckParameterChanged

    def CheckParameterValid(self, *, AxesGroup: _T.AxesGroup) -> bool:  # PROTECTED
        CheckParameterValid: bool = False

        # init return value
        CheckParameterValid = True

        # Check ParCfg.Com.TelegramLengthPlcToRob
        if self.ParCfg.Com.TelegramLengthPlcToRob < 128:
            # Set Warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_PLC_TO_ROB_VERY_SMALL, Overwrite=True)

        # Check ParCfg.Com.TelegramLengthRobToPlc
        if self.ParCfg.Com.TelegramLengthRobToPlc < 128:
            # Set Warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_ROB_TO_PLC_VERY_SMALL, Overwrite=True)

        # Region ParCfg.Com {{{
        # Check LifeSignTimeout
        if self.ParCfg.Com.LifeSignTimeOut < 10:
            # set to valid min value
            self.ParCfg.Com.LifeSignTimeOut = 10

            # Set info
            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='LifeSignTimeout to small and set from {1}ms to 10ms', Para1=TIME_TO_STRING(self.ParCfg.Com.LifeSignTimeOut))

        # Check ParCfg.Com.TelegramLengthPlcToRob
        if self.ParCfg.Com.TelegramLengthPlcToRob < 64 or self.ParCfg.Com.TelegramLengthPlcToRob > self.ROBOT_OUT_DATA_SIZE:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Com.TelegramLengthPlcToRob {1} invalid', Para1=UINT_TO_STRING(self.ParCfg.Com.TelegramLengthPlcToRob))
            # no further validation
            return CheckParameterValid

        # Check ParCfg.Com.TelegramLengthRobToPlc
        if self.ParCfg.Com.TelegramLengthRobToPlc < 64 or self.ParCfg.Com.TelegramLengthRobToPlc > self.ROBOT_IN_DATA_SIZE:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Com.TelegramLengthRobToPlc {1} invalid', Para1=UINT_TO_STRING(self.ParCfg.Com.TelegramLengthRobToPlc))
            # no further validation
            return CheckParameterValid

        # EndRegion }}}
        # Region ParCfg.Rob.OptionalCyclic {{{
        # Check configuration if optional cyclic CartesianPosition valid ?
        if self.ParCfg.Rob.OptionalCyclic.UseCartesianPosition and self.ParCfg.Rob.OptionalCyclic.UseCartesianPositionExt:
            # set to valid configuration
            self.ParCfg.Rob.OptionalCyclic.UseCartesianPosition = True
            self.ParCfg.Rob.OptionalCyclic.UseCartesianPositionExt = False

            # Set info
            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_RECV_EXT_CART_POS_NOT_USABLE_WITH_RECV_CART_POS, Overwrite=True)

            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='UseCartesianPosition and UseCartesianPositionExt cannot be configured together -> UseCartesianPosition is automatically activated')

        # Check configuration if optional cyclic JointPosition valid ?
        # {warning 'ToDo: Yaskawa need this combination for debugging via JointPosExt '}
        if (self.ParCfg.Rob.OptionalCyclic.UseJointPosition and self.ParCfg.Rob.OptionalCyclic.UseJointPositionExt) and False:
            # set to valid configuration
            self.ParCfg.Rob.OptionalCyclic.UseJointPosition = True
            self.ParCfg.Rob.OptionalCyclic.UseJointPositionExt = False

            # Set info
            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_RECV_EXT_JOINT_POS_NOT_USABLE_WITH_RECV_JOINT_POS, Overwrite=True)

            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='UseJointPosition and UseJointPositionExt cannot be configured together -> UseJointPosition is automatically activated')

        # EndRegion }}}
        # Region ParCfg.Parameter.SynchronizationModes {{{
        # Check ToolData synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_DATA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check ToolData synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_DATA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check FrameData synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_DATA_SYNC_MODE_INVALID, Overwrite=False)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check FrameData synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_DATA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check LoadData synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_DATA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check LoadData synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_DATA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check WorkAreas synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check WorkAreas synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check SWLimits synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check SWLimits synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check DefaultDynamics synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check DefaultDynamics synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check ReferenceDynamics synchronisation mode during startup
        # Automatic is not allowed during startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] >= SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP]))
            # no further validation
            return CheckParameterValid

        # Check ReferenceDynamics synchronisation mode after startup
        if self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] < SyncMode.NO_SYNCHRONIZATION or self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] > SyncMode.AUTOMATIC:
            # parameter(s) not valid
            CheckParameterValid = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)  # own defined error - not in specification
            # Set warning
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID, Overwrite=True)

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] invalid SyncMode {1}', Para1=SYNC_MODE_TO_STRING(Value=self.ParCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]))
            # no further validation
            return CheckParameterValid
        # EndRegion }}}
        return CheckParameterValid

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'MC_RobotTaskFB'

        # Create log entry
        self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='PLC started / restarted')
        return FB_init

    def HandleAliveBit(self, *, LifeSign: int = 0) -> None:  # PRIVATE
        if self._HandleAliveBit_First and LifeSign > 0:
            # init alive value
            self._aliveValue = LifeSign
            # reset first flag
            self._HandleAliveBit_First = False

        self._aliveCheck(IN=self._aliveValue == LifeSign, PT=self.ParCfg.Com.LifeSignTimeOut + self.ParCfg.Plc.CycleTime)
        self._alive_R(CLK=self._aliveBit)
        self._alive_F(CLK=self._aliveBit)

        if self._aliveValue != LifeSign:
            self._aliveValue = LifeSign
            self._aliveBit = True

        if self._aliveCheck.Q:
            self._aliveBit = False

        if self._alive_R.Q:
            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='Data Exchange is running (Alive-Bit)')

        if self._alive_F.Q:
            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='Data Exchange has stopped (Alive-Bit)')

    def HandleAxesGroup(self, *, AxesGroup: _T.AxesGroup, ToolData: list[Tool], FrameData: list[Frame], LoadData: list[Load], WorkAreas: list[RobotWorkArea], SWLimits: _T.SWLimits, DefaultDynamics: _T.DefaultDynamics, ReferenceDynamics: _T.ReferenceDynamics) -> None:  # PRIVATE
        self.HandleAxesGroupAcyclic(AxesGroup=AxesGroup)
        self.HandleAxesGroupCyclic(AxesGroup=AxesGroup)
        self.HandleAxesGroupCyclicOptional(AxesGroup=AxesGroup)
        self.HandleAxesGroupMessageLog(AxesGroup=AxesGroup)
        self.HandleAxesGroupParameter(AxesGroup=AxesGroup)
        self.HandleAxesGroupState(AxesGroup=AxesGroup)
        self.HandleAxesGroupSystemData(AxesGroup=AxesGroup, ToolData=ToolData, FrameData=FrameData, LoadData=LoadData, WorkAreas=WorkAreas, SWLimits=SWLimits, DefaultDynamics=DefaultDynamics, ReferenceDynamics=ReferenceDynamics)

    def HandleAxesGroupAcyclic(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # Call active command register FB
        AxesGroup.Acyclic.ActiveCommandRegister(SystemTime=self.SystemTime, RegisterSize=MIN(RobotLibraryParameter.ACTIVE_CMD_REGISTER_ENTRIES_MAX, AxesGroup.Parameter.Rob.Parameter.LengthACR), InternalLogger=AxesGroup.MessageLog, ExternalLogger=AxesGroup.MessageLog.ExternalLogger, LogLevel=AxesGroup.MessageLog.LogLevel)

    def HandleAxesGroupCyclic(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # set instance AxesGroupID
        AxesGroup.Cyclic.PlcToRob.AxesGroupID = self.AxesGroupID
        # Set Version
        copy_into(AxesGroup.Cyclic.PlcToRob.SRCIVersion, RobotLibraryConstants.SRCIVersion)

        AxesGroup.Cyclic.PlcToRob.TelegramLengthPlcToRob = self._parCfg.Com.TelegramLengthPlcToRob
        AxesGroup.Cyclic.PlcToRob.TelegramLengthRobToPlc = self._parCfg.Com.TelegramLengthRobToPlc

        AxesGroup.Cyclic.PlcToRob.TelegramNumberPlcToRob = PlcOptionalCyclicToUint(OptionalCyclic=AxesGroup.Parameter.Plc.OptionalCyclic)
        AxesGroup.Cyclic.PlcToRob.TelegramNumberRobToPlc = RobOptionalCyclicToUint(OptionalCyclic=AxesGroup.Parameter.Rob.OptionalCyclic)

        # Set Date + Time
        AxesGroup.Cyclic.PlcToRob.ClientDate = DATE_TO_IEC_DATE(Value=self.SystemTime.SystemDate)
        AxesGroup.Cyclic.PlcToRob.ClientTime = TIME_TO_IEC_TIME(Value=self.SystemTime.SystemTime)

    def HandleAxesGroupCyclicOptional(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # PlcToRob {{{
        AxesGroup.CyclicOptional.PlcToRob.SubProgramData.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCallSubprogram
        AxesGroup.CyclicOptional.PlcToRob.CartesianPosition.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCartesianPosition
        AxesGroup.CyclicOptional.PlcToRob.JointPosition.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseJointPosition
        AxesGroup.CyclicOptional.PlcToRob.Force.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseForce
        AxesGroup.CyclicOptional.PlcToRob.CartesianPositionExt.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseCartesianPositionExt
        AxesGroup.CyclicOptional.PlcToRob.JointPositionExt.Active = AxesGroup.Parameter.Plc.OptionalCyclic.UseJointPositionExt

        # }}}
        # RobToPlc {{{
        AxesGroup.CyclicOptional.RobToPlc.SubProgramData.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCallSubprogram
        AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCartesianPosition
        AxesGroup.CyclicOptional.RobToPlc.JointPosition.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseJointPosition
        AxesGroup.CyclicOptional.RobToPlc.Force.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseForce
        AxesGroup.CyclicOptional.RobToPlc.Current.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCurrent
        AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCartesianPositionExt
        AxesGroup.CyclicOptional.RobToPlc.JointPositionExt.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseJointPositionExt
        AxesGroup.CyclicOptional.RobToPlc.ForceExt.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseForceExt
        AxesGroup.CyclicOptional.RobToPlc.CurrentExt.Active = AxesGroup.Parameter.Rob.OptionalCyclic.UseCurrentExt
        # }}}

    def HandleAxesGroupMessageLog(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # Set External logger
        AxesGroup.MessageLog.ExternalLogger = self.ExternalLogger
        AxesGroup.MessageLog.LogLevel = self.LogLevel

        if AxesGroup.State.GroupReset_R.Q:
            AxesGroup.MessageLog.DeleteMessages()
            AxesGroup.MessageLog.DeleteSystemLogs()

    def HandleAxesGroupParameter(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        if self._exchangeConfiguration.Enabled:
            copy_into(AxesGroup.Parameter.Plc.Parameter, self._parCfg.Plc.Parameter)
            copy_into(AxesGroup.Parameter.Plc.OptionalCyclic, self._parCfg.Plc.OptionalCyclic)
            copy_into(AxesGroup.Parameter.Rob.OptionalCyclic, self._parCfg.Rob.OptionalCyclic)

            AxesGroup.Parameter.Rob.Parameter.LengthACR = self._exchangeConfiguration.OutCmd.LengthACR
            AxesGroup.Parameter.Rob.Parameter.HighestToolIndex = self._exchangeConfiguration.OutCmd.HighestToolIndex
            AxesGroup.Parameter.Rob.Parameter.HighestFrameIndex = self._exchangeConfiguration.OutCmd.HighestFrameIndex
            AxesGroup.Parameter.Rob.Parameter.HighestLoadIndex = self._exchangeConfiguration.OutCmd.HighestLoadIndex
            AxesGroup.Parameter.Rob.Parameter.HighestWorkAreaIndex = self._exchangeConfiguration.OutCmd.HighestWorkAreaIndex
            copy_into(AxesGroup.Parameter.Rob.Parameter.DataInSync, self._exchangeConfiguration.OutCmd.DataInSync)
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexTool = self._exchangeConfiguration.OutCmd.ChangeIndexTool
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexFrame = self._exchangeConfiguration.OutCmd.ChangeIndexFrame
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexLoad = self._exchangeConfiguration.OutCmd.ChangeIndexLoad
            AxesGroup.Parameter.Rob.Parameter.ChangeIndexWorkArea = self._exchangeConfiguration.OutCmd.ChangeIndexWorkArea
            AxesGroup.Parameter.Rob.Parameter.RAWorkingHours = self._exchangeConfiguration.OutCmd.RAWorkingHours
            AxesGroup.Parameter.Rob.Parameter.BrakeTestRequired = self._exchangeConfiguration.OutCmd.BrakeTestRequired
            AxesGroup.Parameter.Rob.Parameter.StepModeExactStopActive = self._exchangeConfiguration.OutCmd.StepModeExactStopActive
            AxesGroup.Parameter.Rob.Parameter.StepModeBlendingActive = self._exchangeConfiguration.OutCmd.StepModeBlendingActive
            AxesGroup.Parameter.Rob.Parameter.PathAccuracyMode = self._exchangeConfiguration.OutCmd.PathAccuracyMode
            AxesGroup.Parameter.Rob.Parameter.AvoidSingularity = self._exchangeConfiguration.OutCmd.AvoidSingularity
            AxesGroup.Parameter.Rob.Parameter.CollisionDetectionEnabled = self._exchangeConfiguration.OutCmd.CollisionDetectionEnabled
            AxesGroup.Parameter.Rob.Parameter.AcceleratingSupported = self._exchangeConfiguration.OutCmd.AcceleratingSupported
            AxesGroup.Parameter.Rob.Parameter.DecceleratingSupported = self._exchangeConfiguration.OutCmd.DecceleratingSupported
            AxesGroup.Parameter.Rob.Parameter.ConstantVelocitySupported = self._exchangeConfiguration.OutCmd.ConstantVelocitySupported
            AxesGroup.Parameter.Rob.Parameter.RCWorkingHours = self._exchangeConfiguration.OutCmd.RCWorkingHours
        else:
            copy_into(AxesGroup.Parameter.Plc.Parameter, self.ParCfg.Plc.Parameter)
            copy_into(AxesGroup.Parameter.Plc.OptionalCyclic, self.ParCfg.Plc.OptionalCyclic)
            copy_into(AxesGroup.Parameter.Rob.OptionalCyclic, self.ParCfg.Rob.OptionalCyclic)

    def HandleAxesGroupState(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # internal index for loops
        _idx: int = 0

        AxesGroup.State.AliveOk = self._aliveBit
        AxesGroup.State.Initialized = self.Initialized and AxesGroup.State.AliveOk
        AxesGroup.State.Synchronized = self.Synchronized and AxesGroup.State.AliveOk
        AxesGroup.State.CMDsEnabled = AxesGroup.State.Initialized or AxesGroup.State.Synchronized

        copy_into(AxesGroup.State.StatusRobotArm, AxesGroup.Cyclic.RobToPlc.StatusRobotArm)
        AxesGroup.State.ConfigExchanged = self._exchangeConfiguration.Enabled

        AxesGroup.State.UnifiedFrameIndex = DINT_TO_USINT(MIN(MIN(AxesGroup.SystemData.FrameDataMax, RobotLibraryParameter.FRAME_MAX - 1), self._exchangeConfiguration.OutCmd.HighestFrameIndex))
        AxesGroup.State.UnifiedToolIndex = DINT_TO_USINT(MIN(MIN(AxesGroup.SystemData.ToolDataMax, RobotLibraryParameter.TOOL_MAX - 1), self._exchangeConfiguration.OutCmd.HighestToolIndex))
        AxesGroup.State.UnifiedLoadIndex = DINT_TO_USINT(MIN(MIN(AxesGroup.SystemData.LoadDataMax, RobotLibraryParameter.LOAD_MAX - 1), self._exchangeConfiguration.OutCmd.HighestLoadIndex))
        AxesGroup.State.UnifiedWorkAreaIndex = DINT_TO_USINT(MIN(MIN(AxesGroup.SystemData.WorkAreasMax, RobotLibraryParameter.WORK_AREAS_MAX - 1), self._exchangeConfiguration.OutCmd.HighestWorkAreaIndex))

        copy_into(AxesGroup.State.DataEnableSync, self._exchangeConfiguration.ParCmd.DataEnableSync)
        AxesGroup.State.SyncStateRc.InSync.Frame = self._exchangeConfiguration.OutCmd.DataInSync.FramesInSync
        AxesGroup.State.SyncStateRc.InSync.Tool = self._exchangeConfiguration.OutCmd.DataInSync.ToolsInSync
        AxesGroup.State.SyncStateRc.InSync.Load = self._exchangeConfiguration.OutCmd.DataInSync.LoadsInSync
        AxesGroup.State.SyncStateRc.InSync.WorkArea = self._exchangeConfiguration.OutCmd.DataInSync.WorkAreasInSync
        AxesGroup.State.SyncStateRc.InSync.SwLimits = self._exchangeConfiguration.OutCmd.DataInSync.SoftwareLimitsInSync
        AxesGroup.State.SyncStateRc.InSync.DefaultDynamics = self._exchangeConfiguration.OutCmd.DataInSync.DefaultDynamicsInSync
        AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics = self._exchangeConfiguration.OutCmd.DataInSync.ReferenceDynamicsInSync

        AxesGroup.State.SyncStateRc.UnSyncNo.Frame = self._exchangeConfiguration.OutCmd.ChangeIndexFrame
        AxesGroup.State.SyncStateRc.UnSyncNo.Tool = self._exchangeConfiguration.OutCmd.ChangeIndexTool
        AxesGroup.State.SyncStateRc.UnSyncNo.Load = self._exchangeConfiguration.OutCmd.ChangeIndexLoad
        AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea = self._exchangeConfiguration.OutCmd.ChangeIndexWorkArea

        # Update internal data
        copy_into(AxesGroup.State.SystemTime, self.SystemTime)
        AxesGroup.State.OnlineChange = self.OnlineChange
        AxesGroup.State.Initialized = self.Initialized

        # Create rising and falling edges for Online Change
        AxesGroup.State.OnlineChange_R(CLK=self.OnlineChange)
        AxesGroup.State.OnlineChange_F(CLK=self.OnlineChange)

        # Create rising and falling edges for GroupReset
        AxesGroup.State.GroupReset_R(CLK=AxesGroup.State.GroupReset)
        AxesGroup.State.GroupReset_F(CLK=AxesGroup.State.GroupReset)

        # Copy function block results
        copy_into(AxesGroup.State.RobotData, self._readRobotData.OutCmd)
        copy_into(AxesGroup.State.ConfigurationData, self._exchangeConfiguration.OutCmd)

    def HandleAxesGroupSystemData(self, *, AxesGroup: _T.AxesGroup, ToolData: list[Tool], FrameData: list[Frame], LoadData: list[Load], WorkAreas: list[RobotWorkArea], SWLimits: _T.SWLimits, DefaultDynamics: _T.DefaultDynamics, ReferenceDynamics: _T.ReferenceDynamics) -> None:  # PRIVATE
        # Update ToolData
        AxesGroup.SystemData.ToolDataPtr = ADR(ToolData, None, array_type(ToolData, _iec.StructType(Tool)))
        AxesGroup.SystemData.ToolDataMin = LOWER_BOUND(ToolData)
        AxesGroup.SystemData.ToolDataMax = UPPER_BOUND(ToolData)
        AxesGroup.SystemData.ToolDataCount = DINT_TO_UDINT(1 + AxesGroup.SystemData.ToolDataMax - AxesGroup.SystemData.ToolDataMin)

        # Update LoadData
        AxesGroup.SystemData.LoadDataPtr = ADR(LoadData, None, array_type(LoadData, _iec.StructType(Load)))
        AxesGroup.SystemData.LoadDataMin = LOWER_BOUND(LoadData)
        AxesGroup.SystemData.LoadDataMax = UPPER_BOUND(LoadData)
        AxesGroup.SystemData.LoadDataCount = DINT_TO_UDINT(1 + AxesGroup.SystemData.LoadDataMax - AxesGroup.SystemData.LoadDataMin)

        # Update FrameData
        AxesGroup.SystemData.FrameDataPtr = ADR(FrameData, None, array_type(FrameData, _iec.StructType(Frame)))
        AxesGroup.SystemData.FrameDataMin = LOWER_BOUND(FrameData)
        AxesGroup.SystemData.FrameDataMax = UPPER_BOUND(FrameData)
        AxesGroup.SystemData.FrameDataCount = DINT_TO_UDINT(1 + AxesGroup.SystemData.FrameDataMax - AxesGroup.SystemData.FrameDataMin)

        # Update WorkAreas
        AxesGroup.SystemData.WorkAreasPtr = ADR(WorkAreas, None, array_type(WorkAreas, _iec.StructType(RobotWorkArea)))
        AxesGroup.SystemData.WorkAreasMin = LOWER_BOUND(WorkAreas)
        AxesGroup.SystemData.WorkAreasMax = UPPER_BOUND(WorkAreas)
        AxesGroup.SystemData.WorkAreasCount = DINT_TO_UDINT(1 + AxesGroup.SystemData.WorkAreasMax - AxesGroup.SystemData.WorkAreasMin)

        # Update SoftwareLimits
        AxesGroup.SystemData.SWLimits = SWLimits
        # Update DefaultDynamics
        AxesGroup.SystemData.DefaultDynamics = DefaultDynamics
        # Update ReferenceDynamics
        AxesGroup.SystemData.ReferenceDynamics = ReferenceDynamics

    def HandleInvalidFrames(self, *, AxesGroup: _T.AxesGroup, RobotInData: list[int]) -> None:  # PRIVATE
        # Value of lifesign in header
        _lifeSignHeader: int = 0
        # Value of lifesign in footer
        _lifeSignFooter: int = 0

        if AxesGroup.Cyclic.RobToPlc.TelegramState == TelegramState.INITIALIZED:
            # Get lifesign values
            _lifeSignHeader = GetHalfeByteHi(Value=RobotInData[self.ROBOT_IN_DATA_MIN + 1])
            _lifeSignFooter = GetHalfeByteHi(Value=RobotInData[self.ROBOT_IN_DATA_MAX + 0])

        # Timer for invalid frame(s) message
        self._HandleInvalidFrames__invalidFrameCounterCheck_D(IN=True, PT=RobotLibraryParameter.INVALID_FRAMES_CHECK_TIMEOUT)

        # Check Frame is valid :
        # ----------------------
        if _lifeSignHeader != _lifeSignFooter:
            AxesGroup.State.InvalidFrames = wrap(AxesGroup.State.InvalidFrames + 1, 'UDINT')

        # Check timeout for invalid frame message
        if self._HandleInvalidFrames__invalidFrameCounterCheck_D.Q:
            # reset timer
            self._HandleInvalidFrames__invalidFrameCounterCheck_D(IN=False)

            # compare invalid frame(s) counter
            if AxesGroup.State.InvalidFrames != self._HandleInvalidFrames__lastInvalidFrames:
                # store last invalid frame(s) counter value
                self._HandleInvalidFrames__lastInvalidFrames = AxesGroup.State.InvalidFrames
                # Create log entry
                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=0, MessageText='Detected invalid frames {1} in total', Para1=UDINT_TO_STRING(AxesGroup.State.InvalidFrames))

        # Reset invalid frames counter with rising edge of group reset
        if AxesGroup.State.GroupReset_R.Q:
            AxesGroup.State.InvalidFrames = 0
            self._HandleInvalidFrames__lastInvalidFrames = 0

            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='Reset invalid frames counter by executing GroupReset')

    def HandleLifeSign(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        if self._HandleLifeSign__first or not self.Enable:
            # init LifeSign
            AxesGroup.Cyclic.PlcToRob.LifeSign = 0
            # reset first flag
            self._HandleLifeSign__first = False
            # prevent inc LifeSign in the 1st cycle (Code below)
            return

        AxesGroup.Cyclic.PlcToRob.LifeSign = wrap(AxesGroup.Cyclic.PlcToRob.LifeSign + 1, 'BYTE')

        if AxesGroup.Cyclic.PlcToRob.LifeSign > 15:
            AxesGroup.Cyclic.PlcToRob.LifeSign = 1  # 0 is only in the very 1st cycle to indicate the system start in logging

        if self.Enable and self._alive_F.Q:
            # Reset initialized flag
            self.Initialized = False
            # Reset Synchronized flag
            self.Synchronized = False

            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_CONNECTION_LOST, Overwrite=True)
            # Create log entry
            self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.FATAL_ERROR, MessageCode=0, MessageText='LifeSign timeout -> Reinitialization required !')

        # Reset connection lost error
        if (not self.Enable and self._aliveBit) and self.ErrorID == RobotLibraryErrorIdEnum.ERR_CONNECTION_LOST:
            self.ErrorID = 0

    def HandleLogMessagesAck(self, *, AxesGroup: _T.AxesGroup) -> None:
        if self._readMessages.Enabled:
            # Set Message ID as Acknowlege ID
            self._readMessages.ParCmd.MsgID = self._readMessages.OutCmd.MsgId
        else:
            # Reset Acknowlege ID
            self._readMessages.ParCmd.MsgID = 0
        # IF (( _readMessages.Enabled           ) AND
        #     ( _readMessages.OutCmd.MsgId > 0  ))
        # THEN
        #   // Check if message has been entered into the message log ?
        #   IF ( AxesGroup.MessageLog.CheckMessageCodePresent(_readMessages.OutCmd.ErrorCode ))
        #   THEN
        #     // Set Message ID as Acknowlege ID
        #    _readMessages.ParCmd.MsgID := _readMessages.OutCmd.MsgId;
        # 	END_IF
        # END_IF

    def HandleSeqAck(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # internal index for loops
        _idx: int = 0

        for _idx in range(0, AxesGroup.State.SequenceCountSend + 1):
            AxesGroup.State.CurrentACK[_idx] = self.Telegram.RobToPlc.Sequence[_idx].Header.SEQ_ACK

            if not self.Enable:
                AxesGroup.State.CurrentSEQ[0] = 0
                AxesGroup.State.CurrentSEQ[1] = 0

            # Check Seq/Ack :
            # ----------------------
            if AxesGroup.State.CurrentACK[_idx] == AxesGroup.State.CurrentSEQ[_idx]:
                AxesGroup.State.CurrentSEQ[_idx] = wrap(MAX(AxesGroup.State.CurrentSEQ[0], AxesGroup.State.CurrentSEQ[1]) + 1, 'UINT')

                # {warning 'ToDo: Test for Yaskawa'}
                if AxesGroup.State.CurrentSEQ[_idx] >= 255:
                    AxesGroup.State.CurrentSEQ[_idx] = 0

                AxesGroup.State.NewSEQ[_idx] = True

    def HandleSync(self, *, AxesGroup: _T.AxesGroup, ToolData: list[Tool], FrameData: list[Frame], LoadData: list[Load], WorkAreas: list[RobotWorkArea], SWLimits: _T.SWLimits, DefaultDynamics: _T.DefaultDynamics, ReferenceDynamics: _T.ReferenceDynamics) -> None:  # PRIVATE
        # flag that indicates at least any iten has enabled synchronisation
        _dataEnableSyncAny: bool = False
        # flag that indicates that the frame datas are synchronized or deactivated
        _inSyncFrameOk: bool = False
        # flag that indicates that the tool datas are synchronized or deactivated
        _inSyncToolOk: bool = False
        # flag that indicates that the load datas are synchronized or deactivated
        _inSyncLoadOk: bool = False
        # flag that indicates that the work areas are synchronized or deactivated
        _inSyncWorkAreaOk: bool = False
        # flag that indicates that the SW limits are synchronized or deactivated
        _inSyncSwLimitsOk: bool = False
        # flag that indicates that the default dynamice are synchronized or deactivated
        _inSyncDefaultDynamicOk: bool = False
        # flag that indicates that the reference dynamice are synchronized or deactivated
        _InSyncReferenceDynamicOk: bool = False

        self.HandleSyncToolData(AxesGroup=AxesGroup, ToolData=ToolData)
        self.HandleSyncFrameData(AxesGroup=AxesGroup, FrameData=FrameData)
        self.HandleSyncLoadData(AxesGroup=AxesGroup, LoadData=LoadData)
        self.HandleSyncRobotDefaultDynamics(AxesGroup=AxesGroup, DefaultDynamics=DefaultDynamics)
        self.HandleSyncRobotReferenceDynamics(AxesGroup=AxesGroup, ReferenceDynamics=ReferenceDynamics)
        self.HandleSyncRobotSWLimits(AxesGroup=AxesGroup, SWLimits=SWLimits)
        self.HandleSyncToolData(AxesGroup=AxesGroup, ToolData=ToolData)
        self.HandleSyncWorkArea(AxesGroup=AxesGroup, WorkAreas=WorkAreas)

        # check any synchronisation activated ?
        _dataEnableSyncAny = (((((AxesGroup.State.DataEnableSync.EnableSyncFrame or AxesGroup.State.DataEnableSync.EnableSyncTool) or AxesGroup.State.DataEnableSync.EnableSyncLoad) or AxesGroup.State.DataEnableSync.EnableSyncWorkArea) or AxesGroup.State.DataEnableSync.EnableSyncSWLimits) or AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics) or AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics

        _inSyncFrameOk = AxesGroup.State.SyncStatePlc.InSync.Frame and AxesGroup.State.SyncStateRc.InSync.Frame or not AxesGroup.State.DataEnableSync.EnableSyncFrame

        _inSyncToolOk = AxesGroup.State.SyncStatePlc.InSync.Tool and AxesGroup.State.SyncStateRc.InSync.Tool or not AxesGroup.State.DataEnableSync.EnableSyncTool

        _inSyncLoadOk = AxesGroup.State.SyncStatePlc.InSync.Load and AxesGroup.State.SyncStateRc.InSync.Load or not AxesGroup.State.DataEnableSync.EnableSyncLoad

        _inSyncWorkAreaOk = AxesGroup.State.SyncStatePlc.InSync.WorkArea and AxesGroup.State.SyncStateRc.InSync.WorkArea or not AxesGroup.State.DataEnableSync.EnableSyncWorkArea

        _inSyncSwLimitsOk = AxesGroup.State.SyncStatePlc.InSync.SwLimits and AxesGroup.State.SyncStateRc.InSync.SwLimits or not AxesGroup.State.DataEnableSync.EnableSyncSWLimits

        _inSyncDefaultDynamicOk = AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics and AxesGroup.State.SyncStateRc.InSync.DefaultDynamics or not AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics

        _InSyncReferenceDynamicOk = AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics and AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics or not AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics

        self.Synchronized = ((((((_inSyncFrameOk and _inSyncToolOk) and _inSyncLoadOk) and _inSyncWorkAreaOk) and _inSyncSwLimitsOk) and _inSyncDefaultDynamicOk) and _InSyncReferenceDynamicOk) and _dataEnableSyncAny

        # Update exchange configuration parameter
        self._exchangeConfiguration.ParCmd.DataInSync.FramesInSync = AxesGroup.State.SyncStatePlc.InSync.Frame  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncFrame );
        self._exchangeConfiguration.ParCmd.DataInSync.ToolsInSync = AxesGroup.State.SyncStatePlc.InSync.Tool  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncTool );
        self._exchangeConfiguration.ParCmd.DataInSync.LoadsInSync = AxesGroup.State.SyncStatePlc.InSync.Load  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncLoad );
        self._exchangeConfiguration.ParCmd.DataInSync.WorkAreasInSync = AxesGroup.State.SyncStatePlc.InSync.WorkArea  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncWorkArea );
        self._exchangeConfiguration.ParCmd.DataInSync.SoftwareLimitsInSync = AxesGroup.State.SyncStatePlc.InSync.SwLimits  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncSWLimits );
        self._exchangeConfiguration.ParCmd.DataInSync.DefaultDynamicsInSync = AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics );
        self._exchangeConfiguration.ParCmd.DataInSync.ReferenceDynamicsInSync = AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics  # OR ( NOT AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics);

    def HandleSyncFrameData(self, *, AxesGroup: _T.AxesGroup, FrameData: list[Frame]) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx: int = 0

        # Set internal references
        _stepName = '_stepSyncFrameData = '
        # _rStep REF= self._stepSyncFrameData  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncFrameData  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncFrameData  (reference: _rTimeout is replaced by it)
        # _rSyncIdx REF= self._syncIdxFrameData  (reference: _rSyncIdx is replaced by it)

        match self._stepSyncFrameData:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # Check More Data on RC than on PLC -> Synchronization not possible
                if AxesGroup.State.ConfigurationData.HighestFrameIndex > AxesGroup.SystemData.FrameDataCount:
                    self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_FRAME_COUNT_RC_HIGHER_THAN_PLC, Overwrite=False)
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadFrameData and AxesGroup.State.RobotData.RCSupportedFunctions.WriteFrameData) and AxesGroup.State.Initialized) and (not self.Error):
                    # Check PLC frames < RC frames and SyncFrame enabled ?
                    if AxesGroup.State.DataEnableSync.EnableSyncFrame == True and AxesGroup.Parameter.Rob.Parameter.HighestFrameIndex > AxesGroup.SystemData.FrameDataMax:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_TOO_SHORT, Overwrite=True)

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Start initial reading of FrameData from RC', Para1='')

                    # init frame number
                    self._syncIdxFrameData = DINT_TO_USINT(AxesGroup.SystemData.FrameDataMin)
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = self._stepSyncFrameData + 1

            # Start read FrameData
            case 1:
                if (not self._readFrameData.Busy and (not self._readFrameData.Error)) and (not self._readFrameData.Done):
                    # set command parameter
                    self._readFrameData.ParCmd.FrameNo = self._syncIdxFrameData
                    # execute command
                    self._readFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = self._stepSyncFrameData + 1
                else:
                    # check error ?
                    if self._readFrameData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            # Wait Framedata read
            case 2:
                if (not self._readFrameData.Busy and (not self._readFrameData.Error)) and self._readFrameData.Done:
                    # reset execution
                    self._readFrameData.Execute = False
                    # set available bit
                    self._frameData[self._syncIdxFrameData].Available = True
                    FrameData[self._syncIdxFrameData].Available = True
                    # Copy data
                    copy_into(self._frameData[self._syncIdxFrameData].Data, self._readFrameData.OutCmd.FrameData)

                    # Check frame data is equal ?
                    if not IsFrameDataEqual(Data1=self._frameData[self._syncIdxFrameData].Data, Data2=FrameData[self._syncIdxFrameData].Data, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Frame = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData] = True
                        # inc count of unsynchronised plc frames
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Frame + 1, 'USINT')

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Detected a difference in Frame[{1}] between PLC and RC', Para1=DINT_TO_STRING(self._syncIdxFrameData))

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncFrame:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_FRAME_DATA_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Frame:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_NUMBER_SYNC_ERROR, Overwrite=False)

                    # Check all frames read ?
                    if self._syncIdxFrameData < AxesGroup.State.UnifiedFrameIndex:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                        # inc frame index
                        self._syncIdxFrameData = wrap(self._syncIdxFrameData + 1, 'USINT')
                        # dec step counter
                        self._stepSyncFrameData = self._stepSyncFrameData - 1
                    else:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                        # inc step counter
                        self._stepSyncFrameData = self._stepSyncFrameData + 1
                else:
                    # check error ?
                    if self._readFrameData.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        FrameData[self._syncIdxFrameData].Available = False
                        self._frameData[self._syncIdxFrameData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            # Check synchronisation state ?
            case 3:
                if AxesGroup.State.SyncStatePlc.UnSyncNo.Frame == 0 or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Frame = AxesGroup.State.SyncStatePlc.UnSyncNo.Frame == 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Frame:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                for _idx in range(AxesGroup.SystemData.FrameDataMin, AxesGroup.SystemData.FrameDataMax + 1):
                                    # Overwrite PLC data with RC data
                                    copy_into(FrameData[_idx], self._frameData[_idx])

                                # Reset data changed flags
                                copy_into(AxesGroup.State.DataChanged.Frame, _dataChangedNone.Frame)
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Frame = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Frame = True
                                # Reset count of unsynchronised plc frames
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                                # inc step counter
                                self._stepSyncFrameData = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frames triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Applied the initial read frame data from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                # Check conflicts to solve ?
                                for self._syncIdxFrameData in range(0, AxesGroup.State.UnifiedFrameIndex + 1):
                                    if AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData]:
                                        _found = True
                                        break
                                else:
                                    self._syncIdxFrameData = st_for_end(0, AxesGroup.State.UnifiedFrameIndex)

                                if _found:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Frame = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Frame = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                                    # inc step counter
                                    self._stepSyncFrameData = self._stepSyncFrameData + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    copy_into(AxesGroup.State.DataChanged.Frame, _dataChangedNone.Frame)
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Frame = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Frame = True
                                    # Reset count of unsynchronised frames
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                                    # inc step counter
                                    self._stepSyncFrameData = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write frame data
            case 4:
                if not self._writeFrameData.Busy and (not self._writeFrameData.Error):
                    # set command parameter
                    self._writeFrameData.ParCmd.FrameNo = self._syncIdxFrameData
                    copy_into(self._writeFrameData.ParCmd.FrameData, FrameData[self._syncIdxFrameData].Data)
                    # execute command
                    self._writeFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = self._stepSyncFrameData + 1
                else:
                    # check error ?
                    if self._writeFrameData.Error:
                        self.ErrorID = self._writeFrameData.ErrorID
                        self.ErrorAddTxt = self._writeFrameData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            # Wait frame data written ?
            case 5:
                if (not self._writeFrameData.Busy and (not self._writeFrameData.Error)) and self._writeFrameData.Done:
                    # execute command
                    self._writeFrameData.Execute = False
                    # apply frame data to internal frame data
                    copy_into(self._frameData[self._syncIdxFrameData], FrameData[self._syncIdxFrameData])
                    # reset data changed bit
                    AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData] = False
                    # dec count of unsynchronised frames
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Frame - 1, 'USINT')
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # dec step counter
                    self._stepSyncFrameData = self._stepSyncFrameData - 2
                else:
                    # check error ?
                    if self._writeFrameData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # reset count of unsynchronised frames
                AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0

                # Check all frame datas
                for self._syncIdxFrameData in range(0, AxesGroup.State.UnifiedFrameIndex + 1):
                    # compare frame data
                    AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData] = not IsFrameDataEqual(Data1=FrameData[self._syncIdxFrameData].Data, Data2=self._frameData[self._syncIdxFrameData].Data, IgnoreTimestamp=False)

                    # Check Frame data changed ?
                    if AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData]:
                        # inc count of unsynchronised plc frames
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Frame + 1, 'USINT')
                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Detected a local change of Frame[{1}] on PLC, SyncTime = {2}', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Frame = AxesGroup.State.SyncStatePlc.UnSyncNo.Frame == 0

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.Frame) != (not AxesGroup.State.SyncStateRc.InSync.Frame):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.Frame and (not AxesGroup.State.SyncStateRc.InSync.Frame):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.Frame:
                    # search for changed index
                    for self._syncIdxFrameData in range(0, AxesGroup.State.UnifiedFrameIndex + 1):
                        if AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxFrameData = st_for_end(0, AxesGroup.State.UnifiedFrameIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Frame:
                    # get changed index
                    self._syncIdxFrameData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                # jump back
                self._stepSyncFrameData = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.Frame:
                    # search for changed index
                    for self._syncIdxFrameData in range(0, AxesGroup.State.UnifiedFrameIndex + 1):
                        if AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 20  # -> read RC data and write it to PLC
                            break
                    else:
                        self._syncIdxFrameData = st_for_end(0, AxesGroup.State.UnifiedFrameIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Frame:
                    # get changed index
                    self._syncIdxFrameData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                # jump back
                self._stepSyncFrameData = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.Frame:
                    # search for changed index
                    for self._syncIdxFrameData in range(0, AxesGroup.State.UnifiedFrameIndex + 1):
                        if AxesGroup.State.DataChanged.Frame[self._syncIdxFrameData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                            # inc step counter
                            self._stepSyncFrameData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxFrameData = st_for_end(0, AxesGroup.State.UnifiedFrameIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Frame:
                    # get changed index
                    self._syncIdxFrameData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Frame, AxesGroup.State.UnifiedFrameIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncFrameData: Synchronization of Frame[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxFrameData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Frame[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readFrameData.Busy and (not self._readFrameData.Error):
                    # set command parameter
                    self._readFrameData.ParCmd.FrameNo = self._syncIdxFrameData
                    # execute command
                    self._readFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = self._stepSyncFrameData + 1
                else:
                    # check error ?
                    if self._readFrameData.Error:
                        self.ErrorID = self._readFrameData.ErrorID
                        self.ErrorAddTxt = self._readFrameData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            case 21:
                if (not self._readFrameData.Busy and (not self._readFrameData.Error)) and self._readFrameData.Done:
                    # reset execution
                    self._readFrameData.Execute = False
                    # update internal frame data
                    copy_into(FrameData[self._syncIdxFrameData].Data, self._readFrameData.OutCmd.FrameData)
                    copy_into(self._frameData[self._syncIdxFrameData].Data, self._readFrameData.OutCmd.FrameData)
                    # set available bit
                    FrameData[self._syncIdxFrameData].Available = True
                    self._frameData[self._syncIdxFrameData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readFrameData.Error:
                        self.ErrorID = self._readFrameData.ErrorID
                        self.ErrorAddTxt = self._readFrameData.ErrorAddTxt
                        # reset available bit
                        FrameData[self._syncIdxFrameData].Available = False
                        self._frameData[self._syncIdxFrameData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeFrameData.Busy and (not self._writeFrameData.Error):
                    # set command parameter
                    self._writeFrameData.ParCmd.FrameNo = self._syncIdxFrameData
                    copy_into(self._writeFrameData.ParCmd.FrameData, FrameData[self._syncIdxFrameData].Data)
                    # execute command
                    self._writeFrameData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = self._stepSyncFrameData + 1
                else:
                    # check error ?
                    if self._writeFrameData.Error:
                        self.ErrorID = self._writeFrameData.ErrorID
                        self.ErrorAddTxt = self._writeFrameData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)

            case 31:
                if (not self._writeFrameData.Busy and (not self._writeFrameData.Error)) and self._writeFrameData.Done:
                    # execute command
                    self._writeFrameData.Execute = False
                    # update internal frame data
                    copy_into(self._frameData[self._syncIdxFrameData], FrameData[self._syncIdxFrameData])
                    # set available bit
                    FrameData[self._syncIdxFrameData].Available = True
                    self._frameData[self._syncIdxFrameData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncFrameData, rTimer=self._timerSyncFrameData)
                    # inc step counter
                    self._stepSyncFrameData = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeFrameData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        FrameData[self._syncIdxFrameData].Available = False
                        self._frameData[self._syncIdxFrameData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncFrameData) == RobotLibraryConstants.OK:
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncFrameData)), 40)
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD, Overwrite=False)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncLoadData(self, *, AxesGroup: _T.AxesGroup, LoadData: list[Load]) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx: int = 0
        # internal Start index for loops
        _idxStart: int = 0

        # Set internal references
        _stepName = '_stepSyncLoadData = '
        # _rStep REF= self._stepSyncLoadData  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncLoadData  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncLoadData  (reference: _rTimeout is replaced by it)
        # _rSyncIdx REF= self._syncIdxLoadData  (reference: _rSyncIdx is replaced by it)

        match self._stepSyncLoadData:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # Check More Data on RC than on PLC -> Synchronization not possible
                if AxesGroup.State.ConfigurationData.HighestToolIndex > AxesGroup.SystemData.LoadDataCount:
                    self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC, Overwrite=False)
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadLoadData and AxesGroup.State.RobotData.RCSupportedFunctions.WriteLoadData) and AxesGroup.State.Initialized) and (not self.Error):
                    # Check PLC loads < RC Loads and SyncLoad enabled ?
                    if AxesGroup.State.DataEnableSync.EnableSyncLoad == True and AxesGroup.Parameter.Rob.Parameter.HighestLoadIndex > AxesGroup.SystemData.LoadDataMax:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_DATA_ARRAY_TOO_SHORT, Overwrite=True)

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Start initial reading of LoadData from RC', Para1='')

                    # calculate start index !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    self._syncIdxLoadData = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = self._stepSyncLoadData + 1

            # Start read LoadData
            case 1:
                if (not self._readLoadData.Busy and (not self._readLoadData.Error)) and (not self._readLoadData.Done):
                    # set command parameter
                    self._readLoadData.ParCmd.LoadNo = self._syncIdxLoadData
                    # execute command
                    self._readLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = self._stepSyncLoadData + 1
                else:
                    # check error ?
                    if self._readLoadData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            # Wait Loaddata read
            case 2:
                if (not self._readLoadData.Busy and (not self._readLoadData.Error)) and self._readLoadData.Done:
                    # reset execution
                    self._readLoadData.Execute = False
                    # set available bit
                    self._loadData[self._syncIdxLoadData].Available = True
                    LoadData[self._syncIdxLoadData].Available = True
                    # Copy data
                    copy_into(self._loadData[self._syncIdxLoadData].Data, self._readLoadData.OutCmd.LoadData)

                    # Check Load data is equal ?
                    if not IsLoadDataEqual(Data1=self._loadData[self._syncIdxLoadData].Data, Data2=LoadData[self._syncIdxLoadData].Data, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Load = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Load[self._syncIdxLoadData] = True
                        # inc count of unsynchronised plc Loads
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Load = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Load + 1, 'USINT')

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Detected a difference in Load[{1}] between PLC and RC', Para1=DINT_TO_STRING(self._syncIdxLoadData))

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncLoad:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_LOAD_DATA_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Load:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_NUMBER_SYNC_ERROR, Overwrite=False)

                    # Check all Loads read ?
                    if self._syncIdxLoadData < AxesGroup.State.UnifiedLoadIndex:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                        # inc Load index
                        self._syncIdxLoadData = wrap(self._syncIdxLoadData + 1, 'USINT')
                        # dec step counter
                        self._stepSyncLoadData = self._stepSyncLoadData - 1
                    else:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                        # inc step counter
                        self._stepSyncLoadData = self._stepSyncLoadData + 1
                else:
                    # check error ?
                    if self._readLoadData.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        LoadData[self._syncIdxLoadData].Available = False
                        self._loadData[self._syncIdxLoadData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            # Check synchronisation state ?
            case 3:
                if AxesGroup.State.SyncStatePlc.UnSyncNo.Load == 0 or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Load = AxesGroup.State.SyncStatePlc.UnSyncNo.Load == 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Load:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                # Overwrite PLC data with RC data
                                for _idx in range(AxesGroup.SystemData.LoadDataMin, AxesGroup.SystemData.LoadDataMax + 1):
                                    # Overwrite PLC data with RC data
                                    copy_into(LoadData[_idx], self._loadData[_idx])

                                # Reset data changed flags
                                copy_into(AxesGroup.State.DataChanged.Load, _dataChangedNone.Load)
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Load = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Load = True
                                # Reset count of unsynchronised plc Loads
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                                # inc step counter
                                self._stepSyncLoadData = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Loads triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Applied the initial read Load data from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                # calculate start index
                                _idxStart = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)

                                # Check conflicts to solve ?
                                # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                                for self._syncIdxLoadData in range(_idxStart, AxesGroup.State.UnifiedLoadIndex + 1):
                                    if AxesGroup.State.DataChanged.Load[self._syncIdxLoadData]:
                                        _found = True
                                        break
                                else:
                                    self._syncIdxLoadData = st_for_end(_idxStart, AxesGroup.State.UnifiedLoadIndex)

                                if _found:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Load = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Load = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                                    # inc step counter
                                    self._stepSyncLoadData = self._stepSyncLoadData + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    copy_into(AxesGroup.State.DataChanged.Load, _dataChangedNone.Load)
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Load = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Load = True
                                    # Reset count of unsynchronised Loads
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                                    # inc step counter
                                    self._stepSyncLoadData = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write Load data
            case 4:
                if not self._writeLoadData.Busy and (not self._writeLoadData.Error):
                    # set command parameter
                    self._writeLoadData.ParCmd.LoadNo = self._syncIdxLoadData
                    copy_into(self._writeLoadData.ParCmd.LoadData, LoadData[self._syncIdxLoadData].Data)
                    # execute command
                    self._writeLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = self._stepSyncLoadData + 1
                else:
                    # check error ?
                    if self._writeLoadData.Error:
                        self.ErrorID = self._writeLoadData.ErrorID
                        self.ErrorAddTxt = self._writeLoadData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            # Wait Load data written ?
            case 5:
                if (not self._writeLoadData.Busy and (not self._writeLoadData.Error)) and self._writeLoadData.Done:
                    # execute command
                    self._writeLoadData.Execute = False
                    # apply Load data to internal Load data
                    copy_into(self._loadData[self._syncIdxLoadData], LoadData[self._syncIdxLoadData])
                    # reset data changed bit
                    AxesGroup.State.DataChanged.Load[self._syncIdxLoadData] = False
                    # dec count of unsynchronised Loads
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Load = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Load - 1, 'USINT')
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # dec step counter
                    self._stepSyncLoadData = self._stepSyncLoadData - 2
                else:
                    # check error ?
                    if self._writeLoadData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # reset count of unsynchronised Loads
                AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0

                # calculate start index
                _idxStart = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)

                # Check all Load datas
                # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                for self._syncIdxLoadData in range(_idxStart, AxesGroup.State.UnifiedLoadIndex + 1):
                    # compare Load data
                    AxesGroup.State.DataChanged.Load[self._syncIdxLoadData] = not IsLoadDataEqual(Data1=LoadData[self._syncIdxLoadData].Data, Data2=self._loadData[self._syncIdxLoadData].Data, IgnoreTimestamp=False)

                    # Check Load data changed ?
                    if AxesGroup.State.DataChanged.Load[self._syncIdxLoadData]:
                        # inc count of unsynchronised plc Loads
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Load = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Load + 1, 'USINT')
                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Detected a local change of Load[{1}] on PLC, SyncTime = {2}', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Load = AxesGroup.State.SyncStatePlc.UnSyncNo.Load == 0

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.Load) != (not AxesGroup.State.SyncStateRc.InSync.Load):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.Load and (not AxesGroup.State.SyncStateRc.InSync.Load):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.Load:
                    # calculate start index
                    _idxStart = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)

                    # search for changed index
                    # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    for self._syncIdxLoadData in range(_idxStart, AxesGroup.State.UnifiedLoadIndex + 1):
                        if AxesGroup.State.DataChanged.Load[self._syncIdxLoadData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxLoadData = st_for_end(_idxStart, AxesGroup.State.UnifiedLoadIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Load:
                    # get changed index
                    self._syncIdxLoadData = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex)  # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                # jump back
                self._stepSyncLoadData = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.Load:
                    # calculate start index
                    _idxStart = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)

                    # search for changed index
                    # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    for self._syncIdxLoadData in range(_idxStart, AxesGroup.State.UnifiedLoadIndex + 1):
                        if AxesGroup.State.DataChanged.Load[self._syncIdxLoadData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 20  # -> read RC data and write it to PLC
                            break
                    else:
                        self._syncIdxLoadData = st_for_end(_idxStart, AxesGroup.State.UnifiedLoadIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Load:
                    # get changed index
                    self._syncIdxLoadData = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex)  # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                # jump back
                self._stepSyncLoadData = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.Load:
                    # calculate start index
                    _idxStart = LIMIT(1, DINT_TO_USINT(AxesGroup.SystemData.LoadDataMin), AxesGroup.State.UnifiedLoadIndex)

                    # search for changed index
                    # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    for self._syncIdxLoadData in range(_idxStart, AxesGroup.State.UnifiedLoadIndex + 1):
                        if AxesGroup.State.DataChanged.Load[self._syncIdxLoadData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                            # inc step counter
                            self._stepSyncLoadData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxLoadData = st_for_end(_idxStart, AxesGroup.State.UnifiedLoadIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Load:
                    # get changed index
                    self._syncIdxLoadData = LIMIT(1, AxesGroup.State.SyncStateRc.UnSyncNo.Load, AxesGroup.State.UnifiedLoadIndex)  # !!! Attention : 0 is not allowed - LoadData starts with 1 !!!
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncLoadData: Synchronization of Load[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxLoadData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Load[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readLoadData.Busy and (not self._readLoadData.Error):
                    # set command parameter
                    self._readLoadData.ParCmd.LoadNo = self._syncIdxLoadData
                    # execute command
                    self._readLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = self._stepSyncLoadData + 1
                else:
                    # check error ?
                    if self._readLoadData.Error:
                        self.ErrorID = self._readLoadData.ErrorID
                        self.ErrorAddTxt = self._readLoadData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            case 21:
                if (not self._readLoadData.Busy and (not self._readLoadData.Error)) and self._readLoadData.Done:
                    # reset execution
                    self._readLoadData.Execute = False
                    # update internal Load data
                    copy_into(LoadData[self._syncIdxLoadData].Data, self._readLoadData.OutCmd.LoadData)
                    copy_into(self._loadData[self._syncIdxLoadData].Data, self._readLoadData.OutCmd.LoadData)
                    # set available bit
                    LoadData[self._syncIdxLoadData].Available = True
                    self._loadData[self._syncIdxLoadData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readLoadData.Error:
                        self.ErrorID = self._readLoadData.ErrorID
                        self.ErrorAddTxt = self._readLoadData.ErrorAddTxt
                        # reset available bit
                        LoadData[self._syncIdxLoadData].Available = False
                        self._loadData[self._syncIdxLoadData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeLoadData.Busy and (not self._writeLoadData.Error):
                    # set command parameter
                    self._writeLoadData.ParCmd.LoadNo = self._syncIdxLoadData
                    copy_into(self._writeLoadData.ParCmd.LoadData, LoadData[self._syncIdxLoadData].Data)
                    # execute command
                    self._writeLoadData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = self._stepSyncLoadData + 1
                else:
                    # check error ?
                    if self._writeLoadData.Error:
                        self.ErrorID = self._writeLoadData.ErrorID
                        self.ErrorAddTxt = self._writeLoadData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)

            case 31:
                if (not self._writeLoadData.Busy and (not self._writeLoadData.Error)) and self._writeLoadData.Done:
                    # execute command
                    self._writeLoadData.Execute = False
                    # update internal Load data
                    copy_into(self._loadData[self._syncIdxLoadData], LoadData[self._syncIdxLoadData])
                    # set available bit
                    LoadData[self._syncIdxLoadData].Available = True
                    self._loadData[self._syncIdxLoadData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncLoadData, rTimer=self._timerSyncLoadData)
                    # inc step counter
                    self._stepSyncLoadData = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeLoadData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        LoadData[self._syncIdxLoadData].Available = False
                        self._loadData[self._syncIdxLoadData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncLoadData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncLoadData)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncRobotDefaultDynamics(self, *, AxesGroup: _T.AxesGroup, DefaultDynamics: _T.DefaultDynamics) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()

        # Set internal references
        _stepName = '_stepSyncDefaultDynamics = '
        # _rStep REF= self._stepSyncDefaultDynamics  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncDefaultDynamics  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncDefaultDynamics  (reference: _rTimeout is replaced by it)

        match self._stepSyncDefaultDynamics:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadRobotDefaultDynamics and AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotDefaultDynamics) and AxesGroup.State.Initialized) and (not self.Error):
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Start initial reading of DefaultDynamics from RC', Para1='')

                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1

            # Start read DefaultDynamics
            case 1:
                if (not self._readRobotDefaultDynamics.Busy and (not self._readRobotDefaultDynamics.Error)) and (not self._readRobotDefaultDynamics.Done):
                    # execute command
                    self._readRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1
                else:
                    # check error ?
                    if self._readRobotDefaultDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            # Wait DefaultDynamics read
            case 2:
                if (not self._readRobotDefaultDynamics.Busy and (not self._readRobotDefaultDynamics.Error)) and self._readRobotDefaultDynamics.Done:
                    # reset execution
                    self._readRobotDefaultDynamics.Execute = False
                    # Copy data
                    copy_into(self._defaultDynamics, self._readRobotDefaultDynamics.OutCmd.DynamicValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1

                    # Check DefaultDynamics data is equal ?
                    if not IsDefaultDynamicsEqual(Data1=self._defaultDynamics, Data2=DefaultDynamics, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.DefaultDynamics = True
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Detected a difference in DefaultDynamics between PLC and RC', Para1='')

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncDefaultDynamics:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_DEFAULT_DYNAMICS_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.DefaultDynamics:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_ERROR, Overwrite=False)
                else:
                    # check error ?
                    if self._readRobotDefaultDynamics.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            # Check synchronisation state ?
            case 3:
                if not AxesGroup.State.DataChanged.DefaultDynamics or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = not AxesGroup.State.DataChanged.DefaultDynamics
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.DefaultDynamics:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                # Overwrite PLC data with RC data
                                copy_into(DefaultDynamics, self._defaultDynamics)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.DefaultDynamics = _dataChangedNone.DefaultDynamics
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.DefaultDynamics = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                                # inc step counter
                                self._stepSyncDefaultDynamics = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Applied the initial read DefaultDynamics from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                if AxesGroup.State.DataChanged.DefaultDynamics:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.DefaultDynamics = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                                    # inc step counter
                                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.DefaultDynamics = _dataChangedNone.DefaultDynamics
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.DefaultDynamics = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                                    # inc step counter
                                    self._stepSyncDefaultDynamics = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write DefaultDynamics data
            case 4:
                if not self._writeRobotDefaultDynamics.Busy and (not self._writeRobotDefaultDynamics.Error):
                    # set command parameter
                    copy_into(self._writeRobotDefaultDynamics.ParCmd.DynamicValues, DefaultDynamics)
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1
                else:
                    # check error ?
                    if self._writeRobotDefaultDynamics.Error:
                        self.ErrorID = self._writeRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            # Wait DefaultDynamics data written ?
            case 5:
                if (not self._writeRobotDefaultDynamics.Busy and (not self._writeRobotDefaultDynamics.Error)) and self._writeRobotDefaultDynamics.Done:
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = False
                    # apply DefaultDynamics data to internal DefaultDynamics data
                    copy_into(self._defaultDynamics, DefaultDynamics)
                    # reset data changed bit
                    AxesGroup.State.DataChanged.DefaultDynamics = False
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # dec step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics - 2
                else:
                    # check error ?
                    if self._writeRobotDefaultDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # compare DefaultDynamics data
                AxesGroup.State.DataChanged.DefaultDynamics = not IsDefaultDynamicsEqual(Data1=DefaultDynamics, Data2=self._defaultDynamics, IgnoreTimestamp=False)

                # Check DefaultDynamics data changed ?
                if AxesGroup.State.DataChanged.DefaultDynamics:
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Detected a local change of DefaultDynamics on PLC, SyncTime = {1}', Para1=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = not AxesGroup.State.DataChanged.DefaultDynamics

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics) != (not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                            # inc step counter
                            self._stepSyncDefaultDynamics = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                            # inc step counter
                            self._stepSyncDefaultDynamics = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                            # inc step counter
                            self._stepSyncDefaultDynamics = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics and (not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                # jump back
                self._stepSyncDefaultDynamics = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                # jump back
                self._stepSyncDefaultDynamics = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.DefaultDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncDefaultDynamics: Synchronization of DefaultDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.DefaultDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readRobotDefaultDynamics.Busy and (not self._readRobotDefaultDynamics.Error):
                    # execute command
                    self._readRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1
                else:
                    # check error ?
                    if self._readRobotDefaultDynamics.Error:
                        self.ErrorID = self._readRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            case 21:
                if (not self._readRobotDefaultDynamics.Busy and (not self._readRobotDefaultDynamics.Error)) and self._readRobotDefaultDynamics.Done:
                    # reset execution
                    self._readRobotDefaultDynamics.Execute = False
                    # update internal DefaultDynamics data
                    copy_into(DefaultDynamics, self._readRobotDefaultDynamics.OutCmd.DynamicValues)
                    copy_into(self._defaultDynamics, self._readRobotDefaultDynamics.OutCmd.DynamicValues)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readRobotDefaultDynamics.Error:
                        self.ErrorID = self._readRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeRobotDefaultDynamics.Busy and (not self._writeRobotDefaultDynamics.Error):
                    # set command parameter
                    copy_into(self._writeRobotDefaultDynamics.ParCmd.DynamicValues, DefaultDynamics)
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = self._stepSyncDefaultDynamics + 1
                else:
                    # check error ?
                    if self._writeRobotDefaultDynamics.Error:
                        self.ErrorID = self._writeRobotDefaultDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotDefaultDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)

            case 31:
                if (not self._writeRobotDefaultDynamics.Busy and (not self._writeRobotDefaultDynamics.Error)) and self._writeRobotDefaultDynamics.Done:
                    # execute command
                    self._writeRobotDefaultDynamics.Execute = False
                    # update internal DefaultDynamics data
                    copy_into(self._defaultDynamics, DefaultDynamics)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncDefaultDynamics, rTimer=self._timerSyncDefaultDynamics)
                    # inc step counter
                    self._stepSyncDefaultDynamics = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeRobotDefaultDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncDefaultDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncDefaultDynamics)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncRobotReferenceDynamics(self, *, AxesGroup: _T.AxesGroup, ReferenceDynamics: _T.ReferenceDynamics) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()

        # Set internal references
        _stepName = '_stepSyncReferenceDynamics = '
        # _rStep REF= self._stepSyncReferenceDynamics  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncReferenceDynamics  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncReferenceDynamics  (reference: _rTimeout is replaced by it)

        match self._stepSyncReferenceDynamics:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadRobotReferenceDynamics and AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotReferenceDynamics) and AxesGroup.State.Initialized) and (not self.Error):
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Start initial reading of ReferenceDynamics from RC', Para1='')

                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1

            # Start read ReferenceDynamics
            case 1:
                if (not self._readRobotReferenceDynamics.Busy and (not self._readRobotReferenceDynamics.Error)) and (not self._readRobotReferenceDynamics.Done):
                    # execute command
                    self._readRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1
                else:
                    # check error ?
                    if self._readRobotReferenceDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            # Wait ReferenceDynamics read
            case 2:
                if (not self._readRobotReferenceDynamics.Busy and (not self._readRobotReferenceDynamics.Error)) and self._readRobotReferenceDynamics.Done:
                    # reset execution
                    self._readRobotReferenceDynamics.Execute = False
                    # Copy data
                    copy_into(self._referenceDynamics, self._readRobotReferenceDynamics.OutCmd.DynamicValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1

                    # Check ReferenceDynamics data is equal ?
                    if not IsReferenceDynamicsEqual(Data1=self._referenceDynamics, Data2=ReferenceDynamics, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.ReferenceDynamics = True
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Detected a difference in ReferenceDynamics between PLC and RC', Para1='')

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncReferenceDynamics:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_REFERENCE_DYNAMICS_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.ReferenceDynamics:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_ERROR, Overwrite=False)
                else:
                    # check error ?
                    if self._readRobotReferenceDynamics.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            # Check synchronisation state ?
            case 3:
                if not AxesGroup.State.DataChanged.ReferenceDynamics or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = not AxesGroup.State.DataChanged.ReferenceDynamics
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.ReferenceDynamics:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                # Overwrite PLC data with RC data
                                copy_into(ReferenceDynamics, self._referenceDynamics)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.ReferenceDynamics = _dataChangedNone.ReferenceDynamics
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.ReferenceDynamics = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                                # inc step counter
                                self._stepSyncReferenceDynamics = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Applied the initial read ReferenceDynamics from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                if AxesGroup.State.DataChanged.ReferenceDynamics:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.ReferenceDynamics = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                                    # inc step counter
                                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.ReferenceDynamics = _dataChangedNone.ReferenceDynamics
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.ReferenceDynamics = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                                    # inc step counter
                                    self._stepSyncReferenceDynamics = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write ReferenceDynamics data
            case 4:
                if not self._writeRobotReferenceDynamics.Busy and (not self._writeRobotReferenceDynamics.Error):
                    # set command parameter
                    copy_into(self._writeRobotReferenceDynamics.ParCmd.DynamicValues, ReferenceDynamics)
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1
                else:
                    # check error ?
                    if self._writeRobotReferenceDynamics.Error:
                        self.ErrorID = self._writeRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            # Wait ReferenceDynamics data written ?
            case 5:
                if (not self._writeRobotReferenceDynamics.Busy and (not self._writeRobotReferenceDynamics.Error)) and self._writeRobotReferenceDynamics.Done:
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = False
                    # apply ReferenceDynamics data to internal ReferenceDynamics data
                    copy_into(self._referenceDynamics, ReferenceDynamics)
                    # reset data changed bit
                    AxesGroup.State.DataChanged.ReferenceDynamics = False
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # dec step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics - 2
                else:
                    # check error ?
                    if self._writeRobotReferenceDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # compare ReferenceDynamics data
                AxesGroup.State.DataChanged.ReferenceDynamics = not IsReferenceDynamicsEqual(Data1=ReferenceDynamics, Data2=self._referenceDynamics, IgnoreTimestamp=False)

                # Check ReferenceDynamics data changed ?
                if AxesGroup.State.DataChanged.ReferenceDynamics:
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Detected a local change of ReferenceDynamics on PLC, SyncTime = {1}', Para1=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = not AxesGroup.State.DataChanged.ReferenceDynamics

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics) != (not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                            # inc step counter
                            self._stepSyncReferenceDynamics = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                            # inc step counter
                            self._stepSyncReferenceDynamics = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                            # inc step counter
                            self._stepSyncReferenceDynamics = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics and (not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                # jump back
                self._stepSyncReferenceDynamics = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                # jump back
                self._stepSyncReferenceDynamics = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncReferenceDynamics: Synchronization of ReferenceDynamics triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.ReferenceDynamics[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readRobotReferenceDynamics.Busy and (not self._readRobotReferenceDynamics.Error):
                    # execute command
                    self._readRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1
                else:
                    # check error ?
                    if self._readRobotReferenceDynamics.Error:
                        self.ErrorID = self._readRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            case 21:
                if (not self._readRobotReferenceDynamics.Busy and (not self._readRobotReferenceDynamics.Error)) and self._readRobotReferenceDynamics.Done:
                    # reset execution
                    self._readRobotReferenceDynamics.Execute = False
                    # update internal ReferenceDynamics data
                    copy_into(ReferenceDynamics, self._readRobotReferenceDynamics.OutCmd.DynamicValues)
                    copy_into(self._referenceDynamics, self._readRobotReferenceDynamics.OutCmd.DynamicValues)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readRobotReferenceDynamics.Error:
                        self.ErrorID = self._readRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._readRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeRobotReferenceDynamics.Busy and (not self._writeRobotReferenceDynamics.Error):
                    # set command parameter
                    copy_into(self._writeRobotReferenceDynamics.ParCmd.DynamicValues, ReferenceDynamics)
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = self._stepSyncReferenceDynamics + 1
                else:
                    # check error ?
                    if self._writeRobotReferenceDynamics.Error:
                        self.ErrorID = self._writeRobotReferenceDynamics.ErrorID
                        self.ErrorAddTxt = self._writeRobotReferenceDynamics.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)

            case 31:
                if (not self._writeRobotReferenceDynamics.Busy and (not self._writeRobotReferenceDynamics.Error)) and self._writeRobotReferenceDynamics.Done:
                    # execute command
                    self._writeRobotReferenceDynamics.Execute = False
                    # update internal ReferenceDynamics data
                    copy_into(self._referenceDynamics, ReferenceDynamics)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncReferenceDynamics, rTimer=self._timerSyncReferenceDynamics)
                    # inc step counter
                    self._stepSyncReferenceDynamics = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeRobotReferenceDynamics.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncReferenceDynamics) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncReferenceDynamics)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncRobotSWLimits(self, *, AxesGroup: _T.AxesGroup, SWLimits: _T.SWLimits) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()

        # Set internal references
        _stepName = '_stepSyncSWLimits = '
        # _rStep REF= self._stepSyncSWLimits  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncSWLimits  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncSWLimits  (reference: _rTimeout is replaced by it)

        match self._stepSyncSWLimits:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # Check RC function for sync mode is available ?
                if (AxesGroup.State.Initialized == True and AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotSWLimits == False) and ((self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] == SyncMode.CLIENT_TO_SERVER or self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] == SyncMode.CLIENT_TO_SERVER) or self._parCfg.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] == SyncMode.AUTOMATIC):
                    self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=False)
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='HandleSyncRobotSWLimits: SyncMode needs WriteRobotSWLimits function which is not available on RC', Para1='')
                    return

                # wait for initialisation done
                # ReadRobotSwLimits is mandatory
                # (     AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotSWLimits ) AND // WriteRobotSwLimits is optional
                if (AxesGroup.State.RobotData.RCSupportedFunctions.ReadRobotSWLimits and AxesGroup.State.Initialized) and (not self.Error):
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Start initial reading of SwLimits from RC', Para1='')

                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1

            # Start read SwLimits
            case 1:
                if (not self._readRobotSWLimits.Busy and (not self._readRobotSWLimits.Error)) and (not self._readRobotSWLimits.Done):
                    # execute command
                    self._readRobotSWLimits.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1
                else:
                    # check error ?
                    if self._readRobotSWLimits.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            # Wait SwLimits read
            case 2:
                if (not self._readRobotSWLimits.Busy and (not self._readRobotSWLimits.Error)) and self._readRobotSWLimits.Done:
                    # reset execution
                    self._readRobotSWLimits.Execute = False
                    # Copy data
                    copy_into(self._swLimits, self._readRobotSWLimits.OutCmd.LimitValues)
                    # Set plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1

                    # Check SwLimits data is equal ?
                    if not IsSwLimitsEqual(Data1=self._swLimits, Data2=SWLimits, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.SwLimits = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.SwLimits = True
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Detected a difference in SwLimits between PLC and RC', Para1='')

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncSWLimits:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_SWLIMIT_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.SWLimits:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_ERROR, Overwrite=False)
                else:
                    # check error ?
                    if self._readRobotSWLimits.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            # Check synchronisation state ?
            case 3:
                if not AxesGroup.State.DataChanged.SwLimits or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = not AxesGroup.State.DataChanged.SwLimits
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.SWLimits:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                # Overwrite PLC data with RC data
                                copy_into(SWLimits, self._swLimits)
                                # Reset data changed flags
                                AxesGroup.State.DataChanged.SwLimits = _dataChangedNone.SwLimits
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.SwLimits = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                                # inc step counter
                                self._stepSyncSWLimits = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Applied the initial read SwLimits from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                if AxesGroup.State.DataChanged.SwLimits:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.SwLimits = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                                    # inc step counter
                                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by StartUp-Compare, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.DURING_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    AxesGroup.State.DataChanged.SwLimits = _dataChangedNone.SwLimits
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.SwLimits = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.SwLimits = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                                    # inc step counter
                                    self._stepSyncSWLimits = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write SwLimits data
            case 4:
                if not self._writeRobotSWLimits.Busy and (not self._writeRobotSWLimits.Error):
                    # set command parameter
                    copy_into(self._writeRobotSWLimits.ParCmd.LimitValues, SWLimits)
                    self._writeRobotSWLimits.ParCmd.ResetToFactoryDefaults = False
                    # execute command
                    self._writeRobotSWLimits.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1
                else:
                    # check error ?
                    if self._writeRobotSWLimits.Error:
                        self.ErrorID = self._writeRobotSWLimits.ErrorID
                        self.ErrorAddTxt = self._writeRobotSWLimits.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            # Wait SwLimits data written ?
            case 5:
                if (not self._writeRobotSWLimits.Busy and (not self._writeRobotSWLimits.Error)) and self._writeRobotSWLimits.Done:
                    # execute command
                    self._writeRobotSWLimits.Execute = False
                    # apply SwLimits data to internal SwLimits data
                    copy_into(self._swLimits, SWLimits)
                    # reset data changed bit
                    AxesGroup.State.DataChanged.SwLimits = False
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # dec step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits - 2
                else:
                    # check error ?
                    if self._writeRobotSWLimits.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # compare SwLimits data
                AxesGroup.State.DataChanged.SwLimits = not IsSwLimitsEqual(Data1=SWLimits, Data2=self._swLimits, IgnoreTimestamp=False)

                # Check SwLimits data changed ?
                if AxesGroup.State.DataChanged.SwLimits:
                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Detected a local change of SwLimits on PLC, SyncTime = {1}', Para1=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                # Update plc in sync flag
                AxesGroup.State.SyncStatePlc.InSync.SwLimits = not AxesGroup.State.DataChanged.SwLimits

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.SwLimits) != (not AxesGroup.State.SyncStateRc.InSync.SwLimits):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                            # inc step counter
                            self._stepSyncSWLimits = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                            # inc step counter
                            self._stepSyncSWLimits = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                            # inc step counter
                            self._stepSyncSWLimits = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.SwLimits and (not AxesGroup.State.SyncStateRc.InSync.SwLimits):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                # jump back
                self._stepSyncSWLimits = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                # jump back
                self._stepSyncSWLimits = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by PLC, SyncMode = {1}, SyncTime = {2}, SyncDirection = PLC -> RC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.SwLimits:
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncSwLimits: Synchronization of SwLimits triggered by RC, SyncMode = {1}, SyncTime = {2}, SyncDirection = RC -> PLC', Para1=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.SWLimits[SyncTime.AFTER_START_UP]), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readRobotSWLimits.Busy and (not self._readRobotSWLimits.Error):
                    # execute command
                    self._readRobotSWLimits.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1
                else:
                    # check error ?
                    if self._readRobotSWLimits.Error:
                        self.ErrorID = self._readRobotSWLimits.ErrorID
                        self.ErrorAddTxt = self._readRobotSWLimits.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            case 21:
                if (not self._readRobotSWLimits.Busy and (not self._readRobotSWLimits.Error)) and self._readRobotSWLimits.Done:
                    # reset execution
                    self._readRobotSWLimits.Execute = False
                    # update internal SwLimits data
                    copy_into(SWLimits, self._readRobotSWLimits.OutCmd.LimitValues)
                    copy_into(self._swLimits, self._readRobotSWLimits.OutCmd.LimitValues)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readRobotSWLimits.Error:
                        self.ErrorID = self._readRobotSWLimits.ErrorID
                        self.ErrorAddTxt = self._readRobotSWLimits.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeRobotSWLimits.Busy and (not self._writeRobotSWLimits.Error):
                    # set command parameter
                    self._writeRobotSWLimits.ParCmd.ResetToFactoryDefaults = False
                    copy_into(self._writeRobotSWLimits.ParCmd.LimitValues, SWLimits)
                    # execute command
                    self._writeRobotSWLimits.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = self._stepSyncSWLimits + 1
                else:
                    # check error ?
                    if self._writeRobotSWLimits.Error:
                        self.ErrorID = self._writeRobotSWLimits.ErrorID
                        self.ErrorAddTxt = self._writeRobotSWLimits.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)

            case 31:
                if (not self._writeRobotSWLimits.Busy and (not self._writeRobotSWLimits.Error)) and self._writeRobotSWLimits.Done:
                    # execute command
                    self._writeRobotSWLimits.Execute = False
                    # update internal SwLimits data
                    copy_into(self._swLimits, SWLimits)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncSWLimits, rTimer=self._timerSyncSWLimits)
                    # inc step counter
                    self._stepSyncSWLimits = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeRobotSWLimits.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncSWLimits) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncSWLimits)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncToolData(self, *, AxesGroup: _T.AxesGroup, ToolData: list[Tool]) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx: int = 0

        # Set internal references
        _stepName = '_stepSyncToolData = '
        # _rStep REF= self._stepSyncToolData  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncToolData  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncToolData  (reference: _rTimeout is replaced by it)
        # _rSyncIdx REF= self._syncIdxToolData  (reference: _rSyncIdx is replaced by it)

        match self._stepSyncToolData:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # Check More Data on RC than on PLC -> Synchronization not possible
                if AxesGroup.State.ConfigurationData.HighestToolIndex > AxesGroup.SystemData.ToolDataCount:
                    self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_TOOL_COUNT_RC_HIGHER_THAN_PLC, Overwrite=False)
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadToolData and AxesGroup.State.RobotData.RCSupportedFunctions.WriteToolData) and AxesGroup.State.Initialized) and (not self.Error):
                    # Check PLC tools < RC tools and SyncTool enabled ?
                    if AxesGroup.State.DataEnableSync.EnableSyncTool == True and AxesGroup.Parameter.Rob.Parameter.HighestToolIndex > AxesGroup.SystemData.ToolDataMax:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_TOO_SHORT, Overwrite=True)

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Start initial reading of ToolData from RC', Para1='')

                    # init tool number
                    self._syncIdxToolData = DINT_TO_USINT(AxesGroup.SystemData.ToolDataMin)
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = self._stepSyncToolData + 1

            # Start read ToolData
            case 1:
                if (not self._readToolData.Busy and (not self._readToolData.Error)) and (not self._readToolData.Done):
                    # set command parameter
                    self._readToolData.ParCmd.ToolNo = self._syncIdxToolData
                    # execute command
                    self._readToolData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = self._stepSyncToolData + 1
                else:
                    # check error ?
                    if self._readToolData.Error and self.WarningID == RobotLibraryWarningIdEnum.NO_WARNING:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            # Wait Tooldata read
            case 2:
                if (not self._readToolData.Busy and (not self._readToolData.Error)) and self._readToolData.Done:
                    # reset execution
                    self._readToolData.Execute = False
                    # set available bit
                    self._toolData[self._syncIdxToolData].Available = True
                    ToolData[self._syncIdxToolData].Available = True
                    # Copy data
                    copy_into(self._toolData[self._syncIdxToolData].Data, self._readToolData.OutCmd.ToolData)

                    # Check tool data is equal ?
                    if not IsToolDataEqual(Data1=self._toolData[self._syncIdxToolData].Data, Data2=ToolData[self._syncIdxToolData].Data, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.Tool = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.Tool[self._syncIdxToolData] = True
                        # inc count of unsynchronised plc tools
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Tool + 1, 'USINT')

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Detected a difference in Tool[{1}] between PLC and RC', Para1=DINT_TO_STRING(self._syncIdxToolData))

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncTool and self.InfoID == RobotLibraryInfoIdEnum.NO_INFO:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_TOOL_DATA_DISABLED, Overwrite=True)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Tool and self.WarningID == RobotLibraryWarningIdEnum.NO_WARNING:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_NUMBER_SYNC_ERROR, Overwrite=True)

                    # Check all tools read ?
                    if self._syncIdxToolData < AxesGroup.State.UnifiedToolIndex:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                        # inc tool index
                        self._syncIdxToolData = wrap(self._syncIdxToolData + 1, 'USINT')
                        # dec step counter
                        self._stepSyncToolData = self._stepSyncToolData - 1
                    else:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                        # inc step counter
                        self._stepSyncToolData = self._stepSyncToolData + 1
                else:
                    # check error ?
                    if self._readToolData.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        ToolData[self._syncIdxToolData].Available = False
                        self._toolData[self._syncIdxToolData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            # Check synchronisation state ?
            case 3:
                if AxesGroup.State.SyncStatePlc.UnSyncNo.Tool == 0 or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.Tool = AxesGroup.State.SyncStatePlc.UnSyncNo.Tool == 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.Tool:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                for _idx in range(AxesGroup.SystemData.ToolDataMin, AxesGroup.SystemData.ToolDataMax + 1):
                                    # Overwrite PLC data with RC data
                                    copy_into(ToolData[_idx], self._toolData[_idx])
                                # Reset data changed flags
                                copy_into(AxesGroup.State.DataChanged.Tool, _dataChangedNone.Tool)
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.Tool = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.Tool = True
                                # Reset count of unsynchronised plc tools
                                AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                                # inc step counter
                                self._stepSyncToolData = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tools triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Applied the initial read tool data from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                # Check conflicts to solve ?
                                for self._syncIdxToolData in range(0, AxesGroup.State.UnifiedToolIndex + 1):
                                    if AxesGroup.State.DataChanged.Tool[self._syncIdxToolData]:
                                        _found = True
                                        break
                                else:
                                    self._syncIdxToolData = st_for_end(0, AxesGroup.State.UnifiedToolIndex)

                                if _found:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Tool = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.Tool = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                                    # inc step counter
                                    self._stepSyncToolData = self._stepSyncToolData + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    copy_into(AxesGroup.State.DataChanged.Tool, _dataChangedNone.Tool)
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.Tool = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.Tool = True
                                    # Reset count of unsynchronised tools
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                                    # inc step counter
                                    self._stepSyncToolData = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write tool data
            case 4:
                if not self._writeToolData.Busy and (not self._writeToolData.Error):
                    # set command parameter
                    self._writeToolData.ParCmd.ToolNo = self._syncIdxToolData
                    copy_into(self._writeToolData.ParCmd.ToolData, ToolData[self._syncIdxToolData].Data)
                    # execute command
                    self._writeToolData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = self._stepSyncToolData + 1
                else:
                    # check error ?
                    if self._writeToolData.Error:
                        self.ErrorID = self._writeToolData.ErrorID
                        self.ErrorAddTxt = self._writeToolData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            # Wait tool data written ?
            case 5:
                if (not self._writeToolData.Busy and (not self._writeToolData.Error)) and self._writeToolData.Done:
                    # execute command
                    self._writeToolData.Execute = False
                    # apply tool data to internal tool data
                    copy_into(self._toolData[self._syncIdxToolData], ToolData[self._syncIdxToolData])
                    # reset data changed bit
                    AxesGroup.State.DataChanged.Tool[self._syncIdxToolData] = False
                    # dec count of unsynchronised tools
                    AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Tool - 1, 'USINT')
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # dec step counter
                    self._stepSyncToolData = self._stepSyncToolData - 2
                else:
                    # check error ?
                    if self._writeToolData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # reset count of unsynchronised tools
                AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0

                # Check all tool datas
                for self._syncIdxToolData in range(0, AxesGroup.State.UnifiedToolIndex + 1):
                    # compare tool data
                    AxesGroup.State.DataChanged.Tool[self._syncIdxToolData] = not IsToolDataEqual(Data1=ToolData[self._syncIdxToolData].Data, Data2=self._toolData[self._syncIdxToolData].Data, IgnoreTimestamp=False)

                    # Check Tool data changed ?
                    if AxesGroup.State.DataChanged.Tool[self._syncIdxToolData]:
                        # inc count of unsynchronised plc tools
                        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.Tool + 1, 'USINT')
                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Detected a local change of Tool[{1}] on PLC, SyncTime = {2}', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.Tool = AxesGroup.State.SyncStatePlc.UnSyncNo.Tool == 0

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.Tool) != (not AxesGroup.State.SyncStateRc.InSync.Tool):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.Tool and (not AxesGroup.State.SyncStateRc.InSync.Tool):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.Tool:
                    # search for changed index
                    for self._syncIdxToolData in range(0, AxesGroup.State.UnifiedToolIndex + 1):
                        if AxesGroup.State.DataChanged.Tool[self._syncIdxToolData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxToolData = st_for_end(0, AxesGroup.State.UnifiedToolIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Tool:
                    # get changed index
                    self._syncIdxToolData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                # jump back
                self._stepSyncToolData = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.Tool:
                    # search for changed index
                    for self._syncIdxToolData in range(0, AxesGroup.State.UnifiedToolIndex + 1):
                        if AxesGroup.State.DataChanged.Tool[self._syncIdxToolData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 20  # -> read RC data and write it to PLC
                            break
                    else:
                        self._syncIdxToolData = st_for_end(0, AxesGroup.State.UnifiedToolIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Tool:
                    # get changed index
                    self._syncIdxToolData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                # jump back
                self._stepSyncToolData = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.Tool:
                    # search for changed index
                    for self._syncIdxToolData in range(0, AxesGroup.State.UnifiedToolIndex + 1):
                        if AxesGroup.State.DataChanged.Tool[self._syncIdxToolData]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                            # inc step counter
                            self._stepSyncToolData = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxToolData = st_for_end(0, AxesGroup.State.UnifiedToolIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.Tool:
                    # get changed index
                    self._syncIdxToolData = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.Tool, AxesGroup.State.UnifiedToolIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncToolData: Synchronization of Tool[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxToolData), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.Tool[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readToolData.Busy and (not self._readToolData.Error):
                    # set command parameter
                    self._readToolData.ParCmd.ToolNo = self._syncIdxToolData
                    # execute command
                    self._readToolData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = self._stepSyncToolData + 1
                else:
                    # check error ?
                    if self._readToolData.Error:
                        self.ErrorID = self._readToolData.ErrorID
                        self.ErrorAddTxt = self._readToolData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            case 21:
                if (not self._readToolData.Busy and (not self._readToolData.Error)) and self._readToolData.Done:
                    # reset execution
                    self._readToolData.Execute = False
                    # update internal tool data
                    copy_into(ToolData[self._syncIdxToolData].Data, self._readToolData.OutCmd.ToolData)
                    copy_into(self._toolData[self._syncIdxToolData].Data, self._readToolData.OutCmd.ToolData)
                    # set available bit
                    ToolData[self._syncIdxToolData].Available = True
                    self._toolData[self._syncIdxToolData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readToolData.Error:
                        self.ErrorID = self._readToolData.ErrorID
                        self.ErrorAddTxt = self._readToolData.ErrorAddTxt
                        # reset available bit
                        ToolData[self._syncIdxToolData].Available = False
                        self._toolData[self._syncIdxToolData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeToolData.Busy and (not self._writeToolData.Error):
                    # set command parameter
                    self._writeToolData.ParCmd.ToolNo = self._syncIdxToolData
                    copy_into(self._writeToolData.ParCmd.ToolData, ToolData[self._syncIdxToolData].Data)
                    # execute command
                    self._writeToolData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = self._stepSyncToolData + 1
                else:
                    # check error ?
                    if self._writeToolData.Error:
                        self.ErrorID = self._writeToolData.ErrorID
                        self.ErrorAddTxt = self._writeToolData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)

            case 31:
                if (not self._writeToolData.Busy and (not self._writeToolData.Error)) and self._writeToolData.Done:
                    # execute command
                    self._writeToolData.Execute = False
                    # update internal tool data
                    copy_into(self._toolData[self._syncIdxToolData], ToolData[self._syncIdxToolData])
                    # set available bit
                    ToolData[self._syncIdxToolData].Available = True
                    self._toolData[self._syncIdxToolData].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncToolData, rTimer=self._timerSyncToolData)
                    # inc step counter
                    self._stepSyncToolData = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeToolData.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        ToolData[self._syncIdxToolData].Available = False
                        self._toolData[self._syncIdxToolData].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncToolData) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncToolData)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleSyncWorkArea(self, *, AxesGroup: _T.AxesGroup, WorkAreas: list[RobotWorkArea]) -> None:  # PRIVATE
        # Internal step counter name
        _stepName: str = ''
        # Internal reference to step counter
        # _rStep: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timer
        # _rTimer: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to timeout
        # _rTimeout: REFERENCE TO ... (alias, see REF= below)
        # Internal reference to synchroniztion index
        # _rSyncIdx: REFERENCE TO ... (alias, see REF= below)
        # internal bit for condition found
        _found: bool = False
        # empty data set to reset all DataChanged bits
        _dataChangedNone: AxesGroupStateDataChanged = AxesGroupStateDataChanged()
        # internal index for loops
        _idx: int = 0

        # Set internal references
        _stepName = '_stepSyncWorkArea = '
        # _rStep REF= self._stepSyncWorkArea  (reference: _rStep is replaced by it)
        # _rTimer REF= self._timerSyncWorkArea  (reference: _rTimer is replaced by it)
        # _rTimeout REF= self._timeoutSyncWorkArea  (reference: _rTimeout is replaced by it)
        # _rSyncIdx REF= self._syncIdxWorkArea  (reference: _rSyncIdx is replaced by it)

        match self._stepSyncWorkArea:
            case 0:
                if self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION and self._parCfg.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # Check More Data on RC than on PLC -> Synchronization not possible
                if AxesGroup.State.ConfigurationData.HighestWorkAreaIndex > AxesGroup.SystemData.WorkAreasCount:
                    self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_WORKAREA_COUNT_RC_HIGHER_THAN_PLC, Overwrite=False)
                    return

                # wait for initialisation done
                if ((AxesGroup.State.RobotData.RCSupportedFunctions.ReadWorkArea and AxesGroup.State.RobotData.RCSupportedFunctions.WriteWorkArea) and AxesGroup.State.Initialized) and (not self.Error):
                    # Check PLC WorkAreas < RC WorkAreas and SyncWorkArea enabled ?
                    if AxesGroup.State.DataEnableSync.EnableSyncWorkArea == True and AxesGroup.Parameter.Rob.Parameter.HighestWorkAreaIndex > AxesGroup.SystemData.WorkAreasMax:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_ARRAY_TOO_SHORT, Overwrite=True)

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Start initial reading of WorkArea from RC', Para1='')

                    # init WorkArea number
                    self._syncIdxWorkArea = DINT_TO_USINT(AxesGroup.SystemData.WorkAreasMin)
                    # init count of unsynchronized elements
                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1

            # Start read WorkArea
            case 1:
                if (not self._readWorkArea.Busy and (not self._readWorkArea.Error)) and (not self._readWorkArea.Done):
                    # set command parameter
                    self._readWorkArea.ParCmd.WorkAreaNo = self._syncIdxWorkArea
                    # execute command
                    self._readWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1
                else:
                    # check error ?
                    if self._readWorkArea.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=False)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            # Wait WorkArea read
            case 2:
                if (not self._readWorkArea.Busy and (not self._readWorkArea.Error)) and self._readWorkArea.Done:
                    # reset execution
                    self._readWorkArea.Execute = False
                    # set available bit
                    self._workAreas[self._syncIdxWorkArea].Available = True
                    WorkAreas[self._syncIdxWorkArea].Available = True
                    # Copy data
                    copy_into(self._workAreas[self._syncIdxWorkArea].Data, self._readWorkArea.OutCmd.WorkAreaData)

                    # Check WorkArea data is equal ?
                    if not IsWorkAreaEqual(Data1=self._workAreas[self._syncIdxWorkArea].Data, Data2=WorkAreas[self._syncIdxWorkArea].Data, IgnoreTimestamp=True):
                        # Reset plc in sync flag
                        AxesGroup.State.SyncStatePlc.InSync.WorkArea = False
                        # Set data changed flag
                        AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea] = True
                        # inc count of unsynchronised plc WorkAreas
                        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea + 1, 'USINT')

                        # Create log entry
                        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Detected a difference in WorkArea[{1}] between PLC and RC', Para1=DINT_TO_STRING(self._syncIdxWorkArea))

                        # Check synchronisation is enabled ?
                        if not AxesGroup.State.DataEnableSync.EnableSyncWorkArea:
                            self.SetInfo(InfoID=RobotLibraryInfoIdEnum.INFO_SYNC_WORK_AREA_DISABLED, Overwrite=False)

                        # Check user interaction needed ?
                        if AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.WorkAreas:
                            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_NUMBER_SYNC_ERROR, Overwrite=False)

                    # Check all WorkAreas read ?
                    if self._syncIdxWorkArea < AxesGroup.State.UnifiedWorkAreaIndex:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                        # inc WorkArea index
                        self._syncIdxWorkArea = wrap(self._syncIdxWorkArea + 1, 'USINT')
                        # dec step counter
                        self._stepSyncWorkArea = self._stepSyncWorkArea - 1
                    else:
                        # set timeout
                        SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                        # inc step counter
                        self._stepSyncWorkArea = self._stepSyncWorkArea + 1
                else:
                    # check error ?
                    if self._readWorkArea.Error:
                        # Set warning
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        WorkAreas[self._syncIdxWorkArea].Available = False
                        self._workAreas[self._syncIdxWorkArea].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            # Check synchronisation state ?
            case 3:
                if AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea == 0 or AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    # Update bit for data in sync
                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea == 0
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 10  # -> jump to after startup

                    # Create log entry
                    self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization Startup Phase done', Para1='')
                else:
                    # Check user interaction needed ?
                    if not AxesGroup.Parameter.Plc.Parameter.SyncUserInteraction.WorkAreas:
                        match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP]:

                            case SyncMode.SERVER_TO_CLIENT:
                                # Overwrite PLC data with RC data
                                for _idx in range(AxesGroup.SystemData.WorkAreasMin, AxesGroup.SystemData.WorkAreasMax + 1):
                                    # Overwrite PLC data with RC data
                                    copy_into(WorkAreas[_idx], WorkAreas[_idx])

                                # Reset data changed flags
                                copy_into(AxesGroup.State.DataChanged.WorkArea, _dataChangedNone.WorkArea)
                                # Reset Synchronizing flag
                                AxesGroup.State.Synchronizing.WorkAreas = False
                                # Set plc in sync flag
                                AxesGroup.State.SyncStatePlc.InSync.WorkArea = True
                                # Reset count of unsynchronised plc WorkAreas
                                AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                                # set timeout
                                SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                                # inc step counter
                                self._stepSyncWorkArea = 10  # -> jump to after startup

                                # Create log entry
                                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkAreas triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                # Create log entry
                                self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Applied the initial read WorkArea data from RC', Para1='')

                            case SyncMode.CLIENT_TO_SERVER:

                                # Check conflicts to solve ?
                                for self._syncIdxWorkArea in range(0, AxesGroup.State.UnifiedWorkAreaIndex + 1):
                                    if AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea]:
                                        _found = True
                                        break
                                else:
                                    self._syncIdxWorkArea = st_for_end(0, AxesGroup.State.UnifiedWorkAreaIndex)

                                if _found:
                                    # Reset plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = False
                                    # Set Synchronizing flag
                                    AxesGroup.State.Synchronizing.WorkAreas = True
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                                    # inc step counter
                                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1  # -> write PLC data to RC
                                    # Create log entry
                                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by StartUp-Compare, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.DURING_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.DURING_START_UP))
                                else:
                                    # Reset data changed flags
                                    copy_into(AxesGroup.State.DataChanged.WorkArea, _dataChangedNone.WorkArea)
                                    # Reset Synchronizing flag
                                    AxesGroup.State.Synchronizing.WorkAreas = False
                                    # Set plc in sync flag
                                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = True
                                    # Reset count of unsynchronised WorkAreas
                                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0
                                    # set timeout
                                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                                    # inc step counter
                                    self._stepSyncWorkArea = 10  # -> jump to after startup
                            case _:
                                # invalid sync mode for startup
                                self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_SYNC_MODE_INVALID, Overwrite=True)

            # Start write WorkArea data
            case 4:
                if not self._writeWorkArea.Busy and (not self._writeWorkArea.Error):
                    # set command parameter
                    self._writeWorkArea.ParCmd.WorkAreaNo = self._syncIdxWorkArea
                    copy_into(self._writeWorkArea.ParCmd.WorkAreaData, WorkAreas[self._syncIdxWorkArea].Data)
                    # execute command
                    self._writeWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1
                else:
                    # check error ?
                    if self._writeWorkArea.Error:
                        self.ErrorID = self._writeWorkArea.ErrorID
                        self.ErrorAddTxt = self._writeWorkArea.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            # Wait WorkArea data written ?
            case 5:
                if (not self._writeWorkArea.Busy and (not self._writeWorkArea.Error)) and self._writeWorkArea.Done:
                    # execute command
                    self._writeWorkArea.Execute = False
                    # apply WorkArea data to internal WorkArea data
                    copy_into(self._workAreas[self._syncIdxWorkArea], WorkAreas[self._syncIdxWorkArea])
                    # reset data changed bit
                    AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea] = False
                    # dec count of unsynchronised WorkAreas
                    AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea - 1, 'USINT')
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # dec step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea - 2
                else:
                    # check error ?
                    if self._writeWorkArea.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            # --------------------------------------------
            # SyncMode after startup :
            # --------------------------------------------
            case 10:
                if AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP] == SyncMode.NO_SYNCHRONIZATION:
                    return

                # reset count of unsynchronised WorkAreas
                AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0

                # Check all WorkArea datas
                for self._syncIdxWorkArea in range(0, AxesGroup.State.UnifiedWorkAreaIndex + 1):
                    # compare WorkArea data
                    AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea] = not IsWorkAreaEqual(Data1=WorkAreas[self._syncIdxWorkArea].Data, Data2=self._workAreas[self._syncIdxWorkArea].Data, IgnoreTimestamp=False)

                    # Check WorkArea data changed ?
                    if AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea]:
                        # inc count of unsynchronised plc WorkAreas
                        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = wrap(AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea + 1, 'USINT')
                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Detected a local change of WorkArea[{1}] on PLC, SyncTime = {2}', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))

                    # Update plc in sync flag
                    AxesGroup.State.SyncStatePlc.InSync.WorkArea = AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea == 0

                # Check synchronization is needed ?
                if (not AxesGroup.State.SyncStatePlc.InSync.WorkArea) != (not AxesGroup.State.SyncStateRc.InSync.WorkArea):
                    match AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]:
                        # NO_SYNCHRONIZATION
                        case SyncMode.NO_SYNCHRONIZATION:
                            # no further action
                            pass

                        # CLIENT_TO_SERVER
                        case SyncMode.CLIENT_TO_SERVER:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 11

                        # SERVER_TO_CLIENT
                        case SyncMode.SERVER_TO_CLIENT:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 12

                        # AUTOMATIC
                        case SyncMode.AUTOMATIC:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 13
                else:
                    # datas changeḍ on both sides ? -> Warning
                    if not AxesGroup.State.SyncStatePlc.InSync.WorkArea and (not AxesGroup.State.SyncStateRc.InSync.WorkArea):
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_BOTH_SIDES_CHANGED, Overwrite=True)

            # ------------------------------------------
            # SyncMode : CLIENT_TO_SERVER
            # ------------------------------------------
            case 11:
                if not AxesGroup.State.SyncStatePlc.InSync.WorkArea:
                    # search for changed index
                    for self._syncIdxWorkArea in range(0, AxesGroup.State.UnifiedWorkAreaIndex + 1):
                        if AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxWorkArea = st_for_end(0, AxesGroup.State.UnifiedWorkAreaIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.WorkArea:
                    # get changed index
                    self._syncIdxWorkArea = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 30  # -> write PLC data to RC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                # jump back
                self._stepSyncWorkArea = 10

            # ------------------------------------------
            # SyncMode : SERVER_TO_CLIENT
            # ------------------------------------------
            case 12:
                if not AxesGroup.State.SyncStatePlc.InSync.WorkArea:
                    # search for changed index
                    for self._syncIdxWorkArea in range(0, AxesGroup.State.UnifiedWorkAreaIndex + 1):
                        if AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 20  # -> read RC data and write it to PLC
                            break
                    else:
                        self._syncIdxWorkArea = st_for_end(0, AxesGroup.State.UnifiedWorkAreaIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.WorkArea:
                    # get changed index
                    self._syncIdxWorkArea = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 20  # -> read RC data and write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                # jump back
                self._stepSyncWorkArea = 10

            # ------------------------------------------
            # SyncMode : AUTOMATIC
            # ------------------------------------------
            case 13:
                if not AxesGroup.State.SyncStatePlc.InSync.WorkArea:
                    # search for changed index
                    for self._syncIdxWorkArea in range(0, AxesGroup.State.UnifiedWorkAreaIndex + 1):
                        if AxesGroup.State.DataChanged.WorkArea[self._syncIdxWorkArea]:
                            # set timeout
                            SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                            # inc step counter
                            self._stepSyncWorkArea = 30  # -> write PLC data to RC
                            break
                    else:
                        self._syncIdxWorkArea = st_for_end(0, AxesGroup.State.UnifiedWorkAreaIndex)

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by PLC, SyncMode = {2}, SyncTime = {3}, SyncDirection = PLC -> RC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # Conflict triggered by RC ?
                if not AxesGroup.State.SyncStateRc.InSync.WorkArea:
                    # get changed index
                    self._syncIdxWorkArea = LIMIT(0, AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea, AxesGroup.State.UnifiedWorkAreaIndex)
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 20  # -> read RC data an write it to PLC

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.DEBUG, MessageCode=0, MessageText='SyncWorkArea: Synchronization of WorkArea[{1}] triggered by RC, SyncMode = {2}, SyncTime = {3}, SyncDirection = RC -> PLC', Para1=DINT_TO_STRING(self._syncIdxWorkArea), Para2=SYNC_MODE_TO_STRING(Value=AxesGroup.Parameter.Plc.Parameter.SynchronizationModes.WorkAreas[SyncTime.AFTER_START_UP]), Para3=SYNC_TIME_TO_STRING(Value=SyncTime.AFTER_START_UP))
                    return

                # set timeout
                SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)

            # jump back
            # _rStep := 10;
            # ------------------------------------------
            # Read Data from RC and write it to PLC
            # ------------------------------------------
            case 20:
                if not self._readWorkArea.Busy and (not self._readWorkArea.Error):
                    # set command parameter
                    self._readWorkArea.ParCmd.WorkAreaNo = self._syncIdxWorkArea
                    # execute command
                    self._readWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1
                else:
                    # check error ?
                    if self._readWorkArea.Error:
                        self.ErrorID = self._readWorkArea.ErrorID
                        self.ErrorAddTxt = self._readWorkArea.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            case 21:
                if (not self._readWorkArea.Busy and (not self._readWorkArea.Error)) and self._readWorkArea.Done:
                    # reset execution
                    self._readWorkArea.Execute = False
                    # update internal WorkArea data
                    copy_into(WorkAreas[self._syncIdxWorkArea].Data, self._readWorkArea.OutCmd.WorkAreaData)
                    copy_into(self._workAreas[self._syncIdxWorkArea].Data, self._readWorkArea.OutCmd.WorkAreaData)
                    # set available bit
                    WorkAreas[self._syncIdxWorkArea].Available = True
                    self._workAreas[self._syncIdxWorkArea].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 10  # -> jump to after startup
                else:
                    # check error ?
                    if self._readWorkArea.Error:
                        self.ErrorID = self._readWorkArea.ErrorID
                        self.ErrorAddTxt = self._readWorkArea.ErrorAddTxt
                        # reset available bit
                        WorkAreas[self._syncIdxWorkArea].Available = False
                        self._workAreas[self._syncIdxWorkArea].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            # ------------------------------------------
            # Write data from PLC to RC
            # ------------------------------------------
            case 30:
                if not self._writeWorkArea.Busy and (not self._writeWorkArea.Error):
                    # set command parameter
                    self._writeWorkArea.ParCmd.WorkAreaNo = self._syncIdxWorkArea
                    copy_into(self._writeWorkArea.ParCmd.WorkAreaData, WorkAreas[self._syncIdxWorkArea].Data)
                    # execute command
                    self._writeWorkArea.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = self._stepSyncWorkArea + 1
                else:
                    # check error ?
                    if self._writeWorkArea.Error:
                        self.ErrorID = self._writeWorkArea.ErrorID
                        self.ErrorAddTxt = self._writeWorkArea.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)

            case 31:
                if (not self._writeWorkArea.Busy and (not self._writeWorkArea.Error)) and self._writeWorkArea.Done:
                    # execute command
                    self._writeWorkArea.Execute = False
                    # update internal WorkArea data
                    copy_into(self._workAreas[self._syncIdxWorkArea], WorkAreas[self._syncIdxWorkArea])
                    # set available bit
                    WorkAreas[self._syncIdxWorkArea].Available = True
                    self._workAreas[self._syncIdxWorkArea].Available = True
                    # set timeout
                    SetTimeout(PT=self._timeoutSyncWorkArea, rTimer=self._timerSyncWorkArea)
                    # inc step counter
                    self._stepSyncWorkArea = 10  # -> jump to after startup;
                else:
                    # check error ?
                    if self._writeWorkArea.Error:
                        self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD, Overwrite=True)
                        # reset available bit
                        WorkAreas[self._syncIdxWorkArea].Available = False
                        self._workAreas[self._syncIdxWorkArea].Available = False

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerSyncWorkArea) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepSyncWorkArea)), 40)
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT(_stepName, DINT_TO_STRING(self._stepCmd)), 40)

    def HandleTelegramStateCtrl(self) -> None:  # PRIVATE
        # Telegram Control
        # ----------------
        if self._lastTelegramControl != GetHalfeByteLo(Value=self.Telegram.PlcToRob.Header.AxesGroupID_Control):
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SRCI Interface control changed from {1} to {2}', Para1=TELEGRAM_CONTROL_TO_STRING(Control=self._lastTelegramControl), Para2=TELEGRAM_CONTROL_TO_STRING(Control=ControlHalfByte(GetHalfeByteLo(Value=self.Telegram.PlcToRob.Header.AxesGroupID_Control))))

            self._lastTelegramControl = ControlHalfByte(GetHalfeByteLo(Value=self.Telegram.PlcToRob.Header.AxesGroupID_Control))

        # Telegram State
        # ----------------
        if self._lastTelegramState != self.Telegram.RobToPlc.Header.TelegramState:
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='SRCI Interface state changed from {1} to {2}', Para1=TELEGRAM_STATE_TO_STRING(State=self._lastTelegramState), Para2=TELEGRAM_STATE_TO_STRING(State=self.Telegram.RobToPlc.Header.TelegramState))

            # Check Interface changed after being initialized ?
            if (self.Enable and self._lastTelegramState == TelegramState.INITIALIZED) and (self.Telegram.RobToPlc.Header.TelegramState == TelegramState.READY_FOR_INITIALIZATION or self.Telegram.RobToPlc.Header.TelegramState == TelegramState.READY_TO_RESUME):
                # {warning 'ToDo'}
                # SetError( ErrorID := RobotLibraryErrorIdEnum.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7  , Overwrite := TRUE );
                pass

            # apply new telegram state
            self._lastTelegramState = self.Telegram.RobToPlc.Header.TelegramState

    def HandleUserData(self, *, AxesGroup: _T.AxesGroup, UserData: _T.UserData) -> None:
        # Common
        UserData.LogLevel = self.LogLevel

        UserData.PLCManufacturedID = self._parCfg.Plc.Parameter.ManufacturedID
        UserData.PLCOrderID = self._parCfg.Plc.Parameter.OrderID
        UserData.PLCSerialNumber = self._parCfg.Plc.Parameter.SerialNumber
        UserData.PLCFirmwareVersion = self._parCfg.Plc.Parameter.FirmwareVersion
        UserData.PLCInterfaceVersion = self._parCfg.Plc.Parameter.InterfaceVersion
        copy_into(UserData.PLCLibraryVersion, RobotLibraryConstants.PLCLibraryVersion)

        # Communication
        UserData.LifeSignTimeOut = self._parCfg.Com.LifeSignTimeOut

        # Plc Parameter
        copy_into(UserData.SynchronizationModes, self._parCfg.Plc.Parameter.SynchronizationModes)
        copy_into(UserData.EnableSync, SyncModesToDataEnableSync(Value=self._parCfg.Plc.Parameter.SynchronizationModes))

        # Robot Parameter
        UserData.DelayTime = self._parCfg.Rob.Parameter.DelayTime
        UserData.WaitForNrOfCmd = self._parCfg.Rob.Parameter.WaitForNrOfCmd
        UserData.WaitAtBlendingZone = self._parCfg.Rob.Parameter.WaitAtBlendingZone
        UserData.AllowSecSeqWhileSubprogram = self._parCfg.Rob.Parameter.AllowSecSeqWhileSubprogram
        UserData.AllowDynamicBlending = self._parCfg.Rob.Parameter.AllowDynamicBlending
        UserData.SyncReaction = self._parCfg.Rob.Parameter.SyncReaction
        UserData.SyncDelay = self._parCfg.Rob.Parameter.SyncDelay
        UserData.MessageLevel = self._parCfg.Rob.Parameter.MessageLevel

        # ReadRobotData
        UserData.RCManufacturer = AxesGroup.State.RobotData.RCManufacturer
        UserData.RCOrderID = AxesGroup.State.RobotData.RCOrderID
        UserData.RCSerialNumber = AxesGroup.State.RobotData.RCSerialNumber
        UserData.RASerialNumber = AxesGroup.State.RobotData.RASerialNumber
        UserData.RCFirmwareVersion = AxesGroup.State.RobotData.RCFirmwareVersion

        UserData.RCInterpreterVersion.MajorVersion = STRING_TO_USINT(MID(AxesGroup.State.RobotData.RCInterpreterVersion, 1, 1))
        UserData.RCInterpreterVersion.MinorVersion = STRING_TO_USINT(MID(AxesGroup.State.RobotData.RCInterpreterVersion, 1, 2))
        UserData.RCInterpreterVersion.PatchVersion = STRING_TO_USINT(MID(AxesGroup.State.RobotData.RCInterpreterVersion, 1, 3))

        copy_into(UserData.AxisJointUsed, AxesGroup.State.RobotData.AxisJointUsed)
        copy_into(UserData.AxisExternalUsed, AxesGroup.State.RobotData.AxisExternalUsed)
        copy_into(UserData.AxisJointUnit, AxesGroup.State.RobotData.AxisJointUnit)
        copy_into(UserData.AxisExternalUnit, AxesGroup.State.RobotData.AxisExternalUnit)
        copy_into(UserData.RCSupportedFunctions, AxesGroup.State.RobotData.RCSupportedFunctions)

        UserData.BrakeTestRequired = AxesGroup.State.ConfigurationData.BrakeTestRequired
        UserData.PathAccuracyMode = AxesGroup.State.ConfigurationData.PathAccuracyMode
        UserData.AvoidSingularity = AxesGroup.State.ConfigurationData.AvoidSingularity
        UserData.ConstantVelocitySupported = AxesGroup.State.ConfigurationData.ConstantVelocitySupported
        UserData.StepModeExactStopActive = AxesGroup.State.ConfigurationData.StepModeExactStopActive
        UserData.StepModeBlendingActive = AxesGroup.State.ConfigurationData.StepModeBlendingActive
        UserData.AcceleratingSupported = AxesGroup.State.ConfigurationData.AcceleratingSupported
        UserData.DeceleratingSupported = AxesGroup.State.ConfigurationData.DecceleratingSupported

        UserData.Initialized = self.Initialized
        UserData.Synchronized = self.Synchronized

        # Cyclic data
        copy_into(UserData.RCSRCIVersion, AxesGroup.Cyclic.RobToPlc.SRCIVersion)
        UserData.IsMoving = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.IsMoving
        UserData.PrimarySequencePaused = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.PrimarySequencePaused
        UserData.InPrimaryPos = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.InPrimaryPos
        UserData.SecondarySequenceActive = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.SecondarySequenceActive
        UserData.ErrorPending = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.ErrorPending
        UserData.RestartInProgress = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RestartInProgress
        UserData.Enabled = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Enabled
        UserData.Idle = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.IDLE
        UserData.Executing = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.EXECUTING
        UserData.Interrupted = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RaSequenceState == RaSequenceState.INTERRUPTED
        UserData.IsBlending = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.IsBlending
        UserData.OperationMode = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.OperationMode
        UserData.CollisionDetectionEnabled = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.CollisionDetectedEnabled
        UserData.CollisionDetected = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.CollisionDetected
        UserData.RestartRequested = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.RestartRequested
        UserData.Accelerating = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Accelerating
        UserData.Decelerating = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.Decelerating
        UserData.ConstantVelocity = AxesGroup.Cyclic.RobToPlc.StatusRobotArm.ConstantVelocity
        UserData.ActualOverride = PERCENT_UINT_TO_REAL(Value=AxesGroup.Cyclic.RobToPlc.Override, IsOptional=False)

        # Cyclic optional data
        copy_into(UserData.CartesianPosition, AxesGroup.CyclicOptional.RobToPlc.CartesianPosition)
        copy_into(UserData.ExtCartesianPosition, AxesGroup.CyclicOptional.RobToPlc.CartesianPositionExt)
        copy_into(UserData.JointPosition, AxesGroup.CyclicOptional.RobToPlc.JointPosition)
        copy_into(UserData.ExtJointPosition, AxesGroup.CyclicOptional.RobToPlc.JointPositionExt)

        # Synchronizing
        UserData.ToolDataSynchronizing = AxesGroup.State.Synchronizing.Tool
        UserData.FrameDataSynchronizing = AxesGroup.State.Synchronizing.Frame
        UserData.LoadDataSynchronizing = AxesGroup.State.Synchronizing.Load
        UserData.WorkAreaDataSynchronizing = AxesGroup.State.Synchronizing.WorkAreas
        UserData.SWLimitsSynchronizing = AxesGroup.State.Synchronizing.SwLimits
        UserData.DefaultDynamicsSynchronizing = AxesGroup.State.Synchronizing.DefaultDynamics
        UserData.ReferenceDynamicsSynchronizing = AxesGroup.State.Synchronizing.ReferenceDynamics

        UserData.ActivateTwoSequences = self._parCfg.Com.TwoSequences
        UserData.ReadingCartesianPosition = AxesGroup.State.ReadingCartesianPosition
        UserData.ReadingExtCartesianPosition = AxesGroup.State.ReadingCartesianPositionExt
        UserData.ReadingJointPosition = AxesGroup.State.ReadingJointPosition
        UserData.ReadingExtJointPosition = AxesGroup.State.ReadingJointPositionExt

    def OnCall(self, *, AxesGroup: _T.AxesGroup) -> None:  # PRIVATE
        # map numeric value to enum, so that the corresponding message text is directly shown by the tooltip
        self.ErrorIdEnum = RobotLibraryErrorIdEnum(self.ErrorID)
        self.WarningIdEnum = RobotLibraryWarningIdEnum(self.WarningID)
        self.InfoIdEnum = RobotLibraryInfoIdEnum(self.InfoID)

        self.Error = self.HasError

        # Check Payload and In/Out data size
        if self.ROBOT_IN_DATA_SIZE < 64 or self.ROBOT_OUT_DATA_SIZE < 64:
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_LIBRARY_PARA, Overwrite=True)
            return

        # Check AxesGroupID valid
        if self.AxesGroupID < RobotLibraryConstants.AXES_GROUP_ID_MIN or self.AxesGroupID > RobotLibraryConstants.AXES_GROUP_ID_MAX:
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INVALID_AXES_GROUP_ID, Overwrite=True)
            return

        # Reset flag for initialization / Synchronization
        if (self.Initialized or self.Synchronized) and AxesGroup.Cyclic.RobToPlc.TelegramState != TelegramState.INITIALIZED:
            # Reset initialized flag
            self.Initialized = False
            # Reset Synchronized flag
            self.Synchronized = False
            # Set error
            self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0x80A2, Overwrite=True)

        # Warning for ACR Registers running low
        if AxesGroup.Acyclic.ActiveCommandRegister.CurrentAcrUsagePercent > RobotLibraryParameter.ACR_USAGE_WARNING_LIMIT:
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_ACR_FREE_ENTRIES_LOW, Overwrite=True)

        # Check ToolData boundary
        if AxesGroup.SystemData.ToolDataMin != 0:
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite=False)

        # Check FrameData boundary
        if AxesGroup.SystemData.FrameDataMin != 0 and (not self.HasWarning):
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite=False)

        # Check WorkAreas boundary
        if AxesGroup.SystemData.WorkAreasMin != 0 and (not self.HasWarning):
            self.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO, Overwrite=False)

        # Check configuration parameter changed ?
        self.CheckParameterChanged(AxesGroup=AxesGroup)

    def OnExecRun(self, *, AxesGroup: _T.AxesGroup) -> int:
        OnExecRun: int = 0

        # building rising and falling edges
        self._enable_R(CLK=self.Enable)
        self._enable_F(CLK=self.Enable)

        if self._enable_F.Q:
            self.Reset(AxesGroup=AxesGroup)

        OnExecRun = RobotLibraryConstants.RUNNING

        match self._stepCmd:

            case 0:
                if self._enable_R.Q:
                    # Create log entry
                    self.CreateLogMessage(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='Robot Task Enabled')

                    # reset the rising edge
                    self._enable_R()
                    # set busy flag
                    self.Busy = True
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # Reset FastStop
                    AxesGroup.Cyclic.PlcToRob.FastStop = 0
                    # Reset Active command register
                    AxesGroup.Acyclic.ActiveCommandRegister.Reset()

                    # check parameter valid
                    if self.CheckParameterValid(AxesGroup=AxesGroup):
                        # take configuration parameter if not yet enabled
                        copy_into(self._parCfg, self.ParCfg)
                        # inc step counter
                        self._stepCmd = self._stepCmd + 1

            case 1:
                match AxesGroup.Cyclic.RobToPlc.TelegramState:

                    case TelegramState.UNDEFINED:
                        pass

                    case _ if TelegramState.ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE <= AxesGroup.Cyclic.RobToPlc.TelegramState <= TelegramState.ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED:
                        # clear error
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.ACK_ERROR
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESET  # always a reset, so that on the robot side the ACR is reseted

                    case TelegramState.ERROR_173_SERVER_CONNECTION_LOST:
                        # Reset interface including the ACR register on server side
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESET

                    case TelegramState.READY_TO_RESUME:
                        # Resume
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.RESUME

                    case TelegramState.READY_FOR_INITIALIZATION:
                        # Request initialization
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.INITIALIZE

                    case TelegramState.INITIALIZED:
                        # Reset Telegram Control
                        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.NONE

                        # Check SRCI Version is compatible ?
                        if AxesGroup.Cyclic.RobToPlc.SRCIVersion.MajorVersion == RobotLibraryConstants.SRCIVersion.MajorVersion:
                            # set timeout
                            SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                            # inc step counter
                            self._stepCmd = self._stepCmd + 1
                        else:
                            # set error
                            self.ErrorID = RobotLibraryErrorIdEnum.ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0x80A4
                            self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)
                    case _:
                        # TelegrammState in error
                        self.SetError(ErrorID=RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0xA2, Overwrite=True)
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

                # timeout exceeded ?
                if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                    # Check Telegram State error ?
                    if AxesGroup.Cyclic.RobToPlc.TelegramState >= TelegramState.ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE or AxesGroup.Cyclic.RobToPlc.TelegramState <= TelegramState.ERROR_173_SERVER_CONNECTION_LOST:
                        self.ErrorID = AxesGroup.Cyclic.RobToPlc.TelegramState
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)
                    else:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 2:
                if not self._readMessages.Busy and (not self._readMessages.Error):
                    # start function block
                    self._readMessages.Enable = True
                    self._readMessages.ParCmd.MsgID = 0
                    self._readMessages.ParCmd.MessageLevel = self._parCfg.Rob.Parameter.MessageLevel

                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._readMessages.Error:
                        self.ErrorID = self._readMessages.ErrorID
                        self.ErrorAddTxt = self._readMessages.ErrorAddTxt
                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 3:
                if self._readMessages.Enabled and (not self._readMessages.Error):
                    # ---------------------------------------------------------------
                    # !!! ReadMessages must stay active for the Message mechanism !!!
                    # ---------------------------------------------------------------
                    # ReadMessages.Enable := FALSE;
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._readMessages.Error:
                        self.ErrorID = self._readMessages.ErrorID
                        self.ErrorAddTxt = self._readMessages.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 4:
                if not self._exchangeConfiguration.Busy and (not self._exchangeConfiguration.Error):
                    # set command parameter
                    self._exchangeConfiguration.ParCmd.LogLevel = self.LogLevel
                    self._exchangeConfiguration.ParCmd.WaitAtBlendingZone = self._parCfg.Rob.Parameter.WaitAtBlendingZone
                    self._exchangeConfiguration.ParCmd.AllowSecSeqWhileSubprogram = self._parCfg.Rob.Parameter.AllowSecSeqWhileSubprogram
                    self._exchangeConfiguration.ParCmd.AllowDynamicBlending = self._parCfg.Rob.Parameter.AllowDynamicBlending
                    self._exchangeConfiguration.ParCmd.DelayTime = self._parCfg.Rob.Parameter.DelayTime
                    self._exchangeConfiguration.ParCmd.WaitForNrOfCmd = self._parCfg.Rob.Parameter.WaitForNrOfCmd
                    self._exchangeConfiguration.ParCmd.LifeSignTimeOut = TIME_TO_UINT(self._parCfg.Com.LifeSignTimeOut)
                    self._exchangeConfiguration.ParCmd.SyncDelay = self._parCfg.Rob.Parameter.SyncDelay
                    self._exchangeConfiguration.ParCmd.SyncReaction = self._parCfg.Rob.Parameter.SyncReaction
                    copy_into(self._exchangeConfiguration.ParCmd.DataEnableSync, SyncModesToDataEnableSync(Value=self._parCfg.Plc.Parameter.SynchronizationModes))
                    self._exchangeConfiguration.ParCmd.DataInSync.ToolsInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.FramesInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.LoadsInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.WorkAreasInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.SoftwareLimitsInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.DefaultDynamicsInSync = False
                    self._exchangeConfiguration.ParCmd.DataInSync.ReferenceDynamicsInSync = False

                    # start function block
                    self._exchangeConfiguration.Enable = True
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._exchangeConfiguration.Error:
                        self.ErrorID = self._exchangeConfiguration.ErrorID
                        self.ErrorAddTxt = self._exchangeConfiguration.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 5:
                if self._exchangeConfiguration.Enabled and (not self._exchangeConfiguration.Error):
                    # ---------------------------------------------------------------------
                    # !!! ExchangeConfiguration must stay active for the Sync mechanism !!!
                    # ---------------------------------------------------------------------
                    # ExchangeConfiguration.Enable := FALSE;
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._exchangeConfiguration.Error:
                        self.ErrorID = self._exchangeConfiguration.ErrorID
                        self.ErrorAddTxt = self._exchangeConfiguration.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 6:
                if not self._readRobotData.Busy and (not self._readRobotData.Error):
                    # start function block
                    self._readRobotData.Execute = True
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._readRobotData.Error:
                        self.ErrorID = self._readRobotData.ErrorID
                        self.ErrorAddTxt = self._readRobotData.ErrorAddTxt
                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 7:
                if (self._readRobotData.Done and (not self._readRobotData.Busy)) and (not self._readRobotData.Error):
                    # set initialized flag
                    self.Initialized = True
                    # start function block
                    self._readRobotData.Execute = False
                    # set timeout
                    SetTimeout(PT=self._timeoutCmd, rTimer=self._timerCmd)
                    # inc step counter
                    self._stepCmd = self._stepCmd + 1
                else:
                    # check error ?
                    if self._readRobotData.Error:
                        self.ErrorID = self._readRobotData.ErrorID
                        self.ErrorAddTxt = self._readRobotData.ErrorAddTxt

                    # timeout exceeded ?
                    if CheckTimeout(rTimer=self._timerCmd) == RobotLibraryConstants.OK:
                        self.ErrorID = RobotLibraryErrorIdEnum.ERR_TIMEOUT_CMD
                        self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)

            case 8:
                self.Initialized = not self.Error and (not self.Synchronized)  # {warning 'ToDo'}
                self.Initialized = not self.Synchronized

                # Wait for task disable
                if not self.Enable:
                    # Reset active command register
                    AxesGroup.Acyclic.ActiveCommandRegister.Reset()
                    # reset internal variables
                    self.Reset(AxesGroup=AxesGroup)
                    # Reset step counter
                    self._stepCmd = 0
                    # finished okay
                    OnExecRun = RobotLibraryConstants.OK
            case _:
                # invalid step
                self.ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP
                self.ErrorAddTxt = trunc_str(CONCAT('_stepCmd = ', DINT_TO_STRING(self._stepCmd)), 40)
        return OnExecRun

    def Reset(self, *, AxesGroup: _T.AxesGroup) -> None:
        # reset flags
        self.Busy = False
        self.Initialized = False
        self.Synchronized = False
        self.Error = False
        self.ErrorID = 0
        self.ErrorAddTxt = ''
        self.WarningID = 0
        self.InfoID = 0

        # Reset internal functon blocks
        self._exchangeConfiguration.Enable = False
        self._readRobotData.Execute = False
        self._readMessages.Enable = False
        self._readToolData.Execute = False
        self._readFrameData.Execute = False
        self._readLoadData.Execute = False
        self._readWorkArea.Execute = False
        self._readRobotSWLimits.Execute = False
        self._readRobotDefaultDynamics.Execute = False
        self._readRobotReferenceDynamics.Execute = False
        self._writeToolData.Execute = False
        self._writeFrameData.Execute = False
        self._writeLoadData.Execute = False
        self._writeWorkArea.Execute = False
        self._writeRobotSWLimits.Execute = False
        self._writeRobotDefaultDynamics.Execute = False
        self._writeRobotReferenceDynamics.Execute = False

        # Set Client error to force server error
        AxesGroup.Cyclic.PlcToRob.Control = ControlHalfByte.NONE

        # Reset synchronisation state variables
        AxesGroup.State.SyncStatePlc.InSync.Frame = False
        AxesGroup.State.SyncStatePlc.InSync.Tool = False
        AxesGroup.State.SyncStatePlc.InSync.Load = False
        AxesGroup.State.SyncStatePlc.InSync.WorkArea = False
        AxesGroup.State.SyncStatePlc.InSync.SwLimits = False
        AxesGroup.State.SyncStatePlc.InSync.DefaultDynamics = False
        AxesGroup.State.SyncStatePlc.InSync.ReferenceDynamics = False

        AxesGroup.State.SyncStatePlc.UnSyncNo.Frame = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.Tool = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.Load = 0
        AxesGroup.State.SyncStatePlc.UnSyncNo.WorkArea = 0

        AxesGroup.State.SyncStateRc.InSync.Frame = False
        AxesGroup.State.SyncStateRc.InSync.Tool = False
        AxesGroup.State.SyncStateRc.InSync.Load = False
        AxesGroup.State.SyncStateRc.InSync.WorkArea = False
        AxesGroup.State.SyncStateRc.InSync.SwLimits = False
        AxesGroup.State.SyncStateRc.InSync.DefaultDynamics = False
        AxesGroup.State.SyncStateRc.InSync.ReferenceDynamics = False

        AxesGroup.State.SyncStateRc.UnSyncNo.Frame = 0
        AxesGroup.State.SyncStateRc.UnSyncNo.Tool = 0
        AxesGroup.State.SyncStateRc.UnSyncNo.Load = 0
        AxesGroup.State.SyncStateRc.UnSyncNo.WorkArea = 0

        # Reset active command register
        AxesGroup.Acyclic.ActiveCommandRegister.Reset()

        # reset step counters
        self._stepCmd = 0
        self._stepSyncFrameData = 0
        self._stepSyncLoadData = 0
        self._stepSyncDefaultDynamics = 0
        self._stepSyncReferenceDynamics = 0
        self._stepSyncSWLimits = 0
        self._stepSyncToolData = 0
        self._stepSyncWorkArea = 0

    def SetError(self, *, ErrorID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasError or Overwrite:
            self.ErrorID = ErrorID

    def SetInfo(self, *, InfoID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasInfo or Overwrite:
            self.InfoID = InfoID

    def SetWarning(self, *, WarningID: int = 0, Overwrite: bool = False) -> None:  # PUBLIC
        if not self.HasWarning or Overwrite:
            self.WarningID = WarningID

    def _get_HasError(self) -> bool:
        HasError: bool = False

        HasError = self.ErrorID != RobotLibraryErrorIdEnum.NO_ERROR
        return HasError

    HasError = property(_get_HasError, None)  # PROTECTED

    def _get_HasInfo(self) -> bool:
        HasInfo: bool = False

        HasInfo = self.InfoID != RobotLibraryInfoIdEnum.NO_INFO
        return HasInfo

    HasInfo = property(_get_HasInfo, None)  # PROTECTED

    def _get_HasWarning(self) -> bool:
        HasWarning: bool = False

        HasWarning = self.WarningID != RobotLibraryWarningIdEnum.NO_WARNING
        return HasWarning

    HasWarning = property(_get_HasWarning, None)  # PROTECTED
