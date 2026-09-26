
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ErrorIdEnum
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
from RobotLibrary.IEC_Types import WORD, WORDEnum


class ErrorIdEnum(WORDEnum):

    NO_ERROR = 0
    """ no error """

    #START

    ERR_INVALID_STEP = 1
    """ 
    Program fault : Invalid step
    """

    ERR_INVALID_LIBRARY_PARA = 2
    """ 
    Program fault : Invalid library parameter
    """

    ERR_INVALID_AXES_GROUP_ID = 3
    """ 
    Program fault : Invalid axes groups ID
    """

    ERR_FUNCTION_NOT_SUPPORTED = 5
    """
    Function is not supported
    """

    ERR_TIMEOUT_CMD = 6
    """
    Program fault : Timeout during command execution
    """

    ERR_INVALID_PAR_CMD_SYNC_REACTION = 7
    """
    Parameter fault : Invalid command parameter SyncReaction
    """

    ERR_INVALID_PAR_CMD = 8             
    """
    Invalid command parameter - see log file for details (LogLevel Error)
    """

    ERR_SYNC_STATE_PROHIBITS_COMMAND = 9
    """
    Synchronisation state prohibits command execution
    """

    ERR_SYNC_MODE_INVALID = 10    
    """
    Synchronisation mode is invalid
    """

    ERR_LOADNO_UNAVAILABLE  = 11
    """ 
    Client Invalid parameter value - LoadNo not available on RC\n
    Commands using the parameter "LoadNo"
    """

    ERR_WORKAREANO_RANGE  = 12
    """ 
    Client Invalid parameter value - WorkAreaNo outside of the allowed range -1..254\n
    Commands using the parameter "WorkAreaNo" 
    """

    ERR_WORKAREANO_UNAVAILABLE  = 13
    """ 
    Client Invalid parameter value - LoadNo not available on RC\n
    Commands using the parameter "LoadNo" 
    """
        
    ERR_TRIGGERMODE_NOT_ALLOWED = 14
    """ 
    Client Specified TriggerMode not allowed\n
    Commands using the parameter "TriggerMode" 
    """

    ERR_FRAMECALCULATIONMODE_INVALID = 15
    """ 
    Client Specified Frame calculation mode not valid\n
    Commands using the parameter "FrameCalculationMode"
    """

    # END
    # {warning 'ToDo: This is an internal error ID, which is not defined in SRCI specification'}

    ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0xA1 = 0xA1
    """
    Telegram control does not match the telegram state
    """

    ERR_INIT_LOST_UNKNOWN_0xA2  = 0xA2
    """
    Initialization lost for unknown reason. See message log after reinitializing
    """

    ERR_TELEGRAM_LENGTH_MISMATCH_0xA3 = 0xA3
    """
    Telegram length does not match the length provided in the communication interface.
    """

    ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0xA4 = 0xA4
    """
    Incompatible major SRCI version
    """

    ERR_LIFESIGN_TIMEOUT_0xA5 = 0xA5
    """
    Lifesign timeout
    """

    ERR_CYCLIC_DATA_TOO_LARGE_0xA6 = 0xA6
    """
    The selected optional cyclic data does not fit in the given telegram size
    """

    ERR_INTERFACE_WAS_RESET_AFTER_INIT_0xA7 = 0xA7
    """
    The robot interface was reset after being initialized
    """

    ERR_TELEGRAM_SEQ_TIMEOUT_0xA8 = 0xA8
    """
    Telegram sequence timeout
    """

    ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0xA9 = 0xA9
    """
    The telegram number changed after initialization
    """

    ERR_AXESGROUP_ID_INVALID_0xAA = 0xAA,
    """
    Invalid AxesGroupID
    """

    ERR_TELEGRAM_NUMBER_INVALID_0xAB = 0xAB
    """
    Telegram number is invalid. E.g. TwoSequences is only activated in one direction
    """

    ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0xAC = 0xAC
    """
    Telegram Number is not supported
    """

    ERR_SERVER_CONNECTION_LOST_0xAD = 0xAD
    """
    Server Connection to the communication partner was lost
    """


    # Table 5-96: Telegram and Initialization State 
    # Initialization may fail due to several reasons, described in the following table. T he failure is
    # signaled using the telegram state byte.


    # 7.1 Table "A" – Command ErrorIDs 
    # If an error related to the execution of a function block occurs, the function block returns an ErrorID
    # to specify the error. The errors are stored in the PLC message buffer and are displayed on the
    # function block outputs.
    # In the PLC message buffer, they are dynamically arranged by the client to be displayed as follows:
    # <Origin> <MessageType> <Command name> <Description>
    # More information about the general message handling mechanism can be found in 5.5.11
    # Diagnostics.
    # The following table gives an overview over the existing ErrorIDs reported by commands and the
    # corresponding description.

    # ------------------------------------------------------
    # CLIENT ErrorIDs
    # ------------------------------------------------------

    ERR_VELOCITY_INVALID  = 0x8401
    """ 
    Client Specified Velocity not valid\n
    Commands using the parameter "Velocity"\n
    """

    ERR_ACCELERATION_INVALID  = 0x8402
    """ 
    Client Specified Acceleration not valid\n
    Commands using the parameter "Acceleration"\n
    """

    ERR_DECELERATION_INVALID  = 0x8403
    """ 
    Client Specified Deceleration not valid\n
    Commands using the parameter "Deceleration"\n
    """

    ERR_JERK_INVALID  = 0x8404
    """ 
    Client Specified Jerk not valid\n
    Commands using the parameter "Jerk"\n
    """

    ERR_CONFIGMODE_ELBOW_INVALID  = 0x8405
    """ 
    Client Invalid parameter value - ConfigMode Elbow\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_CONFIGMODE_SHOULDER_INVALID  = 0x8406
    """ 
    Client Invalid parameter value - ConfigMode Shoulder\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_CONFIGMODE_WRIST_INVALID  = 0x8407
    """ 
    Client Invalid parameter value - ConfigMode Wrist\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_TRAJECTORYMODE_INVALID  = 0x8409
    """ 
    Client Invalid parameter value - TrajectoryMode\n
    Commands using the parameter "TrajectoryMode"\n
    """

    ERR_OVERRIDE_INVALID  = 0x8410
    """ 
    Client Invalid parameter value - Override\n
    Commands using the parameter "Override"\n
    """

    ERR_ABORTINGMODE_INVALID  = 0x8411
    """ 
    Client Invalid parameter value - AbortingMode.\n
    Only 0: Buffer / 1: Abort are valid.\n
    Commands using the parameter "AbortingMode"\n
    """

    ERR_TOOLNO_RANGE  = 0x8412
    """ 
    Client Invalid parameter value - ToolNo outside of the allowed range -1..254\n
    Commands using the parameter "ToolNo"\n
    """

    ERR_TOOLNO_UNAVAILABLE  = 0x8413
    """ 
    Client Invalid parameter value - ToolNo not available on RC\n
    Commands using the parameter "ToolNo"\n
    """

    ERR_FRAMENO_RANGE  = 0x8414
    """ 
    Client Invalid parameter value - FrameNo outside of the allowed range -1..254\n
    Commands using the parameter "FrameNo"\n
    """

    ERR_FRAMENO_UNAVAILABLE  = 0x8415
    """ 
    Client Invalid parameter value - FrameNo not available on RC\n
    Commands using the parameter "FrameNo"\n
    """

    ERR_ACYCLICDATA_TOO_LARGE  = 0x8416
    """ 
    Client The array specified for AcyclicData exceeds the supported maximum length of 190 bytes\n
    Command "CallSubprogram"
    """

    ERR_RETURNACYCLICDATA_TRUNCATED  = 0x8417
    """ 
    Client The array length specified for ReturnAcyclicData is not sufficient for the returned data. The data has been truncated\n
    Command "CallSubprogram"\n
    """

    ERR_LOADNO_RANGE  = 0x8418
    """ 
    Client Invalid parameter value - LoadNo outside of the allowed range -1..254\n
    All commands\n
    """

    ERR_EXPORTMODE_NOT_EXIST = 0x8419
    """
    Invalid parameter value - the requested ExportMode does not exist
    """

    ERR_EXPORTNAME_NOT_EXIST = 0x8420
    """
    Invalid parameter value - the requested ExportName does not exist
    """

    ERR_EXPORTNAME_ALREADY_EXISTS = 0x8421
    """
    The given ExportName is already exist
    """

    ERR_DATALOG_NO_MEMORY_LEFT = 0x8422
    """
    No memory is left for data log
    """

    ERR_DATALOG_ERROR_OCCURRED = 0x8425
    """
    An Error occurred during data loging . Message encludes Error ID
    """

    ERR_INTERNAL_UNDEFINED_STEP = 0x8601
    """
    Internal System Error "Undefined Step" 
    """

    ERR_PROCESSINGMODE_NOT_DEFINED  = 0x8602
    """ 
    Client Specified ProcessingMode not defined\n
    Commands using the parameter "ProcessingMode"\n
    """

    ERR_PROCESSINGMODE_NOT_ALLOWED  = 0x8603
    """ 
    Client Specified ProcessingMode not allowed\n
    Commands using the parameter "ProcessingMode"\n
    """

    ERR_EMITTERID_NOT_ALLOWED = 0x8604
    """ 
    Client Specified Emitter ID not allowed\n
    Commands using the parameter "EmitterID"\n
    """

    ERR_LISTENERID_NOT_ALLOWED   = 0x8605
    """ 
    Client Specified Listener ID not allowed\n
    Commands using the parameter "ListenerID"\n
    """

    ERR_PROCSEQFLAG_CHANGED  = 0x8609,
    """ 
    Client ProcessingMode or SequenceFlag changed during execution\n
    Commands using the parameter "ProcessingMode" or "SequenceFlag"\n
    """

    ERR_PRIORITY_TOO_LOW = 0x8610
    """
    Specified priority to low 
    """

    ERR_PRIORITY_TOO_HIGH = 0x8611
    """
    Specified priority to high 
    """

    ERR_COMMANDS_NOT_ENABLED  = 0x8612
    """ 
    Client Commands are not Enabled (First Robot must be initialized)\n
    All commands\n
    """

    ERR_ROBOT_ERROR_NO_ID  = 0x8613
    """ 
    Client Error received from robot without error ID\n
    All commands\n
    """

    ERR_AXESGROUP_CHANGED  = 0x8614
    """ 
    Client AxesGroup changed during execution\n
    All commands\n
    """

    ERR_INTERNAL_ERROR_WITHOUT_ID = 0x8615
    """
    Internal System Error "Error without Error ID
    """

    ERR_SEQFLAG_NOT_ALLOWED  = 0x8616
    """
    Client Specified SEQ Flag not allowed\n
    Commands using the parameter "SequenceFlag"\n
    """

    ERR_AXESGROUP_CLEARED  = 0x8617
    """ 
    Client AxesGroup cleared during execution\n
    All commands\n
    """

    ERR_NO_FREE_ACR_ENTRY  = 0x8618
    """ 
    Client No free ACR entry available\n
    All commands\n
    """

    ERR_SEQFLAG_INVALID_IN_PROC_MODE  = 0x8625
    """ 
    Client Sequence flag must be 0 in the selected ProcessingMode\n
    Commands using the parameter "ProcessingMode" or "SequenceFlag"\n
    """

    ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO  = 0x8626
    """ 
    Client Specified Listener ID must be > 0 for selected trigger based ProcessingMode\n
    Commands using the parameter "ListenerID"\n
    """

    ERR_EMITTERID_MUST_BE_ZERO  = 0x8627
    """ 
    Client Specified Emitter ID must be 0\n
    Commands using the parameter "EmitterID"\n
    """

    ERR_LISTENERID_MUST_BE_POSITIVE  = 0x8635
    """ 
    Client Specified Listener ID must be a positive value (>= 0)\n
    Commands using the parameter "ListenerID"\n
    """


    # ------------------------------------------------------
    # SERVER ErrorIDs
    # ------------------------------------------------------

    ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_ENABLED = 0x8C01
    """ 
    Server Continue not possible - robot is not enabled\n
    Command "GroupContinue"\n
    """

    ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_IN_PRIMARY_POS = 0x8C02
    """ 
    Server Continue not possible - robot is not inPrimaryPosition\n
    Command "GroupContinue"\n
    """

    ERR_ROBOT_DISABLED  = 0x8C03
    """ 
    Server Robot disabled\n
    Command "EnableRobot"\n
    """

    ERR_ROBOT_DISABLED_BY_ERROR  = 0x8C04
    """ 
    Server Robot disabled due to an error\n
    Command "EnableRobot"\n
    """

    ERR_MANDATORY_CMDS_MISSING  = 0x8C05
    """ 
    Server Not all mandatory commands have been called yet\n
    Command "EnableRobot"n
    """

    ERR_RI_NOT_SYNCHRONIZED  = 0x8C06
    """ 
    Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies enabling in this state\n
    Command "EnableRobot"n
    """

    ERR_LIMIT_EXCEEDED_RETURN_POS  = 0x8C07
    """ 
    Server Limit exceeded. Move closer to return position\n
    Command "ReturnToPrimary"\n
    """

    ERR_SET_OPMODE_T1EXT_REQUIRED  = 0x8C08
    """ 
    Server Invalid parameter value - Must switch to T1Ext when changing between AutoExt and T2Ext\n
    Command "SetOperationMode"\n
    """

    ERR_WRITE_DYNAMIC_FRAME  = 0x8C09
    """ 
    Server Cannot write to a dynamic frame (frame used by e.g. conveyor tracking)\n
    Command "WriteFrameData"\n
    """

    ERR_CONTINUE_NOT_POSSIBLE_BY_MANUAL_MODE  = 0x8C10
    """ 
    Server Continue not possible in manual operation mode\n
    Command "GroupContinue"\n
    """

    ERR_FRAME_REFERENCING_INVALID  = 0x8C12
    """ 
    Server It is not allowed to reference a frame which already references another frame\n
    Command "WriteFrame"\n
    """

    ERR_FRAME_INVALID  = 0x8C13
    """ 
    Server The referenced Frame is invalid, dynamic (frame used by e.g. conveyor tracking) or does not exist\n
    Command "WriteFrame"\n
    """

    ERR_TOOLID_DIFFERS_TARGET  = 0x8C1
    """ 
    Server Currently used tool ID differs from the tool ID of the target position\n
    Command "ReturnToPrimary"\n
    """

    ERR_WRITE_FRAME_DURING_MOVE  = 0x8C15
    """ 
    Server Writing a Frame during an active movement is not supported by this RC\n
    Command "WriteFrame"\n
    """

    ERR_WRITE_TOOL_DURING_MOVE  = 0x8C16
    """ 
    Server Writing a Tool during an active movement is not supported by this RC\n
    Command "WriteToolData"\n
    """

    ERR_WRITE_LOAD_DURING_MOVE  = 0x8C17
    """ 
    Server Writing a Load during an active movement is not supported by this RC\n
    Command "WriteLoadData"\n
    """

    ERR_MANUAL_STEP_NOT_ALLOWED  = 0x8C20
    """ 
    Server ManualStep is not allowed in Automatic External\n
    Command "EnableRobot"\n
    """

    ERR_MANUAL_STEP_ONLY_IN_STEP_MODE_ALLOWED  = 0x8C21
    """ 
    Server ManualStep is only allowed when StepMode is active\n
    Command "EnableRobot"\n
    """

    ERR_TOOLDATA_DIFFERS  = 0x8C22
    """ 
    Server The current ToolData has changed and differs from the one when the primary position was left. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_LOADDATA_DIFFERS = 0x8C23
    """ 
    Server The current LoadData has changed and differs from the one when the primary position was left. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_FRAMEDATA_DIFFERS = 0x8C24
    """ 
    Server The current FrameData has changed and differs from the one when the primary position was left. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_REF_FRAMEDATA_CHANGED  = 0x8C25
    """ 
    Server The current reference FrameData has changed and differs from the one when the primary position was left. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_TOOLNO_DIFFERS_TARGET  = 0x8C26,
    """ 
    Server The ToolNo differs from the one in the return position. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_FRAMENO_DIFFERS_TARGET  = 0x8C27
    """ 
    Server The FrameNo differs from the one in the return position. Returning is not possible.\n
    Command "ReturnToPrimary"\n
    """

    ERR_CONTINUE_WHILE_STOPPING  = 0x8C28
    """ 
    Server Continue is not possible while the Robot is interrupting or stopping.\n
    Command "GroupContinue"\n
    """

    ERR_SOFTWARE_LIMITS_FOR_NON_EXISTING_AXIS  = 0x8C29
    """ 
    Server Software limits could not be set because values were specified for non-existing axes\n
    Command "WriteSWLimits"\n
    """

    ERR_RI_NOT_SYNCHRONIZED_CONTINUE_DENIED  = 0x8C30
    """ 
    Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies continue in this state\n
    Command "GroupContinue"\n
    """

    ERR_ENABLE_SWITCH_REQUIRED  = 0x8C31
    """ 
    Server Enable switch must be active to enable the robot\n
    Command "EnableRobot"\n
    """

    ERR_MANUAL_STEP_WHILE_DISABLED  = 0x8C32
    """ 
    Server Manual step sent while robot not enabled\n
    Command "EnableRobot"\n
    """

    ERR_JOG_NOT_ALLOWED_DURING_MOVE  = 0x8C33
    """ 
    Server Jog not possible during active movement\n
    Command "GroupJog"\n
    """

    ERR_TARGET_POS_FOR_NON_EXISTING_AXIS  = 0x8C34
    """ 
    Server Target position was commanded for an external axis which does not exist\n
    All move commands\n
    """

    ERR_JOG_AXIS_NOT_EXIST  = 0x8C35
    """ 
    Server Jog of axis is not possible. Axis does not exist\n
    Command "GroupJog"\n
    """

    ERR_INC_JOG_ONE_AXIS_ONLY  = 0x8C36
    """ 
    Server Incremental jog is only possible in one axis of rotation\n
    Command "GroupJog"\n
    """

    ERR_JOBID_NOT_EXIST  = 0x8C37
    """ 
    Server A program for the supplied JobID does not exist.\n
    Commands: "CallSubprogram", "StopSubprogram"\n
    """

    ERR_ONLY_ALLOWED_IN_SEQ_BUFFER  = 0x8C38
    """ 
    Server A program including motion commands is only allowed to be executed in a sequence buffer\n
    Command "CallSubprogram"\n
    """

    ERR_JOB_ALREADY_RUNNING  = 0x8C39
    """ 
    Server A program with the same number is already running. Multiple instances are not supported\
    Command "CallSubprogram"\n
    """

    ERR_JOBID_CHANGE_PM3_NOT_ALLOWED  = 0x8C42
    """ 
    Server Changing the JobID in PM 3 during runtime of this CMD is not supported.\n
    Command "CallSubprogram"\n
    """

    ERR_CONTINUE_DURING_STOPPING  = 0x8C43
    """ 
    Server Continue is not possible while the robot is stopping due to GroupInterrupt, GroupStop, SetSequence, or GroupJog\n
    Command "GroupContinue"\n
    """

    ERR_JOG_STOPPED_BY_ENABLE_RELEASED  = 0x8C52
    """ 
    Server GroupJog motion was stopped due to the release of the enable switch.\
    Command "GroupJog"\n
    """

    ERR_SWLIMITS_NOT_ALLOWED_ROBOT_IS_OUTSIDE  = 0x8C53
    """ 
    Server Setting the limits is not possible because the current robot position is currently outside of those limits.\
    Command "WriteSWLimits"\n
    """

    ERR_SWLIMITS_NOT_ALLOWED_DURING_MOVE  = 0x8C54
    """ 
    Server Setting the limits is not possible while a motion is active.\n
    Command "WriteSWLimits"\n
    """

    ERR_POSITION_NOT_REACHABLE = 0x8C55
    """
    Position not reachable.
    """

    ERR_OPMODE_CHANGE_NOT_POSSIBLE_BY_PLC  = 0x8C56,
    """ 
    Server Change of operation mode by the PLC not possible. The RC must be in an "External" operation mode\n
    Command "SetOperationMode"\n
    """

    ERR_AUXPOINT_IDENTICAL_WITH_OTHER_POS  = 0x8C57
    """ 
    Server Auxpoint must not be identical to start or end position of the motion\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_AUXPOINT_INVALID  = 0x8C58
    """ 
    Server Auxpoint invalid\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_CALC_NOT_POSSIBLE_BY_POS = 0x8C59,
    """ 
    Server Supplied positions must not be identical or at a larger distance apart\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_CALC_NOT_POSSIBLE_BY_PARA  = 0x8C60
    """ 
    Server Calculation not possible with the given parameters\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_CALC_NOT_POSSIBLE_BY_POS_ON_LINE = 0x8C61
    """ 
    Server Positions must not be on one line\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_INV_KINEMATIC_NO_SOLUTION = 0x8C62
    """ 
    Server No solution found for the given CartesianPosition\n
    Command "CalculateInverseKinematic"\n
    """

    ERR_INV_KINEMATIC_SOLUTION_OUTSIDE_SWLIMITS = 0x8C63
    """ 
    Server Solution is outside of the hardware limits\n
    Commands: "CalculateInverseKinematic", "CalculateForwardKinematic"\n
    """

    ERR_PARAM_WRITE_PROTECTED  = 0x8C64
    """ 
    Server The selected parameter is write protected and can thus not be changed\n
    Command "WriteSystemVariable"\n
    """

    ERR_POS_INDEX_OUT_OF_RANGE  = 0x8C65
    """ 
    Server Number of received positions exceeds the maximum expected number (index out of range)\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_POS_INDEX_MISMATCH  = 0x8C66
    """ 
    Server Number of received positions does not correspond to the required number for the selected mode\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_MAXIMUM_DISTANCE_EXCEEDED = 0x8C67
    """
    The defined MaximumDistance to the given target JointPosition has been exceeded. Move closer to the target or increase the MaximumDistance.
    """

    ERR_INVALID_SAFEREFERENCE_POSITION = 0x8C68
    """
    The given JointPosition does not match the RAs safe referencing position.
    """

    ERR_SAFETY_SENSOR_NOT_TRIGGERED = 0x8C69
    """
    The safety sensor did not trigger
    """

    ERR_RESTART_WHILE_ROBOT_MOVING = 0x8C70
    """
    Restart is only possible if the robot is not moving.
    """

    ERR_UNSUPPORTED_COMBINED_JOG = 0x8C71
    """
    Simultaneous rotational and translational jog is not supported 
    """

    ERR_GROUPRESET_PENDING_MESSAGES = 0x8C72
    """
    GroupReset not possible, as not all messages were transmitted yet 
    """

    ERR_INVALID_PARAM_ACCELERATION_RATE = 0x8D01,
    """ 
    Server Invalid parameter value - AccelerationRate\n
    Commands using the parameter "AccelerationRate"\n
    """

    ERR_INVALID_PARAM_BLENDING_MODE = 0x8D03
    """ 
    Server Invalid parameter value - BlendingMode\n
    Commands using the parameter "BlendingMode"\n
    """

    ERR_INVALID_PARAM_BLENDING_PARA  = 0x8D04
    """ 
    Server Invalid parameter value - BlendingParameter\n
    Commands using the parameter "BlendingParameter"\n
    """

    ERR_INVALID_PARAM_CONFIGMODE_ELBOW = 0x8D05
    """ 
    Server Invalid parameter value - ConfigMode Elbow\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_INVALID_PARAM_DECELERATION_RATE = 0x8D06
    """ 
    Server Invalid parameter value - DecelerationRate\n
    Commands using the parameter "DecelerationRate"\n
    """

    ERR_INVALID_PARAM_VALUE_ZERO = 0x8D07
    """ 
    Server Invalid parameter value - No value greater than zero\n
    Commands: "WriteDefaultDynamics", "WriteReferenceDynamics"\n
    """

    ERR_INVALID_PARAM_FRAMENO = 0x8D08
    """ 
    Server Invalid parameter value - FrameNo\n
    Commands using the parameter "FrameNo"\n
    """

    ERR_INVALID_PARAM_INC_ROTATION  = 0x8D09
    """ 
    Server Invalid parameter value - IncrementalRotation\n
    Command "GroupJog"\n
    """

    ERR_INVALID_PARAM_INC_TRANSLATION = 0x8D10
    """ 
    Server Invalid parameter value - IncrementalTranslation\n
    Command "GroupJog"\n
    """

    ERR_INVALID_PARAM_JERK_RATE = 0x8D11
    """ 
    Server Invalid parameter value - JerkRate\n
    Commands using the parameter "JerkRate"\n
    """


    ERR_INVALID_PARAM_JOG_POS_AND_JOG_NEG = 0x8D12
    """
    Server Invalid parameter value - Control Positive and negative jog direction was active at the same time\n
    Command "GroupJog"\n
    """

    ERR_INVALID_PARAM_JOINT_POS = 0x8D13
    """
    Server Invalid parameter value - JointPosition\n
    Commands using the parameter "JointPosition"\n
    """

    ERR_INVALID_PARAM_LIFE_SIGN_TIMEOUT = 0x8D14
    """
    Server Invalid parameter value - LifesignTimeout\n
    Command "ExchangeConfiguration"\n
    """

    ERR_INVALID_PARAM_SWLIMITS = 0x8D15,
    """ 
    Server Invalid parameter value - SoftwareLimits all values must not be zero\n
    Command "WriteRobotSWLimits"\n
    """

    ERR_INVALID_PARAM_LIMITVALUES = 0x8D16
    """
    Server Invalid parameter value - LimitValues\n
    Command "WriteRobotSWLimits"\n
    """

    ERR_INVALID_PARAM_LOADNO = 0x8D17
    """ 
    Server Invalid parameter value - LoadNo\n
    Commands using the parameter "LoadNo"\n
    """

    ERR_INVALID_PARAM_LOG_LEVEL = 0x8D18
    """ 
    Server Invalid parameter value - LogLevel\n
    Command "ExchangeConfiguration"\n
    """

    ERR_INVALID_PARAM_MODE = 0x8D21
    """ 
    Server Invalid parameter value - Mode\n
    Commands using the parameter "Mode"\n
    """

    ERR_INVALID_PARAM_ORI_MODE = 0x8D22
    """
    Server Invalid parameter value - OriMode\n
    Commands using the parameter "OriMode"\n
    """

    ERR_INVALID_PARAM_OVERRIDE = 0x8D23
    """ 
    Server Invalid parameter value - Override\n
    Commands using the parameter "Override"\n
    """

    ERR_INVALID_PARAM_POSITION = 0x8D24
    """
    Server Invalid parameter value - Position\n
    Commands using the parameter "Position"\n
    """

    ERR_INVALID_PARAM_REF_DYNAMICS_LESS_THAN_ZERO = 0x8D25
    """
    Server Invalid parameter value - ReferenceDynamics all values less than zero\n
    Command "WriteReferenceDynamics"\n
    """

    ERR_INVALID_PARAM_ACCELERATION = 0x8D26
    """
    Server Invalid parameter value - Acceleration\n
    Commands using the parameter "Acceleration"\n
    """

    ERR_INVALID_PARAM_DECELERATION = 0x8D27
    """
    Server Invalid parameter value - Deceleration\n
    Commands using the parameter "Deceleration"\n
    """

    ERR_INVALID_PARAM_JERK = 0x8D28
    """
    Server Invalid parameter value - Jerk\n
    Commands using the parameter "Jerk"\n
    """

    ERR_INVALID_PARAM_VELOCITY = 0x8D29
    """ 
    Server Invalid parameter value - Velocity\n
    Commands using the parameter "Velocity"\n
    """

    ERR_INVALID_PARAM_RETURN_MODE = 0x8D30
    """ 
    Server Invalid parameter value - ReturnMode\n
    Command "ReturnToPrimary"\n
    """

    ERR_INVALID_PARAM_TARGET_SEQUENCE = 0x8D31
    """ 
    Server Invalid parameter value - TargetSequence\n
    Command "SetSequence"\n
    """

    ERR_INVALID_PARAM_OPERATION_MODE = 0x8D32
    """
    Server Invalid parameter value - OperationMode\n
    Command "SetOperationMode"\n
    """

    ERR_INVALID_PARAM_SYNC_REACTION = 0x8D33
    """ 
    Server Invalid parameter value - SyncReaction\n
    Command "LRob_ExchangeConfiguration"\n
    """

    ERR_INVALID_PARAM_TIME = 0x8D34,
    """
    Server Invalid parameter value - Time\n
    Commands using the parameter "Time"\n
    """

    ERR_INVALID_PARAM_TOOLNO = 0x8D35
    """
    Server Invalid parameter value - ToolNo\n
    Commands using the parameter "ToolNo"\n
    """

    ERR_INVALID_PARAM_TRAJECTORY_MODE = 0x8D36
    """ 
    Server Invalid parameter value - TrajectoryMode\n
    Command "ReturnToPrimary"\n
    """

    ERR_INVALID_PARAM_TURN_MODE = 0x8D37
    """ 
    Server Invalid parameter value - TurnMode\n
    Commands using the parameter "TurnMode"\n
    """

    ERR_INVALID_PARAM_VELOCITY_MODE = 0x8D38
    """ 
    Server Invalid parameter value - VelocityRate\n
    Commands using the parameter "VelocityRate"\n
    """

    ERR_INVALID_PARAM_WAIT_FOR_NR_OF_CMD = 0x8D39
    """ 
    Server Invalid parameter value - WaitForNrOfCmd\n
    Command "LRob_ExchangeConfiguration"\n
    """

    ERR_INVALID_PARAM_CONFIG_MODE_SHOULDER = 0x8D40
    """
    Server Invalid parameter value - ConfigMode Shoulder\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_INVALID_PARAM_CONFIG_MODE_WRIST = 0x8D41
    """ 
    Server Invalid parameter value - ConfigMode Wrist\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_INVALID_PARAM_STEP_MODE = 0x8D42
    """
    Server Invalid parameter value - StepMode\n
    Commands using the parameter "StepMode"\n
    """

    ERR_STEP_MODE_NOT_VALID = 0x8D43
    """
    Server The supplied StopMode is not valid. Use 0, 1, or 2\n
    Command "StopSubprogram"\n
    """

    ERR_STOP_MODE_2_TARGETID_NEG1 = 0x8D44
    """ 
    Server When StopMode 2: (Stop all subprograms) is selected, the TargetID must be -1.\n
    Command "StopSubprogram"\n
    """

    ERR_STOP_MODE_0_TARGETID_NOT_NEG1 = 0x8D45
    """
    Server When StopMode 0: (Stop via JobID) is selected, the TargetID must NOT be -1.\n
    Command "StopSubprogram"\n
    """

    ERR_STOP_MODE_1_TARGETID_NOT_NEG1  = 0x8D46
    """
    Server When StopMode 1: (Stop via InstanceID) is selected, the TargetID must NOT be -1.\n
    Command "StopSubprogram"\n
    """

    ERR_INVALID_PARAM_INDEX_OUT_OF_RANGE = 0x8D47
    """
    Server Invalid parameter value - Index out of range\n
    All Commands\n
    """

    ERR_INVALID_PARAM_SAME_INDEX_MULTIPLE_TIMES = 0x8D48
    """
    Server Invalid parameter value - Same index was used multiple times\n
    Commands: "WriteDigitalOutputs", "WriteIntegers", "WriteReals", "WriteAnalogOutputs", "ReadDigitalInputs", "ReadDigitalOutputs", "ReadIntegers", "ReadReals"\n
    """

    ERR_INVALID_PARAM_MASS_EXCEEDS_PAYLOAD  = 0x8D49
    """ 
    Server Invalid parameter value - Specified mass greater than the maximum RA payload.\n
    Command "WriteLoad"\n
    """

    ERR_INVALID_PARAM_AT_LEAST_ONE_INDEX_REQUIRED  = 0x8D50
    """
    Server Invalid parameter value - At least one index must not be 0 and result in a read/write operation.\n
    Commands: "WriteDigitalOutputs", "WriteIntegers", "WriteReals", "WriteAnalogOutputs", "ReadDigitalInputs", "ReadDigitalOutputs", "ReadIntegers", "ReadReals"\n
    """

    ERR_INVALID_PARAM_MESSAGE_LEVEL = 0x8D51
    """
    Server Invalid parameter value - MessageLevel must be between 0-28\n
    Command "ReadMessages"\n
    """

    ERR_INVALID_PARAM_CIRCPLANE_MISMATCH_CIRCMODE = 0x8D61
    """ 
    Server Invalid parameter value - CircPlane does not match CircMode\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_INVALID_PARAM_CIRCMODE_OUT_OF_RANGE = 0x8D62
    """
    Server Invalid parameter value - CircMode outside of the allowed range 0..3\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_INVALID_PARAM_TOLERANCE_ONLY_CIRCMODE_1 = 0x8D63
    """
    Server Invalid parameter value - Tolerance must only be used for CircMode 1\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_INVALID_PARAM_ANGLE_ONLY_CIRCMODE_2 = 0x8D64
    """
    Server Invalid parameter value - Angle must only be used for CircMode 2\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_INVALID_PARAM_PATH_CHOICE_OUT_OF_RANGE = 0x8D65
    """
    Server Invalid parameter value - PathChoice outside of the allowed range 0..1\n
    Commands\
    """

    ERR_INVALID_PARAM_SHIFT_MODE_OUT_OF_RANGE = 0x8D66
    """ 
    Server Invalid parameter value - Mode outside of the allowed range 0..4\n
    Command "ShiftPosition"\n
    """

    ERR_INVALID_PARAM_ROTATION_ANGLE_ONLY_MODE_3 = 0x8D67
    """ 
    Server Invalid parameter value - RotationAngle only allowed in mode 3\n
    Command "ShiftPosition"\n
    """

    ERR_INVALID_PARAM_TRANSFORMATION_PARAM_2_INVALID = 0x8D68
    """
    Server Invalid parameter value - TransformationParameter_2 value does not match the selected mode\n
    Command "ShiftPosition"\n
    """

    ERR_INVALID_PARAM_TOOLNO_OUT_OF_RANGE = 0x8D69
    """ 
    Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on the RC\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_INVALID_PARAM_FRAMENO_OUT_OF_RANGE = 0x8D70
    """
    Server Invalid parameter value - FrameNo outside of the allowed range 0..254 or does not exist on the RC\n
    Command "CalculateCartesianPosition"\n
    """

    ERR_INVALID_PARAM_TARGET_TOOLNO_OUT_OF_RANGE = 0x8D71
    """ 
    Server Invalid parameter value - TargetToolNo outside of the allowed range 0..254 or does not exist on the RC\n
    Command "CalculateCartesianPosition"\n
    """

    ERR_INVALID_PARAM_TARGET_FRAMENO_OUT_OF_RANGE = 0x8D72
    """
    Server Invalid parameter value - TargetFrameNo outside of the allowed range 0..254 or does not exist on the RC\n
    Command "CalculateCartesianPosition"\n
    """

    ERR_INVALID_PARAM_ERR_TOOLNO_INVALID = 0x8D73
    """
    Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on the RC\n
    Command "CalculateCartesianPosition"\n
    """

    ERR_INVALID_PARAM_PARAMETER_ID_INVALID = 0x8D74
    """
    Server Invalid parameter value - ParameterID does not exist on the RC\n
    Commands: "ReadSystemVariable", "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_SUB_PARAMETER_ID_INVALID = 0x8D75
    """
    Server Invalid parameter value - SubParameterID does not exist on the RC for the supplied ParameterID\n
    Commands: "ReadSystemVariable", "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_SUB_PARAMETER_MUST_BE_ZERO = 0x8D76
    """
    Server Invalid parameter value - SubParameterID must be 0 for a parameter without subparameters\n
    Commands: "ReadSystemVariable", "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_SUB_PARAMETER_MUST_NOT_BE_ZERO = 0x8D77
    """ 
    Server Invalid parameter value - SubParameterID must not be 0 for a parameter with subparameters\n
    Commands: "ReadSystemVariable", "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_TYPE_OUT_OF_RANGE = 0x8D78
    """
    Server Invalid parameter value - DataType outside of the allowed range 1..13\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_TYPE_MISMATCH = 0x8D79
    """ 
    Server Invalid parameter value - DataType does not match the data type of the parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_0_INVALID = 0x8D80
    """ 
    Server Invalid parameter value - Data_0 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_1_INVALID = 0x8D81
    """ 
    Server Invalid parameter value - Data_1 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_2_INVALID = 0x8D82
    """
    Server Invalid parameter value - Data_2 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_3_INVALID = 0x8D83
    """ 
    Server Invalid parameter value - Data_3 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_4_INVALID = 0x8D84
    """ 
    Server Invalid parameter value - Data_4 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_5_INVALID = 0x8D85
    """ 
    Server Invalid parameter value - Data_5 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_DATA_6_INVALID = 0x8D86
    """
    Server Invalid parameter value - Data_6 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"
    """

    ERR_INVALID_PARAM_DATA_7_INVALID = 0x8D87
    """ 
    Server Invalid parameter value - Data_7 contains invalid data for the target parameter\n
    Command "WriteSystemVariable"\n
    """

    ERR_INVALID_PARAM_REFERENCE_FRAME_OUT_OF_RANGE = 0x8D88
    """ 
    Server Invalid parameter value - ReferenceFrame outside of the allowed range 0..254 or does not exist on the RC\n
    Command "CalculateFrame"\n
    """

    ERR_OPTIONAL_PARAM_DECELERATION_RATE_NOT_SUPPORTED = 0x8E03
    """ 
    Server Optional parameter value not supported - DecelerationRate\n
    Commands using the parameter "DecelerationRate"\n
    """

    ERR_OPTIONAL_PARAM_JERK_RATE_NOT_SUPPORTED = 0x8E04
    """
    Server Optional parameter value not supported - JerkRate\n
    Commands using the parameter "JerkRate"\n
    """

    ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED = 0x8E05
    """ 
    Server Optional parameter value not supported - BlendingMode\n
    Commands using the parameter "BlendingMode"\n
    """

    ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED = 0x8E06
    """ 
    Server Optional parameter value not supported - Time\n
    Commands using the parameter "Time"\n
    """

    ERR_OPTIONAL_PARAM_POSITION_NOT_SUPPORTED = 0x8E07
    """ 
    Server Optional parameter value not supported - Position\n
    Commands using the parameter "Position"\n
    """

    ERR_OPTIONAL_PARAM_ORI_MODE_NOT_SUPPORTED = 0x8E08
    """ 
    Server Optional parameter value not supported - OriMode\n
    Commands using the parameter "OriMode"\n
    """

    ERR_OPTIONAL_PARAM_CONFIG_MODE_NOT_SUPPORTED = 0x8E09
    """ 
    Server Optional parameter value not supported - ConfigMode\n
    Commands using the parameter "ConfigMode"\n
    """

    ERR_OPTIONAL_PARAM_TURN_MODE_NOT_SUPPORTED = 0x8E10
    """ 
    Server Optional parameter value not supported - TurnMode\n
    Commands using the parameter "TurnMode"\n
    """

    ERR_OPTIONAL_PARAM_TRAJECTORY_MODE_NOT_SUPPORTED = 0x8E11
    """ 
    Server Optional parameter value not supported - TrajectoryMode\n
    Command "ReturnToPrimary"\n
    """

    ERR_OPTIONAL_PARAM_OPERATION_MODE_NOT_SUPPORTED = 0x8E12
    """ 
    Server Optional parameter value not supported - OperationMode\n
    Command "SetOperationMode"\n
    """

    ERR_OPTIONAL_PARAM_INC_ROTATION_NOT_SUPPORTED = 0x8E13
    """ 
    Server Optional parameter value not supported - IncrementalRotation\n
    Command "GroupJog"\n
    """

    ERR_OPTIONAL_PARAM_INC_TRANSLATION_NOT_SUPPORTED = 0x8E14,
    """
    Server Optional parameter value not supported - IncrementalTranslation\n
    Command "GroupJog"\n
    """

    ERR_OPTIONAL_PARAM_STEP_MODE_EXACT_STOP_NOT_SUPPORTED = 0x8E16
    """ 
    Server Optional parameter value not supported - StepMode Exact Stop\n
    Command "EnableRobot"\n
    """

    ERR_OPTIONAL_PARAM_STEP_MODE_BLENDING_NOT_SUPPORTED = 0x8E17
    """ 
    Server Optional parameter value not supported - StepMode Blending\n
    Command "EnableRobot"\n
    """

    ERR_CONFIG_MODES_MUST_BE_IDENTICAL = 0x8E19
    """
    Only identical config modes for shoulder, elbow and wrist are supported.
    """

    ERR_OPTIONAL_PARAM_MODIFIED_CONVENTION_NOT_SUPPORTED = 0x8E20
    """ 
    Server Optional parameter value not supported - ModifiedConvention\n
    Command "ReadDHParameter"\n
    """

    ERR_OPTIONAL_PARAM_WAIT_AT_BLENDING_POINT_NOT_SUPPORTED = 0x8E21
    """ 
    Server Optional parameter value not supported - WaitAtBlendingPoint\n
    Command "ExchangeConfig"\n
    """

    ERR_OPTIONAL_PARAM_ANGLE_NOT_SUPPORTED = 0x8E23
    """ 
    Server Optional parameter not supported - Angle\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_OPTIONAL_PARAM_PATH_CHOICE_NOT_SUPPORTED = 0x8E24
    """
    Server Optional parameter not supported - PathChoice\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_OPTIONAL_PARAM_TOLERANCE_NOT_SUPPORTED = 0x8E25
    """ 
    Server Optional parameter not supported - Tolerance\n
    Commands: "MoveCircularAbsolute", "MoveCircularRelative", "MoveCircularCam"\n
    """

    ERR_OPTIONAL_PARAM_TRANSFORMATION_PARAM2_NOT_SUPPORTED = 0x8E26
    """ 
    Server Optional parameter not supported - TransformationParameter_2\n
    Command "ShiftPosition"\n
    """

    ERR_OPTIONAL_PARAM_ROTATION_ANGLE_NOT_SUPPORTED = 0x8E27
    """ 
    Server Optional parameter not supported - RotationAngle\n
    Command "ShiftPosition"\n
    """

    ERR_OPTIONAL_PARAM_VALUE_NOT_SUPPORTED = 0x8E28
    """ 
    Server Optional parameter value not supported - Mode\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_OPTIONAL_PARAM_EXTERNAL_TCP_NOT_SUPPORTED = 0x8E29
    """ 
    Server Optional parameter not supported - ExternalTCP\n
    Commands: "CalculateTool", "CalculateFrame"\n
    """

    ERR_OPTIONAL_PARAM_RELATIVE_POS_NOT_SUPPORTED = 0x8E30
    """ 
    Server Optional parameter not supported - RelativePosition\n
    Commands using the parameter "RelativePosition"\n
    """

    ERR_OPTIONAL_PARAM_MAXIMUM_DISTANCE_NOT_SUPPORTED = 0x8E31
    """
    Optional parameter not supported - Maximum Distance
    """

    ERR_OPTIONAL_PARAM_CIRCMODE_VALUE_NOT_SUPPORTED = 0x8E32
    """ 
    Optional parameter value not supported - CircMode
    """

    ERR_OPTIONAL_PARAM_IX_NOT_SUPPORTED = 0x8E33
    """ 
    Optional parameter not supported - IX
    """

    ERR_OPTIONAL_PARAM_IY_NOT_SUPPORTED = 0x8E34
    """ 
    Optional parameter not supported - IY
    """

    ERR_OPTIONAL_PARAM_IZ_NOT_SUPPORTED = 0x8E35
    """ 
    Optional parameter not supported - IZ
    """

    ERR_OPTIONAL_PARAM_RX_NOT_SUPPORTED = 0x8E36
    """ 
    Optional parameter not supported - RX
    """

    ERR_OPTIONAL_PARAM_RY_NOT_SUPPORTED = 0x8E37
    """ 
    Optional parameter not supported - RY
    """

    ERR_OPTIONAL_PARAM_RZ_NOT_SUPPORTED = 0x8E38
    """ 
    Optional parameter not supported - RZ
    """

    ERR_OPTIONAL_PARAM_INCREMENTAL_JOG_NOT_SUPPORTED = 0x8E39
    """ 
    Optional parameter not supported - IncrementalJog
    """

    ERR_EMITTER_ID_MUST_NOT_BE_ZERO = 0x8F04
    """ 
    Server Specified Emitter ID must not be 0\n
    Commands using the parameter "EmitterID"\n
    """

    ERR_INVALID_PARAM_EXECUTION_MODE = 0x8F10
    """ 
    Server Invalid parameter value - Execution mode\n
    All Commands\n
    """

    ERR_CMD_NOT_IMPLEMENTED = 0x8F11
    """ 
    Server Command not implemented\n
    All Commands\n
    """

    ERR_CMD_ONLY_ONE_INSTANCE_ALLOWED = 0x8F12  
    """ 
    Server Only one instance of this command is allowed\n
    Commands: "EnableRobot", "GroupJog", "ReturnToPrimary", "ExchangeConfig"\n
    """

    ERR_CMD_REQUIRES_INTERRUPT_OR_IDLE_STATE = 0x8F13
    """ 
    Server Command requires an active interrupt or idle state to be executed\n
    Commands: "GroupJog", "ReturnToPrimary"\n
    """

    ERR_CMD_NOT_ALLOWED_DURING_ACTIVE_INTERRUPT = 0x8F14
    """ 
    Server Command cannot be executed during active interrupt\n
    Command "ReturnToPrimary"\n
    """

    ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD = 0x8F15
    """ 
    Server Secondary sequence is blocked by command (e.g. GroupJog, ReturnToPrimary). No other commands may be buffered in secondary sequence\n
    All commands processed in secondary sequence\n
    """

    ERR_SECONDARY_SEQUENCE_NOT_ACTIVE = 0x8F16
    """ 
    Server The secondary sequence is not active. Commands may only be buffered in this sequence if it is active\n
    Commands using the parameter "SequenceFlag"\n
    """

    ERR_SECONDARY_SEQUENCE_NOT_EMPTY = 0x8F17
    """ 
    Server Secondary sequence is not empty. The command requires the secondary sequence to be empty\n
    Commands: "GroupJog", "ReturnToPrimary"\n
    """

    ERR_TRANSACTION_NOT_POSSIBLE_IN_STATE_MACHINE = 0x8F18
    """
    Server Transaction not possible in the state machine\n
    All commands\n
    """

    ERR_CMD_NOT_POSSIBLE_BY_OP_MODE_LOCAL = 0x8F19
    """ 
    Server Cannot execute command because current operation mode is local.\n
    Commands that are not available in local modes\n
    """

    ERR_CMD_TYPE_OUT_OF_RANGE = 0x8F20
    """ 
    Server Command type out of range\n
    All commands\n
    """

    ERR_CMD_NOT_POSSIBLE_DURING_CALL_SUB_PROGRAM = 0x8F21
    """ 
    Server Execution of this CMD is not possible while CallSubprogram is in progress in the sequence\n
    Commands: "SetSequence", "GroupJog"\n
    """

    ERR_OPERATION_NOT_POSSIBLE_SEE_LOG = 0x8F36
    """ 
    Server Operation not possible. See MessageLog for further information\n
    All commands\n
    """

    ERR_INTERNAL_ERROR_DURING_CMD = 0x8FFF
    """ 
    Server An RC internal error occurred during execution of this command. Check the message log for additional information\n
    All commands\n
    """

    # 7.2 Table "B" – RI ErrorIDs
    # RI errors can occur on the PLC as well as on the RC. In the event of an RI error on the PLC, the
    # corresponding ErrorID is written to the PLC message buffer independent of the function call
    # "ReadMessages". In the event of an RI error on the RC, the ErrorID is transmitted via the function
    # block "ReadMessages" and is also stored in PLC message buffer.
    # In the PLC message buffer, they are dynamically arranged by the client to be displayed as follows:
    # <Origin> <MessageType> <Description>
    # More information about the general message handling mechanism can be found in 5.5.11
    # Diagnostics.
    # The following table gives an overview over the existing "ErrorIDs" reported via RI errors and the
    # corresponding description.

    # ------------------------------------------------------
    # Client ErrorIDs
    # ------------------------------------------------------

    ERR_WRONG_TELEGRAM_STATE  = 0x8001
    """ 
    Client Wrong Telegram State (Two Sequences not in both directions active)
    """

    ERR_ACYCLIC_AREA_TO_SMALL_PLC_TO_ROB  = 0x8002
    """ 
    Client Acyclic area client to server too small
    """

    ERR_ACYCLIC_AREA_TO_SMALL_ROB_TO_PLC = 0x8003
    """ 
    Client Acyclic area server to client too small
    """

    ERR_LIFESIGN_TIMEOUT_0x8005 = 0x8004
    """ 
    Client Lifesign timeout
    """

    ERR_TELEGRAM_SEQ_TIMEOUT_0x8005 = 0x8005
    """ 
    Client Telegram sequence timeout
    """

    ERR_AXESGROUP_INVALID = 0x8007
    """
    Client Assigned AxesGroup not valid
    """

    ERR_PERIPHERY_INVALID = 0x8008
    """ 
    Client Assigned periphery not valid
    """

    ERR_INVALID_ROBOT_STATE = 0x8009
    """ 
    Client Invalid state of the robot (more than 1 CMD active)
    """

    ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT  = 0x8013
    """ 
    Client Telegram Number changed after initialization. Reinitialize by disabling and enabling the RobotTask.
    """

    ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0x80A1 = 0x80A1
    """ 
    Client Telegram control does not match the telegram state
    """

    ERR_INIT_LOST_UNKNOWN_0x80A2  = 0x80A2
    """ 
    Client Initialization lost for unknown reason. See message log after reinitializing
    """

    ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3  = 0x80A3
    """ 
    Client Telegram length does not match the length provided in the communication interface, or the communication interface is too small.
    """

    ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0x80A4  = 0x80A4
    """
    Client Incompatible major SRCI version
    """

    ERR_LIFESIGN_TIMEOUT_0x80A5 = 0x80A5
    """ 
    Client Lifesign timeout
    """

    ERR_CYCLIC_DATA_TOO_LARGE_0x80A6  = 0x80A6
    """ 
    Client The selected optional cyclic data does not fit in the given telegram size
    """

    ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7  = 0x80A7
    """ 
    Client The robot interface was reset after being initialized
    """

    ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8_0x80A8  = 0x80A8
    """ 
    Client Telegram sequence timeout
    """

    ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0x80A9 = 0x80A9
    """ 
    Client The telegram number changed after initialization
    """

    ERR_AXESGROUP_ID_INVALID_0x80AA  = 0x80AA
    """
    Client Error: Invalid AxesGroupID
    """

    ERR_TELEGRAM_NUMBER_INVALID_0x80AB  = 0x80AB
    """
    Client Telegram number is invalid. E.g. TwoSequences is only activated in one direction
    """

    ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0x80AC = 0x80AC
    """
    Client Telegram Number is not supported
    """

    ERR_ACR_REGISER_IS_FULL  = 0x8A01
    """ 
    Server The ACR is full. RA is disabled
    """

    ERR_MANDATORY_CMD_STOPPED  = 0x8A02
    """ 
    Server The execution of a mandatory command has been stopped. Exchange config must run for the system to run
    """

    ERR_INCONSISTENT_DATA_RECEIVED  = 0x8A03
    """ 
    Server Inconsistent data received. Make sure the complete telegram data is sent to RC in one frame.
    """

    ERR_CONNECTION_LOST  = 0x8AAD
    """ 
    Client Connection to the communication partner was lost
    """

    ERR_FATAL_ERROR_REINIT_REQUIRED  = 0x9001
    """ 
    Client Fatal Error occurred. Reinitialization of Robot_Task is required
    """


    # ------------------------------------------------------
    # SERVER ErrorIDs
    # ------------------------------------------------------

    ERR_INTERNAL_ERROR  = 0x9A01
    """ 
    Server Internal error
    """

    ERR_DESERIALIZE_ERROR  = 0x9A02
    """ 
    Server Internal error in deserialize
    """

    ERR_CMD_ID_OUT_OF_RANGE  = 0x9A03
    """
    Server CMD ID out of range 1.ACR_Length
    """

    ERR_FRAGMENT_LENGTH_INVALID = 0x9A04
    """ 
    Server Invalid fragment length
    """

    ERR_CMD_PRIORITY_CHANGED = 0x9A05
    """ 
    Server Command priority or type changed during runtime
    """

    ERR_TRIED_TO_RESET_NONEMPTY_ACR_REGISTER = 0x9A06
    """ 
    Server Tried to reset a non-empty ACR entry
    """

    ERR_SEQUENCE_PAYLOAD_INVALID_LENGTH = 0x9A07
    """ 
    Server Error: Invalid Sequence payload length (e.g., sequence payload length is specified 999 even if telegram length is only 100.)
    """

    ERR_ACTION_BYTE_INVALID = 0x9A08
    """ 
    Server Invalid ActionByte
    """

    ERR_CMD_PAYLOAD_LENGTH_INVALID = 0x9A09
    """ 
    Server Invalid Command payload length
    """

    ERR_CMD_PAYLOAD_POINTER_INVALID = 0x9A10
    """ 
    Server Error: Invalid Command payload pointer (e.g., Out of bounds)
    """

    ERR_EXEC_MODE_CHANGE_ILLEGAL = 0x9A14
    """
    Server Illegal Execution Mode change
    """

    # Set enum size for ctypes evaluation
    setattr(WORDEnum, 'ctypes_type', WORD)      