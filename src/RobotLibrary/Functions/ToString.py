"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ToString
Author:      Thorsten Brach
Date:        2024-06-01

Description:
  Converts various data types to their string representations

Copyright:
    (C) 2024 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from typing import Dict, Any
import inspect
import re
import textwrap
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.IEC_Standard import CONCAT
from RobotLibrary.IEC_Types import REAL, SINT, WORD, BOOL, DINT, INT, BYTE, UINT
from RobotLibrary.Enumerations.Events.InfoIdEnum import InfoIdEnum
from RobotLibrary.Enumerations.Events.WarningIdEnum import WarningIdEnum
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum
from RobotLibrary.Enumerations.Mode.StepMode import StepMode


#-------------------------------------------------------------------------
# WORD_TO_STRING_HEX
#-------------------------------------------------------------------------
def WORD_TO_STRING_HEX(value : WORD) -> str:
    """Convert a WORD value to its hexadecimal string representation."""
    return f"{int(value):04X}"

#-------------------------------------------------------------------------
# INT_TO_STRING_HEX
#-------------------------------------------------------------------------
def INT_TO_STRING_HEX(value : INT | int) -> str:
    """Convert a INT value to its hexadecimal string representation."""
    return f"{int(value):04X}"

#-------------------------------------------------------------------------
# WORD_TO_STRING_BIN
#-------------------------------------------------------------------------
def WORD_TO_STRING_BIN(value : WORD | UINT) -> str:
    """Convert a WORD value to its binary string representation."""
    
    return f"{int(value):016b}"


#-------------------------------------------------------------------------
# STEP_MODE_TO_STRING
#-------------------------------------------------------------------------
def STEP_MODE_TO_STRING(value : StepMode) -> str:

    return value.name + f" ({int(value)})"

#-------------------------------------------------------------------------
# BOOL_TO_STRING
#-------------------------------------------------------------------------
def BOOL_TO_STRING(value : BOOL | bool) -> str:
    """Convert a BOOL value to its string representation."""
    return "TRUE" if bool(value) else "FALSE"

#-------------------------------------------------------------------------
# DINT_TO_STRING
#-------------------------------------------------------------------------
def DINT_TO_STRING(value : DINT) -> str:
    """Convert a DINT value to its string representation."""
    return str(int(value))

#-------------------------------------------------------------------------
# INT_TO_STRING
#-------------------------------------------------------------------------
def INT_TO_STRING(value : INT | int ) -> str:
    """Convert a DINT value to its string representation."""
    return str(int(value))


#-------------------------------------------------------------------------
# UINT_TO_STRING
#-------------------------------------------------------------------------
def UINT_TO_STRING(value : UINT | int ) -> str:
    """Convert a UINT value to its string representation."""
    return str(int(value))


#-------------------------------------------------------------------------
# BYTE_TO_STRING - returns the byte in binary representation
#-------------------------------------------------------------------------
def BYTE_TO_STRING_BIN(value: BYTE | int) -> str:
    """Convert a BYTE value to its binary string representation."""
    return f"{int(value):08b}"

#-------------------------------------------------------------------------
# BYTE_TO_STRING - returns the byte in decimal representation
#-------------------------------------------------------------------------
def BYTE_TO_STRING(value: BYTE | int) -> str:
    """Convert a BYTE value to its string representation."""
    return str(int(value))


#-------------------------------------------------------------------------
# FRAGMENT_ACTION_TO_STRING - returns the fragment action as string
#-------------------------------------------------------------------------
def FRAGMENT_ACTION_TO_STRING(value: BYTE) -> str:

    # return value of function
    FRAGMENT_ACTION_TO_STRING : str = ''

    if ( value.Bit[0] ):
        FRAGMENT_ACTION_TO_STRING = CONCAT(FRAGMENT_ACTION_TO_STRING, ' Complete (Bit 0)')

    if ( value.Bit[1] ): 
        FRAGMENT_ACTION_TO_STRING = CONCAT(FRAGMENT_ACTION_TO_STRING, ' Reset (Bit 1)')

    if ( value.Bit[2] ):
        FRAGMENT_ACTION_TO_STRING = CONCAT(FRAGMENT_ACTION_TO_STRING, ' Clear (Bit 2)')

    return FRAGMENT_ACTION_TO_STRING


#-------------------------------------------------------------------------
# CMD_TYPE_TO_STRING - returns the command type as string
#-------------------------------------------------------------------------
def CMD_TYPE_TO_STRING(value: CmdType) -> str:
    """Return enum name and numeric value in the form "Name (value)".
    """
    return f"{value.name} ({int(value)})"


#-------------------------------------------------------------------------
# MESSAGE_CODE_TO_STRING
#-------------------------------------------------------------------------
def MESSAGE_CODE_TO_STRING(value: Any) -> str:
    """Return a readable text for a SRCI message code.

    Tries to resolve the numeric code against `InfoIdEnum`, `WarningIdEnum`,
    and `ErrorIdEnum`. If found, returns a friendly string in the form
    "INFO: Collision Detected" / "WARN: Acyclic Range Client To Server Very Small"
    / "ERROR: Invalid Param Velocity". If not found, returns
    "Unknown message code: 0xXXXX" (or 0xXXXXXXXX for values > 0xFFFF).
    """
    # Normalize to int (unwrap FieldProxy/IEC types carrying .value)
    raw = value
    try:
        while hasattr(raw, 'value') and not isinstance(raw, (int, float, str, bool, bytes)):
            raw = raw.value
    except Exception:
        pass
    code = int(raw)

    # Lazy-load documentation mapping from enum source files
    docs = _get_message_docs()
    doc = docs.get(code)
    if doc:
        # Return the documentation comment verbatim if available
        return doc.strip()

    def _friendly_name(enum_name: str, category_prefixes: tuple[str, ...]) -> str:
        # strip common category prefixes from the enum member name
        for p in category_prefixes:
            if enum_name.startswith(p):
                enum_name = enum_name[len(p):]
                break
        # turn underscores into spaces and title-case for readability
        return enum_name.replace('_', ' ').title()

    # Try Info
    try:
        info = InfoIdEnum(code)
        return f"INFO: {_friendly_name(info.name, ('INFO_',))}"
    except ValueError:
        pass

    # Try Warning
    try:
        warn = WarningIdEnum(code)
        return f"WARN: {_friendly_name(warn.name, ('WARN_',))}"
    except ValueError:
        pass

    # Try Error
    try:
        err = ErrorIdEnum(code)
        return f"ERROR: {_friendly_name(err.name, ('ERR_', 'ERROR_'))}"
    except ValueError:
        pass

    # Unknown code: present hex with width depending on magnitude
    width = 8 if code > 0xFFFF else 4
    return f"Unknown message code: 0x{code:0{width}X}"


# -------------------------------------------------------------------------
# Internals: parse enum source to build code -> doc mapping
# -------------------------------------------------------------------------
_MESSAGE_DOCS_CACHE: Dict[int, str] | None = None

def _get_message_docs() -> Dict[int, str]:
    global _MESSAGE_DOCS_CACHE
    if _MESSAGE_DOCS_CACHE is not None:
        return _MESSAGE_DOCS_CACHE
    mapping: Dict[int, str] = {}

    def _parse_enum_docs(enum_cls) -> None:
        try:
            src = inspect.getsource(enum_cls)
        except Exception:
            return
        lines = src.splitlines()
        assign_re = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*(0x[0-9A-Fa-f]+|\d+)\s*$")
        i = 0
        while i < len(lines):
            m = assign_re.match(lines[i])
            if not m:
                i += 1
                continue
            # parse numeric code
            val_text = m.group(2)
            try:
                code_val = int(val_text, 16) if val_text.startswith(('0x','0X')) else int(val_text)
            except Exception:
                i += 1
                continue
            # look ahead for a triple-quoted block
            j = i + 1
            # skip empty lines
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            doc_text = None
            if j < len(lines) and lines[j].lstrip().startswith('"""'):
                # capture until closing triple quotes
                start_line = lines[j]
                # remove leading triple quotes
                first = start_line[start_line.find('"""')+3:]
                buf = [first]
                j += 1
                while j < len(lines):
                    line = lines[j]
                    if '"""' in line:
                        # closing
                        end_index = line.find('"""')
                        buf.append(line[:end_index])
                        j += 1
                        break
                    buf.append(line)
                    j += 1
                doc_text = "\n".join(buf)
                # normalize indentation and convert escaped newlines to real ones
                doc_text = textwrap.dedent(doc_text)
                doc_text = doc_text.replace('\\n', '\n')
            if doc_text:
                mapping[code_val] = doc_text
            i = j if j > i else i + 1

    # Parse all three enums
    _parse_enum_docs(InfoIdEnum)
    _parse_enum_docs(WarningIdEnum)
    _parse_enum_docs(ErrorIdEnum)

    _MESSAGE_DOCS_CACHE = mapping
    return mapping


#-------------------------------------------------------------------------
# VALID_REAL_TO_STRING
#-------------------------------------------------------------------------
def VALID_REAL_TO_STRING( Value : float | REAL ) -> str:
    """Convert a VALID_REAL value to its string representation."""
    
    Value = float(Value)
    
    if ( Value != Value ):  # NaN check
        return "NaN"
    elif ( Value == float('inf') ):
        return "Infinity"
    elif ( Value == float('-inf') ):
        return "-Infinity"
    else:
        return str(Value)