# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      MESSAGE_CODE_TO_STRING
#  Author:      Thorsten Brach
#  Date:        2025-03-31
#
#  Description:
#
#
#  Copyright:
#    (C) 2025 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""MESSAGE_CODE_TO_STRING

ST-Source: Functions/Convert/TO_STRING/MESSAGE_CODE_TO_STRING.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.functions.String.StrReplace import StrReplace
from srci.iec.conv import DWORD_TO_STRING
from srci.types import RobotLibraryErrorIdEnum, RobotLibraryInfoIdEnum, RobotLibraryWarningIdEnum

__all__ = ['MESSAGE_CODE_TO_STRING']


def MESSAGE_CODE_TO_STRING(*, MessageCode: int = 0) -> str:
    MESSAGE_CODE_TO_STRING: str = ''

    match MessageCode:

        # ---------------------------------
        # Info ID's
        # ---------------------------------
        case RobotLibraryInfoIdEnum.INFO_COLLISION_DETECTED:
            MESSAGE_CODE_TO_STRING = 'Server Collision detected'

        case RobotLibraryInfoIdEnum.INFO_MOTION_ERROR:
            MESSAGE_CODE_TO_STRING = 'Server Error occurred during motion. Check the message buffer for more information'

        case RobotLibraryInfoIdEnum.INFO_TARGET_POS_UNREACHABLE:
            MESSAGE_CODE_TO_STRING = 'Server Target position not reachable'

        case RobotLibraryInfoIdEnum.INFO_SW_LIMITS_REACHED:
            MESSAGE_CODE_TO_STRING = 'Server Software limits reached'

        case RobotLibraryInfoIdEnum.INFO_ABORT_BY_GROUP_STOP:
            MESSAGE_CODE_TO_STRING = 'Server Abortion of this command was requested by a GroupStop'

        case RobotLibraryInfoIdEnum.INFO_ABORT_BY_MOTION_CMD:
            MESSAGE_CODE_TO_STRING = 'Server Abortion of this command was requested by another motion command'

        case RobotLibraryInfoIdEnum.INFO_READ_SW_LIMITS:
            MESSAGE_CODE_TO_STRING = 'Server Reading the currently used software limits. Updated software limits are active after restart.'

        case RobotLibraryInfoIdEnum.INFO_NO_ACTIVE_SUBPROGRAM:
            MESSAGE_CODE_TO_STRING = 'Server No SubProgram was stopped because none was active'

        case RobotLibraryInfoIdEnum.INFO_JOBID_NOT_RUNNING:
            MESSAGE_CODE_TO_STRING = 'Server A program for the supplied JobID is not running or does not exist.'

        case RobotLibraryInfoIdEnum.INFO_INSTANCEID_NOT_RUNNING:
            MESSAGE_CODE_TO_STRING = 'Server A program for the supplied InstanceID is not running or does not exist.'

        case RobotLibraryInfoIdEnum.INFO_WAITING_AT_BLEND_ZONE:
            MESSAGE_CODE_TO_STRING = 'Server The robot is waiting at the blending zone.'

        case RobotLibraryInfoIdEnum.INFO_JOG_INTERRUPTED_BY_GROUP_STOP:
            MESSAGE_CODE_TO_STRING = 'Server Jog motion was interrupted by GroupStop'

        case RobotLibraryInfoIdEnum.INFO_JOG_INTERRUPTED_BY_RA_STATE:
            MESSAGE_CODE_TO_STRING = 'Server Jog motion was interrupted by RA sequence state INTERRUPTED'

        case RobotLibraryInfoIdEnum.INFO_MANUAL_START_IGNORED_DURING_EMPTY_SEQ:
            MESSAGE_CODE_TO_STRING = 'Server Manual start is ignored when the sequence is empty'

        case RobotLibraryInfoIdEnum.INFO_PARAM_INDEX_ZERO_NOT_WRITEABLE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - A value was given for index 0. Index 0 is not writeable. Remove the value or change the index.'

        case RobotLibraryInfoIdEnum.INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_NON_ZERO_INDEX:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value OutputBitmask - No bitmask was given for a non zero index. Set the index to zero, or set a valid bitmask.'

        case RobotLibraryInfoIdEnum.INFO_PARAM_OUTPUT_BITMASK_INVALID_FOR_ZERO_INDEX:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value OutputBitmask - A bitmask was given for a zero index. Set the bitmask to zero, or set a non zero index.'

        case RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_STATE:
            MESSAGE_CODE_TO_STRING = 'Server Command interrupted due to RA sequence state INTERRUPTED'

        case RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_NOT_ENABLED:
            MESSAGE_CODE_TO_STRING = 'Server Command interrupted due to RA power state NOT_ENABLED'

        case RobotLibraryInfoIdEnum.INFO_CMD_INTERRUPTED_BY_RA_SEQ_STATE_DURING_STEP_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Command interrupted due to RA sequence state INTERRUPTED while single step mode is active'

        case RobotLibraryInfoIdEnum.INFO_RESET_WARNINGS_BY_INTERNAL_CODE:
            MESSAGE_CODE_TO_STRING = 'Server Internal code used to reset warnings'

        case RobotLibraryInfoIdEnum.INFO_LIFESIGN_TIMEOUT_TO_SMALL_AND_SET_TO_10MS:
            MESSAGE_CODE_TO_STRING = 'Client Lifesign smaller than lower limit. It has been increased to 10ms.'

        case RobotLibraryInfoIdEnum.INFO_RECV_EXT_CART_POS_NOT_USABLE_WITH_RECV_CART_POS:
            MESSAGE_CODE_TO_STRING = 'Client ReceiveExtendedCartesianPosition cannot be used without ReceiveCartesianPos. RecCarPos is automatically activated.'

        case RobotLibraryInfoIdEnum.INFO_RECV_EXT_JOINT_POS_NOT_USABLE_WITH_RECV_JOINT_POS:
            MESSAGE_CODE_TO_STRING = 'Client ReceiveExtendedJointPosition cannot be used without ReceiveJointPosition. RecJointPos is automatically activated.'

        case RobotLibraryInfoIdEnum.INFO_SYNC_TOOL_DATA_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of tool data is disabled, and the data is different on the RC. Tool = "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_TOOL_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (TOOL)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_FRAME_DATA_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of frame data is disabled, and the data is different on the RC. Frame = "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_FRAME_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (FRAME)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_LOAD_DATA_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of load data is disabled, and the data is different on the RC. Load = "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_LOAD_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (LOAD)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_WORK_AREA_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of work area data is disabled, and the data is different on the RC. WorkArea = "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_WORK_AREA_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (WORKAREA)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_SWLIMIT_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of Software Limits data is disabled, and the data is different on the RC.'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_SWLIMITS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (SW LIMITS)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_DEFAULT_DYNAMICS_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of default dynamics data is disabled, and the data is different on the RC.'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_DEFAULT_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (DEFAULT DYNAMICS)'

        case RobotLibraryInfoIdEnum.INFO_SYNC_REFERENCE_DYNAMICS_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of reference dynamics data is disabled, and the data is different on the RC.'

        case RobotLibraryInfoIdEnum.INFO_CHANGE_REFERENCE_DYNAMICS_SYNC_MODE_TO_NEGATIVE_ONLY_AT_PLC_START_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Change the Syncmode to Negative only works on Startup with PLC (REFERENCE DYNAMICS)'

        case RobotLibraryInfoIdEnum.INFO_RA_DISABLED_BY_OPMODE_CHANGE:
            MESSAGE_CODE_TO_STRING = 'Server RA disabled due to operation mode change'

        case RobotLibraryInfoIdEnum.INFO_OPERATION_MODE_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Server Operation mode changed'

        case RobotLibraryInfoIdEnum.INFO_SERVER_STATE_RESET_BY_CLIENT_REQUEST:
            MESSAGE_CODE_TO_STRING = 'Server The server state has been reset on client request. Client restart may be a cause.'

        case RobotLibraryInfoIdEnum.INFO_OVERRIDE_DECREASED_TO_PREVENT_EXEEDING_MONITORING_VELOCITY:
            MESSAGE_CODE_TO_STRING = 'Server The actual override has been decreased to not exceed a movements monitoring velocity.'

        case RobotLibraryInfoIdEnum.INFO_EXCESSIVE_LOGGING:
            MESSAGE_CODE_TO_STRING = 'Server Excessive logging may degrade system performance.'

        case RobotLibraryInfoIdEnum.INFO_FIRST_MOTION_REDUCED_VELOCITY:
            MESSAGE_CODE_TO_STRING = 'Server The first motion is executed with reduced velocity.'

        # ---------------------------------
        # Warning ID's
        # ---------------------------------
        case RobotLibraryWarningIdEnum.WARN_HIGHPRIORITY_IGNORED_SEQ_MODE:
            MESSAGE_CODE_TO_STRING = 'Client HighPriority Input is ignored when a sequential ProcessingMode is selected'

        case RobotLibraryWarningIdEnum.WARN_CYCLIC_DATA_DISABLED_STILL_ACTIVE:
            MESSAGE_CODE_TO_STRING = 'Client Optional Cyclic data was disabled by the user but is still enabled until reinitialization of RobotTask'

        case RobotLibraryWarningIdEnum.WARN_ACR_FREE_ENTRIES_LOW:
            MESSAGE_CODE_TO_STRING = 'Client Number of free entries in the ACR is running out'

        case RobotLibraryWarningIdEnum.WARN_FRAME_USED_IN_SEQUENCE:
            MESSAGE_CODE_TO_STRING = 'Server The Frame is currently used in the sequence'

        case RobotLibraryWarningIdEnum.WARN_TOOL_USED_IN_SEQUENCE:
            MESSAGE_CODE_TO_STRING = 'Server The Tool is currently used in the sequence'

        case RobotLibraryWarningIdEnum.WARN_LOAD_USED_IN_SEQUENCE:
            MESSAGE_CODE_TO_STRING = 'Server The Load is currently used in the sequence'

        case RobotLibraryWarningIdEnum.WARN_MONITORING_DOES_NOT_APPLY_TO_BUFFERED_CMDS:
            MESSAGE_CODE_TO_STRING = 'Server The monitoring does not apply to motion CMDs which are already buffered.'

        case RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_PLC_TO_ROB_VERY_SMALL:
            MESSAGE_CODE_TO_STRING = 'Client Acyclic range client to server very small'

        case RobotLibraryWarningIdEnum.WARN_ACYCLIC_RANGE_ROB_TO_PLC_VERY_SMALL:
            MESSAGE_CODE_TO_STRING = 'Client Acyclic range server to client very small'

        case RobotLibraryWarningIdEnum.WARN_TELEGRAM_NO_CHANGED_DURING_OPERATION:
            MESSAGE_CODE_TO_STRING = 'Client Telegram number was changed during operation'

        case RobotLibraryWarningIdEnum.WARN_SAVE_TOOL_FAILED:
            MESSAGE_CODE_TO_STRING = 'Client Save Tool locally failed. Index not available in user data.'

        case RobotLibraryWarningIdEnum.WARN_SAVE_FRAME_FAILED:
            MESSAGE_CODE_TO_STRING = 'Client Save Frame locally failed. Index not available in user data.'

        case RobotLibraryWarningIdEnum.WARN_SAVE_LOAD_FAILED:
            MESSAGE_CODE_TO_STRING = 'Client Save Load locally failed. Index not available in user data.'

        case RobotLibraryWarningIdEnum.WARN_SAVE_WORKAREA_FAILED:
            MESSAGE_CODE_TO_STRING = 'Client Save WorkArea locally failed. Index not available in user data.'

        case RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_NOT_START_AT_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Array of tool data supplied to RobotTask does not start at 0.'

        case RobotLibraryWarningIdEnum.WARN_TOOL_DATA_ARRAY_TOO_SHORT:
            MESSAGE_CODE_TO_STRING = 'Client Array of tool data supplied to RobotTask must be longer than the number of tools on the RC.'

        case RobotLibraryWarningIdEnum.WARN_TOOL_DATA_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Tool data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_TOOL_NUMBER_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Tool "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Tool "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_NOT_START_AT_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Array of frame data supplied to RobotTask does not start at 0.'

        case RobotLibraryWarningIdEnum.WARN_FRAME_DATA_ARRAY_TOO_SHORT:
            MESSAGE_CODE_TO_STRING = 'Client Array of frame data supplied to RobotTask must be longer than the number of frames on the RC.'

        case RobotLibraryWarningIdEnum.WARN_FRAME_DATA_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Frame data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_FRAME_NUMBER_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Frame "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Frame "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_LOAD_DATA_ARRAY_NOT_START_AT_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Array of load data supplied to RobotTask does not start at 0.'

        case RobotLibraryWarningIdEnum.WARN_LOAD_DATA_ARRAY_TOO_SHORT:
            MESSAGE_CODE_TO_STRING = 'Client Array of load data supplied to RobotTask must be longer than the number of tools on the RC.'

        case RobotLibraryWarningIdEnum.WARN_LOAD_DATA_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Load data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_LOAD_NUMBER_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Load "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Load "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_WORK_AREA_ARRAY_NOT_START_AT_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Array of workarea data supplied to RobotTask does not start at 0.'

        case RobotLibraryWarningIdEnum.WARN_WORK_AREA_ARRAY_TOO_SHORT:
            MESSAGE_CODE_TO_STRING = 'Client Array of workarea data supplied to RobotTask must be longer than the number of tools on the RC.'

        case RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Workarea data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_WORK_AREA_NUMBER_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with WorkArea "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_WORK_AREA_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with WorkArea "NUMBER" (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Software limits data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Software Limits (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Software Limits (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Default dynamics data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Default Dynamics (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Default Dynamics (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_MODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Reference dynamics data sync mode is invalid.'

        case RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_ERROR:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync with Reference Dynamics (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_BOTH_SIDES_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client Error Sync Data changed in both Sides with Reference Dynamics (Please Enter a valid SyncMode)'

        case RobotLibraryWarningIdEnum.WARN_TOOL_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of tool is not possible due to error in the read or write tool cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_FRAME_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of frame is not possible due to error in the read or write frame cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_LOAD_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of load is not possible due to error in the read or write load cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_SW_LIMITS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of swLimits is not possible due to error in the read or write swLimits cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_REFERENCE_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of referenceDynamics is not possible due to error in the read or write referenceDynamics cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_DEFAULT_DYNAMICS_SYNC_FAILED_BY_ERROR_OF_READ_OR_WRITE_CMD:
            MESSAGE_CODE_TO_STRING = 'Client Synchronization of defaultDynamics is not possible due to error in the read or write defaultDynamics cmd. See dedicated message log entry for more information.'

        case RobotLibraryWarningIdEnum.WARN_LEGACY_SRCI_ENCODING:
            MESSAGE_CODE_TO_STRING = 'Client Using the legacy SRCI version encoding. It will not be compatible with the newest RC interpreter versions.'

        case RobotLibraryWarningIdEnum.WARN_ACR_ALMOST_FULL:
            MESSAGE_CODE_TO_STRING = 'Server The ACR is almost full. Filling it completely disables the robot. Make sure to limit the number of commands in the system.'

        # ---------------------------------
        # Error ID's
        # ---------------------------------
        case RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD:
            MESSAGE_CODE_TO_STRING = 'Invalid command parameter - see log file for details (LogLevel Error)'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0xA1:
            MESSAGE_CODE_TO_STRING = 'Telegram control does not match the telegram state'

        case RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0xA2:
            MESSAGE_CODE_TO_STRING = 'Initialization lost for unknown reason. See message log after reinitializing'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0xA3:
            MESSAGE_CODE_TO_STRING = 'Telegram length does not match the length provided in the communication interface.'

        case RobotLibraryErrorIdEnum.ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0xA4:
            MESSAGE_CODE_TO_STRING = 'Incompatible major SRCI version'

        case RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0xA5:
            MESSAGE_CODE_TO_STRING = 'Lifesign timeout'

        case RobotLibraryErrorIdEnum.ERR_CYCLIC_DATA_TOO_LARGE_0xA6:
            MESSAGE_CODE_TO_STRING = 'The selected optional cyclic data does not fit in the given telegram size'

        case RobotLibraryErrorIdEnum.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0xA7:
            MESSAGE_CODE_TO_STRING = 'The robot interface was reset after being initialized'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_SEQ_TIMEOUT_0xA8:
            MESSAGE_CODE_TO_STRING = 'Telegram sequence timeout'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0xA9:
            MESSAGE_CODE_TO_STRING = 'The telegram number changed after initialization'

        case RobotLibraryErrorIdEnum.ERR_AXESGROUP_ID_INVALID_0xAA:
            MESSAGE_CODE_TO_STRING = 'Invalid AxesGroupID'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_INVALID_0xAB:
            MESSAGE_CODE_TO_STRING = 'Telegram number is invalid. E.g. TwoSequences is only activated in one direction'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0xAC:
            MESSAGE_CODE_TO_STRING = 'Telegram Number is not supported'

        case RobotLibraryErrorIdEnum.ERR_SERVER_CONNECTION_LOST_0xAD:
            MESSAGE_CODE_TO_STRING = 'Server Connection to the communication partner was lost'

        case RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Specified Velocity not valid'

        case RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Specified Acceleration not valid'

        case RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Specified Deceleration not valid'

        case RobotLibraryErrorIdEnum.ERR_JERK_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Specified Jerk not valid'

        case RobotLibraryErrorIdEnum.ERR_CONFIGMODE_ELBOW_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - ConfigMode Elbow'

        case RobotLibraryErrorIdEnum.ERR_CONFIGMODE_SHOULDER_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - ConfigMode Shoulder'

        case RobotLibraryErrorIdEnum.ERR_CONFIGMODE_WRIST_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - ConfigMode Wrist'

        case RobotLibraryErrorIdEnum.ERR_TRAJECTORYMODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - TrajectoryMode'

        case RobotLibraryErrorIdEnum.ERR_OVERRIDE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - Override'

        case RobotLibraryErrorIdEnum.ERR_ABORTINGMODE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - AbortingMode. Only 0: Buffer / 1: Abort are valid.'

        case RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - ToolNo outside of the allowed range -1..254'

        case RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - ToolNo not available on RC'

        case RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - FrameNo outside of the allowed range -1..254'

        case RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - FrameNo NOT available on RC'

        case RobotLibraryErrorIdEnum.ERR_ACYCLICDATA_TOO_LARGE:
            MESSAGE_CODE_TO_STRING = 'Client The array specified for AcyclicData exceeds the supported maximum length of 190 bytes'

        case RobotLibraryErrorIdEnum.ERR_RETURNACYCLICDATA_TRUNCATED:
            MESSAGE_CODE_TO_STRING = 'Client The array length specified for ReturnAcyclicData is not sufficient for the returned data. The data has been truncated'

        case RobotLibraryErrorIdEnum.ERR_LOADNO_RANGE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid parameter value - LoadNo outside of the allowed range -1..254'

        case RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED:
            MESSAGE_CODE_TO_STRING = 'Client Specified ProcessingMode not defined'

        case RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Specified ProcessingMode not allowed'

        case RobotLibraryErrorIdEnum.ERR_EMITTERID_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Specified Emitter ID not allowed'

        case RobotLibraryErrorIdEnum.ERR_LISTENERID_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Specified Listener ID not allowed'

        case RobotLibraryErrorIdEnum.ERR_PROCSEQFLAG_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client ProcessingMode or SequenceFlag changed during execution'

        case RobotLibraryErrorIdEnum.ERR_COMMANDS_NOT_ENABLED:
            MESSAGE_CODE_TO_STRING = 'Client Commands are not Enabled (First Robot must be initialized)'

        case RobotLibraryErrorIdEnum.ERR_ROBOT_ERROR_NO_ID:
            MESSAGE_CODE_TO_STRING = 'Client Error received from robot without error ID'

        case RobotLibraryErrorIdEnum.ERR_AXESGROUP_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Client AxesGroup changed during execution'

        case RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Client Specified SEQ Flag not allowed'

        case RobotLibraryErrorIdEnum.ERR_AXESGROUP_CLEARED:
            MESSAGE_CODE_TO_STRING = 'Client AxesGroup cleared during execution'

        case RobotLibraryErrorIdEnum.ERR_NO_FREE_ACR_ENTRY:
            MESSAGE_CODE_TO_STRING = 'Client No free ACR entry available'

        case RobotLibraryErrorIdEnum.ERR_SEQFLAG_INVALID_IN_PROC_MODE:
            MESSAGE_CODE_TO_STRING = 'Client Sequence flag must be 0 in the selected ProcessingMode'

        case RobotLibraryErrorIdEnum.ERR_LISTENERID_MUST_BE_GREATER_THAN_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Specified Listener ID must be > 0 for selected trigger based ProcessingMode'

        case RobotLibraryErrorIdEnum.ERR_EMITTERID_MUST_BE_ZERO:
            MESSAGE_CODE_TO_STRING = 'Client Specified Emitter ID must be 0'

        case RobotLibraryErrorIdEnum.ERR_LISTENERID_MUST_BE_POSITIVE:
            MESSAGE_CODE_TO_STRING = 'Client Specified Listener ID must be a positive value (>= 0)'

        case RobotLibraryErrorIdEnum.ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_ENABLED:
            MESSAGE_CODE_TO_STRING = 'Server Continue not possible - robot is not enabled'

        case RobotLibraryErrorIdEnum.ERROR_CONTINUE_NOT_POSSIBLE_BY_NOT_IN_PRIMARY_POS:
            MESSAGE_CODE_TO_STRING = 'Server Continue not possible - robot is not inPrimaryPosition'

        case RobotLibraryErrorIdEnum.ERR_ROBOT_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Server Robot disabled'

        case RobotLibraryErrorIdEnum.ERR_ROBOT_DISABLED_BY_ERROR:
            MESSAGE_CODE_TO_STRING = 'Server Robot disabled due to an error'

        case RobotLibraryErrorIdEnum.ERR_MANDATORY_CMDS_MISSING:
            MESSAGE_CODE_TO_STRING = 'Server Not all mandatory commands have been called yet'

        case RobotLibraryErrorIdEnum.ERR_RI_NOT_SYNCHRONIZED:
            MESSAGE_CODE_TO_STRING = 'Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies enabling in this state'

        case RobotLibraryErrorIdEnum.ERR_LIMIT_EXCEEDED_RETURN_POS:
            MESSAGE_CODE_TO_STRING = 'Server Limit exceeded. Move closer to return position'

        case RobotLibraryErrorIdEnum.ERR_SET_OPMODE_T1EXT_REQUIRED:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Must switch to T1Ext when changing between AutoExt and T2Ext'

        case RobotLibraryErrorIdEnum.ERR_WRITE_DYNAMIC_FRAME:
            MESSAGE_CODE_TO_STRING = 'Server Cannot write to a dynamic frame (frame used by e.g. conveyor tracking)'

        case RobotLibraryErrorIdEnum.ERR_CONTINUE_NOT_POSSIBLE_BY_MANUAL_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Continue not possible in manual operation mode'

        case RobotLibraryErrorIdEnum.ERR_FRAME_REFERENCING_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server It is not allowed to reference a frame which already references another frame'

        case RobotLibraryErrorIdEnum.ERR_FRAME_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server The referenced Frame is invalid, dynamic (frame used by e.g. conveyor tracking) or does not exist'

        case RobotLibraryErrorIdEnum.ERR_TOOLID_DIFFERS_TARGET:
            MESSAGE_CODE_TO_STRING = 'Server Currently used tool ID differs from the tool ID of the target position'

        case RobotLibraryErrorIdEnum.ERR_WRITE_FRAME_DURING_MOVE:
            MESSAGE_CODE_TO_STRING = 'Server Writing a Frame during an active movement is not supported by this RC'

        case RobotLibraryErrorIdEnum.ERR_WRITE_TOOL_DURING_MOVE:
            MESSAGE_CODE_TO_STRING = 'Server Writing a Tool during an active movement is not supported by this RC'

        case RobotLibraryErrorIdEnum.ERR_WRITE_LOAD_DURING_MOVE:
            MESSAGE_CODE_TO_STRING = 'Server Writing a Load during an active movement is not supported by this RC'

        case RobotLibraryErrorIdEnum.ERR_MANUAL_STEP_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Server ManualStep is not allowed in Automatic External'

        case RobotLibraryErrorIdEnum.ERR_MANUAL_STEP_ONLY_IN_STEP_MODE_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Server ManualStep is only allowed when StepMode is active'

        case RobotLibraryErrorIdEnum.ERR_TOOLDATA_DIFFERS:
            MESSAGE_CODE_TO_STRING = 'Server The current ToolData has changed and differs from the one when the primary position was left. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_LOADDATA_DIFFERS:
            MESSAGE_CODE_TO_STRING = 'Server The current LoadData has changed and differs from the one when the primary position was left. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_FRAMEDATA_DIFFERS:
            MESSAGE_CODE_TO_STRING = 'Server The current FrameData has changed and differs from the one when the primary position was left. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_REF_FRAMEDATA_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Server The current reference FrameData has changed and differs from the one when the primary position was left. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_TOOLNO_DIFFERS_TARGET:
            MESSAGE_CODE_TO_STRING = 'Server The ToolNo differs from the one in the return position. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_FRAMENO_DIFFERS_TARGET:
            MESSAGE_CODE_TO_STRING = 'Server The FrameNo differs from the one in the return position. Returning is not possible.'

        case RobotLibraryErrorIdEnum.ERR_CONTINUE_WHILE_STOPPING:
            MESSAGE_CODE_TO_STRING = 'Server Continue is not possible while the Robot is interrupting or stopping.'

        case RobotLibraryErrorIdEnum.ERR_SOFTWARE_LIMITS_FOR_NON_EXISTING_AXIS:
            MESSAGE_CODE_TO_STRING = 'Server Software limits could not be set because values were specified for non-existing axes'

        case RobotLibraryErrorIdEnum.ERR_RI_NOT_SYNCHRONIZED_CONTINUE_DENIED:
            MESSAGE_CODE_TO_STRING = 'Server RI state is NOT_SYNCHRONIZED and the respective syncReaction denies continue in this state'

        case RobotLibraryErrorIdEnum.ERR_ENABLE_SWITCH_REQUIRED:
            MESSAGE_CODE_TO_STRING = 'Server Enable switch must be active to enable the robot'

        case RobotLibraryErrorIdEnum.ERR_MANUAL_STEP_WHILE_DISABLED:
            MESSAGE_CODE_TO_STRING = 'Server Manual step sent while robot not enabled'

        case RobotLibraryErrorIdEnum.ERR_JOG_NOT_ALLOWED_DURING_MOVE:
            MESSAGE_CODE_TO_STRING = 'Server Jog not possible during active movement'

        case RobotLibraryErrorIdEnum.ERR_TARGET_POS_FOR_NON_EXISTING_AXIS:
            MESSAGE_CODE_TO_STRING = 'Server Target position was commanded for an external axis which does not exist'

        case RobotLibraryErrorIdEnum.ERR_JOG_AXIS_NOT_EXIST:
            MESSAGE_CODE_TO_STRING = 'Server Jog of axis is not possible. Axis does not exist'

        case RobotLibraryErrorIdEnum.ERR_INC_JOG_ONE_AXIS_ONLY:
            MESSAGE_CODE_TO_STRING = 'Server Incremental jog is only possible in one axis of rotation'

        case RobotLibraryErrorIdEnum.ERR_JOBID_NOT_EXIST:
            MESSAGE_CODE_TO_STRING = 'Server A program for the supplied JobID does not exist.'

        case RobotLibraryErrorIdEnum.ERR_ONLY_ALLOWED_IN_SEQ_BUFFER:
            MESSAGE_CODE_TO_STRING = 'Server A program including motion commands is only allowed to be executed in a sequence buffer'

        case RobotLibraryErrorIdEnum.ERR_JOB_ALREADY_RUNNING:
            MESSAGE_CODE_TO_STRING = 'Server A program with the same number is already running. Multiple instances are not supported'

        case RobotLibraryErrorIdEnum.ERR_JOBID_CHANGE_PM3_NOT_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Server Changing the JobID in PM 3 during runtime of this CMD is not supported.'

        case RobotLibraryErrorIdEnum.ERR_CONTINUE_DURING_STOPPING:
            MESSAGE_CODE_TO_STRING = 'Server Continue is not possible while the robot is stopping due to GroupInterrupt, GroupStop, SetSequence, or GroupJog'

        case RobotLibraryErrorIdEnum.ERR_JOG_STOPPED_BY_ENABLE_RELEASED:
            MESSAGE_CODE_TO_STRING = 'Server GroupJog motion was stopped due to the release of the enable switch.'

        case RobotLibraryErrorIdEnum.ERR_SWLIMITS_NOT_ALLOWED_ROBOT_IS_OUTSIDE:
            MESSAGE_CODE_TO_STRING = 'Server Setting the limits is not possible because the current robot position is currently outside of those limits.'

        case RobotLibraryErrorIdEnum.ERR_SWLIMITS_NOT_ALLOWED_DURING_MOVE:
            MESSAGE_CODE_TO_STRING = 'Server Setting the limits is not possible while a motion is active.'

        case RobotLibraryErrorIdEnum.ERR_OPMODE_CHANGE_NOT_POSSIBLE_BY_PLC:
            MESSAGE_CODE_TO_STRING = 'Server Change of operation mode by the PLC not possible. The RC must be in an "External" operation mode'

        case RobotLibraryErrorIdEnum.ERR_AUXPOINT_IDENTICAL_WITH_OTHER_POS:
            MESSAGE_CODE_TO_STRING = 'Server Auxpoint must not be identical to start or end position of the motion'

        case RobotLibraryErrorIdEnum.ERR_AUXPOINT_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Auxpoint invalid'

        case RobotLibraryErrorIdEnum.ERR_CALC_NOT_POSSIBLE_BY_POS:
            MESSAGE_CODE_TO_STRING = 'Server Supplied positions must not be identical or at a larger distance apart'

        case RobotLibraryErrorIdEnum.ERR_CALC_NOT_POSSIBLE_BY_PARA:
            MESSAGE_CODE_TO_STRING = 'Server Calculation not possible with the given parameters'

        case RobotLibraryErrorIdEnum.ERR_CALC_NOT_POSSIBLE_BY_POS_ON_LINE:
            MESSAGE_CODE_TO_STRING = 'Server Positions must not be on one line'

        case RobotLibraryErrorIdEnum.ERR_INV_KINEMATIC_NO_SOLUTION:
            MESSAGE_CODE_TO_STRING = 'Server No solution found for the given CartesianPosition'

        case RobotLibraryErrorIdEnum.ERR_INV_KINEMATIC_SOLUTION_OUTSIDE_SWLIMITS:
            MESSAGE_CODE_TO_STRING = 'Server Solution is outside of the hardware limits'

        case RobotLibraryErrorIdEnum.ERR_PARAM_WRITE_PROTECTED:
            MESSAGE_CODE_TO_STRING = 'Server The selected parameter is write protected and can thus not be changed'

        case RobotLibraryErrorIdEnum.ERR_POS_INDEX_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Number of received positions exceeds the maximum expected number (index out of range)'

        case RobotLibraryErrorIdEnum.ERR_POS_INDEX_MISMATCH:
            MESSAGE_CODE_TO_STRING = 'Server Number of received positions does not correspond to the required number for the selected mode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ACCELERATION_RATE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - AccelerationRate'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_BLENDING_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - BlendingMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_BLENDING_PARA:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - BlendingParameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_CONFIGMODE_ELBOW:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ConfigMode Elbow'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DECELERATION_RATE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - DecelerationRate'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_VALUE_ZERO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - No value greater than zero'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_FRAMENO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - FrameNo'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_INC_ROTATION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - IncrementalRotation'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_INC_TRANSLATION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - IncrementalTranslation'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_JERK_RATE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - JerkRate'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_JOG_POS_AND_JOG_NEG:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Control Positive and negative jog direction was active at the same time'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_JOINT_POS:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - JointPosition'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_LIFE_SIGN_TIMEOUT:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - LifesignTimeout'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SWLIMITS:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - SoftwareLimits all values must not be zero'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_LIMITVALUES:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - LimitValues'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_LOADNO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - LoadNo'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_LOG_LEVEL:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - LogLevel'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Mode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ORI_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - OriMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_OVERRIDE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Override'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_POSITION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Position'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_REF_DYNAMICS_LESS_THAN_ZERO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ReferenceDynamics all values less than zero'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ACCELERATION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Acceleration'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DECELERATION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Deceleration'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_JERK:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Jerk'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_VELOCITY:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Velocity'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_RETURN_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ReturnMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TARGET_SEQUENCE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TargetSequence'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_OPERATION_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - OperationMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SYNC_REACTION:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - SyncReaction'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TIME:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Time'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TOOLNO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ToolNo'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TRAJECTORY_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TrajectoryMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TURN_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TurnMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_VELOCITY_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - VelocityRate'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_WAIT_FOR_NR_OF_CMD:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - WaitForNrOfCmd'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_CONFIG_MODE_SHOULDER:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ConfigMode Shoulder'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_CONFIG_MODE_WRIST:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ConfigMode Wrist'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_STEP_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - StepMode'

        case RobotLibraryErrorIdEnum.ERR_STEP_MODE_NOT_VALID:
            MESSAGE_CODE_TO_STRING = 'Server The supplied StopMode is not valid. Use 0, 1, or 2'

        case RobotLibraryErrorIdEnum.ERR_STOP_MODE_2_TARGETID_NEG1:
            MESSAGE_CODE_TO_STRING = 'Server When StopMode 2: (Stop all subprograms) is selected, the TargetID must be -1.'

        case RobotLibraryErrorIdEnum.ERR_STOP_MODE_0_TARGETID_NOT_NEG1:
            MESSAGE_CODE_TO_STRING = 'Server When StopMode 0: (Stop via JobID) is selected, the TargetID must NOT be -1.'

        case RobotLibraryErrorIdEnum.ERR_STOP_MODE_1_TARGETID_NOT_NEG1:
            MESSAGE_CODE_TO_STRING = 'Server When StopMode 1: (Stop via InstanceID) is selected, the TargetID must NOT be -1.'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_INDEX_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Index out of range'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SAME_INDEX_MULTIPLE_TIMES:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Same index was used multiple times'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_MASS_EXCEEDS_PAYLOAD:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Specified mass greater than the maximum RA payload.'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_AT_LEAST_ONE_INDEX_REQUIRED:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - At least one index must not be 0 and result in a read/write operation.'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_MESSAGE_LEVEL:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - MessageLevel must be between 0-28'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_CIRCPLANE_MISMATCH_CIRCMODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - CircPlane does not match CircMode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_CIRCMODE_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - CircMode outside of the allowed range 0..3'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TOLERANCE_ONLY_CIRCMODE_1:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Tolerance must only be used for CircMode 1'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ANGLE_ONLY_CIRCMODE_2:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Angle must only be used for CircMode 2'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_PATH_CHOICE_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - PathChoice outside of the allowed range 0..1'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SHIFT_MODE_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Mode outside of the allowed range 0..4'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ROTATION_ANGLE_ONLY_MODE_3:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - RotationAngle only allowed in mode 3'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TRANSFORMATION_PARAM_2_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TransformationParameter_2 value does not match the selected mode'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TOOLNO_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_FRAMENO_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - FrameNo outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TARGET_TOOLNO_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TargetToolNo outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_TARGET_FRAMENO_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - TargetFrameNo outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_ERR_TOOLNO_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ToolNo outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_PARAMETER_ID_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ParameterID does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SUB_PARAMETER_ID_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - SubParameterID does not exist on the RC for the supplied ParameterID'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SUB_PARAMETER_MUST_BE_ZERO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - SubParameterID must be 0 for a parameter without subparameters'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_SUB_PARAMETER_MUST_NOT_BE_ZERO:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - SubParameterID must NOT be 0 FOR a parameter with subparameters'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_TYPE_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - DataType outside of the allowed range 1..13'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_TYPE_MISMATCH:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - DataType does not match the data type of the parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_0_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_0 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_1_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_1 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_2_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_2 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_3_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_3 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_4_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_4 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_5_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_5 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_6_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_6 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_DATA_7_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Data_7 contains invalid data for the target parameter'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_REFERENCE_FRAME_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - ReferenceFrame outside of the allowed range 0..254 or does not exist on the RC'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_DECELERATION_RATE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - DecelerationRate'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_JERK_RATE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - JerkRate'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_BLENDING_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - BlendingMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TIME_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - Time'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_POSITION_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - Position'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_ORI_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - OriMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_CONFIG_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - ConfigMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TURN_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - TurnMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TRAJECTORY_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - TrajectoryMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_OPERATION_MODE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value NOT supported - OperationMode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_INC_ROTATION_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - IncrementalRotation'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_INC_TRANSLATION_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - IncrementalTranslation'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_STEP_MODE_EXACT_STOP_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - StepMode Exact Stop'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_STEP_MODE_BLENDING_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - StepMode Blending'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_MODIFIED_CONVENTION_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - ModifiedConvention'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_WAIT_AT_BLENDING_POINT_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - WaitAtBlendingPoint'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_ANGLE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - Angle'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_PATH_CHOICE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - PathChoice'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TOLERANCE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - Tolerance'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_TRANSFORMATION_PARAM2_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - TransformationParameter_2'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_ROTATION_ANGLE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - RotationAngle'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_VALUE_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter value not supported - Mode'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_EXTERNAL_TCP_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - ExternalTCP'

        case RobotLibraryErrorIdEnum.ERR_OPTIONAL_PARAM_RELATIVE_POS_NOT_SUPPORTED:
            MESSAGE_CODE_TO_STRING = 'Server Optional parameter not supported - RelativePosition'

        case RobotLibraryErrorIdEnum.ERR_EMITTER_ID_MUST_NOT_BE_ZERO:
            MESSAGE_CODE_TO_STRING = 'Server Specified Emitter ID must not be 0'

        case RobotLibraryErrorIdEnum.ERR_INVALID_PARAM_EXECUTION_MODE:
            MESSAGE_CODE_TO_STRING = 'Server Invalid parameter value - Execution mode'

        case RobotLibraryErrorIdEnum.ERR_CMD_NOT_IMPLEMENTED:
            MESSAGE_CODE_TO_STRING = 'Server Command not implemented'

        case RobotLibraryErrorIdEnum.ERR_CMD_ONLY_ONE_INSTANCE_ALLOWED:
            MESSAGE_CODE_TO_STRING = 'Server Only one instance of this command is allowed'

        case RobotLibraryErrorIdEnum.ERR_CMD_REQUIRES_INTERRUPT_OR_IDLE_STATE:
            MESSAGE_CODE_TO_STRING = 'Server Command requires an active interrupt or idle state to be executed'

        case RobotLibraryErrorIdEnum.ERR_CMD_NOT_ALLOWED_DURING_ACTIVE_INTERRUPT:
            MESSAGE_CODE_TO_STRING = 'Server Command cannot be executed during active interrupt'

        case RobotLibraryErrorIdEnum.ERR_SECONDARY_SEQUENCE_BLOCKED_BY_CMD:
            MESSAGE_CODE_TO_STRING = 'Server Secondary sequence is blocked by command (e.g. GroupJog, ReturnToPrimary). No other commands may be buffered in secondary sequence'

        case RobotLibraryErrorIdEnum.ERR_SECONDARY_SEQUENCE_NOT_ACTIVE:
            MESSAGE_CODE_TO_STRING = 'Server The secondary sequence is not active. Commands may only be buffered in this sequence if it is active'

        case RobotLibraryErrorIdEnum.ERR_SECONDARY_SEQUENCE_NOT_EMPTY:
            MESSAGE_CODE_TO_STRING = 'Server Secondary sequence is not empty. The command requires the secondary sequence to be empty'

        case RobotLibraryErrorIdEnum.ERR_TRANSACTION_NOT_POSSIBLE_IN_STATE_MACHINE:
            MESSAGE_CODE_TO_STRING = 'Server Transaction not possible in the state machine'

        case RobotLibraryErrorIdEnum.ERR_CMD_NOT_POSSIBLE_BY_OP_MODE_LOCAL:
            MESSAGE_CODE_TO_STRING = 'Server Cannot execute command because current operation mode is local.'

        case RobotLibraryErrorIdEnum.ERR_CMD_TYPE_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server Command type out of range'

        case RobotLibraryErrorIdEnum.ERR_CMD_NOT_POSSIBLE_DURING_CALL_SUB_PROGRAM:
            MESSAGE_CODE_TO_STRING = 'Server Execution of this CMD is not possible while CallSubprogram is in progress in the sequence'

        case RobotLibraryErrorIdEnum.ERR_OPERATION_NOT_POSSIBLE_SEE_LOG:
            MESSAGE_CODE_TO_STRING = 'Server Operation not possible. See MessageLog for further information'

        case RobotLibraryErrorIdEnum.ERR_INTERNAL_ERROR_DURING_CMD:
            MESSAGE_CODE_TO_STRING = 'Server An RC internal error occurred during execution of this command. Check the message log for additional information'

        case RobotLibraryErrorIdEnum.ERR_WRONG_TELEGRAM_STATE:
            MESSAGE_CODE_TO_STRING = 'Client Wrong Telegram State (Two Sequences not in both directions active)'

        case RobotLibraryErrorIdEnum.ERR_ACYCLIC_AREA_TO_SMALL_PLC_TO_ROB:
            MESSAGE_CODE_TO_STRING = 'Client Acyclic area client to server too small'

        case RobotLibraryErrorIdEnum.ERR_ACYCLIC_AREA_TO_SMALL_ROB_TO_PLC:
            MESSAGE_CODE_TO_STRING = 'Client Acyclic area server to client too small'

        case RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0x8005:
            MESSAGE_CODE_TO_STRING = 'Client Lifesign timeout'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_SEQ_TIMEOUT_0x8005:
            MESSAGE_CODE_TO_STRING = 'Client Telegram sequence timeout'

        case RobotLibraryErrorIdEnum.ERR_AXESGROUP_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Assigned AxesGroup not valid'

        case RobotLibraryErrorIdEnum.ERR_PERIPHERY_INVALID:
            MESSAGE_CODE_TO_STRING = 'Client Assigned periphery not valid'

        case RobotLibraryErrorIdEnum.ERR_INVALID_ROBOT_STATE:
            MESSAGE_CODE_TO_STRING = 'Client Invalid state of the robot (more than 1 CMD active)'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_CHANGED_AFTER_INIT:
            MESSAGE_CODE_TO_STRING = 'Client Telegram Number changed after initialization. Reinitialize by disabling and enabling the RobotTask.'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_CONTROL_MISMATCH_TELEGRAM_STATE_0x80A1:
            MESSAGE_CODE_TO_STRING = 'Client Telegram control does not match the telegram state'

        case RobotLibraryErrorIdEnum.ERR_INIT_LOST_UNKNOWN_0x80A2:
            MESSAGE_CODE_TO_STRING = 'Client Initialization lost for unknown reason. See message log after reinitializing'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_LENGTH_MISMATCH_0x80A3:
            MESSAGE_CODE_TO_STRING = 'Client Telegram length does not match the length provided in the communication interface, or the communication interface is too small.'

        case RobotLibraryErrorIdEnum.ERR_SRCI_MAJOR_VERSION_INCOMPATIBLE_0x80A4:
            MESSAGE_CODE_TO_STRING = 'Client Incompatible major SRCI version'

        case RobotLibraryErrorIdEnum.ERR_LIFESIGN_TIMEOUT_0x80A5:
            MESSAGE_CODE_TO_STRING = 'Client Lifesign timeout'

        case RobotLibraryErrorIdEnum.ERR_CYCLIC_DATA_TOO_LARGE_0x80A6:
            MESSAGE_CODE_TO_STRING = 'Client The selected optional cyclic data does not fit in the given telegram size'

        case RobotLibraryErrorIdEnum.ERR_INTERFACE_WAS_RESET_AFTER_INIT_0x80A7:
            MESSAGE_CODE_TO_STRING = 'Client The robot interface was reset after being initialized'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_SEQ_TIMEOUT_0x80A8_0x80A8:
            MESSAGE_CODE_TO_STRING = 'Client Telegram sequence timeout'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NO_CHANGED_AFTER_INIT_0x80A9:
            MESSAGE_CODE_TO_STRING = 'Client The telegram number changed after initialization'

        case RobotLibraryErrorIdEnum.ERR_AXESGROUP_ID_INVALID_0x80AA:
            MESSAGE_CODE_TO_STRING = 'Client Error: Invalid AxesGroupID'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_INVALID_0x80AB:
            MESSAGE_CODE_TO_STRING = 'Client Telegram number is invalid. E.g. TwoSequences is only activated in one direction'

        case RobotLibraryErrorIdEnum.ERR_TELEGRAM_NUMBER_NOT_SUPPORTED_0x80AC:
            MESSAGE_CODE_TO_STRING = 'Client Telegram Number is not supported'

        case RobotLibraryErrorIdEnum.ERR_ACR_REGISER_IS_FULL:
            MESSAGE_CODE_TO_STRING = 'Server The ACR is full. RA is disabled'

        case RobotLibraryErrorIdEnum.ERR_MANDATORY_CMD_STOPPED:
            MESSAGE_CODE_TO_STRING = 'Server The execution of a mandatory command has been stopped. Exchange config must run for the system to run'

        case RobotLibraryErrorIdEnum.ERR_INCONSISTENT_DATA_RECEIVED:
            MESSAGE_CODE_TO_STRING = 'Server Inconsistent data received. Make sure the complete telegram data is sent to RC in one frame.'

        case RobotLibraryErrorIdEnum.ERR_CONNECTION_LOST:
            MESSAGE_CODE_TO_STRING = 'Client Connection to the communication partner was lost'

        case RobotLibraryErrorIdEnum.ERR_FATAL_ERROR_REINIT_REQUIRED:
            MESSAGE_CODE_TO_STRING = 'Client Fatal Error occurred. Reinitialization of Robot_Task is required'

        case RobotLibraryErrorIdEnum.ERR_INTERNAL_ERROR:
            MESSAGE_CODE_TO_STRING = 'Server Internal error'

        case RobotLibraryErrorIdEnum.ERR_DESERIALIZE_ERROR:
            MESSAGE_CODE_TO_STRING = 'Server Internal error in deserialize'

        case RobotLibraryErrorIdEnum.ERR_CMD_ID_OUT_OF_RANGE:
            MESSAGE_CODE_TO_STRING = 'Server CMD ID out of range 1.ACR_Length'

        case RobotLibraryErrorIdEnum.ERR_FRAGMENT_LENGTH_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid fragment length'

        case RobotLibraryErrorIdEnum.ERR_CMD_PRIORITY_CHANGED:
            MESSAGE_CODE_TO_STRING = 'Server Command priority or type changed during runtime'

        case RobotLibraryErrorIdEnum.ERR_TRIED_TO_RESET_NONEMPTY_ACR_REGISTER:
            MESSAGE_CODE_TO_STRING = 'Server Tried to reset a non-empty ACR entry'

        case RobotLibraryErrorIdEnum.ERR_SEQUENCE_PAYLOAD_INVALID_LENGTH:
            MESSAGE_CODE_TO_STRING = 'Server Error: Invalid Sequence payload length (e.g., sequence payload length is specified 999 even if telegram length is only 100.)'

        case RobotLibraryErrorIdEnum.ERR_ACTION_BYTE_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid ActionByte'

        case RobotLibraryErrorIdEnum.ERR_CMD_PAYLOAD_LENGTH_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Invalid Command payload length'

        case RobotLibraryErrorIdEnum.ERR_CMD_PAYLOAD_POINTER_INVALID:
            MESSAGE_CODE_TO_STRING = 'Server Error: Invalid Command payload pointer (e.g., Out of bounds)'

        case RobotLibraryErrorIdEnum.ERR_EXEC_MODE_CHANGE_ILLEGAL:
            MESSAGE_CODE_TO_STRING = 'Server Illegal Execution Mode change'
        case _:
            MESSAGE_CODE_TO_STRING = StrReplace(Str='Unkown message code : {0}', SubStr1='{0}', SubStr2=DWORD_TO_STRING(MessageCode))
    return MESSAGE_CODE_TO_STRING
