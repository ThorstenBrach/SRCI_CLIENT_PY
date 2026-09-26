"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      WarningIdEnum
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


class WarningIdEnum(WORDEnum):

    NO_WARNING = 0
    """
    No warning.
    """

    WARN_HIGHPRIORITY_IGNORED_SEQ_MODE = 0x7301
    """
    Client HighPriority Input is ignored when a sequential ProcessingMode is selected\n
    Commands: "WriteDigitalOutputs", "WriteIntegers", "WriteReals", "WriteAnalogOutputs\n
    """

    WARN_CYCLIC_DATA_DISABLED_STILL_ACTIVE = 0x7303
    """
    Client Optional Cyclic data was disabled by the user but is still enabled until reinitialization of RobotTask\n
    Command: "ReadActualPositionCyclic"\n
    """

    WARN_ACR_FREE_ENTRIES_LOW = 0x7605
    """
    Client Number of free entries in the ACR is running out\n
    All commands\n
    """

    WARN_PARAM_CHANGE_NOT_POSSIBLE_DEACTIVATE_FIRST_CTX = 0x7606
    """
    Change of parameters relevant to the execution context (e.g. ProcessingMode, SequenceFlag) is not possible. Deactivate first.\n
    """

    WARN_PARAM_CHANGE_NOT_POSSIBLE_DEACTIVATE_FIRST = 0x7607
    """
    Change of parameters is not possible. Deactivate first\n
    """

    WARN_FRAME_USED_IN_SEQUENCE = 0x7C03
    """
    Server The Frame is currently used in the sequence\n
    Command: "WriteFrameData"\n
    """

    WARN_TOOL_USED_IN_SEQUENCE = 0x7C04
    """
    Server The Tool is currently used in the sequence\n
    Command: "WriteToolData"\n
    """

    WARN_LOAD_USED_IN_SEQUENCE = 0x7C06
    """
    Server The Load is currently used in the sequence\n
    Command: "WriteLoadData"\n
    """

    WARN_HOLD_TO_RUN_REQUIRES_MOTION_IN_SEQUENCE = 0x7C08
    """
    HoldToRun not possible. One motion command must be in the sequence when HoldToRun is activated\n
    """

    WARN_TRIGGER_EVENT_WITHOUT_ASSOCIATED_ACTION = 0x7C12
    """
    Trigger event was emitted but no associated Action exists for specified EmitterID\n
    """

    WARN_TRIGGER_MODE2_NOT_SUPPORTED_FOR_ALL_MOVES = 0x7C13
    """
    Trigger Mode 2 (Distance in mm) is not possible for all move commands (e.g. MoveAxes)\n
    """

    WARN_MONITORING_DOES_NOT_APPLY_TO_BUFFERED_CMDS = 0x7C14
    """
    Server The monitoring does not apply to motion CMDs which are already buffered.\n
    Command: "SetTriggerMotion" \n
    """

    WARN_SAFE_REFERENCING_VELOCITY_REDUCED = 0x7C15
    """
    Motion velocity is reduced as Safe Referencing is required.\n
    """

    WARN_SAFE_REFERENCING_ADDITIONAL_STEPS_REQUIRED = 0x7C16
    """
    Additional steps are required to complete the SafeReferencing. Check the MessageLog for further information.\n
    """

    WARN_ACYCLIC_RANGE_PLC_TO_ROB_VERY_SMALL = 0x7001
    """
    Client Acyclic range client to server very small\n
    """

    WARN_ACYCLIC_RANGE_ROB_TO_PLC_VERY_SMALL = 0x7002
    """
    Client Acyclic range server to client very small\n
    """

    WARN_TELEGRAM_NO_CHANGED_DURING_OPERATION = 0x7003
    """
    Client Telegram number was changed during operation\n
    """

    WARN_SAVE_TOOL_FAILED = 0x7005
    """
    Client Save Tool locally failed. Index not available in user data.\n
    """

    WARN_SAVE_FRAME_FAILED = 0x7006
    """
    Client Save Frame locally failed. Index not available in user data.\n
    """

    WARN_SAVE_LOAD_FAILED = 0x7007
    """
    Client Save Load locally failed. Index not available in user data.\n
    """

    WARN_SAVE_WORKAREA_FAILED = 0x7008
    """
    Client Save WorkArea locally failed. Index not available in user data.\n
    """

    WARN_TOOL_DATA_ARRAY_NOT_START_AT_ZERO = 0x7009
    """
    Client Array of tool data supplied to RobotTask does not start at 0.\n
    """

    WARN_TOOL_DATA_ARRAY_TOO_SHORT = 0x7010
    """
    Client Array of tool data supplied to RobotTask must be longer than the number of tools on the RC.\n
    """

    WARN_TOOL_DATA_SYNC_MODE_INVALID = 0x7011
    """
    Client Tool data sync mode is invalid.\n
    """

    WARN_TOOL_NUMBER_SYNC_ERROR = 0x7012
    """
    Client Error Sync with Tool \"NUMBER\" (Please Enter a valid SyncMode)\n
    """

    WARN_TOOL_SYNC_BOTH_SIDES_CHANGED = 0x7013
    """
    Client Error Sync Data changed in both Sides with Tool \"NUMBER\" (Please Enter a valid SyncMode)\n
    """

    WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO = 0x7015
    """
    Client Array of frame data supplied to RobotTask does not start at 0.\n
    """

    WARN_FRAME_DATA_ARRAY_TOO_SHORT = 0x7016
    """
    Client Array of frame data supplied to RobotTask must be longer than the number of frames on the RC.\n
    """

    WARN_FRAME_DATA_SYNC_MODE_INVALID = 0x7017
    """
    Client Frame data sync mode is invalid.\n
    """

    WARN_FRAME_NUMBER_SYNC_ERROR = 0x7018
    """
    Client Error Sync with Frame "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_FRAME_SYNC_BOTH_SIDES_CHANGED = 0x7019
    """
    Client Error Sync Data changed in both Sides with Frame "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_LOAD_DATA_ARRAY_NOT_START_AT_ZERO = 0x7021
    """
    Client Array of load data supplied to RobotTask does not start at 0.\n
    """

    WARN_LOAD_DATA_ARRAY_TOO_SHORT = 0x7022
    """
    Client Array of load data supplied to RobotTask must be longer than the number of tools on the RC.\n
    """

    WARN_LOAD_DATA_SYNC_MODE_INVALID = 0x7023
    """
    Client Load data sync mode is invalid.\n
    """

    WARN_LOAD_NUMBER_SYNC_ERROR = 0x7024
    """
    Client Error Sync with Load "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_LOAD_SYNC_BOTH_SIDES_CHANGED = 0x7025
    """
    Client Error Sync Data changed in both Sides with Load "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_WORK_AREA_ARRAY_NOT_START_AT_ZERO = 0x7027
    """
    Client Array of workarea data supplied to RobotTask does not start at 0.\n
    """

    WARN_WORK_AREA_ARRAY_TOO_SHORT = 0x7028
    """
    Client Array of workarea data supplied to RobotTask must be longer than the number of tools on the RC.\n
    """

    WARN_WORK_AREA_SYNC_MODE_INVALID = 0x7029
    """
    Client Workarea data sync mode is invalid.\n
    """

    WARN_WORK_AREA_NUMBER_SYNC_ERROR = 0x7030
    """
    Client Error Sync with WorkArea "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_WORK_AREA_SYNC_BOTH_SIDES_CHANGED = 0x7031
    """
    Client Error Sync Data changed in both Sides with WorkArea "NUMBER" (Please Enter a valid SyncMode)\n
    """

    WARN_SW_LIMITS_SYNC_MODE_INVALID = 0x7033
    """
    Client Software limits data sync mode is invalid.\n
    """

    WARN_SW_LIMITS_SYNC_ERROR = 0x7034
    """
    Client Error Sync with Software Limits (Please Enter a valid SyncMode)\n
    """

    WARN_SW_LIMITS_SYNC_BOTH_SIDES_CHANGED = 0x7035
    """
    Client Error Sync Data changed in both Sides with Software Limits (Please Enter a valid SyncMode)\n
    """

    WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID = 0x7037
    """
    Client Default dynamics data sync mode is invalid.\n
    """

    WARN_DEFAULT_DYNAMICS_SYNC_ERROR = 0x7038
    """
    Client Error Sync with Default Dynamics (Please Enter a valid SyncMode)\n
    """

    WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED = 0x7039
    """
    Client Error Sync Data changed in both Sides with Default Dynamics (Please Enter a valid SyncMode)\n
    """

    WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID = 0x7041
    """
    Client Reference dynamics data sync mode is invalid.\n
    """

    WARN_REFERENCE_DYNAMICS_SYNC_ERROR = 0x7042
    """
    Client Error Sync with Reference Dynamics (Please Enter a valid SyncMode)\n
    """

    WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED = 0x7043
    """
    Client Error Sync Data changed in both Sides with Reference Dynamics (Please Enter a valid SyncMode)\n
    """

    WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7044
    """
    Client Synchronization of tool is not possible due to error in the read or write tool cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7045
    """
    Client Synchronization of frame is not possible due to error in the read or write frame cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7046
    """
    Client Synchronization of load is not possible due to error in the read or write load cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7047
    """
    Client Synchronization of swLimits is not possible due to error in the read or write swLimits cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7048
    """
    Client Synchronization of referenceDynamics is not possible due to error in the read or write referenceDynamics cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7049
    """
    Client Synchronization of defaultDynamics is not possible due to error in the read or write defaultDynamics cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_LEGACY_SRCI_ENCODING = 0x7050
    """
    Client Using the legacy SRCI version encoding. It will not be compatible with the newest RC interpreter versions.\n
    """

    WARN_INVALID_ROBOT_STATE_MULTIPLE_CMDS_ACTIVE = 0x7051
    """
    Invalid state of the robot (more than 1 CMD active)
    """

    # {warning 'ToDo: No event for WorkArea defined in specification V1.3 !!!'}
    WARN_WORK_AREA_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD = 0x7052
    """
    Client Synchronization of workarea is not possible due to error in the read or write load cmd.\n
    See dedicated message log entry for more information.\n
    """

    WARN_ACR_ALMOST_FULL = 0x7A01
    """
    Server The ACR is almost full. Filling it completely disables the robot.\n
    Make sure to limit the number of commands in the system.\n
    """
    # Set enum size for ctypes evaluation
    setattr(WORDEnum, 'ctypes_type', WORD)        