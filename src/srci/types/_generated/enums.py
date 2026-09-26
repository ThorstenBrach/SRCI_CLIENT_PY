"""SRCI enumerations - generated from the PLC library, DO NOT EDIT.

Source: third_party/robotlibrary/RobotLibrary.xml (sha256 6d064f48fb9cb9c5)
Regenerate with ``python -m tools.plcopen_gen``.
"""
# ruff: noqa
# fmt: off
from __future__ import annotations

from srci.types import iec as _iec

__all__ = [
    'AbortingMode',
    'AbortingModeEnum',
    'ActiveCommandRegisterState',
    'AreaType',
    'ArmConfigElbow',
    'ArmConfigShoulder',
    'ArmConfigWrist',
    'AxesGroupParameterCmdEntries',
    'AxisUnit',
    'BlendingMode',
    'BufferStateCmd',
    'BufferStateRsp',
    'CircMode',
    'CircPlane',
    'CmdMessageState',
    'CmdType',
    'CollisionReactionMode',
    'ComDirection',
    'ConnectionMode',
    'ControlHalfByte',
    'ConveyorType',
    'DataType',
    'DefinitionMode',
    'DetectionMode',
    'ErrorReaction',
    'ErrorTriggerMode',
    'ExecutionMode',
    'FrameCalculationMode',
    'FunctionMode',
    'InitializationState',
    'InterpolationMode',
    'JogMode',
    'LimitMode',
    'LoadMeasurementMode',
    'LoadMeasurementSteps',
    'LogLevel',
    'LogLevelEnum',
    'LogonMode',
    'MeasuringIoMode',
    'MeasuringUnitMode',
    'MessageLevel',
    'MessageLevelEnum',
    'MessageType',
    'OperationMode',
    'OriMode',
    'OrientationMode',
    'PathChoice',
    'PriorityLevel',
    'ProcessingMode',
    'ProcessingModeEnum',
    'RaPowerState',
    'RaSequenceState',
    'ReferenceElement',
    'ReferenceType',
    'ResistanceForceMode',
    'ReturnMode',
    'RiState',
    'RobotLibraryErrorIdEnum',
    'RobotLibraryInfoIdEnum',
    'RobotLibraryWarningIdEnum',
    'SensorConnectionMode',
    'SequenceFlag',
    'SequenceFlagEnum',
    'Severity',
    'SingularityAvoidanceMode',
    'SplineMode',
    'StepMode',
    'StopMode',
    'SyncDirection',
    'SyncInMode',
    'SyncMode',
    'SyncReaction',
    'SyncTime',
    'TelegramState',
    'ThresholdMode',
    'ToolCalculationMode',
    'TrajectoryMode',
    'TransformMode',
    'TriggerCondition',
    'TriggerModeIo',
    'TriggerModeLimit',
    'TriggerModeMeasurement',
    'TriggerReactionMode',
    'TurnMode',
    'UnitLimitAxis',
    'UnitType',
    'WorkAreaReactionMode',
]


class ArmConfigElbow(_iec.IecIntEnum):
    """ArmConfigElbow (INT)"""
    USE_CONFIG = 0
    """Use config in position"""
    SAME = 1
    """Do not change config with this movement. (default)"""
    FREE = 2
    """Configuration in position is not used but the Robot is free to change config"""
    DOWN = 3
    """Set elbow configuration in position to Down"""
    UP = 4
    """Set elbow configuration in position to up"""


_iec.register_enum(ArmConfigElbow, _iec.INT)


class ArmConfigShoulder(_iec.IecIntEnum):
    """ArmConfigShoulder (INT)"""
    USE_CONFIG = 0
    """Use config in position"""
    SAME = 1
    """Do not change config with this movement. (default)"""
    FREE = 2
    """Configuration in position is not used but the Robot is free to change config"""
    BACK = 3
    """Set shoulder configuration in position to Back"""
    FRONT = 4
    """Set shoulder configuration in position to Front"""


_iec.register_enum(ArmConfigShoulder, _iec.INT)


class ArmConfigWrist(_iec.IecIntEnum):
    """ArmConfigWrist (INT)"""
    USE_CONFIG = 0
    """Use config in position"""
    SAME = 1
    """Do not change config with this movement. (default)"""
    FREE = 2
    """Configuration in position is not used but the Robot is free to change config"""
    FLIP = 3
    """Set wrist configuration in position to Flip"""
    NON_FLIP = 4
    """Set wrist configuration in position to Non-Flip"""


_iec.register_enum(ArmConfigWrist, _iec.INT)


class RobotLibraryErrorIdEnum(_iec.IecIntEnum):
    """RobotLibraryErrorIdEnum (WORD)"""
    NO_ERROR = 0
    ERR_INVALID_STEP = 1
    """START Program fault : Invalid step"""
    ERR_INVALID_LIBRARY_PARA = 2
    """Program fault : Invalid library parameter"""
    ERR_INVALID_AXES_GROUP_ID = 3
    """Program fault : Invalid axes groups ID"""
    ERR_FUNCTION_NOT_SUPPORTED = 5
    """Function is not supported"""
    ERR_TIMEOUT_CMD = 6
    """Program fault : Timeout during command execution"""
    ERR_INVALID_PAR_CMD_SYNC_REACTION = 7
    """Parameter fault : Invalid command parameter SyncReaction"""
    ERR_INVALID_PAR_CMD = 8
    """Invalid command parameter - see log file for details (LogLevel Error)"""
    ERR_SYNC_STATE_PROHIBITS_COMMAND = 9
    """Synchronisation state prohibits command execution"""
    ERR_SYNC_MODE_INVALID = 10
    """Synchronisation mode is invalid"""
    ERR_LOADNO_UNAVAILABLE = 11
    """
    Client Invalid parameter value - LoadNo not available on RC Commands using the parameter
    "LoadNo"
    """
    ERR_WORKAREANO_RANGE = 12
    """
    Client Invalid parameter value - WorkAreaNo outside of the allowed range -1..254 Commands using
    the parameter "WorkAreaNo"
    """
    ERR_WORKAREANO_UNAVAILABLE = 13
    """
    Client Invalid parameter value - LoadNo not available on RC Commands using the parameter
    "LoadNo"
    """
    ERR_TRIGGERMODE_NOT_ALLOWED = 14
    """Client Specified TriggerMode not allowed Commands using the parameter "TriggerMode" """
    ERR_FRAMECALCULATIONMODE_INVALID = 15
    """
    Client Specified Frame calculation mode not valid Commands using the parameter
    "FrameCalculationMode"
    """
    ERR_SYNC_TOOL_COUNT_RC_HIGHER_THAN_PLC = 16
    """RC tool count higher than PLC tool count -> Synchronization not possible"""
    ERR_SYNC_LOAD_COUNT_RC_HIGHER_THAN_PLC = 17
    """RC load count higher than PLC load count -> Synchronization not possible"""
    ERR_SYNC_FRAME_COUNT_RC_HIGHER_THAN_PLC = 18
    """RC frame count higher than PLC frame count -> Synchronization not possible"""
    ERR_SYNC_WORKAREA_COUNT_RC_HIGHER_THAN_PLC = 19
    """RC workarea count higher than PLC workarea count -> Synchronization not possible"""
    ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0xA1 = 161
    """END Telegram control does not match the telegram state"""
    ERR_INIT_LOST_UNKNOWN_0xA2 = 162
    """Initialization lost for unknown reason. See message log after reinitializing"""
    ERR_TELEGRAM_LENGTH_MISMATCH_0xA3 = 163
    """Telegram length does not match the length provided in the communication interface."""
    ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0xA4 = 164
    """Incompatible major SRCI version"""
    ERR_LIFESIGN_TIMEOUT_0xA5 = 165
    """Lifesign timeout"""
    ERR_CYCLIC_DATA_TOO_LARGE_0xA6 = 166
    """The selected optional cyclic data does not fit in the given telegram size"""
    ERR_INTERFACE_WAS_RESET_AFTER_INIT_0xA7 = 167
    """The robot interface was reset after being initialized"""
    ERR_TELEGRAM_SEQ_TIMEOUT_0xA8 = 168
    """Telegram sequence timeout"""
    ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0xA9 = 169
    """The telegram number changed after initialization"""
    ERR_AXESGROUP_ID_INVALID_0xAA = 170
    """Invalid AxesGroupID"""
    ERR_TELEGRAM_NUMBER_INVALID_0xAB = 171
    """Telegram number is invalid. E.g. TwoSequences is only activated in one direction"""
    ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0xAC = 172
    """Telegram Number is not supported"""
    ERR_SERVER_CONNECTION_LOST_0xAD = 173
    """Server Connection to the communication partner was lost"""
    ERR_VELOCITY_INVALID = 33793
    """
    Table 5-96: Telegram and Initialization State Initialization may fail due to several reasons,
    described in the following table. T he failure is signaled using the telegram state byte. 7.1
    Table "A" – Command ErrorIDs If an error related to the execution of a function block occurs,
    the function block returns an ErrorID to specify the error. The errors are stored in the PLC
    message buffer and are displayed on the function block outputs. In the PLC message buffer, they
    are dynamically arranged by the client to be displayed as follows: <Origin> <MessageType>
    <Command name> <Description> More information about the general message handling mechanism can
    be found in 5.5.11 Diagnostics. The following table gives an overview over the existing ErrorIDs
    reported by commands and the corresponding description.
    ------------------------------------------------------ CLIENT ErrorIDs
    ------------------------------------------------------ Client Specified Velocity not valid
    Commands using the parameter "Velocity"
    """
    ERR_ACCELERATION_INVALID = 33794
    """Client Specified Acceleration not valid Commands using the parameter "Acceleration" """
    ERR_DECELERATION_INVALID = 33795
    """Client Specified Deceleration not valid Commands using the parameter "Deceleration" """
    ERR_JERK_INVALID = 33796
    """Client Specified Jerk not valid Commands using the parameter "Jerk" """
    ERR_CONFIGMODE_ELBOW_INVALID = 33797
    """Client Invalid parameter value - ConfigMode Elbow Commands using the parameter "ConfigMode" """
    ERR_CONFIGMODE_SHOULDER_INVALID = 33798
    """Client Invalid parameter value - ConfigMode Shoulder Commands using the parameter "ConfigMode" """
    ERR_CONFIGMODE_WRIST_INVALID = 33799
    """Client Invalid parameter value - ConfigMode Wrist Commands using the parameter "ConfigMode" """
    ERR_TRAJECTORYMODE_INVALID = 33801
    """Client Invalid parameter value - TrajectoryMode Commands using the parameter "TrajectoryMode" """
    ERR_OVERRIDE_INVALID = 33808
    """Client Invalid parameter value - Override Commands using the parameter "Override" """
    ERR_ABORTINGMODE_INVALID = 33809
    """
    Client Invalid parameter value - AbortingMode. Only 0: Buffer / 1: Abort are valid. Commands
    using the parameter "AbortingMode"
    """
    ERR_TOOLNO_RANGE = 33810
    """
    Client Invalid parameter value - ToolNo outside of the allowed range -1..254 Commands using the
    parameter "ToolNo"
    """
    ERR_TOOLNO_UNAVAILABLE = 33811
    """
    Client Invalid parameter value - ToolNo not available on RC Commands using the parameter
    "ToolNo"
    """
    ERR_FRAMENO_RANGE = 33812
    """
    Client Invalid parameter value - FrameNo outside of the allowed range -1..254 Commands using the
    parameter "FrameNo"
    """
    ERR_FRAMENO_UNAVAILABLE = 33813
    """
    Client Invalid parameter value - FrameNo not available on RC Commands using the parameter
    "FrameNo"
    """
    ERR_ACYCLICDATA_TOO_LARGE = 33814
    """
    Client The array specified for AcyclicData exceeds the supported maximum length of 190 bytes
    Command "CallSubprogram"
    """
    ERR_RETURNACYCLICDATA_TRUNCATED = 33815
    """
    Client The array length specified for ReturnAcyclicData is not sufficient for the returned data.
    The data has been truncated Command "CallSubprogram"
    """
    ERR_LOADNO_RANGE = 33816
    """Client Invalid parameter value - LoadNo outside of the allowed range -1..254 All commands"""
    ERR_EXPORTMODE_NOT_EXIST = 33817
    """Invalid parameter value - the requested ExportMode does not exist"""
    ERR_EXPORTNAME_NOT_EXIST = 33824
    """Invalid parameter value - the requested ExportName does not exist"""
    ERR_EXPORTNAME_ALREADY_EXISTS = 33825
    """The given ExportName is already exist"""
    ERR_DATALOG_NO_MEMORY_LEFT = 33826
    """No memory is left for data log"""
    ERR_DATALOG_ERROR_OCCURRED = 33829
    """An Error occurred during data loging . Message encludes Error ID"""
    ERR_INTERNAL_UNDEFINED_STEP = 34305
    """Internal System Error "Undefined Step" """
    ERR_PROCESSINGMODE_NOT_DEFINED = 34306
    """Client Specified ProcessingMode not defined Commands using the parameter "ProcessingMode" """
    ERR_PROCESSINGMODE_NOT_ALLOWED = 34307
    """Client Specified ProcessingMode not allowed Commands using the parameter "ProcessingMode" """
    ERR_EMITTERID_NOT_ALLOWED = 34308
    """Client Specified Emitter ID not allowed Commands using the parameter "EmitterID" """
    ERR_LISTENERID_NOT_ALLOWED = 34309
    """Client Specified Listener ID not allowed Commands using the parameter "ListenerID" """
    ERR_PROCSEQFLAG_CHANGED = 34313
    """
    Client ProcessingMode or SequenceFlag changed during execution Commands using the parameter
    "ProcessingMode" or "SequenceFlag"
    """
    ERR_PRIORITY_TOO_LOW = 34320
    """Specified priority to high"""
    ERR_PRIORITY_TOO_HIGH = 34321
    """Specified priority to low"""
    ERR_COMMANDS_NOT_ENABLED = 34322
    """Client Commands are not Enabled (First Robot must be initialized) All commands"""
    ERR_ROBOT_ERROR_NO_ID = 34323
    """Client Error received from robot without error ID All commands"""
    ERR_AXESGROUP_CHANGED = 34324
    """Client AxesGroup changed during execution All commands"""
    ERR_INTERNAL_ERROR_WITHOUT_ID = 34325
    """Internal System Error "Error without Error ID"""
    ERR_SEQFLAG_NOT_ALLOWED = 34326
    """Client Specified SEQ Flag not allowed Commands using the parameter "SequenceFlag" """
    ERR_AXESGROUP_CLEARED = 34327
    """Client AxesGroup cleared during execution All commands"""
    ERR_NO_FREE_ACR_ENTRY = 34328
    """Client No free ACR entry available All commands"""
    ERR_SEQFLAG_INVALID_IN_PROC_MODE = 34341
    """
    Client Sequence flag must be 0 in the selected ProcessingMode Commands using the parameter
    "ProcessingMode" or "SequenceFlag"
    """
    ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO = 34342
    """
    Client Specified Listener ID must be > 0 for selected trigger based ProcessingMode Commands
    using the parameter "ListenerID"
    """
    ERR_EMITTERID_MUST_BE_ZERO = 34343
    """Client Specified Emitter ID must be 0 Commands using the parameter "EmitterID" """
    ERR_LISTENERID_MUST_BE_POSITIVE = 34357
    """
    Client Specified Listener ID must be a positive value (>= 0) Commands using the parameter
    "ListenerID"
    """
    ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_ENABLED = 35841
    """
    ------------------------------------------------------ SERVER ErrorIDs
    ------------------------------------------------------ Server Continue not possible - robot is
    not enabled Command "GroupContinue"
    """
    ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_IN_PRIMARY_POS = 35842
    """Server Continue not possible - robot is not inPrimaryPosition Command "GroupContinue" """
    ERR_ROBOT_DISABLED = 35843
    """Server Robot disabled Command "EnableRobot" """
    ERR_ROBOT_DISABLED_BY_ERROR = 35844
    """Server Robot disabled due to an error Command "EnableRobot" """
    ERR_MANDATORY_CMDS_MISSING = 35845
    """Server Not all mandatory commands have been called yet Command "EnableRobot" """
    ERR_RI_NOT_SYNCHRONIZED = 35846
    """
    Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies enabling in this
    state Command "EnableRobot"
    """
    ERR_LIMIT_EXCEEDED_RETURN_POS = 35847
    """Server Limit exceeded. Move closer to return position Command "ReturnToPrimary" """
    ERR_SET_OPMODE_T1EXT_REQUIRED = 35848
    """
    Server Invalid parameter value - Must switch to T1Ext when changing between AutoExt and T2Ext
    Command "SetOperationMode"
    """
    ERR_WRITE_DYNAMIC_FRAME = 35849
    """
    Server Cannot write to a dynamic frame (frame used by e.g. conveyor tracking) Command
    "WriteFrameData"
    """
    ERR_CONTINUE_NOT_POSSIBLE_BY_MANUAL_MODE = 35856
    """Server Continue not possible in manual operation mode Command "GroupContinue" """
    ERR_FRAME_REFERENCING_INVALID = 35858
    """
    Server It is not allowed to reference a frame which already references another frame Command
    "WriteFrame"
    """
    ERR_FRAME_INVALID = 35859
    """
    Server The referenced Frame is invalid, dynamic (frame used by e.g. conveyor tracking) or does
    not exist Command "WriteFrame"
    """
    ERR_TOOLID_DIFFERS_TARGET = 35860
    """
    Server Currently used tool ID differs from the tool ID of the target position Command
    "ReturnToPrimary"
    """
    ERR_WRITE_FRAME_DURING_MOVE = 35861
    """
    Server Writing a Frame during an active movement is not supported by this RC Command
    "WriteFrame"
    """
    ERR_WRITE_TOOL_DURING_MOVE = 35862
    """
    Server Writing a Tool during an active movement is not supported by this RC Command
    "WriteToolData"
    """
    ERR_WRITE_LOAD_DURING_MOVE = 35863
    """
    Server Writing a Load during an active movement is not supported by this RC Command
    "WriteLoadData"
    """
    ERR_MANUAL_STEP_NOT_ALLOWED = 35872
    """Server ManualStep is not allowed in Automatic External Command "EnableRobot" """
    ERR_MANUAL_STEP_ONLY_IN_STEP_MODE_ALLOWED = 35873
    """Server ManualStep is only allowed when StepMode is active Command "EnableRobot" """
    ERR_TOOLDATA_DIFFERS = 35874
    """
    Server The current ToolData has changed and differs from the one when the primary position was
    left. Returning is not possible. Command "ReturnToPrimary"
    """
    ERR_LOADDATA_DIFFERS = 35875
    """
    Server The current LoadData has changed and differs from the one when the primary position was
    left. Returning is not possible. Command "ReturnToPrimary"
    """
    ERR_FRAMEDATA_DIFFERS = 35876
    """
    Server The current FrameData has changed and differs from the one when the primary position was
    left. Returning is not possible. Command "ReturnToPrimary"
    """
    ERR_REF_FRAMEDATA_CHANGED = 35877
    """
    Server The current reference FrameData has changed and differs from the one when the primary
    position was left. Returning is not possible. Command "ReturnToPrimary"
    """
    ERR_TOOLNO_DIFFERS_TARGET = 35878
    """
    Server The ToolNo differs from the one in the return position. Returning is not possible.
    Command "ReturnToPrimary"
    """
    ERR_FRAMENO_DIFFERS_TARGET = 35879
    """
    Server The FrameNo differs from the one in the return position. Returning is not possible.
    Command "ReturnToPrimary"
    """
    ERR_CONTINUE_WHILE_STOPPING = 35880
    """
    Server Continue is not possible while the Robot is interrupting or stopping. Command
    "GroupContinue"
    """
    ERR_SOFTWARE_LIMITS_FOR_NON_EXISTING_AXIS = 35881
    """
    Server Software limits could not be set because values were specified for non-existing axes
    Command "WriteSWLimits"
    """
    ERR_RI_NOT_SYNCHRONIZED_CONTINUE_DENIED = 35888
    """
    Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies continue in this
    state Command "GroupContinue"
    """
    ERR_ENABLE_SWITCH_REQUIRED = 35889
    """Server Enable switch must be active to enable the robot Command "EnableRobot" """
    ERR_MANUAL_STEP_WHILE_DISABLED = 35890
    """Server Manual step sent while robot not enabled Command "EnableRobot" """
    ERR_JOG_NOT_ALLOWED_DURING_MOVE = 35891
    """Server Jog not possible during active movement Command "GroupJog" """
    ERR_TARGET_POS_FOR_NON_EXISTING_AXIS = 35892
    """Server Target position was commanded for an external axis which does not exist All move commands"""
    ERR_JOG_AXIS_NOT_EXIST = 35893
    """Server Jog of axis is not possible. Axis does not exist Command "GroupJog" """
    ERR_INC_JOG_ONE_AXIS_ONLY = 35894
    """Server Incremental jog is only possible in one axis of rotation Command "GroupJog" """
    ERR_JOBID_NOT_EXIST = 35895
    """
    Server A program for the supplied JobID does not exist. Commands: "CallSubprogram",
    "StopSubprogram"
    """
    ERR_ONLY_ALLOWED_IN_SEQ_BUFFER = 35896
    """
    Server A program including motion commands is only allowed to be executed in a sequence buffer
    Command "CallSubprogram"
    """
    ERR_JOB_ALREADY_RUNNING = 35897
    """
    Server A program with the same number is already running. Multiple instances are not supported
    Command "CallSubprogram"
    """
    ERR_JOBID_CHANGE_PM3_NOT_ALLOWED = 35906
    """
    Server Changing the JobID in PM 3 during runtime of this CMD is not supported. Command
    "CallSubprogram"
    """
    ERR_CONTINUE_DURING_STOPPING = 35907
    """
    Server Continue is not possible while the robot is stopping due to GroupInterrupt, GroupStop,
    SetSequence, or GroupJog Command "GroupContinue"
    """
    ERR_JOG_STOPPED_BY_ENABLE_RELEASED = 35922
    """Server GroupJog motion was stopped due to the release of the enable switch. Command "GroupJog" """
    ERR_SWLIMITS_NOT_ALLOWED_ROBOT_IS_OUTSIDE = 35923
    """
    Server Setting the limits is not possible because the current robot position is currently
    outside of those limits. Command "WriteSWLimits"
    """
    ERR_SWLIMITS_NOT_ALLOWED_DURING_MOVE = 35924
    """Server Setting the limits is not possible while a motion is active. Command "WriteSWLimits" """
    ERR_POSITION_NOT_REACHABLE = 35925
    """Position not reachable."""
    ERR_OPMODE_CHANGE_NOT_POSSIBLE_BY_PLC = 35926
    """
    Server Change of operation mode by the PLC not possible. The RC must be in an "External"
    operation mode Command "SetOperationMode"
    """
    ERR_AUXPOINT_IDENTICAL_WITH_OTHER_POS = 35927
    """
    Server Auxpoint must not be identical to start or end position of the motion Commands:
    "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_AUXPOINT_INVALID = 35928
    """
    Server Auxpoint invalid Commands: "MoveCircularAbsolute", "MoveCircularRelative",
    "MoveCircularCam"
    """
    ERR_CALC_NOT_POSSIBLE_BY_POS = 35929
    """
    Server Supplied positions must not be identical or at a larger distance apart Commands:
    "CalculateTool", "CalculateFrame"
    """
    ERR_CALC_NOT_POSSIBLE_BY_PARA = 35936
    """
    Server Calculation not possible with the given parameters Commands: "CalculateTool",
    "CalculateFrame"
    """
    ERR_CALC_NOT_POSSIBLE_BY_POS_ON_LINE = 35937
    """Server Positions must not be on one line Commands: "CalculateTool", "CalculateFrame" """
    ERR_INV_KINEMATIC_NO_SOLUTION = 35938
    """Server No solution found for the given CartesianPosition Command "CalculateInverseKinematic" """
    ERR_INV_KINEMATIC_SOLUTION_OUTSIDE_SWLIMITS = 35939
    """
    Server Solution is outside of the hardware limits Commands: "CalculateInverseKinematic",
    "CalculateForwardKinematic"
    """
    ERR_PARAM_WRITE_PROTECTED = 35940
    """
    Server The selected parameter is write protected and can thus not be changed Command
    "WriteSystemVariable"
    """
    ERR_POS_INDEX_OUT_OF_RANGE = 35941
    """
    Server Number of received positions exceeds the maximum expected number (index out of range)
    Commands: "CalculateTool", "CalculateFrame"
    """
    ERR_POS_INDEX_MISMATCH = 35942
    """
    Server Number of received positions does not correspond to the required number for the selected
    mode Commands: "CalculateTool", "CalculateFrame"
    """
    ERR_MAXIMUM_DISTANCE_EXCEEDED = 35943
    """
    The defined MaximumDistance to the given target JointPosition has been exceeded. Move closer to
    the target or increase the MaximumDistance.
    """
    ERR_INVALID_SAFEREFERENCE_POSITION = 35944
    """The given JointPosition does not match the RAs safe referencing position."""
    ERR_SAFETY_SENSOR_NOT_TRIGGERED = 35945
    """The safety sensor did not trigger"""
    ERR_RESTART_WHILE_ROBOT_MOVING = 35952
    """Restart is only possible if the robot is not moving."""
    ERR_UNSUPPORTED_COMBINED_JOG = 35953
    """Simultaneous rotational and translational jog is not supported"""
    ERR_GROUPRESET_PENDING_MESSAGES = 35954
    """GroupReset not possible, as not all messages were transmitted yet"""
    ERR_INVALID_PARAM_ACCELERATION_RATE = 36097
    """
    Server Invalid parameter value - AccelerationRate Commands using the parameter
    "AccelerationRate"
    """
    ERR_INVALID_PARAM_BLENDING_MODE = 36099
    """Server Invalid parameter value - BlendingMode Commands using the parameter "BlendingMode" """
    ERR_INVALID_PARAM_BLENDING_PARA = 36100
    """
    Server Invalid parameter value - BlendingParameter Commands using the parameter
    "BlendingParameter"
    """
    ERR_INVALID_PARAM_CONFIGMODE_ELBOW = 36101
    """Server Invalid parameter value - ConfigMode Elbow Commands using the parameter "ConfigMode" """
    ERR_INVALID_PARAM_DECELERATION_RATE = 36102
    """
    Server Invalid parameter value - DecelerationRate Commands using the parameter
    "DecelerationRate"
    """
    ERR_INVALID_PARAM_VALUE_ZERO = 36103
    """
    Server Invalid parameter value - No value greater than zero Commands: "WriteDefaultDynamics",
    "WriteReferenceDynamics"
    """
    ERR_INVALID_PARAM_FRAMENO = 36104
    """Server Invalid parameter value - FrameNo Commands using the parameter "FrameNo" """
    ERR_INVALID_PARAM_INC_ROTATION = 36105
    """Server Invalid parameter value - IncrementalRotation Command "GroupJog" """
    ERR_INVALID_PARAM_INC_TRANSLATION = 36112
    """Server Invalid parameter value - IncrementalTranslation Command "GroupJog" """
    ERR_INVALID_PARAM_JERK_RATE = 36113
    """Server Invalid parameter value - JerkRate Commands using the parameter "JerkRate" """
    ERR_INVALID_PARAM_JOG_POS_AND_JOG_NEG = 36114
    """
    Server Invalid parameter value - Control Positive and negative jog direction was active at the
    same time Command "GroupJog"
    """
    ERR_INVALID_PARAM_JOINT_POS = 36115
    """Server Invalid parameter value - JointPosition Commands using the parameter "JointPosition" """
    ERR_INVALID_PARAM_LIFE_SIGN_TIMEOUT = 36116
    """Server Invalid parameter value - LifesignTimeout Command "ExchangeConfiguration" """
    ERR_INVALID_PARAM_SWLIMITS = 36117
    """
    Server Invalid parameter value - SoftwareLimits all values must not be zero Command
    "WriteRobotSWLimits"
    """
    ERR_INVALID_PARAM_LIMITVALUES = 36118
    """Server Invalid parameter value - LimitValues Command "WriteRobotSWLimits" """
    ERR_INVALID_PARAM_LOADNO = 36119
    """Server Invalid parameter value - LoadNo Commands using the parameter "LoadNo" """
    ERR_INVALID_PARAM_LOG_LEVEL = 36120
    """Server Invalid parameter value - LogLevel Command "ExchangeConfiguration" """
    ERR_INVALID_PARAM_MODE = 36129
    """Server Invalid parameter value - Mode Commands using the parameter "Mode" """
    ERR_INVALID_PARAM_ORI_MODE = 36130
    """Server Invalid parameter value - OriMode Commands using the parameter "OriMode" """
    ERR_INVALID_PARAM_OVERRIDE = 36131
    """Server Invalid parameter value - Override Commands using the parameter "Override" """
    ERR_INVALID_PARAM_POSITION = 36132
    """Server Invalid parameter value - Position Commands using the parameter "Position" """
    ERR_INVALID_PARAM_REF_DYNAMICS_LESS_THAN_ZERO = 36133
    """
    Server Invalid parameter value - ReferenceDynamics all values less than zero Command
    "WriteReferenceDynamics"
    """
    ERR_INVALID_PARAM_ACCELERATION = 36134
    """Server Invalid parameter value - Acceleration Commands using the parameter "Acceleration" """
    ERR_INVALID_PARAM_DECELERATION = 36135
    """Server Invalid parameter value - Deceleration Commands using the parameter "Deceleration" """
    ERR_INVALID_PARAM_JERK = 36136
    """Server Invalid parameter value - Jerk Commands using the parameter "Jerk" """
    ERR_INVALID_PARAM_VELOCITY = 36137
    """Server Invalid parameter value - Velocity Commands using the parameter "Velocity" """
    ERR_INVALID_PARAM_RETURN_MODE = 36144
    """Server Invalid parameter value - ReturnMode Command "ReturnToPrimary" """
    ERR_INVALID_PARAM_TARGET_SEQUENCE = 36145
    """Server Invalid parameter value - TargetSequence Command "SetSequence" """
    ERR_INVALID_PARAM_OPERATION_MODE = 36146
    """Server Invalid parameter value - OperationMode Command "SetOperationMode" """
    ERR_INVALID_PARAM_SYNC_REACTION = 36147
    """Server Invalid parameter value - SyncReaction Command "LRob_ExchangeConfiguration" """
    ERR_INVALID_PARAM_TIME = 36148
    """Server Invalid parameter value - Time Commands using the parameter "Time" """
    ERR_INVALID_PARAM_TOOLNO = 36149
    """Server Invalid parameter value - ToolNo Commands using the parameter "ToolNo" """
    ERR_INVALID_PARAM_TRAJECTORY_MODE = 36150
    """Server Invalid parameter value - TrajectoryMode Command "ReturnToPrimary" """
    ERR_INVALID_PARAM_TURN_MODE = 36151
    """Server Invalid parameter value - TurnMode Commands using the parameter "TurnMode" """
    ERR_INVALID_PARAM_VELOCITY_MODE = 36152
    """Server Invalid parameter value - VelocityRate Commands using the parameter "VelocityRate" """
    ERR_INVALID_PARAM_WAIT_FOR_NR_OF_CMD = 36153
    """Server Invalid parameter value - WaitForNrOfCmd Command "LRob_ExchangeConfiguration" """
    ERR_INVALID_PARAM_CONFIG_MODE_SHOULDER = 36160
    """Server Invalid parameter value - ConfigMode Shoulder Commands using the parameter "ConfigMode" """
    ERR_INVALID_PARAM_CONFIG_MODE_WRIST = 36161
    """Server Invalid parameter value - ConfigMode Wrist Commands using the parameter "ConfigMode" """
    ERR_INVALID_PARAM_STEP_MODE = 36162
    """Server Invalid parameter value - StepMode Commands using the parameter "StepMode" """
    ERR_STEP_MODE_NOT_VALID = 36163
    """Server The supplied StopMode is not valid. Use 0, 1, or 2 Command "StopSubprogram" """
    ERR_STOP_MODE_2_TARGETID_NEG1 = 36164
    """
    Server When StopMode 2: (Stop all subprograms) is selected, the TargetID must be -1. Command
    "StopSubprogram"
    """
    ERR_STOP_MODE_0_TARGETID_NOT_NEG1 = 36165
    """
    Server When StopMode 0: (Stop via JobID) is selected, the TargetID must NOT be -1. Command
    "StopSubprogram"
    """
    ERR_STOP_MODE_1_TARGETID_NOT_NEG1 = 36166
    """
    Server When StopMode 1: (Stop via InstanceID) is selected, the TargetID must NOT be -1. Command
    "StopSubprogram"
    """
    ERR_INVALID_PARAM_INDEX_OUT_OF_RANGE = 36167
    """Server Invalid parameter value - Index out of range All Commands"""
    ERR_INVALID_PARAM_SAME_INDEX_MULTIPLE_TIMES = 36168
    """
    Server Invalid parameter value - Same index was used multiple times Commands:
    "WriteDigitalOutputs", "WriteIntegers", "WriteReals", "WriteAnalogOutputs", "ReadDigitalInputs",
    "ReadDigitalOutputs", "ReadIntegers", "ReadReals"
    """
    ERR_INVALID_PARAM_MASS_EXCEEDS_PAYLOAD = 36169
    """
    Server Invalid parameter value - Specified mass greater than the maximum RA payload. Command
    "WriteLoad"
    """
    ERR_INVALID_PARAM_AT_LEAST_ONE_INDEX_REQUIRED = 36176
    """
    Server Invalid parameter value - At least one index must not be 0 and result in a read/write
    operation. Commands: "WriteDigitalOutputs", "WriteIntegers", "WriteReals", "WriteAnalogOutputs",
    "ReadDigitalInputs", "ReadDigitalOutputs", "ReadIntegers", "ReadReals"
    """
    ERR_INVALID_PARAM_MESSAGE_LEVEL = 36177
    """Server Invalid parameter value - MessageLevel must be between 0-28 Command "ReadMessages" """
    ERR_INVALID_PARAM_CIRCPLANE_MISMATCH_CIRCMODE = 36193
    """
    Server Invalid parameter value - CircPlane does not match CircMode Commands:
    "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_INVALID_PARAM_CIRCMODE_OUT_OF_RANGE = 36194
    """
    Server Invalid parameter value - CircMode outside of the allowed range 0..3 Commands:
    "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_INVALID_PARAM_TOLERANCE_ONLY_CIRCMODE_1 = 36195
    """
    Server Invalid parameter value - Tolerance must only be used for CircMode 1 Commands:
    "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_INVALID_PARAM_ANGLE_ONLY_CIRCMODE_2 = 36196
    """
    Server Invalid parameter value - Angle must only be used for CircMode 2 Commands:
    "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_INVALID_PARAM_PATH_CHOICE_OUT_OF_RANGE = 36197
    """Server Invalid parameter value - PathChoice outside of the allowed range 0..1 Commands"""
    ERR_INVALID_PARAM_SHIFT_MODE_OUT_OF_RANGE = 36198
    """Server Invalid parameter value - Mode outside of the allowed range 0..4 Command "ShiftPosition" """
    ERR_INVALID_PARAM_ROTATION_ANGLE_ONLY_MODE_3 = 36199
    """Server Invalid parameter value - RotationAngle only allowed in mode 3 Command "ShiftPosition" """
    ERR_INVALID_PARAM_TRANSFORMATION_PARAM_2_INVALID = 36200
    """
    Server Invalid parameter value - TransformationParameter_2 value does not match the selected
    mode Command "ShiftPosition"
    """
    ERR_INVALID_PARAM_TOOLNO_OUT_OF_RANGE = 36201
    """
    Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on
    the RC Commands: "CalculateTool", "CalculateFrame"
    """
    ERR_INVALID_PARAM_FRAMENO_OUT_OF_RANGE = 36208
    """
    Server Invalid parameter value - FrameNo outside of the allowed range 0..254 or does not exist
    on the RC Command "CalculateCartesianPosition"
    """
    ERR_INVALID_PARAM_TARGET_TOOLNO_OUT_OF_RANGE = 36209
    """
    Server Invalid parameter value - TargetToolNo outside of the allowed range 0..254 or does not
    exist on the RC Command "CalculateCartesianPosition"
    """
    ERR_INVALID_PARAM_TARGET_FRAMENO_OUT_OF_RANGE = 36210
    """
    Server Invalid parameter value - TargetFrameNo outside of the allowed range 0..254 or does not
    exist on the RC Command "CalculateCartesianPosition"
    """
    ERR_INVALID_PARAM_ERR_TOOLNO_INVALID = 36211
    """
    Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on
    the RC Command "CalculateCartesianPosition"
    """
    ERR_INVALID_PARAM_PARAMETER_ID_INVALID = 36212
    """
    Server Invalid parameter value - ParameterID does not exist on the RC Commands:
    "ReadSystemVariable", "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_SUB_PARAMETER_ID_INVALID = 36213
    """
    Server Invalid parameter value - SubParameterID does not exist on the RC for the supplied
    ParameterID Commands: "ReadSystemVariable", "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_SUB_PARAMETER_MUST_BE_ZERO = 36214
    """
    Server Invalid parameter value - SubParameterID must be 0 for a parameter without subparameters
    Commands: "ReadSystemVariable", "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_SUB_PARAMETER_MUST_NOT_BE_ZERO = 36215
    """
    Server Invalid parameter value - SubParameterID must not be 0 for a parameter with subparameters
    Commands: "ReadSystemVariable", "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_TYPE_OUT_OF_RANGE = 36216
    """
    Server Invalid parameter value - DataType outside of the allowed range 1..13 Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_TYPE_MISMATCH = 36217
    """
    Server Invalid parameter value - DataType does not match the data type of the parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_0_INVALID = 36224
    """
    Server Invalid parameter value - Data_0 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_1_INVALID = 36225
    """
    Server Invalid parameter value - Data_1 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_2_INVALID = 36226
    """
    Server Invalid parameter value - Data_2 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_3_INVALID = 36227
    """
    Server Invalid parameter value - Data_3 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_4_INVALID = 36228
    """
    Server Invalid parameter value - Data_4 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_5_INVALID = 36229
    """
    Server Invalid parameter value - Data_5 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_6_INVALID = 36230
    """
    Server Invalid parameter value - Data_6 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_DATA_7_INVALID = 36231
    """
    Server Invalid parameter value - Data_7 contains invalid data for the target parameter Command
    "WriteSystemVariable"
    """
    ERR_INVALID_PARAM_REFERENCE_FRAME_OUT_OF_RANGE = 36232
    """
    Server Invalid parameter value - ReferenceFrame outside of the allowed range 0..254 or does not
    exist on the RC Command "CalculateFrame"
    """
    ERR_OPTIONAL_PARAM_DECELERATION_RATE_NOT_SUPPORTED = 36355
    """
    Server Optional parameter value not supported - DecelerationRate Commands using the parameter
    "DecelerationRate"
    """
    ERR_OPTIONAL_PARAM_JERK_RATE_NOT_SUPPORTED = 36356
    """Server Optional parameter value not supported - JerkRate Commands using the parameter "JerkRate" """
    ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED = 36357
    """
    Server Optional parameter value not supported - BlendingMode Commands using the parameter
    "BlendingMode"
    """
    ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED = 36358
    """Server Optional parameter value not supported - Time Commands using the parameter "Time" """
    ERR_OPTIONAL_PARAM_POSITION_NOT_SUPPORTED = 36359
    """Server Optional parameter value not supported - Position Commands using the parameter "Position" """
    ERR_OPTIONAL_PARAM_ORI_MODE_NOT_SUPPORTED = 36360
    """Server Optional parameter value not supported - OriMode Commands using the parameter "OriMode" """
    ERR_OPTIONAL_PARAM_CONFIG_MODE_NOT_SUPPORTED = 36361
    """
    Server Optional parameter value not supported - ConfigMode Commands using the parameter
    "ConfigMode"
    """
    ERR_OPTIONAL_PARAM_TURN_MODE_NOT_SUPPORTED = 36368
    """Server Optional parameter value not supported - TurnMode Commands using the parameter "TurnMode" """
    ERR_OPTIONAL_PARAM_TRAJECTORY_MODE_NOT_SUPPORTED = 36369
    """Server Optional parameter value not supported - TrajectoryMode Command "ReturnToPrimary" """
    ERR_OPTIONAL_PARAM_OPERATION_MODE_NOT_SUPPORTED = 36370
    """Server Optional parameter value not supported - OperationMode Command "SetOperationMode" """
    ERR_OPTIONAL_PARAM_INC_ROTATION_NOT_SUPPORTED = 36371
    """Server Optional parameter value not supported - IncrementalRotation Command "GroupJog" """
    ERR_OPTIONAL_PARAM_INC_TRANSLATION_NOT_SUPPORTED = 36372
    """Server Optional parameter value not supported - IncrementalTranslation Command "GroupJog" """
    ERR_OPTIONAL_PARAM_STEP_MODE_EXACT_STOP_NOT_SUPPORTED = 36374
    """Server Optional parameter value not supported - StepMode Exact Stop Command "EnableRobot" """
    ERR_OPTIONAL_PARAM_STEP_MODE_BLENDING_NOT_SUPPORTED = 36375
    """Server Optional parameter value not supported - StepMode Blending Command "EnableRobot" """
    ERR_CONFIG_MODES_MUST_BE_IDENTICAL = 36377
    """Only identical config modes for shoulder, elbow and wrist are supported."""
    ERR_OPTIONAL_PARAM_MODIFIED_CONVENTION_NOT_SUPPORTED = 36384
    """Server Optional parameter value not supported - ModifiedConvention Command "ReadDHParameter" """
    ERR_OPTIONAL_PARAM_WAIT_AT_BLENDING_POINT_NOT_SUPPORTED = 36385
    """Server Optional parameter value not supported - WaitAtBlendingPoint Command "ExchangeConfig" """
    ERR_OPTIONAL_PARAM_ANGLE_NOT_SUPPORTED = 36387
    """
    Server Optional parameter not supported - Angle Commands: "MoveCircularAbsolute",
    "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_OPTIONAL_PARAM_PATH_CHOICE_NOT_SUPPORTED = 36388
    """
    Server Optional parameter not supported - PathChoice Commands: "MoveCircularAbsolute",
    "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_OPTIONAL_PARAM_TOLERANCE_NOT_SUPPORTED = 36389
    """
    Server Optional parameter not supported - Tolerance Commands: "MoveCircularAbsolute",
    "MoveCircularRelative", "MoveCircularCam"
    """
    ERR_OPTIONAL_PARAM_TRANSFORMATION_PARAM2_NOT_SUPPORTED = 36390
    """Server Optional parameter not supported - TransformationParameter_2 Command "ShiftPosition" """
    ERR_OPTIONAL_PARAM_ROTATION_ANGLE_NOT_SUPPORTED = 36391
    """Server Optional parameter not supported - RotationAngle Command "ShiftPosition" """
    ERR_OPTIONAL_PARAM_VALUE_NOT_SUPPORTED = 36392
    """Server Optional parameter value not supported - Mode Commands: "CalculateTool", "CalculateFrame" """
    ERR_OPTIONAL_PARAM_EXTERNAL_TCP_NOT_SUPPORTED = 36393
    """
    Server Optional parameter not supported - ExternalTCP Commands: "CalculateTool",
    "CalculateFrame"
    """
    ERR_OPTIONAL_PARAM_RELATIVE_POS_NOT_SUPPORTED = 36400
    """
    Server Optional parameter not supported - RelativePosition Commands using the parameter
    "RelativePosition"
    """
    ERR_OPTIONAL_PARAM_MAXIMUM_DISTANCE_NOT_SUPPORTED = 36401
    """Optional parameter not supported - Maximum Distance"""
    ERR_OPTIONAL_PARAM_CIRCMODE_VALUE_NOT_SUPPORTED = 36402
    """Optional parameter value not supported - CircMode"""
    ERR_OPTIONAL_PARAM_IX_NOT_SUPPORTED = 36403
    """Optional parameter not supported - IX"""
    ERR_OPTIONAL_PARAM_IY_NOT_SUPPORTED = 36404
    """Optional parameter not supported - IY"""
    ERR_OPTIONAL_PARAM_IZ_NOT_SUPPORTED = 36405
    """Optional parameter not supported - IZ"""
    ERR_OPTIONAL_PARAM_RX_NOT_SUPPORTED = 36406
    """Optional parameter not supported - RX"""
    ERR_OPTIONAL_PARAM_RY_NOT_SUPPORTED = 36407
    """Optional parameter not supported - RY"""
    ERR_OPTIONAL_PARAM_RZ_NOT_SUPPORTED = 36408
    """Optional parameter not supported - RZ"""
    ERR_OPTIONAL_PARAM_INCREMENTAL_JOG_NOT_SUPPORTED = 36409
    """Optional parameter not supported - IncrementalJog"""
    ERR_EMITTER_ID_MUST_NOT_BE_ZERO = 36612
    """Server Specified Emitter ID must not be 0 Commands using the parameter "EmitterID" """
    ERR_INVALID_PARAM_EXECUTION_MODE = 36624
    """Server Invalid parameter value - Execution mode All Commands"""
    ERR_CMD_NOT_IMPLEMENTED = 36625
    """Server Command not implemented All Commands"""
    ERR_CMD_ONLY_ONE_INSTANCE_ALLOWED = 36626
    """
    Server Only one instance of this command is allowed Commands: "EnableRobot", "GroupJog",
    "ReturnToPrimary", "ExchangeConfig"
    """
    ERR_CMD_REQUIRES_INTERRUPT_OR_IDLE_STATE = 36627
    """
    Server Command requires an active interrupt or idle state to be executed Commands: "GroupJog",
    "ReturnToPrimary"
    """
    ERR_CMD_NOT_ALLOWED_DURING_ACTIVE_INTERRUPT = 36628
    """Server Command cannot be executed during active interrupt Command "ReturnToPrimary" """
    ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD = 36629
    """
    Server Secondary sequence is blocked by command (e.g. GroupJog, ReturnToPrimary). No other
    commands may be buffered in secondary sequence All commands processed in secondary sequence
    """
    ERR_SECONDARY_SEQUENCE_NOT_ACTIVE = 36630
    """
    Server The secondary sequence is not active. Commands may only be buffered in this sequence if
    it is active Commands using the parameter "SequenceFlag"
    """
    ERR_SECONDARY_SEQUENCE_NOT_EMPTY = 36631
    """
    Server Secondary sequence is not empty. The command requires the secondary sequence to be empty
    Commands: "GroupJog", "ReturnToPrimary"
    """
    ERR_TRANSACTION_NOT_POSSIBLE_IN_STATE_MACHINE = 36632
    """Server Transaction not possible in the state machine All commands"""
    ERR_CMD_NOT_POSSIBLE_BY_OP_MODE_LOCAL = 36633
    """
    Server Cannot execute command because current operation mode is local. Commands that are not
    available in local modes
    """
    ERR_CMD_TYPE_OUT_OF_RANGE = 36640
    """Server Command type out of range All commands"""
    ERR_CMD_NOT_POSSIBLE_DURING_CALL_SUB_PROGRAM = 36641
    """
    Server Execution of this CMD is not possible while CallSubprogram is in progress in the sequence
    Commands: "SetSequence", "GroupJog"
    """
    ERR_OPERATION_NOT_POSSIBLE_SEE_LOG = 36662
    """Server Operation not possible. See MessageLog for further information All commands"""
    ERR_INTERNAL_ERROR_DURING_CMD = 36863
    """
    Server An RC internal error occurred during execution of this command. Check the message log for
    additional information All commands
    """
    ERR_WRONG_TELEGRAM_STATE = 32769
    """
    7.2 Table "B" – RI ErrorIDs RI errors can occur on the PLC as well as on the RC. In the event of
    an RI error on the PLC, the corresponding ErrorID is written to the PLC message buffer
    independent of the function call "ReadMessages". In the event of an RI error on the RC, the
    ErrorID is transmitted via the function block "ReadMessages" and is also stored in PLC message
    buffer. In the PLC message buffer, they are dynamically arranged by the client to be displayed
    as follows: <Origin> <MessageType> <Description> More information about the general message
    handling mechanism can be found in 5.5.11 Diagnostics. The following table gives an overview
    over the existing "ErrorIDs" reported via RI errors and the corresponding description.
    ------------------------------------------------------ Client ErrorIDs
    ------------------------------------------------------ Client Wrong Telegram State (Two
    Sequences not in both directions active)
    """
    ERR_ACYCLIC_AREA_TO_SMALL_PLC_TO_ROB = 32770
    """Client Acyclic area client to server too small"""
    ERR_ACYCLIC_AREA_TO_SMALL_ROB_TO_PLC = 32771
    """Client Acyclic area server to client too small"""
    ERR_LIFESIGN_TIMEOUT_0x8005 = 32772
    """Client Lifesign timeout"""
    ERR_TELEGRAM_SEQ_TIMEOUT_0x8005 = 32773
    """Client Telegram sequence timeout"""
    ERR_AXESGROUP_INVALID = 32775
    """Client Assigned AxesGroup not valid"""
    ERR_PERIPHERY_INVALID = 32776
    """Client Assigned periphery not valid"""
    ERR_INVALID_ROBOT_STATE = 32777
    """Client Invalid state of the robot (more than 1 CMD active)"""
    ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT = 32787
    """
    Client Telegram Number changed after initialization. Reinitialize by disabling and enabling the
    RobotTask.
    """
    ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0x80A1 = 32929
    """Client Telegram control does not match the telegram state"""
    ERR_INIT_LOST_UNKNOWN_0x80A2 = 32930
    """Client Initialization lost for unknown reason. See message log after reinitializing"""
    ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3 = 32931
    """
    Client Telegram length does not match the length provided in the communication interface, or the
    communication interface is too small.
    """
    ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0x80A4 = 32932
    """Client Incompatible major SRCI version"""
    ERR_LIFESIGN_TIMEOUT_0x80A5 = 32933
    """Client Lifesign timeout"""
    ERR_CYCLIC_DATA_TOO_LARGE_0x80A6 = 32934
    """Client The selected optional cyclic data does not fit in the given telegram size"""
    ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7 = 32935
    """Client The robot interface was reset after being initialized"""
    ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8_0x80A8 = 32936
    """Client Telegram sequence timeout"""
    ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0x80A9 = 32937
    """Client The telegram number changed after initialization"""
    ERR_AXESGROUP_ID_INVALID_0x80AA = 32938
    """Client Error: Invalid AxesGroupID"""
    ERR_TELEGRAM_NUMBER_INVALID_0x80AB = 32939
    """Client Telegram number is invalid. E.g. TwoSequences is only activated in one direction"""
    ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0x80AC = 32940
    """Client Telegram Number is not supported"""
    ERR_ACR_REGISER_IS_FULL = 35329
    """Server The ACR is full. RA is disabled"""
    ERR_MANDATORY_CMD_STOPPED = 35330
    """
    Server The execution of a mandatory command has been stopped. Exchange config must run for the
    system to run
    """
    ERR_INCONSISTENT_DATA_RECEIVED = 35331
    """
    Server Inconsistent data received. Make sure the complete telegram data is sent to RC in one
    frame.
    """
    ERR_CONNECTION_LOST = 35501
    """Client Connection to the communication partner was lost"""
    ERR_FATAL_ERROR_REINIT_REQUIRED = 36865
    """Client Fatal Error occurred. Reinitialization of Robot_Task is required"""
    ERR_INTERNAL_ERROR = 39425
    """
    ------------------------------------------------------ SERVER ErrorIDs
    ------------------------------------------------------ Server Internal error
    """
    ERR_DESERIALIZE_ERROR = 39426
    """Server Internal error in deserialize"""
    ERR_CMD_ID_OUT_OF_RANGE = 39427
    """Server CMD ID out of range 1.ACR_Length"""
    ERR_FRAGMENT_LENGTH_INVALID = 39428
    """Server Invalid fragment length"""
    ERR_CMD_PRIORITY_CHANGED = 39429
    """Server Command priority or type changed during runtime"""
    ERR_TRIED_TO_RESET_NONEMPTY_ACR_REGISTER = 39430
    """Server Tried to reset a non-empty ACR entry"""
    ERR_SEQUENCE_PAYLOAD_INVALID_LENGTH = 39431
    """
    Server Error: Invalid Sequence payload length (e.g., sequence payload length is specified 999
    even if telegram length is only 100.)
    """
    ERR_ACTION_BYTE_INVALID = 39432
    """Server Invalid ActionByte"""
    ERR_CMD_PAYLOAD_LENGTH_INVALID = 39433
    """Server Invalid Command payload length"""
    ERR_CMD_PAYLOAD_POINTER_INVALID = 39440
    """Server Error: Invalid Command payload pointer (e.g., Out of bounds)"""
    ERR_EXEC_MODE_CHANGE_ILLEGAL = 39444
    """Server Illegal Execution Mode change"""


_iec.register_enum(RobotLibraryErrorIdEnum, _iec.WORD)


class RobotLibraryInfoIdEnum(_iec.IecIntEnum):
    """RobotLibraryInfoIdEnum (WORD)"""
    NO_INFO = 0
    INFO_COLLISION_DETECTED = 27649
    """
    /7.5 Table "E" – Command InfoIDs If an info event related to the execution of a function block
    occurs, the function block returns an InfoID to specify the event. The info events are stored in
    the PLC message buffer and are displayed on the function block outputs. In the PLC message
    buffer, they are dynamically arranged by the client to be displayed as follows: <Origin>
    <MessageType> <Command name> <Description> More information about the general message handling
    mechanism can be found in 5.5.11 Diagnostics. The following table gives an overview over the
    existing InfoIDs reported by commands and the corresponding description. Server Collision
    detected Motion commands
    """
    INFO_MOTION_ERROR = 27650
    """
    Server Error occurred during motion. Check the message buffer for more information Motion
    commands
    """
    INFO_TARGET_POS_UNREACHABLE = 27651
    """Server Target position not reachable Motion commands"""
    INFO_SW_LIMITS_REACHED = 27652
    """Server Software limits reached Motion commands"""
    INFO_ABORT_BY_GROUP_STOP = 27653
    """Server Abortion of this command was requested by a GroupStop All sequence related commands"""
    INFO_ABORT_BY_MOTION_CMD = 27654
    """
    Server Abortion of this command was requested by another motion command All sequence related
    commands
    """
    INFO_READ_SW_LIMITS = 27655
    """
    Server Reading the currently used software limits. Updated software limits are active after
    restart. Command "ReadRobotSWLimits"
    """
    INFO_NO_ACTIVE_SUBPROGRAM = 27657
    """Server No SubProgram was stopped because none was active Command "StopSubprogram" """
    INFO_JOBID_NOT_RUNNING = 27665
    """
    Server A program for the supplied JobID is not running or does not exist. Command
    "StopSubprogram"
    """
    INFO_INSTANCEID_NOT_RUNNING = 27666
    """
    Server A program for the supplied InstanceID is not running or does not exist. Command
    "StopSubprogram"
    """
    INFO_WAITING_AT_BLEND_ZONE = 27667
    """Server The robot is waiting at the blending zone. Motion commands"""
    INFO_JOG_INTERRUPTED_BY_GROUP_STOP = 27668
    """Server Jog motion was interrupted by GroupStop Command "GroupJog" """
    INFO_JOG_INTERRUPTED_BY_RA_STATE = 27669
    """Server Jog motion was interrupted by RA sequence state INTERRUPTED Command "GroupJog" """
    INFO_MANUAL_START_IGNORED_DURING_EMPTY_SEQ = 27673
    """Server Manual start is ignored when the sequence is empty Command "EnableRobot" """
    INFO_PARAM_INDEX_ZERO_NOT_WRITEABLE = 27985
    """
    Server Invalid parameter value - A value was given for index 0. Index 0 is not writeable. Remove
    the value or change the index. Commands: "WriteIntegers", "WriteReals", "WriteAnalogOutputs",
    "ReadDigitalInputs", "ReadDigitalOutputs", "ReadIntegers", "ReadReals"
    """
    INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_NON_ZERO_INDEX = 27986
    """
    Server Invalid parameter value OutputBitmask - No bitmask was given for a non zero index. Set
    the index to zero, or set a valid bitmask. Command "WriteDigitalOutputs"
    """
    INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_ZERO_INDEX = 27987
    """
    Server Invalid parameter value OutputBitmask - A bitmask was given for a zero index. Set the
    bitmask to zero, or set a non zero index. Command "WriteDigitalOutputs"
    """
    INFO_CMD_INTERRUPTED_BY_RA_STATE = 28417
    """Server Command interrupted due to RA sequence state INTERRUPTED All sequence related commands"""
    INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED = 28418
    """Server Command interrupted due to RA power state NOT_ENABLED All sequence related commands"""
    INFO_CMD_INTERRUPTED_BY_RA_SEQ_STATE_DURING_STEP_MODE = 28419
    """
    Server Command interrupted due to RA sequence state INTERRUPTED while single step mode is active
    All sequence related commands
    """
    INFO_RESET_WARNINGS_BY_INTERNAL_CODE = 255
    """Server Internal code used to reset warnings All commands"""
    INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS = 24577
    """
    7.6 Table "F" – RI InfoIDs RI info events can occur on the PLC as well as on the RC. In the
    event of an RI info on the PLC, the corresponding InfoID is written to the PLC message buffer
    independent of the function call "ReadMessages". In the event of an RI info on the RC, the
    InfoID is transmitted via the function block "ReadMessages" and is also stored in PLC message
    buffer. In the PLC message buffer, they are dynamically arranged by the client to be displayed
    as follows: <Origin> <MessageType> <Description> More information about the general message
    handling mechanism can be found in 5.5.11 Diagnostics. The following table gives an overview
    over the existing InfoIDs reported via RI info events and the corresponding description. Client
    Lifesign smaller than lower limit. It has been increased to 10ms.
    """
    INFO_RECV_EXT_CART_POS_NOT_USABLE_WITH_RECV_CART_POS = 24578
    """
    Client ReceiveExtendedCartesianPosition cannot be used without ReceiveCartesianPos. RecCarPos is
    automatically activated.
    """
    INFO_RECV_EXT_JOINT_POS_NOT_USABLE_WITH_RECV_JOINT_POS = 24579
    """
    Client ReceiveExtendedJointPosition cannot be used without ReceiveJointPosition. RecJointPos is
    automatically activated.
    """
    INFO_SYNC_TOOL_DATA_DISABLED = 24596
    """
    Client Synchronization of tool data is disabled, and the data is different on the RC. Tool =
    "NUMBER" (Please Enter a valid SyncMode)
    """
    INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24597
    """Client Change the Syncmode to Negative only works on Startup with PLC (TOOL)"""
    INFO_SYNC_FRAME_DATA_DISABLED = 24608
    """
    Client Synchronization of frame data is disabled, and the data is different on the RC. Frame =
    "NUMBER" (Please Enter a valid SyncMode)
    """
    INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24609
    """Client Change the Syncmode to Negative only works on Startup with PLC (FRAME)"""
    INFO_SYNC_LOAD_DATA_DISABLED = 24614
    """
    Client Synchronization of load data is disabled, and the data is different on the RC. Load =
    "NUMBER" (Please Enter a valid SyncMode)
    """
    INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24615
    """Client Change the Syncmode to Negative only works on Startup with PLC (LOAD)"""
    INFO_SYNC_WORK_AREA_DISABLED = 24626
    """
    Client Synchronization of work area data is disabled, and the data is different on the RC.
    WorkArea = "NUMBER" (Please Enter a valid SyncMode)
    """
    INFO_CHANGE_WORK_AREA_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24627
    """Client Change the Syncmode to Negative only works on Startup with PLC (WORKAREA)"""
    INFO_SYNC_SWLIMIT_DISABLED = 24630
    """Client Synchronization of Software Limits data is disabled, and the data is different on the RC."""
    INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24631
    """Client Change the Syncmode to Negative only works on Startup with PLC (SW LIMITS)"""
    INFO_SYNC_DEFAULT_DYNAMICS_DISABLED = 24640
    """
    Client Synchronization of default dynamics data is disabled, and the data is different on the
    RC.
    """
    INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24641
    """Client Change the Syncmode to Negative only works on Startup with PLC (DEFAULT DYNAMICS)"""
    INFO_SYNC_REFERENCE_DYNAMICS_DISABLED = 24644
    """
    Client Synchronization of reference dynamics data is disabled, and the data is different on the
    RC.
    """
    INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 24645
    """Client Change the Syncmode to Negative only works on Startup with PLC (REFERENCE DYNAMICS)"""
    INFO_CONTINUOUS_UPDATE_NOT_POSSIBLE = 26192
    """
    Continuous updating of parameters relevant to the execution context (e.g. ProcessingMode,
    SequenceFlag) is not possible
    """
    INFO_CMD_BOUND_TO_INSTANCE_CONTINUOUS_MODE = 26193
    """
    ommand is bound to instance on RC while executed in continuous processing mode. Reexecution is
    not possible before deactivating
    """
    INFO_CMD_BOUND_TO_INSTANCE_TRIGGER_MODE = 26194
    """
    Command is bound to instance on RC while executed in trigger-based processing mode. Reexecution
    is not possible before deactivating
    """
    INFO_RA_DISABLED_BY_OPMODE_CHANGE = 27137
    """Server RA disabled due to operation mode change"""
    INFO_OPERATION_MODE_CHANGED = 27138
    """Server Operation mode changed"""
    INFO_SERVER_STATE_RESET_BY_CLIENT_REQUEST = 27139
    """Server The server state has been reset on client request. Client restart may be a cause."""
    INFO_OVERRIDE_DECREASED_TO_PREVENT_EXEEDING_MONITORING_VELOCITY = 27143
    """Server The actual override has been decreased to not exceed a movement's monitoring velocity."""
    INFO_EXCESSIVE_LOGGING = 27155
    """Server Excessive logging may degrade system performance."""
    INFO_FIRST_MOTION_REDUCED_VELOCITY = 27656
    """Server The first motion is executed with reduced velocity."""
    INFO_INTERNAL_ERROR_DURING_CMD = 36863
    """
    Server An RC internal error occurred during execution of this command. Check the message log for
    additional information
    """


_iec.register_enum(RobotLibraryInfoIdEnum, _iec.WORD)


class RobotLibraryWarningIdEnum(_iec.IecIntEnum):
    """RobotLibraryWarningIdEnum (WORD)"""
    NO_WARNING = 0
    WARN_HIGHPRIORITY_IGNORED_SEQ_MODE = 29441
    """
    7.3 Table "C" – Command WarningIDs If a warning related to the execution of a function block
    occurs, the function block returns a WarningID to specify the warning. The warnings are stored
    in the PLC message buffer and are displayed on the function block outputs. In the PLC message
    buffer, they are dynamically arranged by the client to be displayed as follows: <Origin>
    <MessageType> <Command name> <Description> More information about the general message handling
    mechanism can be found in 5.5.11 Diagnostics. The following table gives an overview over the
    existing WarningIDs reported by commands and the corresponding description. Client HighPriority
    Input is ignored when a sequential ProcessingMode is selected Commands: "WriteDigitalOutputs",
    "WriteIntegers", "WriteReals", "WriteAnalogOutputs"
    """
    WARN_CYCLIC_DATA_DISABLED_STILL_ACTIVE = 29443
    """
    Client Optional Cyclic data was disabled by the user but is still enabled until reinitialization
    of RobotTask Command: "ReadActualPositionCyclic"
    """
    WARN_ACR_FREE_ENTRIES_LOW = 30213
    """Client Number of free entries in the ACR is running out All commands"""
    WARN_PARAM_CHANGE_NOT_POSSIBLE_DEACTIVATE_FIRST_CTX = 30214
    """
    Change of parameters relevant to the execution context (e.g. ProcessingMode, SequenceFlag) is
    not possible. Deactivate first.
    """
    WARN_PARAM_CHANGE_NOT_POSSIBLE_DEACTIVATE_FIRST = 30215
    """Change of parameters is not possible. Deactivate first"""
    WARN_FRAME_USED_IN_SEQUENCE = 31747
    """Server The Frame is currently used in the sequence Command: "WriteFrameData" """
    WARN_TOOL_USED_IN_SEQUENCE = 31748
    """Server The Tool is currently used in the sequence Command: "WriteToolData" """
    WARN_LOAD_USED_IN_SEQUENCE = 31750
    """Server The Load is currently used in the sequence Command: "WriteLoadData" """
    WARN_HOLD_TO_RUN_REQUIRES_MOTION_IN_SEQUENCE = 31752
    """HoldToRun not possible. One motion command must be in the sequence when HoldToRun is activated"""
    WARN_TRIGGER_EVENT_WITHOUT_ASSOCIATED_ACTION = 31762
    """Trigger event was emitted but no associated Action exists for specified EmitterID"""
    WARN_TRIGGER_MODE2_NOT_SUPPORTED_FOR_ALL_MOVES = 31763
    """Trigger Mode 2 (Distance in mm) is not possible for all move commands (e.g. MoveAxes)"""
    WARN_MONITORING_DOES_NOT_APPLY_TO_BUFFERED_CMDS = 31764
    """
    Server The monitoring does not apply to motion CMDs which are already buffered. Command:
    "SetTriggerMotion"
    """
    WARN_SAFE_REFERENCING_VELOCITY_REDUCED = 31765
    """Motion velocity is reduced as Safe Referencing is required."""
    WARN_SAFE_REFERENCING_ADDITIONAL_STEPS_REQUIRED = 31766
    """
    Additional steps are required to complete the SafeReferencing. Check the MessageLog for further
    information.
    """
    WARN_ACYCLIC_RANGE_PLC_TO_ROB_VERY_SMALL = 28673
    """
    7.4 Table "D" – RI WarningIDs RI warnings can occur on the PLC as well as on the RC. In the
    event of an RI warning on the PLC, the corresponding WarningID is written to the PLC message
    buffer independent of the function call "ReadMessages". In the event of an RI warning on the RC,
    the WarningID is transmitted via the function block "ReadMessages" and is also stored in PLC
    message buffer. In the PLC message buffer, they are dynamically arranged by the client to be
    displayed as follows: <Origin> <MessageType> <Description> More information about the general
    message handling mechanism can be found in 5.5.11 Diagnostics. The following table gives an
    overview over the existing WarningIDs reported via RI warnings and the corresponding
    description. Client Acyclic range client to server very small
    """
    WARN_ACYCLIC_RANGE_ROB_TO_PLC_VERY_SMALL = 28674
    """Client Acyclic range server to client very small"""
    WARN_TELEGRAM_NO_CHANGED_DURING_OPERATION = 28675
    """Client Telegram number was changed during operation"""
    WARN_SAVE_TOOL_FAILED = 28677
    """Client Save Tool locally failed. Index not available in user data."""
    WARN_SAVE_FRAME_FAILED = 28678
    """Client Save Frame locally failed. Index not available in user data."""
    WARN_SAVE_LOAD_FAILED = 28679
    """Client Save Load locally failed. Index not available in user data."""
    WARN_SAVE_WORKAREA_FAILED = 28680
    """Client Save WorkArea locally failed. Index not available in user data."""
    WARN_TOOL_DATA_ARRAY_NOT_START_AT_ZERO = 28681
    """Client Array of tool data supplied to RobotTask does not start at 0."""
    WARN_TOOL_DATA_ARRAY_TOO_SHORT = 28688
    """
    Client Array of tool data supplied to RobotTask must be longer than the number of tools on the
    RC.
    """
    WARN_TOOL_DATA_SYNC_MODE_INVALID = 28689
    """Client Tool data sync mode is invalid."""
    WARN_TOOL_NUMBER_SYNC_ERROR = 28690
    """Client Error Sync with Tool "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_TOOL_SYNC_BOTH_SIDES_CHANGED = 28691
    """Client Error Sync Data changed in both Sides with Tool "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO = 28693
    """Client Array of frame data supplied to RobotTask does not start at 0."""
    WARN_FRAME_DATA_ARRAY_TOO_SHORT = 28694
    """
    Client Array of frame data supplied to RobotTask must be longer than the number of frames on the
    RC.
    """
    WARN_FRAME_DATA_SYNC_MODE_INVALID = 28695
    """Client Frame data sync mode is invalid."""
    WARN_FRAME_NUMBER_SYNC_ERROR = 28696
    """Client Error Sync with Frame "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_FRAME_SYNC_BOTH_SIDES_CHANGED = 28697
    """Client Error Sync Data changed in both Sides with Frame "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_LOAD_DATA_ARRAY_NOT_START_AT_ZERO = 28705
    """Client Array of load data supplied to RobotTask does not start at 0."""
    WARN_LOAD_DATA_ARRAY_TOO_SHORT = 28706
    """
    Client Array of load data supplied to RobotTask must be longer than the number of tools on the
    RC.
    """
    WARN_LOAD_DATA_SYNC_MODE_INVALID = 28707
    """Client Load data sync mode is invalid."""
    WARN_LOAD_NUMBER_SYNC_ERROR = 28708
    """Client Error Sync with Load "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_LOAD_SYNC_BOTH_SIDES_CHANGED = 28709
    """Client Error Sync Data changed in both Sides with Load "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_WORK_AREA_ARRAY_NOT_START_AT_ZERO = 28711
    """Client Array of workarea data supplied to RobotTask does not start at 0."""
    WARN_WORK_AREA_ARRAY_TOO_SHORT = 28712
    """
    Client Array of workarea data supplied to RobotTask must be longer than the number of tools on
    the RC.
    """
    WARN_WORK_AREA_SYNC_MODE_INVALID = 28713
    """Client Workarea data sync mode is invalid."""
    WARN_WORK_AREA_NUMBER_SYNC_ERROR = 28720
    """Client Error Sync with WorkArea "NUMBER" (Please Enter a valid SyncMode)"""
    WARN_WORK_AREA_SYNC_BOTH_SIDES_CHANGED = 28721
    """
    Client Error Sync Data changed in both Sides with WorkArea "NUMBER" (Please Enter a valid
    SyncMode)
    """
    WARN_SW_LIMITS_SYNC_MODE_INVALID = 28723
    """Client Software limits data sync mode is invalid."""
    WARN_SW_LIMITS_SYNC_ERROR = 28724
    """Client Error Sync with Software Limits (Please Enter a valid SyncMode)"""
    WARN_SW_LIMITS_SYNC_BOTH_SIDES_CHANGED = 28725
    """
    Client Error Sync Data changed in both Sides with Software Limits (Please Enter a valid
    SyncMode)
    """
    WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID = 28727
    """Client Default dynamics data sync mode is invalid."""
    WARN_DEFAULT_DYNAMICS_SYNC_ERROR = 28728
    """Client Error Sync with Default Dynamics (Please Enter a valid SyncMode)"""
    WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED = 28729
    """
    Client Error Sync Data changed in both Sides with Default Dynamics (Please Enter a valid
    SyncMode)
    """
    WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID = 28737
    """Client Reference dynamics data sync mode is invalid."""
    WARN_REFERENCE_DYNAMICS_SYNC_ERROR = 28738
    """Client Error Sync with Reference Dynamics (Please Enter a valid SyncMode)"""
    WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED = 28739
    """
    Client Error Sync Data changed in both Sides with Reference Dynamics (Please Enter a valid
    SyncMode)
    """
    WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28740
    """
    Client Synchronization of tool is not possible due to error in the read or write tool cmd. See
    dedicated message log entry for more information.
    """
    WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28741
    """
    Client Synchronization of frame is not possible due to error in the read or write frame cmd. See
    dedicated message log entry for more information.
    """
    WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28742
    """
    Client Synchronization of load is not possible due to error in the read or write load cmd. See
    dedicated message log entry for more information.
    """
    WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28743
    """
    Client Synchronization of swLimits is not possible due to error in the read or write swLimits
    cmd. See dedicated message log entry for more information.
    """
    WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28744
    """
    Client Synchronization of referenceDynamics is not possible due to error in the read or write
    referenceDynamics cmd. See dedicated message log entry for more information.
    """
    WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28745
    """
    Client Synchronization of defaultDynamics is not possible due to error in the read or write
    defaultDynamics cmd. See dedicated message log entry for more information.
    """
    WARN_LEGACY_SRCI_ENCODING = 28752
    """
    Client Using the legacy SRCI version encoding. It will not be compatible with the newest RC
    interpreter versions.
    """
    WARN_INVALID_ROBOT_STATE_MULTIPLE_CMDS_ACTIVE = 28753
    """Invalid state of the robot (more than 1 CMD active)"""
    WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 28754
    """
    Client Synchronization of workarea is not possible due to error in the read or write load cmd.
    See dedicated message log entry for more information.
    """
    WARN_ACR_ALMOST_FULL = 31233
    """
    Server The ACR is almost full. Filling it completely disables the robot. Make sure to limit the
    number of commands in the system.
    """


_iec.register_enum(RobotLibraryWarningIdEnum, _iec.WORD)


class SequenceFlag(_iec.IecIntEnum):
    """SequenceFlag (USINT)"""
    NO_SEQUENCE = 0
    """
    • Refers to ProcessingModes 2 to 5 and 9 (2 = Parallel, 3 = Continuous, 4 = not available, 5 =
    Trigger Multiple, 9 = Deactivate ) • Command is not handled by any sequence • For more
    information on ProcessingModes refer to chapter 5.6.4.5
    """
    PRIMARY_SEQUENCE = 1
    """• Command will be handled by primary sequence"""
    SECONDARY_SEQUENCE = 2
    """• Command will be handled by secondary sequence"""


_iec.register_enum(SequenceFlag, _iec.USINT)


class MessageLevel(_iec.IecIntEnum):
    """MessageLevel (USINT)"""
    DEBUG = 4
    """Debugging messages, Informative messages, Warning messages, Error messages, Fatal error messages"""
    INFO = 5
    """Informative messages, Warning messages, Error messages, Fatal error messages"""
    WARNING = 20
    """Warning messages, Error messages, Fatal error messages"""
    ERROR = 28
    """Error messages, Fatal error messages"""


_iec.register_enum(MessageLevel, _iec.USINT)


class PriorityLevel(_iec.IecIntEnum):
    """PriorityLevel (BYTE)"""
    VERY_HIGH = 1
    """priority level is very high"""
    HIGH = 2
    """priority level is high"""
    NORMAL = 3
    """priority level is normal"""
    LOW = 4
    """priority level is low"""


_iec.register_enum(PriorityLevel, _iec.BYTE)


class AxisUnit(_iec.IecIntEnum):
    """AxisUnit (USINT)"""
    DEG = 0
    """Axis unit is in degree [°]"""
    MM = 1
    """Axis unit is in milli meter [mm]"""


_iec.register_enum(AxisUnit, _iec.USINT)


class CircPlane(_iec.IecIntEnum):
    """CircPlane (SINT)"""
    XZ_PLANE = 0
    """x-z-plane"""
    YZ_PLANE = 1
    """y-z-plane"""
    XY_PLANE = 2
    """x-y-plane"""


_iec.register_enum(CircPlane, _iec.SINT)


class ComDirection(_iec.IecIntEnum):
    """ComDirection (INT)"""
    PLC_TO_ROB = 0
    """communication direction PLC to Robot"""
    ROB_TO_PLC = 1
    """communication direction Robot to PLC"""


_iec.register_enum(ComDirection, _iec.INT)


class ControlHalfByte(_iec.IecIntEnum):
    """ControlHalfByte (BYTE)"""
    NONE = 0
    """Default value, no control active"""
    INITIALIZE = 1
    """Initialization is requested by the client"""
    RESUME = 2
    """Resume of operation is requested by the client"""
    RESET = 3
    """
    Resetting of the RC is requested by the client. The RC must stop the motion, and clear all
    state.
    """
    ACK_ERROR = 4
    """Acknowledgement of a telegram state error"""
    CLIENT_ERROR = 5
    """
    Signaling that a client error occurred. The Server must respond by setting its RI state to
    NOT_INITIALIZED
    """


_iec.register_enum(ControlHalfByte, _iec.BYTE)


class ErrorReaction(_iec.IecIntEnum):
    """ErrorReaction (USINT)"""
    ABORT_AND_MOVE = 0
    """
    Abort and move Abort active move command and delete commands buffered in sequence Move robot by
    specified ErrorVector
    """
    ABORT = 1
    """
    1: Abort Abort active move command and delete commands buffered in sequence No additional
    movements
    """
    NO_REACTION = 2
    """2: No reaction Error event is ignored by active move command"""


_iec.register_enum(ErrorReaction, _iec.USINT)


class LoadMeasurementSteps(_iec.IecIntEnum):
    """LoadMeasurementSteps (USINT)"""
    RESET = 0
    """• 0: Reset (default) Delete all positions saved on the RC"""
    FIRST_POSITION = 1
    """• 1: First position Save the first position for the load estimation with the required data"""
    SECOND_POSITION = 2
    """• 2: Second position Save the second position for the load estimation with the required data"""
    THIRD_POSITION = 3
    """• 3: Third position Save the third position for the load estimation with the required data"""
    FOURTH_POSITION = 4
    """• 4: Fourth position Save the fourth position for the load estimation with the required data"""
    LOAD_CALCULATION = 99
    """• 99: Load calculation Start the load calculation with the data saved in the four positions"""


_iec.register_enum(LoadMeasurementSteps, _iec.USINT)


class PathChoice(_iec.IecIntEnum):
    """PathChoice (BYTE)"""
    CLOCKWISE = 0
    """Clockwise movement of the circular path"""
    COUNTERCLOCKWISE = 1
    """Counterclockwise movement of the circular path"""


_iec.register_enum(PathChoice, _iec.BYTE)


class ReferenceElement(_iec.IecIntEnum):
    """ReferenceElement (USINT)"""
    NOT_USED = 0
    """0 (default): Not used"""
    X_AXIS = 1
    """1: X-Axis"""
    Y_AXIS = 2
    """2: Y-Axis"""
    Z_AXIS = 3
    """3: Z-Axis"""
    XY_PLANE = 4
    """4: XY-Plane"""
    XZ_PLANE = 5
    """5: XZ-Plane"""
    YZ_PLANE = 6
    """6: YZ-Plane"""


_iec.register_enum(ReferenceElement, _iec.USINT)


class Severity(_iec.IecIntEnum):
    """Severity (SINT)"""
    DEACTIVATE = 0
    """No events will be logged"""
    DEBUG = 4
    """Debug message • No user action required"""
    INFO = 5
    """Informative message • No user action required"""
    WARNING = 20
    """Warning message • User action will be required at some point"""
    ERROR = 28
    """Error message • User action required immediately"""
    FATAL_ERROR = 29
    """Fatal error message • User action required immediately • Reinitialization OF RI required"""


_iec.register_enum(Severity, _iec.SINT)


class SyncDirection(_iec.IecIntEnum):
    """SyncDirection (INT)"""
    NO_SYNC = 0
    """No synchronization will be executed"""
    PLC_TO_ROB = 1
    """Server data will be overwritten immediately by client data"""
    ROB_TO_PLC = 2
    """Client data will be overwritten immediately by server data"""
    AUTOMATIC = 3
    """Server or client data will be overwritten immediately by changed data"""


_iec.register_enum(SyncDirection, _iec.INT)


class SyncReaction(_iec.IecIntEnum):
    """SyncReaction (USINT)"""
    NO_REACTION = 0
    """• System behavior unaffected"""
    NO_AUTOMATIC_DISABLE = 1
    """
    • No automatic disable • Reaction will only apply when RA is disabled • RA can only be enabled
    if client and server are synchronized
    """
    INTERRUPT_WHEN_SEQUENCE_IS_EMPTY = 2
    """
    • No automatic disable • RA can only be enabled if client and server are synchronized • RA
    sequence state will change to interrupted when no command is buffered in the active sequence •
    Continuation is only possible if client and server are synchronized
    """
    IMMEDIATE_INTERRUPT = 3
    """
    • No automatic disable • RA can only be enabled if client and server are synchronized • RA
    sequence state will change to interrupted • Continuation is only possible if client and server
    are synchronized
    """


_iec.register_enum(SyncReaction, _iec.USINT)


class SyncTime(_iec.IecIntEnum):
    """SyncTime (DINT)"""
    DURING_START_UP = 0
    """Synchronization during startup"""
    AFTER_START_UP = 1
    """Synchronization after startup"""


_iec.register_enum(SyncTime, _iec.DINT)


class TriggerCondition(_iec.IecIntEnum):
    """TriggerCondition (SINT)"""
    TARGET_POSITION_TIME_MS = -5
    """5: Time in ms - point reference is target position"""
    TARGET_POSITION_TCP_VELOCITY_ABSOLUTE = -4
    """4: TCP velocity in mm/s - point reference is target position"""
    TARGET_POSITION_TCP_VELOCITY_PERCENT = -3
    """3: TCP velocity in % of reference velocity - point reference is target position"""
    TARGET_POSITION_DISTANCE_ABSOLUTE = -2
    """2: Distance in mm of trajectory - point reference is target position"""
    TARGET_POSITION_DISTANCE_PERCENT = -1
    """1: Distance in % of trajectory - point reference is target position"""
    UNDEFINED = 0
    """0: Undfined"""
    START_POSITION_DISTANCE_PERCENT = 1
    """1: Distance in % of trajectory - point reference is start position"""
    START_POSITION_DISTANCE_ABSOLUTE = 2
    """2: Distance in mm of trajectory - point reference is start position"""
    START_POSITION_TCP_VELOCITY_PERCENT = 3
    """3: TCP velocity in % of reference velocity - point reference is start position"""
    START_POSITION_TCP_VELOCIT_ABSOLUTE = 4
    """4: TCP velocity in mm/s - point reference is start position"""
    START_POSITION_TIME_MS = 5
    """5: Time in ms - point reference is start position"""


_iec.register_enum(TriggerCondition, _iec.SINT)


class UnitLimitAxis(_iec.IecIntEnum):
    """UnitLimitAxis (USINT)"""
    PERCENTAGE = 0
    """Percentage (%) (default)"""
    NEWTONMETER = 1
    """Newton meter (Nm)"""
    MILLIAMPERE = 2
    """Milliampere (mA)"""


_iec.register_enum(UnitLimitAxis, _iec.USINT)


class AbortingMode(_iec.IecIntEnum):
    """AbortingMode (SINT)"""
    BUFFER = 0
    """
    The current movement command as well as all stored movements are executed as programmed. The new
    motion command is queued in the motion buffer.
    """
    ABORT = 1
    """
    The current movement command is aborted. All buffered motion movements are discarded. The new
    target position is approached, depending on the motion command.
    """


_iec.register_enum(AbortingMode, _iec.SINT)


class BlendingMode(_iec.IecIntEnum):
    """BlendingMode (USINT)"""
    EXACT_STOP = 0
    """Appended, buffered, no blending"""
    DEFINED_VELOCITY = 2
    """Start blending when the defined velocity is reached"""
    CORNER_DISTANCE = 3
    """Define blending sphere with radius"""
    MAX_CORNER_DEVIATION = 4
    """Define blending with deviation"""
    CORNER_DISTANCE_2R = 10
    """Define blending sphere with 2 radiuses"""
    RAMP_OVERLAP = 11
    """Define blending with percentage of overlapping of deceleration and acceleration ramp"""
    CORNER_DISTANCE_1R = 12
    """Define blending sphere with starting radius"""


_iec.register_enum(BlendingMode, _iec.USINT)


class CircMode(_iec.IecIntEnum):
    """CircMode (SINT)"""
    BORDER = 0
    """"AuxPoint" defines a point on the circle crossed on the path from the starting to the end point."""
    CENTER = 1
    """"AuxPoint" defines the center point of the circle."""
    CENTER_WITH_ANGLE = 2
    """
    "AuxPoint" defines the center point of the circle, "Angle" defines the end position of the
    circular motion, and "CircPlane" defines the circle’s plane.
    """
    RADIUS = 3
    """
    "AuxPoint" defines a vector which length is the radius of the circle. The plane of the circle is
    defined by the rule of right thumb while the "AuxPoint" defines the spearhead point of the
    perpendicular.
    """


_iec.register_enum(CircMode, _iec.SINT)


class CollisionReactionMode(_iec.IecIntEnum):
    """CollisionReactionMode (USINT)"""
    STANDING_STILL = 0
    """Standing still"""
    REVERSED_MOVEMENT = 1
    """Reversed movement"""


_iec.register_enum(CollisionReactionMode, _iec.USINT)


class ConnectionMode(_iec.IecIntEnum):
    """ConnectionMode (SINT)"""
    RC_CONNECTED = 0
    """Encoder is connected to RC"""
    PLC_CONNECTED = 1
    """Encoder is connected to PLC"""


_iec.register_enum(ConnectionMode, _iec.SINT)


class DefinitionMode(_iec.IecIntEnum):
    """DefinitionMode (USINT)"""
    Center = 1
    """ZeroPoint describes center point of body"""
    Face = 2
    """ZeroPoint describes point on face of body. Parameter values for X2, Y2, Z2 will be ignored"""


_iec.register_enum(DefinitionMode, _iec.USINT)


class DetectionMode(_iec.IecIntEnum):
    """DetectionMode (USINT)"""
    TORQUE = 0
    """Torque (default)"""
    FORCE = 1
    """Force"""
    ELECTRICAL_CURRENT = 2
    """Electrical current"""
    FOLLOWING_ERROR = 3
    """Following Error"""


_iec.register_enum(DetectionMode, _iec.USINT)


class ErrorTriggerMode(_iec.IecIntEnum):
    """ErrorTriggerMode (SINT)"""
    ANY_COMMAND = 0
    """Any command (default)"""
    GENERAL_COMMANDS = 1
    """General commands"""
    ADMINISTRATIVE_COMMANDS = 2
    """Administrative commands"""
    MOVE_COMMANDS = 3
    """Move commands"""
    PERIPHERY_COMMANDS = 4
    """Periphery commands"""
    EXTENDED_COMMANDS = 5
    """Extended commands"""
    SPECIFIC_COMMAND_OR_RI_MESSAGE = 6
    """Specific command or RI message"""
    SPECIFIC_RC_OR_RA_MESSAGE_CODE = 7
    """Specific RC or RA message code"""
    ANY_RI_MESSAGE_CODE = 8
    """Any RI message code"""
    ANY_RC_OR_RA_MESSAGE_CODE = 9
    """Any RC or RA message code"""


_iec.register_enum(ErrorTriggerMode, _iec.SINT)


class ExecutionMode(_iec.IecIntEnum):
    """ExecutionMode (USINT)"""
    SEQUENCE_PRIMARY = 0
    """Command is buffered in sequence buffer and executed once"""
    SEQUENCE_ABORT_OTHERS_PRIMARY = 1
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer,
    and is executed once
    """
    PARALLEL = 2
    """
    Command is buffered in parallel buffer and executed once. The execution may also be Trigger
    based.
    """
    CONTINUOUS = 3
    """
    Command is buffered in parallel buffer and executed repeatedly until deliberate deactivation by
    user. The de- and activation may also be Trigger based.
    """
    TRIGGER_MULTIPLE = 5
    """
    Command is buffered and executed once when triggered. The CMD remains in the buffer until
    removed by the user.
    """
    SEQUENCE_SECONDARY = 7
    """Command is buffered in sequence buffer and executed once (Secondary)"""
    SEQUENCE_ABORT_OTHERS_SECONDARY = 8
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer
    and is executed once (Secondary)
    """
    STOP_PARALLEL_CONTINUOUS_TRIGGER = 9
    """CMD execution is stopped and/or CMD is removed from the buffer."""


_iec.register_enum(ExecutionMode, _iec.USINT)


class FrameCalculationMode(_iec.IecIntEnum):
    """FrameCalculationMode (SINT)"""
    THREE_POINT_METHOD = 0
    """0: Three-Point-method (default)"""
    FOUR_POINT_METHOD = 1
    """1: Four-Point-method"""
    ONE_POINT_METHOD = 2
    """2: One-Point-method"""


_iec.register_enum(FrameCalculationMode, _iec.SINT)


class FunctionMode(_iec.IecIntEnum):
    """FunctionMode (INT)"""
    enum_member = 0


_iec.register_enum(FunctionMode, _iec.INT)


class InterpolationMode(_iec.IecIntEnum):
    """InterpolationMode (USINT)"""
    Linear_interpolation = 0
    """Linear interpolation"""
    Direct_interpolation = 1
    """Direct interpolation (PTP)"""


_iec.register_enum(InterpolationMode, _iec.USINT)


class JogMode(_iec.IecIntEnum):
    """JogMode (USINT)"""
    JOG_FRAME = 0
    """
    • Jog TCP manually in the given frame (WCS/UCS) • Movement on several coordinate axes
    simultaneously possible
    """
    JOG_TOOL = 1
    """
    • Jog TCP manually in the given tool coordinate system • Movement on several coordinate axes
    simultaneously possible
    """
    JOG_AXES = 2
    """
    • Jog joints manually without referring to a given frame or tool • Movement of several axes
    simultaneously possible.
    """


_iec.register_enum(JogMode, _iec.USINT)


class LimitMode(_iec.IecIntEnum):
    """LimitMode (USINT)"""
    NO_LIMIT_DEFINED = 0
    """
    0: No limit defined (default) The robot can be moved in the direction set with the input
    parameter "CompliantAxes" in a compliant manner by applying an external force on it. By reaching
    the mechanical or software limits, the robot stops.
    """
    LIMIT_DEFINED = 1
    """
    1: Limit defined The robot can be moved along the defined vector in a compliant manner by
    applying an external force on it. By reaching the vector limit defined by the input parameter
    "VectorData", the robot stops.
    """


_iec.register_enum(LimitMode, _iec.USINT)


class LoadMeasurementMode(_iec.IecIntEnum):
    """LoadMeasurementMode (USINT)"""
    ONE_POSITION = 0
    """0: One Position (default) Use one defined position and optional axes ranges"""
    CONFIGURATION_ANGLE = 1
    """1: Configuration Angle Use one defined position and optional axes ranges"""
    AREA = 2
    """2: Area Use a defined area for the measurement"""
    TWO_POSITIONS = 3
    """3: Two Positions Use defined positions for the measurement"""


_iec.register_enum(LoadMeasurementMode, _iec.USINT)


class LogonMode(_iec.IecIntEnum):
    """LogonMode (SINT)"""
    PASSWORD_ONLY = 0
    """Password only (default)"""
    USERNAME_AND_PASSWORD = 1
    """Username and Password"""
    LEVEL_ID_AND_PASSWORD = 2
    """Level ID and Password"""


_iec.register_enum(LogonMode, _iec.SINT)


class MeasuringIoMode(_iec.IecIntEnum):
    """MeasuringIoMode (USINT)"""
    MEASUREMENT_AT_NEXT_RISING_EDGE = 0
    """Measurement at next rising edge • Output "MeasuredPosition_1" used"""
    MEASUREMENT_AT_NEXT_FALLING_EDGE = 1
    """Measurement at next falling edge • Output "MeasuredPosition_1" used"""
    MEASUREMENT_AT_NEXT_EDGE = 2
    """
    Measurement at next edges, regardless of rising or falling edges. • First position stored in
    output "MeasuredPosition_1" • Second position stored in output "MeasuredPosition_2"
    """
    MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_RISING = 3
    """
    Measurement at two edges, beginning with the rising edge: • Rising edge = "MeasuredPosition_1 "
    • Falling edge = "MeasuredPosition_2 "
    """
    MEASUREMENT_AT_TWO_EDGES_BEGIN_WITH_FALLING = 4
    """
    Measurement at two edges, beginning with the falling edge: • Falling edge = " MeasuredPosition_1
    " • Rising edge = "MeasuredPosition_2 "
    """


_iec.register_enum(MeasuringIoMode, _iec.USINT)


class MeasuringUnitMode(_iec.IecIntEnum):
    """MeasuringUnitMode (USINT)"""
    VECTOR_LENGTH = 0
    """
    0: VectorLength (default) Defines the distance in millimeter between two points in cartesian
    space.
    """
    SEGMENT_LENGTH = 1
    """1: SegmentLength Defines the distance in mm covered between the two points in cartesian space"""
    TIME_DURATION = 2
    """2: Time Defines the duration in milliseconds between the start and end point."""


_iec.register_enum(MeasuringUnitMode, _iec.USINT)


class OperationMode(_iec.IecIntEnum):
    """OperationMode (USINT)"""
    T1_LOCAL = 1
    """
    Test mode 1: • Maximum velocity of TCP is restricted to <250 mm/s • Robot can only be moved
    while enable switch is active • Designed for jogging, teaching program, verification • Safety
    door can be opened
    """
    T2_LOCAL = 2
    """
    Test mode 2: • Maximum velocity of TCP not restricted (100%) • Robot can only be moved while
    enable switch is active • Designed for program verification (step mode) • Safety door can be
    opened
    """
    AUTO = 3
    """
    Automatic mode: • Maximum velocity of TCP not restricted (100%) • Robot is executing user
    program automatically • Robot will stop if safety devices report error (e.g. safety door must be
    closed)
    """
    AUTO_EXT = 4
    """
    External Automatic mode (PLC mode) • Robot is operated remotely only • Maximum velocity of TCP
    not restricted (100%) • Robot is executing user program automatically • Jogging possible • Robot
    will stop if safety devices report error (e.g. safety door must be closed)
    """
    T1_EXT = 5
    """
    External Test mode 1 (PLC mode with T1 functionality) • Robot is operated remotely only •
    Maximum velocity of TCP is restricted to <250 mm/s • Robot can only be moved while enable switch
    is active • Designed for jogging, teaching, program verification • Safety door can be opened
    """
    T2_EXT = 6
    """
    External Test mode 2: • Robot is operated remotely only • Maximum velocity of TCP not restricted
    (100%) • Robot can only be moved while enable switch is active • Designed for jogging, program
    verification (step mode) • Safety door can be opened
    """


_iec.register_enum(OperationMode, _iec.USINT)


class OrientationMode(_iec.IecIntEnum):
    """OrientationMode (SINT)"""
    LINEAR_INTERPOLATED = 1
    """Change orientation continuously in a linear way"""
    JOINT_INTERPOLATED = 2
    """Change orientation continuously in a joint interpolated way of wrist joints"""
    FIX = 3
    """No change of orientation during movement"""
    PATH = 4
    """No change of orientation in relation to trajectory"""


_iec.register_enum(OrientationMode, _iec.SINT)


class OriMode(_iec.IecIntEnum):
    """OriMode (USINT)"""
    LINEAR_INTERPOLATED = 1
    """Change orientation continuously in a linear way"""
    JOINT_INTERPOLATED = 2
    """Change orientation continuously in a joint interpolated way."""
    FIX = 3
    """No change of orientation during movement"""
    PATH = 4
    """No change of orientation in relation to trajectory"""


_iec.register_enum(OriMode, _iec.USINT)


class ProcessingMode(_iec.IecIntEnum):
    """ProcessingMode (USINT)"""
    BUFFERED = 0
    """Command is buffered in sequence buffer and executed once"""
    ABORTING = 1
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer,
    and is executed once
    """
    PARALLEL = 2
    """Command is buffered in parallel buffer and executed once"""
    CONTINUOUS = 3
    """
    Command is buffered in parallel buffer and executed repeatedly until deliberate deactivation by
    user
    """
    DEACTIVATE = 9
    """CMD execution is stopped and/or CMD is removed from the buffer"""
    TRIGGER_BUFFERED = 10
    """Command is buffered in sequence buffer and executed once (Trigger based)"""
    TRIGGER_ABORTING = 11
    """
    Command is buffered in sequence buffer, aborts and empties previous commands in sequence buffer,
    and is executed once (Trigger based)
    """
    TRIGGER_ONCE = 12
    """Command is buffered in parallel buffer and executed once (Trigger based)"""
    TRIGGER_CONTINUOUS = 13
    """
    Command is buffered in parallel buffer and executed repeatedly until deliberate deactivation by
    user (Trigger based)
    """
    TRIGGER_MULTIPLE = 14
    """
    Command is buffered and executed multiple times when triggered. The CMD remains in the buffer
    until removed by the user.
    """


_iec.register_enum(ProcessingMode, _iec.USINT)


class ResistanceForceMode(_iec.IecIntEnum):
    """ResistanceForceMode (USINT)"""
    RESISTANCE_FORCE_TCP = 0
    """
    0 (default): ResistanceForceTCP. Set "0" to set the resistance of the RA against the external
    force at the TCP.
    """
    RESISTANCE_FORCE_AXIS = 1
    """
    1: ResistanceForceAxis. Set "1" to set the resistance of the RA against the external force for
    each axis independently.
    """


_iec.register_enum(ResistanceForceMode, _iec.USINT)


class ReturnMode(_iec.IecIntEnum):
    """ReturnMode (BYTE)"""
    INTERRUPT_POSITION = 0
    """Interrupt position"""
    END_POSITION = 1
    """End position"""


_iec.register_enum(ReturnMode, _iec.BYTE)


class SensorConnectionMode(_iec.IecIntEnum):
    """SensorConnectionMode (USINT)"""
    RC_SENSOR_ALGORITHM = 0
    """RC sensor and algorithm Force-Torque-Sensor connected to RC Control algorithm in RC"""
    PLC_SENSOR_RC_ALGORITHM = 1
    """PLC sensor and RC algorithm Force-Torque-Sensor connected to PLC Control algorithm in RC"""
    PLC_SENSOR_ALGORITHM = 2
    """PLC sensor and algorithm Force-Torque-Sensor connected to PLC Control algorithm in PLC"""


_iec.register_enum(SensorConnectionMode, _iec.USINT)


class SingularityAvoidanceMode(_iec.IecIntEnum):
    """SingularityAvoidanceMode (USINT)"""
    NO_CHANGE = 0
    """
    0: NoChange (default) Allow movement of one or more joints to avoid singularities without a
    change of the orientation
    """
    LOCK_J4 = 1
    """1: Lock J4 Lock the 4th joint to avoid singularities"""
    TOOL_ORIENTATION = 2
    """2: ToolOrientation Allow a small movement of the tool orientation to avoid singularities"""


_iec.register_enum(SingularityAvoidanceMode, _iec.USINT)


class SplineMode(_iec.IecIntEnum):
    """SplineMode (UINT)"""
    DISCRETE_POINTS = 0
    """0: Discrete Points"""
    BEZIER_SPLINE = 1
    """1: Bézier Spline"""
    B_SPLINES = 2
    """2: B-Splines"""
    CUBIC_HERMITE_SPLINE = 3
    """3: Cubic Hermite Spline"""
    C_SPLINES = 4
    """4: C-Splines"""


_iec.register_enum(SplineMode, _iec.UINT)


class StepMode(_iec.IecIntEnum):
    """StepMode (USINT)"""
    DEACTIVATE = 0
    """StepMode is deactivated"""
    BLENDING = 1
    """
    Blending • The robot moves on the blended trajectory • The movement is interrupted when the
    active segment changes
    """
    EXACT_STOP = 2
    """
    Exact stop • The robot moves to the defined target positions without blending • The movement is
    interrupted when the defined target position is reached
    """


_iec.register_enum(StepMode, _iec.USINT)


class StopMode(_iec.IecIntEnum):
    """StopMode (USINT)"""
    STOP_JOB_ID = 0
    """
    0: Stop via JobID (default) TargetID is interpreted as JobID All instances of the defined JobID
    are stopped
    """
    STOP_INSTANCE_ID = 1
    """
    1: Stop via InstanceID TargetID is interpreted as InstanceID The instance of the defined
    InstanceID is stopped
    """
    STOP_ALL_SUBPROGRAMS = 2
    """
    2: Stop all subprograms All subprograms independent of the input parameter value of TargetID are
    stopped
    """


_iec.register_enum(StopMode, _iec.USINT)


class SyncInMode(_iec.IecIntEnum):
    """SyncInMode (USINT)"""
    IN_SYNC_IN_ZONE = 0
    """
    • When work piece enters "SyncInZone" • Start synchronization as soon as possible within defined
    acceleration and velocity limits
    """
    AFTER_DISTANCE = 1
    """• Start synchronization after specific distance after execution • "SynInZone" ignored"""
    AFTER_TIME = 2
    """• Start synchronization after specific time after execution • "SynInZone" ignored"""
    IMMEDIATELY = 3
    """• As soon as possible within defined acceleration and velocity limits • "SynInZone" ignored"""


_iec.register_enum(SyncInMode, _iec.USINT)


class SyncMode(_iec.IecIntEnum):
    """SyncMode (USINT)"""
    NO_SYNCHRONIZATION = 0
    """No synchronization will be executed"""
    CLIENT_TO_SERVER = 1
    """Server data will be overwritten immediately by client data"""
    SERVER_TO_CLIENT = 2
    """Client data will be overwritten immediately by server data"""
    AUTOMATIC = 3
    """Server or client data will be overwritten immediately by changed data"""


_iec.register_enum(SyncMode, _iec.USINT)


class ThresholdMode(_iec.IecIntEnum):
    """ThresholdMode (USINT)"""
    AUTOMATIC = 0
    """Automatic."""
    MANUAL = 1
    """Manual (according to LimitAxis)"""


_iec.register_enum(ThresholdMode, _iec.USINT)


class ToolCalculationMode(_iec.IecIntEnum):
    """ToolCalculationMode (SINT)"""
    TWO_POINT_Z_METHOD = 0
    """0: Two Point + Z-Method (default)"""
    THREE_POINT_METHOD = 1
    """1: Three-Point-Method"""
    FOUR_POINT_METHOD = 2
    """2: Four-Point-Method"""
    FIVE_POINT_METHOD = 3
    """3: Five-Point-Method"""
    SIX_POINT_METHOD = 4
    """4: Six-Point-Method"""
    ABC_WORLD_METHOD = 5
    """5: ABC-World-Method"""
    ABC_TWO_POINT_METHOD = 6
    """6: ABC-Two-Point-Method"""


_iec.register_enum(ToolCalculationMode, _iec.SINT)


class TrajectoryMode(_iec.IecIntEnum):
    """TrajectoryMode (USINT)"""
    INVALID = 0
    """Invalid (default)"""
    LINEAR_MOVEMENT = 1
    """Linear movement"""
    PTP_MOVEMENT = 2
    """PTP movement"""


_iec.register_enum(TrajectoryMode, _iec.USINT)


class TransformMode(_iec.IecIntEnum):
    """TransformMode (SINT)"""
    MIRROR_AT_POINT = 0
    """
    0 (default): Mirror at Point with mirroring of the target position’s orientation Requires for
    the mirror Point the "TransformationParameter_1" and the "TransformationParameter_2" set to "Not
    used"
    """
    MIRROR_AT_STRAIGHT_LINE = 1
    """
    1: Mirror at Straight Line with mirroring of the target position’s orientation Requires for the
    Straight Line the "TransformationParameter_1" and the "TransformationParameter_2" set to
    "X-Axis", "Y-Axis" or "Z-Axis"
    """
    MIRROR_AT_PLANE = 2
    """
    2: Mirror at Plane with mirroring of the target position’s orientation Requires for the Plane
    the "TransformationParameter_1" and the "TransformationParameter_2" set to "XY-Axis", "XZ-Axis"
    or "YZ-Axis"
    """
    ROTATE_AROUND_STRAIGHT_LINE = 3
    """
    3: Rotate around Straight Line with rotation of the target position’s orientation Requires for
    the Straight Line the "TransformationParameter_1" and the "TransformationParameter_2" set to
    "X-Axis", "Y-Axis" or "Z-Axis" Requires for the parameter "RotationAngle"
    """
    SHIFT_BY_VECTOR = 4
    """
    4: Shift by Vector Requires for the shifting Vector defined by the Point the
    "TransformationParameter_1" and the "TransformationParameter_2" set to "Not used" Requires for
    the shifting shortest Vector to the Straight Line the "TransformationParameter_1" and the
    "TransformationParameter_2" set to "X-Axis", "Y-Axis" or "Z-Axis" Requires for the shifting
    shortest Vector to the Plane the "TransformationParameter_1" and the "TransformationParameter_2"
    set to "XY-Axis", "XZ-Axis" or "YZ-Axis"
    """


_iec.register_enum(TransformMode, _iec.SINT)


class TriggerModeIo(_iec.IecIntEnum):
    """TriggerModeIo (SINT)"""
    INVALID = 0
    """Invalid (default)"""
    DIGITAL_INPUT_RISING_EDGE = 10
    """Digital Input Rising Edge"""
    DIGITAL_INPUT_FALLING_EDGE = 11
    """Digital Input Falling Edge"""
    DIGITAL_INPUT_RISING_OR_FALLING_EDGE = 12
    """Digital Input Rising or Falling Edge"""
    DIGITAL_INPUT_RISING_OR_FALLING_EDGE_INVERTED = 13
    """Digital Input Rising or Falling Edge (Inverted)"""
    DIGITAL_OUTPUT_RISING_EDGE = 20
    """Digital Output Rising Edge"""
    DIGITAL_OUTPUT_FALLING_EDGE = 21
    """Digital Output Falling Edge"""
    DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE = 22
    """Digital Output Rising or Falling Edge"""
    DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE_INVERTED = 23
    """Digital Output Rising or Falling Edge (Inverted)"""
    ANALOG_INPUT_EXCEEDING_DEFINED_THRESHOLD = 30
    """Analog Input Exceeding Defined Threshold"""
    ANALOG_INPUT_FALLING_BELOW_DEFINED_THRESHOLD = 31
    """Analog Input Falling Below Defined Threshold"""
    ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 32
    """Analog Input Exceeding or Falling Below Defined Threshold"""
    ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 33
    """Analog Input Exceeding or Falling Below Defined Threshold (Inverted)"""
    ANALOG_INPUT_ENTERING_DEFINED_RANGE = 34
    """Analog Input Entering Defined Range"""
    ANALOG_INPUT_LEAVING_DEFINED_RANGE = 35
    """Analog Input Leaving Defined Range"""
    ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE = 36
    """Analog Input Entering or Leaving Defined Range"""
    ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 37
    """Analog Input Entering or Leaving Defined Range (Inverted)"""
    ANALOG_OUTPUT_EXCEEDING_DEFINED_THRESHOLD = 40
    """Analog Output Exceeding Defined Threshold"""
    ANALOG_OUTPUT_FALLING_BELOW_DEFINED_THRESHOLD = 41
    """Analog Output Falling Below Defined Threshold"""
    ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 42
    """Analog Output Exceeding or Falling Below Defined Threshold"""
    ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 43
    """Analog Output Exceeding or Falling Below Defined Threshold (Inverted)"""
    ANALOG_OUTPUT_ENTERING_DEFINED_RANGE = 44
    """Analog Output Entering Defined Range"""
    ANALOG_OUTPUT_LEAVING_DEFINED_RANGE = 45
    """Analog Output Leaving Defined Range"""
    ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE = 46
    """Analog Output Entering or Leaving Defined Range"""
    ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 47
    """Analog Output Entering or Leaving Defined Range (Inverted)"""
    INTEGER_REGISTER_EXCEEDING_DEFINED_THRESHOLD = 50
    """Integer Register Exceeding Defined Threshold"""
    INTEGER_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD = 51
    """Integer Register Falling Below Defined Threshold"""
    INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 52
    """Integer Register Exceeding or Falling Below Defined Threshold"""
    INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_VALUE_INVERTED = 53
    """Integer Register Exceeding or Falling Below Defined Value (Inverted)"""
    INTEGER_REGISTER_ENTERING_DEFINED_RANGE = 54
    """Integer Register Entering Defined Range"""
    INTEGER_REGISTER_LEAVING_DEFINED_RANGE = 55
    """Integer Register Leaving Defined Range"""
    INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE = 56
    """Integer Register Entering or Leaving Defined Range"""
    INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 57
    """Integer Register Entering or Leaving Defined Range (Inverted)"""
    REAL_REGISTER_EXCEEDING_DEFINED_THRESHOLD = 60
    """Real Register Exceeding Defined Threshold"""
    REAL_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD = 61
    """Real Register Falling Below Defined Threshold"""
    REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 62
    """Real Register Exceeding or Falling Below Defined Threshold"""
    REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 63
    """Real Register Exceeding or Falling Below Defined Threshold (Inverted)"""
    REAL_REGISTER_ENTERING_DEFINED_RANGE = 64
    """Real Register Entering Defined Range"""
    REAL_REGISTER_LEAVING_DEFINED_RANGE = 65
    """Real Register Leaving Defined Range"""
    REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE = 66
    """Real Register Entering or Leaving Defined Range"""
    REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 67
    """Real Register Entering or Leaving Defined Range (Inverted)"""


_iec.register_enum(TriggerModeIo, _iec.SINT)


class TriggerModeLimit(_iec.IecIntEnum):
    """TriggerModeLimit (SINT)"""
    INVALID = 0
    """0: Invalid (default)"""
    JOINT_CURRENT = 1
    """1: Joint current in mA"""
    FORCE = 2
    """2: Force in Nm"""
    FOLLOWING_ERROR = 3
    """3: Following error. The distance of the robot position from the path that was calculated"""
    TEMPERATURE = 4
    """Temperature in °C"""


_iec.register_enum(TriggerModeLimit, _iec.SINT)


class TriggerModeMeasurement(_iec.IecIntEnum):
    """TriggerModeMeasurement (USINT)"""
    NO_TRIGGER = 0
    """(default) No trigger related behavior"""
    POSITIVE_START_NEGATIVE_STOP = 1
    """
    1: Starts the measurement with the positive trigger event and stops it with the negative trigger
    event when the trigger function with the identical EmitterID is activated.
    """
    POSITIVE_START_STOP = 2
    """
    2: Starts and stops the measurement with the positive trigger event when the trigger function
    with the identical EmitterID is activated.
    """


_iec.register_enum(TriggerModeMeasurement, _iec.USINT)


class TriggerReactionMode(_iec.IecIntEnum):
    """TriggerReactionMode (SINT)"""
    NO_REACTION = 0
    """No reaction (default)."""
    INTERRUPT = 1
    """Interrupt: Robot movement is paused. Movement can be continued by function GroupContinue."""
    GROUP_STOP = 2
    """
    GroupStop: Robot stops the movement and brings all axes to a halt. Movements aborted by this
    command cannot be continued.
    """
    DISABLE_ROBOT = 3
    """
    Disable robot: The robot’s drives are disabled. This leads to the robot state "Not enabled" (see
    chapter 5.5.3).
    """
    STOP_ACTUAL_MOTION_COMMAND = 4
    """
    Stop actual motion command: Robot movement is paused. Movement can be continued by the next
    motion command.
    """


_iec.register_enum(TriggerReactionMode, _iec.SINT)


class TurnMode(_iec.IecIntEnum):
    """TurnMode (USINT)"""
    USE_TURN_NUMBER = 0
    """Use TurnNumber in position"""
    SAME = 1
    """Do not change TurnNumber with this movement"""
    FREE = 2
    """TurnNumber in position is not used but the Robot is free to change TurnNumber"""


_iec.register_enum(TurnMode, _iec.USINT)


class WorkAreaReactionMode(_iec.IecIntEnum):
    """WorkAreaReactionMode (USINT)"""
    NO_REACTION = 0
    """0: No reaction (default) • RC reports violation • Robot is not stopped"""
    ABORT = 1
    """1: Abort • RC reports violation • RC returns error • Robot is stopped • Sequence buffer emptied"""
    INTERRUPT = 2
    """
    2: Interrupt • RC reports violation • Robot movement is paused • Movement can be continued by
    function GroupContinue
    """


_iec.register_enum(WorkAreaReactionMode, _iec.USINT)


class ActiveCommandRegisterState(_iec.IecIntEnum):
    """ActiveCommandRegisterState (INT)"""
    IS_FREE = 0
    """IS_FREE denotes not used but available resources (empty slots in the ACR)."""
    IS_PROCESSING = 1
    """
    IS_PROCESSING CMDs are actively being processed by client or server. In terms of CMD category,
    IS_PROCESSING also describes commands whose tasks are not currently being executed (not ACTIVE),
    but e.g. a CMD waiting in the Sequence buffer.
    """
    IS_FINAL = 2
    """
    IS_FINAL states are reached on CMD termination. Execution of this Task has been finished and its
    results can be examined.
    """


_iec.register_enum(ActiveCommandRegisterState, _iec.INT)


class BufferStateCmd(_iec.IecIntEnum):
    """BufferStateCmd (INT)"""
    EMPTY = 0
    """PDF Page 353"""
    CREATED = 1
    UPDATE_AVAILABLE = 2
    SENDING = 3
    PROCESSED = 4


_iec.register_enum(BufferStateCmd, _iec.INT)


class BufferStateRsp(_iec.IecIntEnum):
    """BufferStateRsp (INT)"""
    EMPTY = 0
    """PDF Seite 353"""
    RECEIVING = 1
    RECEIVED = 2
    PROCESSED = 3


_iec.register_enum(BufferStateRsp, _iec.INT)


class CmdMessageState(_iec.IecIntEnum):
    """CmdMessageState (USINT)"""
    EMPTY = 0
    """No operation or process is active"""
    CREATED = 1
    """Created but not yet started"""
    BUFFERED = 2
    """Buffered and awaiting execution"""
    BUFFERED_IN_PLANNER = 3
    """Buffered in planner for future execution"""
    ACTIVE = 4
    """Currently active and in progress"""
    INTERRUPTED = 5
    """Interrupted and awaiting continuation"""
    ABORT_REQUEST = 6
    """Requested for abort"""
    DONE = 10
    """Successfully completed"""
    ABORTED = 14
    """Aborted before completion"""
    ERROR = 15
    """Encountered an error during execution"""


_iec.register_enum(CmdMessageState, _iec.USINT)


class InitializationState(_iec.IecIntEnum):
    """InitializationState (INT)"""
    DEFAULT = 0
    """Default"""
    ERROR_TELEGRAM_CONTROL = 161
    """Error: Telegram control does not match the telegram state"""
    ERROR_INIT_LOST = 162
    """Error: Initialization lost for unknown reason. See message log after reinitializing"""
    ERROR_TELEGRAM_LENGTH = 163
    """Error: Telegram length does not match the length provided in the communication interface."""
    ERROR_INCOMPATIBLE_SRCI = 164
    """Error: Incompatible major SRCI version"""
    ERROR_LIFESIGN_TIMEOUT = 165
    """Error: Lifesign timeout"""
    ERROR_CYCLIC_DATA_MISMATCH = 166
    """Error: The selected optional cyclic data does not fit in the given telegram size"""
    ERROR_INTERFACE_RESET = 167
    """Error: The robot interface was reset after being initialized"""
    ERROR_SEQUENCE_TIMEOUT = 168
    """Error: Telegram sequence timeout"""
    ERROR_TELEGRAM_NUMBER_CHANGED = 169
    """Error: The telegram number changed after initialization"""
    ERROR_INVALID_AXES_GROUP = 170
    """Error: Invalid AxesGroupID"""
    ERROR_INVALID_TELEGRAM_NUMBER = 171
    """Error: Telegram number is invalid. E.g. TwoSequences is only activated in one direction"""
    ERROR_TELEGRAM_NUMBER_NOT_SUPPORTED = 172
    """Error: Telegram Number is not supported"""
    READY_TO_RESUME = 253
    """Ready to resume: The RC is currently not initialized but has state in the ACR"""
    READY_FOR_INITIALIZATION = 254
    """Ready for initialization: The RC is currently not initialized and has no state in the ACR"""
    INITIALIZED = 255
    """Initialized: The RC state is Initialized"""


_iec.register_enum(InitializationState, _iec.INT)


class RaPowerState(_iec.IecIntEnum):
    """RaPowerState (USINT)"""
    NOT_ENABLED = 0
    """Robot drives disabled. Robot cannot be moved"""
    ENABLED = 1
    """Robot drives powered on. Robot can be moved according to sequence state"""


_iec.register_enum(RaPowerState, _iec.USINT)


class RaSequenceState(_iec.IecIntEnum):
    """RaSequenceState (USINT)"""
    IDLE = 0
    """Robot can be moved by incoming command"""
    EXECUTING = 1
    """RC is processing command in active sequence"""
    INTERRUPTED = 2
    """Interrupt is active. Robot is waiting for Continue"""


_iec.register_enum(RaSequenceState, _iec.USINT)


class RiState(_iec.IecIntEnum):
    """RiState (USINT)"""
    NOT_INITIALIZED = 0
    """RI is not initialized"""
    INITIALIZED = 1
    """Initialization finished successfully"""
    SYNCHRONIZED = 2
    """Data between RC and PLC has been synchronized"""


_iec.register_enum(RiState, _iec.USINT)


class TelegramState(_iec.IecIntEnum):
    """TelegramState (USINT)"""
    UNDEFINED = 0
    """Default"""
    ERROR_161_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE = 161
    """Telegram control does not match the telegram state"""
    ERROR_162_INIT_LOST_UNKNOWN = 162
    """Initialization lost for unknown reason. See message log after reinitializing"""
    ERROR_163_TELEGRAM_LENGTH_MISMATCH = 163
    """Telegram length does not match the length provided in the communication interface."""
    ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE = 164
    """Incompatible major SRCI version"""
    ERROR_165_LIFESIGN_TIMEOUT = 165
    """Lifesign timeout"""
    ERROR_166_CYCLIC_DATA_TOO_LARGE = 166
    """The selected optional cyclic data does not fit in the given telegram size"""
    ERROR_167_INTERFACE_WAS_RESET_AFTER_INIT = 167
    """The robot interface was reset after being initialized"""
    ERROR_168_TELEGRAM_SEQ_TIMEOUT = 168
    """Telegram sequence timeout"""
    ERROR_169_TELEGRAM_NO_CHANGED_AFTER_INIT = 169
    """The telegram number changed after initialization"""
    ERROR_170_AXESGROUP_ID_INVALID = 170
    """Invalid AxesGroupID"""
    ERROR_171_TELEGRAM_NUMBER_INVALID = 171
    """Telegram number is invalid. E.g. TwoSequences is only activated in one direction"""
    ERROR_172_TELEGRAM_NUMBER_NOT_SUPPORTED = 172
    """Telegram Number is not supported"""
    ERROR_173_SERVER_CONNECTION_LOST = 173
    """Server connection lost"""
    READY_TO_RESUME = 253
    """The RC is currently not initialized but has state in the ACR"""
    READY_FOR_INITIALIZATION = 254
    """The RC is currently not initialized and has no state in the ACR"""
    INITIALIZED = 255
    """The RC state is Initialized"""


_iec.register_enum(TelegramState, _iec.USINT)


class AreaType(_iec.IecIntEnum):
    """AreaType (USINT)"""
    AXES = 0
    """0: Axes"""
    BOX = 1
    """1: Box (default)"""
    CYLINDER = 2
    """2: Cylinder"""
    SPHERE = 3
    """3: Sphere (only DefinitionMode 1)"""


_iec.register_enum(AreaType, _iec.USINT)


class AxesGroupParameterCmdEntries(_iec.IecIntEnum):
    """AxesGroupParameterCmdEntries (UINT)"""
    RobotTask = 0
    """Handles multiple mechanisms required for operation of the interface"""
    ReadRobotData = 9002
    """Read robot-specific data from the RC"""
    EnableRobot = 1
    """Enable/Disable robot into RA power state "Enabled" """
    GroupReset = 2
    """Acknowledgement all pending errors"""
    ReadActualPosition = 3
    """Read the actual position – TCP: X…RZ + config/Turn, Joint: (J1…E6)"""
    ReadActualPositionCyclic = 4
    """Read the actual position cyclically"""
    ReadDHParameter = 5
    """Read D-H-parameters of robot"""
    RestartController = 6
    """Restart/reboot of the RC"""
    ReadActualTCPVelocity = 7
    """Read actual TCP velocity"""
    UserLogin = 8
    """Login on RC from PLC"""
    SwitchLanguage = 9
    """Switch language of robot teach pendant from PLC"""
    ExchangeConfiguration = 10
    """Reads and writes specific configuration parameters on RC that are required for the RI to work"""
    SetSequence = 11
    """Set active sequence"""
    ChangeSpeedOverride = 12
    """Change actual speed override"""
    ReadMessages = 13
    """Read error codes of pending errors and move them into user data block "RobotData" """
    ReadRobotReferenceDynamics = 14
    """Read reference values of robot dynamics for path movement"""
    WriteFrameData = 15
    """Change configuration of selected user frame number"""
    WriteToolData = 16
    """Change configuration of selected tool number"""
    WriteLoadData = 17
    """Change configuration of selected payload number"""
    WriteRobotReferenceDynamics = 18
    """Write reference values of robot dynamics for path movement"""
    WriteRobotDefaultDynamics = 19
    """Write default values of dynamic parameters used by move commands"""
    ReadRobotDefaultDynamics = 20
    """Read default values of dynamic parameters used by move commands"""
    ReadFrameData = 21
    """Read content of selected user frame number"""
    ReadToolData = 22
    """Read content of selected tool number"""
    ReadLoadData = 23
    """Read content of selected payload number"""
    ReadRobotSWLimits = 24
    """Read actual software limits of the axes Positive and negative Limit of Joint J1…J6, E1…E6"""
    WriteRobotSWLimits = 25
    """Change robot limits of robot axes (degree)"""
    SetOperationMode = 26
    """Switch operation mode of RC (Automatic External, T1 External, T2 External)"""
    ReadWorkArea = 27
    """Read configuration of defined work areas"""
    WriteWorkArea = 28
    """Define work area"""
    ActivateWorkArea = 29
    """Enable/Disable work areas of RC and check if TCP is inside/outside of active work area"""
    MonitorWorkArea = 30
    """Monitor enabled work areas"""
    GroupJog = 31
    """Jog robot manually"""
    MoveLinearAbsolute = 32
    """Move the TCP to an absolute cartesian position (linear interpolation)"""
    MoveDirectAbsolute = 33
    """
    Move Joints to an absolute cartesian position (Absolute cartesian PTP) (Joint interpolated
    movement)
    """
    MoveAxesAbsolute = 34
    """Move all joints to an absolute joint position (Absolute Joint PTP)"""
    GroupStop = 35
    """Abort actual movement and delete buffer"""
    GroupInterrupt = 36
    """Interrupt active movement, possible to continue movement"""
    GroupContinue = 37
    """Continue interrupted path"""
    MoveLinearRelative = 38
    """Move the TCP relative to the actual cartesian position (linear interpolation)"""
    MoveDirectRelative = 39
    """
    Move Joints relative to relative cartesian position (Relative cartesian PTP) (Joint interpolated
    movement)
    """
    MoveAxesRelative = 40
    """Move all joints relative to actual joint position (Relative Joint PTP)"""
    ReturnToPrimary = 41
    """Return to path left during active interrupt"""
    MoveCircularAbsolute = 42
    """Move the TCP to an absolute joint position (linear interpolation)"""
    MoveCircularRelative = 43
    """Move the TCP relative to the actual cartesian position (circular interpolation)"""
    MoveLinearOffset = 44
    """Move the TCP relative to a reference cartesian position (linear interpolation)"""
    MoveDirectOffset = 45
    """Move the TCP relative to a reference cartesian position (PTPT interpolation)"""
    WaitTime = 46
    """Set wait command between motion commands"""
    MoveApproachLinear = 47
    """
    Linear Move to target position through auxiliary position defined by offset in all dimensions
    (movement to target position linear)
    """
    MoveDepartLinear = 48
    """
    Linear Move from actual position to destination through auxiliary position defined by offset in
    all dimensions (movement to target position linear)
    """
    MoveApproachDirect = 49
    """
    Direct Move to target position through auxiliary position defined by offset in all dimensions
    (movement to target posi tion PTP)
    """
    MoveDepartDirect = 50
    """
    Direct Move from actual position to destination through auxiliary position defined by offset in
    all dimensions (movement to the target position PTP)
    """
    SearchHardstop = 51
    """Move robot into contact with obstruction (mechanical Limit) and hold it in this position"""
    SearchHardstopJ = 52
    """Move robot into contact with obstruction (mechanical Limit) and hold it in this position"""
    MovePickPlaceLinear = 53
    """Command several interpolated movement of robot arm on linear paths from actual position"""
    MovePickPlaceDirect = 54
    """Commands interpolated movement of robot arm on a partly undefined path from actual position"""
    ActivateConveyorTracking = 55
    """Activate conveyor tracking mode"""
    RedefineTrackingPos = 56
    """Redefine tracking position for conveyor tracking"""
    SyncToConveyor = 57
    """Synchronize robot with conveyor"""
    ConfigureConveyor = 58
    """Configure conveyor parameters"""
    MoveSuperImposed = 59
    """Activate superimposed motion of TCP to defined motion"""
    MoveSuperImposedDynamic = 60
    """Activate superimposed motion of TCP to defined motion"""
    ReadDigitalInputs = 61
    """Read digital input and output group of RC"""
    ReadDigitalOutputs = 62
    """Read digital output group of RC"""
    WriteDigitalOutputs = 63
    """Write digital output group of RC"""
    ReadIntegers = 64
    """Read integer values on RC"""
    ReadReals = 65
    """Read real values on RC"""
    WriteIntegers = 66
    """Write integer values on RC"""
    WriteReals = 67
    """Write real values on RC"""
    MoveLinearCam = 68
    """Set trigger in defined position of path (L = Linear Path) (cartesian) switch periphery."""
    MoveDirectCam = 69
    """Set a trigger in a defined position of a path. (PTP)"""
    MoveCircularCam = 70
    """Set a trigger in a defined position of a circular path"""
    ReadAnalogInput = 71
    """Read analog input of RC"""
    ReadAnalogOutput = 72
    """Read analog output of RC"""
    WriteAnalogOutput = 73
    """Write analog output of RC"""
    MeasuringInput = 74
    """Capture trigger Position, measuring input"""
    AbortMeasuringInput = 75
    """Abort triggering of Position, measuring input"""
    SetTriggerRegister = 76
    """Trigger "Actions" based on I/O related events (e.g. change of DI’s state)"""
    SetTriggerLimit = 77
    """Trigger "Actions" based on physical events (e.g. force limit reached)"""
    SetTriggerUser = 78
    """Trigger "Actions" based on physical events (e.g. force limit reached)"""
    SetTriggerError = 79
    """Trigger "Actions" based on incoming error event"""
    ReactAtTrigger = 80
    """"Action" that initiates specified events when triggered"""
    WaitForTrigger = 81
    """Wait to process next command in sequence until trigger signal is received"""
    ReadSystemVariable = 82
    """Read specific parameter of the robot"""
    WriteSystemVariable = 83
    """Change value of specific vendor parameter"""
    CalculateForwardKinematic = 84
    """Calculate Forward Kinematic"""
    CalculateInverseKinematic = 85
    """Calculate Inverse Kinematic"""
    CalculateCartesianPosition = 86
    """Calculate cartesian position from existing cartesian position"""
    CalculateTool = 87
    """Calculate tool (TCP) with four-point method"""
    CalculateFrame = 88
    """Calculate frame with three-point method"""
    ActivateNextCommand = 89
    """Cancel currently active move command and continue with the next buffered command"""
    ShiftPosition = 90
    """Transform a defined position in space"""
    SetTriggerMotion = 91
    """Trigger an action based on a motion-related parameter (e.g. progress of trajectory)"""
    OpenBrake = 92
    """Release robot arm’s brakes"""
    CallSubprogram = 93
    """Call subprogram stored in RC from PLC"""
    WriteCallSubprogramCyclic = 94
    """Writes cyclic data of called subprogram"""
    ReadCallSubprogramCyclic = 95
    """Reads cyclic data of called subprogram"""
    StopSubprogram = 96
    """Stops an active subprogram"""
    PathAccuracyMode = 97
    """Switch path mode between high and low accuracy"""
    AvoidSingularity = 98
    """Activate/Deactivate functionality to avoid singularities"""
    ForceControl = 99
    """Enables the RC to apply user-defined force/torque through RA’s TCP movement"""
    ForceLimit = 100
    """Commands specified reaction from RA when defined force/torque detected"""
    ReadActualForce = 101
    """Read actual force/torque at TCP"""
    BrakeTest = 102
    """Activate robot cycle brake test and give feedback to PLC"""
    SoftSwitchTCP = 103
    """Push robot: Robot calculates opposite vector and moves slowly in that direction"""
    CreateSpline = 104
    """Create spline on RC from positions stored in PLC"""
    DeleteSpline = 105
    """Delete spline previously created on RC"""
    MoveSpline = 106
    """Move spline previously created on RC"""
    DynamicSpline = 107
    """Create and move spline on RC simultaneously"""
    LoadMeasurementAutomatic = 108
    """Automatic detection of load data"""
    LoadMeasurementSequential = 109
    """Sequential detection of load data"""
    CollisionDetection = 110
    """Turn on/off the collision detection"""
    FreeDrive = 111
    """Move the robot axes by hand"""
    UnitMeasurement = 112
    """
    Measure the length of objects in the cartesian space, execution time for specified section of a
    job or signal output time of a specified signal
    """
    MAX_ENTRY = 113
    """Maximum entry"""


_iec.register_enum(AxesGroupParameterCmdEntries, _iec.UINT)


class CmdType(_iec.IecIntEnum):
    """CmdType (UINT)"""
    RobotTask = 0
    """Handles multiple mechanisms required for operation of the interface"""
    ReadRobotData = 9002
    """Read robot-specific data from the RC"""
    EnableRobot = 1000
    """Enable/Disable robot into RA power state "Enabled" """
    GroupReset = 1001
    """Acknowledgement all pending errors"""
    ReadActualPosition = 5100
    """Read the actual position – TCP: X…RZ + config/Turn, Joint: (J1…E6)"""
    ReadActualPositionCyclic = 1
    """Read the actual position cyclically"""
    ReadDHParameter = 5101
    """Read D-H-parameters of robot"""
    RestartController = 1101
    """Restart/reboot of the RC"""
    ReadActualTCPVelocity = 5111
    """Read actual TCP velocity"""
    UserLogin = 1006
    """Login on RC from PLC"""
    SwitchLanguage = 1005
    """Switch language of robot teach pendant from PLC"""
    ExchangeConfiguration = 9000
    """Reads and writes specific configuration parameters on RC that are required for the RI to work"""
    SetSequence = 1004
    """Set active sequence"""
    ChangeSpeedOverride = 2000
    """Change actual speed override"""
    ReadMessages = 9001
    """Read error codes of pending errors and move them into user data block "RobotData" """
    ReadRobotReferenceDynamics = 5105
    """Read reference values of robot dynamics for path movement"""
    WriteFrameData = 5200
    """Change configuration of selected user frame number"""
    WriteToolData = 5205
    """Change configuration of selected tool number"""
    WriteLoadData = 5201
    """Change configuration of selected payload number"""
    WriteRobotReferenceDynamics = 5203
    """Write reference values of robot dynamics for path movement"""
    WriteRobotDefaultDynamics = 5202
    """Write default values of dynamic parameters used by move commands"""
    ReadRobotDefaultDynamics = 5104
    """Read default values of dynamic parameters used by move commands"""
    ReadFrameData = 5102
    """Read content of selected user frame number"""
    ReadToolData = 5107
    """Read content of selected tool number"""
    ReadLoadData = 5103
    """Read content of selected payload number"""
    ReadRobotSWLimits = 5106
    """Read actual software limits of the axes Positive and negative Limit of Joint J1…J6, E1…E6"""
    WriteRobotSWLimits = 5204
    """Change robot limits of robot axes (degree)"""
    SetOperationMode = 1003
    """Switch operation mode of RC (Automatic External, T1 External, T2 External)"""
    ReadWorkArea = 7502
    """Read configuration of defined work areas"""
    WriteWorkArea = 7503
    """Define work area"""
    ActivateWorkArea = 7500
    """Enable/Disable work areas of RC and check if TCP is inside/outside of active work area"""
    MonitorWorkArea = 7501
    """Monitor enabled work areas"""
    GroupJog = 2100
    """Jog robot manually"""
    MoveLinearAbsolute = 2103
    """Move the TCP to an absolute cartesian position (linear interpolation)"""
    MoveDirectAbsolute = 2102
    """
    Move Joints to an absolute cartesian position (Absolute cartesian PTP) (Joint interpolated
    movement)
    """
    MoveAxesAbsolute = 2101
    """Move all joints to an absolute joint position (Absolute Joint PTP)"""
    GroupStop = 2003
    """Abort actual movement and delete buffer"""
    GroupInterrupt = 2002
    """Interrupt active movement, possible to continue movement"""
    GroupContinue = 2001
    """Continue interrupted path"""
    MoveLinearRelative = 2110
    """Move the TCP relative to the actual cartesian position (linear interpolation)"""
    MoveDirectRelative = 2108
    """
    Move Joints relative to relative cartesian position (Relative cartesian PTP) (Joint interpolated
    movement)
    """
    MoveAxesRelative = 2105
    """Move all joints relative to actual joint position (Relative Joint PTP)"""
    ReturnToPrimary = 2104
    """Return to path left during active interrupt"""
    MoveCircularAbsolute = 2106
    """
    Move the TCP to an absolute joint position (linear interpolation) [Override: F35: spec 6.3.13
    Type 2106 (library 2109)]
    """
    MoveCircularRelative = 2107
    """
    Move the TCP relative to the actual cartesian position (circular interpolation) [Override: F35:
    spec Type 2107 (library 2106)]
    """
    MoveLinearOffset = 2112
    """Move the TCP relative to a reference cartesian position (linear interpolation)"""
    MoveDirectOffset = 2111
    """Move the TCP relative to a reference cartesian position (PTPT interpolation)"""
    WaitTime = 7005
    """Set wait command between motion commands"""
    MoveApproachLinear = 2201
    """
    Linear Move to target position through auxiliary position defined by offset in all dimensions
    (movement to target position linear)
    """
    MoveDepartLinear = 2203
    """
    Linear Move from actual position to destination through auxiliary position defined by offset in
    all dimensions (movement to target position linear)
    """
    MoveApproachDirect = 2200
    """
    Direct Move to target position through auxiliary position defined by offset in all dimensions
    (movement to target posi tion PTP)
    """
    MoveDepartDirect = 2202
    """
    Direct Move from actual position to destination through auxiliary position defined by offset in
    all dimensions (movement to the target position PTP)
    """
    SearchHardstop = 2500
    """Move robot into contact with obstruction (mechanical Limit) and hold it in this position"""
    SearchHardstopJ = 2501
    """Move robot into contact with obstruction (mechanical Limit) and hold it in this position"""
    MovePickPlaceLinear = 2205
    """Command several interpolated movement of robot arm on linear paths from actual position"""
    MovePickPlaceDirect = 2204
    """Commands interpolated movement of robot arm on a partly undefined path from actual position"""
    ActivateConveyorTracking = 2300
    """Activate conveyor tracking mode"""
    RedefineTrackingPos = 2302
    """Redefine tracking position for conveyor tracking"""
    SyncToConveyor = 2303
    """Synchronize robot with conveyor"""
    ConfigureConveyor = 2301
    """Configure conveyor parameters"""
    MoveSuperImposed = 2502
    """Activate superimposed motion of TCP to defined motion"""
    MoveSuperImposedDynamic = 2503
    """Activate superimposed motion of TCP to defined motion"""
    ReadDigitalInputs = 6100
    """Read digital input and output group of RC"""
    ReadDigitalOutputs = 6101
    """Read digital output group of RC"""
    WriteDigitalOutputs = 6104
    """Write digital output group of RC"""
    ReadIntegers = 6102
    """Read integer values on RC"""
    ReadReals = 6103
    """Read real values on RC"""
    WriteIntegers = 6105
    """Write integer values on RC"""
    WriteReals = 6106
    """Write real values on RC"""
    MoveLinearCam = 2402
    """Set trigger in defined position of path (L = Linear Path) (cartesian) switch periphery."""
    MoveDirectCam = 2401
    """Set a trigger in a defined position of a path. (PTP)"""
    MoveCircularCam = 2400
    """Set a trigger in a defined position of a circular path"""
    ReadAnalogInput = 6107
    """Read analog input of RC"""
    ReadAnalogOutput = 6108
    """Read analog output of RC"""
    WriteAnalogOutput = 6109
    """Write analog output of RC"""
    MeasuringInput = 6001
    """Capture trigger Position, measuring input"""
    AbortMeasuringInput = 6000
    """Abort triggering of Position, measuring input"""
    SetTriggerRegister = 3004
    """Trigger "Actions" based on I/O related events (e.g. change of DI’s state)"""
    SetTriggerLimit = 3002
    """Trigger "Actions" based on physical events (e.g. force limit reached)"""
    SetTriggerUser = 3005
    """Trigger "Actions" based on physical events (e.g. force limit reached)"""
    SetTriggerError = 3001
    """Trigger "Actions" based on incoming error event"""
    ReactAtTrigger = 3000
    """"Action" that initiates specified events when triggered"""
    WaitForTrigger = 3006
    """Wait to process next command in sequence until trigger signal is received"""
    ReadSystemVariable = 5109
    """Read specific parameter of the robot"""
    WriteSystemVariable = 5206
    """Change value of specific vendor parameter"""
    CalculateForwardKinematic = 7203
    """Calculate Forward Kinematic"""
    CalculateInverseKinematic = 7204
    """Calculate Inverse Kinematic"""
    CalculateCartesianPosition = 7200
    """Calculate cartesian position from existing cartesian position"""
    CalculateTool = 7202
    """Calculate tool (TCP) with four-point method"""
    CalculateFrame = 7201
    """Calculate frame with three-point method"""
    ActivateNextCommand = 7000
    """Cancel currently active move command and continue with the next buffered command"""
    ShiftPosition = 7205
    """Transform a defined position in space"""
    SetTriggerMotion = 3003
    """Trigger an action based on a motion-related parameter (e.g. progress of trajectory)"""
    OpenBrake = 7100
    """Release robot arm’s brakes"""
    CallSubprogram = 7001
    """Call subprogram stored in RC from PLC"""
    WriteCallSubprogramCyclic = 2
    """Writes cyclic data of called subprogram"""
    ReadCallSubprogramCyclic = 3
    """Reads cyclic data of called subprogram"""
    StopSubprogram = 7008
    """Stops an active subprogram"""
    PathAccuracyMode = 7401
    """Switch path mode between high and low accuracy"""
    AvoidSingularity = 7400
    """Activate/Deactivate functionality to avoid singularities"""
    ForceControl = 7301
    """Enables the RC to apply user-defined force/torque through RA’s TCP movement"""
    ForceLimit = 7302
    """Commands specified reaction from RA when defined force/torque detected"""
    ReadActualForce = 5110
    """Read actual force/torque at TCP"""
    BrakeTest = 7101
    """Activate robot cycle brake test and give feedback to PLC"""
    SoftSwitchTCP = 7300
    """Push robot: Robot calculates opposite vector and moves slowly in that direction"""
    CreateSpline = 2600
    """Create spline on RC from positions stored in PLC"""
    DeleteSpline = 2601
    """Delete spline previously created on RC"""
    MoveSpline = 2603
    """Move spline previously created on RC"""
    DynamicSpline = 2602
    """Create and move spline on RC simultaneously"""
    LoadMeasurementAutomatic = 7006
    """Automatic detection of load data"""
    LoadMeasurementSequential = 7007
    """Sequential detection of load data"""
    CollisionDetection = 7003
    """Turn on/off the collision detection"""
    FreeDrive = 7002
    """Move the robot axes by hand"""
    UnitMeasurement = 7004
    """
    Measure the length of objects in the cartesian space, execution time for specified section of a
    job or signal output time of a specified signal
    """
    MoveLinearAbsoluteJ = 2109
    """[Override: F35: spec 6.3.12 Type 2109 (missing in the library)]"""
    SoftSwitchTcp = 7300
    """[Override: F35: spec Type 7300 (missing in the library)]"""


_iec.register_enum(CmdType, _iec.UINT)


class ConveyorType(_iec.IecIntEnum):
    """ConveyorType (USINT)"""
    LINEAR_CONVEYOR_TRACKING = 0
    """Linear Conveyor Tracking (default)"""
    CIRCULAR_CONVEYOR_TRACKING = 1
    """Circular Conveyor Tracking"""


_iec.register_enum(ConveyorType, _iec.USINT)


class DataType(_iec.IecIntEnum):
    """DataType (USINT)"""
    TYPE_BOOL = 1
    """BOOL"""
    TYPE_BYTE = 2
    """BYTE"""
    TYPE_WORD = 3
    """WORD"""
    TYPE_DWORD = 4
    """DWORD"""
    TYPE_SINT = 5
    """SINT"""
    TYPE_USINT = 6
    """USINT"""
    TYPE_INT = 7
    """INT"""
    TYPE_UINT = 8
    """UINT"""
    TYPE_DINT = 9
    """DINT"""
    TYPE_UDINT = 10
    """UDINT"""
    TYPE_REAL = 11
    """REAL"""
    TYPE_CHAR = 12
    """CHAR"""
    TYPE_CHAR_ARRAY = 13
    """CHAR_ARRAY"""


_iec.register_enum(DataType, _iec.USINT)


class MessageType(_iec.IecIntEnum):
    """MessageType (USINT)"""
    RI = 1
    """RI related messages"""
    RC = 2
    """RC related messages"""
    RA = 3
    """RA related messages"""
    CMD = 4
    """Command related messages"""


_iec.register_enum(MessageType, _iec.USINT)


class ReferenceType(_iec.IecIntEnum):
    """ReferenceType (USINT)"""
    TOOL = 0
    """
    Distance is applied in the Tool coordinate system. The setting of the parameter FrameNo will be
    ignored.
    """
    FRAME = 1
    """
    Distance is applied in the Frame coordinate system. The settings of the ToolNo are also
    effective and must be considered.
    """


_iec.register_enum(ReferenceType, _iec.USINT)


class UnitType(_iec.IecIntEnum):
    """UnitType (USINT)"""
    VOLT = 0
    """Volt"""
    AMPERE = 1
    """Ampere"""


_iec.register_enum(UnitType, _iec.USINT)


# aliases defined in the PLC library
SequenceFlagEnum = SequenceFlag
LogLevel = Severity
LogLevelEnum = Severity
MessageLevelEnum = MessageLevel
AbortingModeEnum = AbortingMode
ProcessingModeEnum = ProcessingMode
