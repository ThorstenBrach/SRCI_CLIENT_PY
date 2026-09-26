"""SRCI constants and library parameters - generated from the PLC library, DO NOT EDIT.

Source: third_party/robotlibrary/RobotLibrary.xml (sha256 6d064f48fb9cb9c5)
Regenerate with ``python -m tools.plcopen_gen``.
"""
# ruff: noqa
# fmt: off
from __future__ import annotations

from typing import ClassVar, Final

from srci.types import iec as _iec
from srci.types._generated import enums as _e
from srci.types._generated.structs import *  # noqa: F403

__all__ = [
    'RobotLibraryConstants',
    'RobotLibraryDefines',
    'RobotLibraryParameter',
]


class RobotLibraryConstants:
    """Global variable list RobotLibraryConstants of the PLC library."""
    SRCIVersion: Final[VersionStruct] = VersionStruct(MajorVersion=1, MinorVersion=5, PatchVersion=0)
    """
    Version of SRCI specification Bit 0-4 : Minor version = Features (0..31) Bit 5-7 : Major version
    = Breaking change (0..07) [Override: PLC library still says 1.3.0, but implements SRCI 1.5 (SDK:
    SRCI_VERSION 1.5)]
    """
    PLCLibraryVersion: Final[VersionStruct] = VersionStruct(MajorVersion=0, MinorVersion=0, PatchVersion=49)
    """Version of the PLC library"""
    AXES_GROUP_ID_MIN: Final[int] = 0
    """Minimal axes group ID"""
    AXES_GROUP_ID_MAX: Final[int] = 15
    """Maximal axes groups ID"""
    OK: Final[int] = 0
    """OK = 0"""
    RUNNING: Final[int] = 1
    """Running = 1"""
    HAS_ERROR: Final[int] = -1
    """HasError = -1"""
    XNULL: Final[int] = 0
    """Null pointer"""
    NULL_POINTER: Final[object | None] = None
    """Null pointer"""
    REAL_CONVERSION_FACTOR: Final[float] = 100.0
    """Real conversion factor ( REAL * 100 -> TO_INT )"""
    ACTIVE_CMD: Final[int] = 1
    """Active command"""
    BUFFER_CMD: Final[int] = 2
    """Buffered command"""
    MAX_ADD_TEXT_LENGTH: Final[int] = 40
    """Maximal length of additional text"""


class RobotLibraryDefines:
    """Global variable list RobotLibraryDefines of the PLC library."""
    MaxTypeNameLength: ClassVar[int] = 0
    """Maximal length of type name"""


class RobotLibraryParameter:
    """Global variable list RobotLibraryParameter of the PLC library."""
    TOOL_MAX: ClassVar[int] = 16
    """Maximal amount of tools"""
    FRAME_MAX: ClassVar[int] = 16
    """Maximal amount of frames"""
    LOAD_MAX: ClassVar[int] = 16
    """Maximal amount of loads"""
    WORK_AREAS_MAX: ClassVar[int] = 16
    """Maximal amount of work areas"""
    SYSTEM_LOG_MAX: ClassVar[int] = 32
    """Maximal amount of system logs"""
    MESSAGE_LOG_MAX: ClassVar[int] = 100
    """Maximal amount of message logs"""
    MESSAGE_TEXT_LEN: ClassVar[int] = 255
    """Maximum string length for message texts"""
    LIST_ENTRIES_MAX: ClassVar[int] = 100
    """Maximal amount of List entries"""
    PARAMETER_PAYLOAD_MAX: ClassVar[int] = 255
    """Maximal amount of bytes for the parameter payload"""
    RESPONSE_PAYLOAD_MAX: ClassVar[int] = 255
    """Maximal amount of bytes for the response payload"""
    SUB_PROGRAM_DATA_MAX: ClassVar[int] = 189
    """Maximal amount of bytes that can be exchanged with the sub program on the RC"""
    SPLINE_DATA_MAX: ClassVar[int] = 64
    """Maximal amount of spline data"""
    ACTIVE_CMD_REGISTER_ENTRIES_MAX: ClassVar[int] = 50
    """Maximal amount of entries in the Active Command Register"""
    MESSAGE_CODES_MAX: ClassVar[int] = 15
    """Maximal amount of message codes"""
    FRAGMENT_MAX: ClassVar[int] = 31
    """
    Maximal amount of fragments [Override: ST-FIX F52: 10 fragments (0..9) per telegram are too few
    - a 256 byte telegram holds up to 27 fragments (header 8 bytes + at least 1 byte payload);
    fragments behind the array were dropped although the telegram was acknowledged -> responses
    lost]
    """
    SWAP_BYTE_ORDER: ClassVar[bool] = True
    """Flag to indicate that the byte order must be changed"""
    INVALID_FRAMES_CHECK_TIMEOUT: ClassVar[int] = 60000
    """Timeout for checking for invalid frames"""
    ACR_USAGE_WARNING_LIMIT: ClassVar[float] = 80.0
    """Warning limit for ACR registers running low"""


_ = _iec  # keep import for type descriptors
