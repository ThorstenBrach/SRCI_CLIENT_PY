"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      InfoIdEnum
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


class InfoIdEnum(WORDEnum):
    NO_INFO = 0
    """
    No info.
    """

    INFO_COLLISION_DETECTED = 0x6C01
    """
    Server Collision detected\n
    Motion commands\n
    """

    INFO_MOTION_ERROR = 0x6C02
    """
    Server Error occurred during motion. Check the message buffer for more information\n
    Motion commands\n
    """

    INFO_TARGET_POS_UNREACHABLE = 0x6C03
    """
    Server Target position not reachable\n
    Motion commands\n
    """

    INFO_SW_LIMITS_REACHED = 0x6C04
    """
    Server Software limits reached\n
    Motion commands\n
    """

    INFO_ABORT_BY_GROUP_STOP = 0x6C05
    """
    Server Abortion of this command was requested by a GroupStop\n
    All sequence related commands\n
    """

    INFO_ABORT_BY_MOTION_CMD = 0x6C06
    """
    Server Abortion of this command was requested by another motion command\n
    All sequence related commands\n
    """

    INFO_READ_SW_LIMITS = 0x6C07
    """
    Server Reading the currently used software limits. Updated software limits are active after restart.\n
    Command "ReadRobotSWLimits"\n
    """

    INFO_NO_ACTIVE_SUBPROGRAM = 0x6C09
    """
    Server No SubProgram was stopped because none was active\n
    Command "StopSubprogram"\n
    """

    INFO_JOBID_NOT_RUNNING = 0x6C11
    """
    Server A program for the supplied JobID is not running or does not exist.\n
    Command "StopSubprogram"\n
    """

    INFO_INSTANCEID_NOT_RUNNING = 0x6C12
    """
    Server A program for the supplied InstanceID is not running or does not exist.\n
    Command "StopSubprogram"\n
    """

    INFO_WAITING_AT_BLEND_ZONE = 0x6C13
    """Server The robot is waiting at the blending zone.\n
    Motion commands\n
    """

    INFO_JOG_INTERRUPTED_BY_GROUP_STOP = 0x6C14
    """
    Server Jog motion was interrupted by GroupStop\n
    Command "GroupJog"\n
    """

    INFO_JOG_INTERRUPTED_BY_RA_STATE = 0x6C15
    """
    Server Jog motion was interrupted by RA sequence state INTERRUPTED\n
    Command "GroupJog"\n
    """

    INFO_MANUAL_START_IGNORED_DURING_EMPTY_SEQ = 0x6C19
    """
    Server Manual start is ignored when the sequence is empty\n
    Command "EnableRobot"\n
    """

    INFO_PARAM_INDEX_ZERO_NOT_WRITEABLE = 0x6D51
    """
    Server Invalid parameter value - A value was given for index 0. Index 0 is not writeable. Remove the value or change the index.\n
    Commands: "WriteIntegers", "WriteReals", "WriteAnalogOutputs", "ReadDigitalInputs", "ReadDigitalOutputs", "ReadIntegers", "ReadReals"\n
    """

    INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_NON_ZERO_INDEX = 0x6D52
    """
    Server Invalid parameter value OutputBitmask - No bitmask was given for a non zero index. Set the index to zero, or set a valid bitmask.\n
    Command "WriteDigitalOutputs"\n
    """

    INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_ZERO_INDEX = 0x6D53
    """
    Server Invalid parameter value OutputBitmask - A bitmask was given for a zero index. Set the bitmask to zero, or set a non zero index.\n
    Command "WriteDigitalOutputs"\n
    """

    INFO_CMD_INTERRUPTED_BY_RA_STATE = 0x6F01
    """
    Server Command interrupted due to RA sequence state INTERRUPTED\n
    All sequence related commands\n
    """

    INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED = 0x6F02
    """
    Server Command interrupted due to RA power state NOT_ENABLED\n
    All sequence related commands\n
    """

    INFO_CMD_INTERRUPTED_BY_RA_SEQ_STATE_DURING_STEP_MODE = 0x6F03
    """
    Server Command interrupted due to RA sequence state INTERRUPTED while single step mode is active\n
    All sequence related commands\n
    """

    INFO_RESET_WARNINGS_BY_INTERNAL_CODE = 0x00FF
    """
    Server Internal code used to reset warnings\n
    All commands\n
    """

    INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS = 0x6001
    """
    Client Lifesign smaller than lower limit. It has been increased to 10ms.\n
    """

    INFO_RECV_EXT_CART_POS_NOT_USABLE_WITH_RECV_CART_POS = 0x6002
    """
    Client ReceiveExtendedCartesianPosition cannot be used without ReceiveCartesianPos. RecCarPos is automatically activated.\n
    """

    INFO_RECV_EXT_JOINT_POS_NOT_USABLE_WITH_RECV_JOINT_POS = 0x6003
    """
    Client ReceiveExtendedJointPosition cannot be used without ReceiveJointPosition. RecJointPos is automatically activated.\n
    """

    INFO_SYNC_TOOL_DATA_DISABLED = 0x6014
    """
    Client Synchronization of tool data is disabled, and the data is different on the RC. Tool = "NUMBER" (Please Enter a valid SyncMode)\n
    """

    INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6015
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (TOOL)\n
    """

    INFO_SYNC_FRAME_DATA_DISABLED = 0x6020
    """
    Client Synchronization of frame data is disabled, and the data is different on the RC. Frame = "NUMBER" (Please Enter a valid SyncMode)\n
    """

    INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6021
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (FRAME)\n
    """

    INFO_SYNC_LOAD_DATA_DISABLED = 0x6026
    """
    Client Synchronization of load data is disabled, and the data is different on the RC. Load = "NUMBER" (Please Enter a valid SyncMode)\n
    """

    INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6027
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (LOAD)\n
    """

    INFO_SYNC_WORK_AREA_DISABLED = 0x6032
    """
    Client Synchronization of work area data is disabled, and the data is different on the RC. WorkArea = "NUMBER" (Please Enter a valid SyncMode)\n
    """

    INFO_CHANGE_WORK_AREA_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6033
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (WORKAREA)\n
    """

    INFO_SYNC_SWLIMIT_DISABLED = 0x6036
    """
    Client Synchronization of Software Limits data is disabled, and the data is different on the RC.\n
    """

    INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6037
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (SW LIMITS)\n
    """

    INFO_SYNC_DEFAULT_DYNAMICS_DISABLED = 0x6040
    """
    Client Synchronization of default dynamics data is disabled, and the data is different on the RC.\n
    """

    INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6041
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (DEFAULT DYNAMICS)\n
    """

    INFO_SYNC_REFERENCE_DYNAMICS_DISABLED = 0x6044
    """
    Client Synchronization of reference dynamics data is disabled, and the data is different on the RC.\n
    """

    INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED = 0x6045
    """
    Client Change the Syncmode to Negative only works on Startup with PLC (REFERENCE DYNAMICS)\n
    """

    INFO_CONTINUOUS_UPDATE_NOT_POSSIBLE = 0x6650
    """
    Continuous updating of parameters relevant to the execution context (e.g. ProcessingMode, SequenceFlag) is not possible\n
    """

    INFO_CMD_BOUND_TO_INSTANCE_CONTINUOUS_MODE = 0x6651
    """
    Command is bound to instance on RC while executed in continuous processing mode. Reexecution is not possible before deactivating\n
    """

    INFO_CMD_BOUND_TO_INSTANCE_TRIGGER_MODE = 0x6652
    """
    Command is bound to instance on RC while executed in trigger-based processing mode. Reexecution is not possible before deactivating\n
    """

    INFO_RA_DISABLED_BY_OPMODE_CHANGE = 0x6A01
    """
    Server RA disabled due to operation mode change\n
    """

    INFO_OPERATION_MODE_CHANGED = 0x6A02
    """
    Server Operation mode changed\n
    """

    INFO_SERVER_STATE_RESET_BY_CLIENT_REQUEST = 0x6A03
    """
    Server The server state has been reset on client request. Client restart may be a cause.\n
    """

    INFO_OVERRIDE_DECREASED_TO_PREVENT_EXEEDING_MONITORING_VELOCITY = 0x6A07
    """
    Server The actual override has been decreased to not exceed a movement's monitoring velocity.\n
    """

    INFO_EXCESSIVE_LOGGING = 0x6A13
    """
    Server Excessive logging may degrade system performance.\n
    """

    INFO_FIRST_MOTION_REDUCED_VELOCITY = 0x6C08
    """
    Server The first motion is executed with reduced velocity.\n
    """

    INFO_INTERNAL_ERROR_DURING_CMD = 0x8FFF
    """
    Server An RC internal error occurred during execution of this command. Check the message log for additional information\n
    """
    
    # Set enum size for ctypes evaluation
    setattr(WORDEnum, 'ctypes_type', WORD)        