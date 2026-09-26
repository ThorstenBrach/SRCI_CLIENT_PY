"""Constants for the robot library."""

from .IEC_Types import TIME, REAL, TO_TIME, TO_REAL


TOOL_MAX =16
"""
Maximal amount of tools
"""

FRAME_MAX = 16
"""
Maximal amount of frames
"""

LOAD_MAX = 16
"""
Maximal amount of loads
"""

WORK_AREAS_MAX = 16
"""
Maximal amount of work areas
"""

SYSTEM_LOG_MAX = 32
"""
Maximal amount of system logs
"""

MESSAGE_LOG_MAX = 100
"""
Maximal amount of message logs
"""

MESSAGE_TEXT_LEN = 255
"""
Maximum string length for message texts
"""

LIST_ENTRIES_MAX = 100
"""
Maximal amount of list entries
"""

PARAMETER_PAYLOAD_MAX = 255
"""
Maximal amount of bytes for the parameter payload
"""

RESPONSE_PAYLOAD_MAX = 255
"""
Maximal amount of bytes for the response payload
"""

SUB_PROGRAM_DATA_MAX = 189
"""
Maximal amount of bytes that can be exchanged with the sub program on the RC
"""

SPLINE_DATA_MAX = 64
"""
Maximal amount of spline data
"""

ACTIVE_CMD_REGISTER_ENTRIES_MAX = 50
"""
Maximal amount of entries in the Active Command Register
"""

MESSAGE_CODES_MAX = 15
"""
Maximal amount of message codes
"""

FRAGMENT_MAX = 9
"""
Maximal amount of fragments
"""

SWAP_BYTE_ORDER = True #type: ignore
"""
Flag to indicate that the byte order must be changed
"""

INVALID_FRAMES_CHECK_TIMEOUT: TIME = TO_TIME(60000)
"""
Timeout for checking for invalid frames
"""

ACR_USAGE_WARNING_LIMIT: float = 80.0
"""
Warning limit for ACR registers running low
"""