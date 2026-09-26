"""Constants for the robot library."""


from RobotLibrary.Structures.Miscellaneous.VersionStruct import VersionStruct 


# Global Constants
# Version of SRCI specification
# Bit 0-4 : Minor version = Features        (0..31)
# Bit 5-7 : Major version = Breaking change (0..07)
SRCIVersion: VersionStruct = VersionStruct(MajorVersion=1, MinorVersion=3, PatchVersion=0)

# Version of the PLC library
PLCLibraryVersion: VersionStruct = VersionStruct(MajorVersion=0, MinorVersion=0, PatchVersion=49)

# Minimal axes group ID
AXES_GROUP_ID_MIN: int = 0

# Maximal axes groups ID
AXES_GROUP_ID_MAX: int = 15

# OK = 0
OK: int = 0 # type: ignore 

# Running = 1
RUNNING: int = 1 # type: ignore

# HasError = -1
HAS_ERROR: int = -1

# Null pointer
XNULL: int = 0

# Null pointer
NULL_POINTER: int = 0  # In Python, use None for pointers, but keeping as int for compatibility

# Real conversion factor ( REAL * 100 -> TO_INT )
REAL_CONVERSION_FACTOR: float = 100.0

# Active command
ACTIVE_CMD: int = 1

# Buffered command
BUFFER_CMD: int = 2

# Maximal length of additional text
MAX_ADD_TEXT_LENGTH: int = 40

# Primary sequence
PRIMARY_SEQUENCE     = 0

# Secondary sequence
SECONDARY_SEQUENCE   = 1