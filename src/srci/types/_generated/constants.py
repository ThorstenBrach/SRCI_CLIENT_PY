# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.types (constants and library parameters)
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SRCI constants and library parameters, generated from the PLC library
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------

"""SRCI constants and library parameters - generated from the PLC library, DO NOT EDIT.

Source: third_party/robotlibrary/RobotLibrary.xml (sha256 2021bed3e05eb890)
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
    = Breaking change (0..07)
    """
    PLCLibraryVersion: Final[VersionStruct] = VersionStruct(MajorVersion=1, MinorVersion=5, PatchVersion=4)
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
    SERVER_LOG_CONTENT_MAX: Final[int] = 179
    """
    ST-FIX F108: characters of a log line per ReadServerLog response (SRCI SDK 1.1: 179; spec table
    6-124: 187)
    """


class RobotLibraryDefines:
    """Global variable list RobotLibraryDefines of the PLC library."""
    MaxTypeNameLength: ClassVar[int] = 0
    """Maximal length of type name"""


class RobotLibraryParameter:
    """Global variable list RobotLibraryParameter of the PLC library."""
    TOOL_MAX: ClassVar[int] = 20
    """
    Maximal amount of tools SRCI_PLC_TEST: 20 like the SDK simulator (was the parameter of the
    library reference)
    """
    FRAME_MAX: ClassVar[int] = 20
    """
    Maximal amount of frames SRCI_PLC_TEST: 20 like the SDK simulator (was the parameter of the
    library reference)
    """
    LOAD_MAX: ClassVar[int] = 20
    """
    Maximal amount of loads SRCI_PLC_TEST: 20 like the SDK simulator (was the parameter of the
    library reference)
    """
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
    """Maximal amount of fragments"""
    SWAP_BYTE_ORDER: ClassVar[bool] = True
    """Flag to indicate that the byte order must be changed"""
    INVALID_FRAMES_CHECK_TIMEOUT: ClassVar[int] = 60000
    """Timeout for checking for invalid frames"""
    ACR_USAGE_WARNING_LIMIT: ClassVar[float] = 80.0
    """Warning limit for ACR registers running low"""
    LOG_LINE_LEN: ClassVar[int] = 1023
    """ST-FIX F108: maximal length of a log line of ReadServerLog / ReadClientLog (element of LogFile)"""


_ = _iec  # keep import for type descriptors
