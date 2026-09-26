
import ctypes
import struct
import datetime
from typing import Any, Optional, Union, get_type_hints, Type, List, Tuple, Dict, Iterator, overload, TypeVar, Generic
from enum import IntEnum

# Explicit endianness packing helper
def _pack_bytes(fmt_code: str, value: Any, order: str = 'big') -> bytes:
    if order not in ('big', 'little'):
        raise ValueError("order must be 'big' or 'little'")
    prefix = '>' if order == 'big' else '<'
    return struct.pack(prefix + fmt_code, value)

T = TypeVar('T')  # Nur einmal deklarieren, ganz oben

# -------------------------
# Bit-Zugriff für Integer-Typen (IEC 61131-3 konform)
# -------------------------
class _BitView:
    """
    Bit-Zugriff Proxy für IEC Integer-Typen.
    Ermöglicht lesenden und schreibenden Zugriff auf einzelne Bits.
    Beispiel:
        b = BYTE(0)
        b.Bit[0] = True   # Setze Bit 0
        b.Bit[7] = True   # Setze Bit 7
        print(int(b))     # 129 (0b10000001)
        print(b.Bit[0])   # True
    """
    __slots__ = ("_parent", "_bits")

    def __init__(self, parent: Any, bits: int) -> None:
        self._parent = parent
        self._bits = bits

    def __getitem__(self, idx: int) -> bool:
        """Lese Bit an Position idx (0-basiert)"""
        if idx < 0 or idx >= self._bits:
            raise IndexError(f"Bit index {idx} out of range (0..{self._bits - 1})")
        return bool((int(self._parent.value) >> idx) & 1)

    def __setitem__(self, idx: int, value: bool) -> None:
        """Setze Bit an Position idx (0-basiert)"""
        if idx < 0 or idx >= self._bits:
            raise IndexError(f"Bit index {idx} out of range (0..{self._bits - 1})")
        current_value = int(self._parent.value)
        if value:
            # Bit setzen
            current_value |= (1 << idx)
        else:
            # Bit löschen
            current_value &= ~(1 << idx)
        self._parent.value = current_value

    def __repr__(self) -> str:
        return f"<BitView {self._bits} bits>"

# --- BOOL Definition (korrekt eingerückt) ---
class BOOL(ctypes.c_bool):
    def __new__(cls, value: Any = False) -> "BOOL":
        instance = ctypes.c_bool.__new__(cls)
        ctypes.c_bool.__init__(instance, bool(value))  # type: ignore
        return instance
    def __bool__(self) -> bool:
        return bool(self.value)
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"BOOL({bool(self.value)})"
    def __or__(self, other: Any) -> "BOOL":
        return BOOL(bool(self) or bool(other))
    def __ror__(self, other: Any) -> "BOOL":
        return BOOL(bool(other) or bool(self))
    def __invert__(self) -> "BOOL":
        return BOOL(not bool(self))
    @classmethod
    def sizeof(cls) -> int:
        """Gibt die Größe in Bytes zurück"""
        return ctypes.sizeof(ctypes.c_bool)
    def size(self) -> int:
        """Instanzmethode für sizeof (für e.Flag.sizeof())"""
        return ctypes.sizeof(ctypes.c_bool)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('B', 1 if bool(self.value) else 0, order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    
    def toString(self) -> str:
        return "TRUE" if bool(self.value) else "FALSE"

class INT(ctypes.c_int16):
    def __new__(cls, value: Any = 0) -> "INT":
        instance = ctypes.c_int16.__new__(cls)
        ctypes.c_int16.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"INT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_int16)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_int16)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_int.Bit[0] = True"""
        return _BitView(self, 16)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('h', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    
    def toString(self) -> str:
        return str(int(self.value))

class DINT(ctypes.c_int32):
    def __new__(cls, value: Any = 0) -> "DINT":
        instance = ctypes.c_int32.__new__(cls)
        ctypes.c_int32.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"DINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_int32)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_int32)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_dint.Bit[0] = True"""
        return _BitView(self, 32)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('i', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    
    def toString(self) -> str:
        return str(int(self.value))

class SINT(ctypes.c_int8):
    def __new__(cls, value: Any = 0) -> "SINT":
        instance = ctypes.c_int8.__new__(cls)
        ctypes.c_int8.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"SINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_int8)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_int8)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_sint.Bit[0] = True"""
        return _BitView(self, 8)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('b', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class UINT(ctypes.c_uint16):
    def __new__(cls, value: Any = 0) -> "UINT":
        instance = ctypes.c_uint16.__new__(cls)
        ctypes.c_uint16.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"UINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint16)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint16)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_uint.Bit[0] = True"""
        return _BitView(self, 16)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('H', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class UDINT(ctypes.c_uint32):
    def __new__(cls, value: Any = 0) -> "UDINT":
        instance = ctypes.c_uint32.__new__(cls)
        ctypes.c_uint32.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"UDINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint32)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint32)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_udint.Bit[0] = True"""
        return _BitView(self, 32)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('I', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class USINT(ctypes.c_uint8):
    def __new__(cls, value: Any = 0) -> "USINT":
        instance = ctypes.c_uint8.__new__(cls)
        ctypes.c_uint8.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"USINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint8)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint8)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_usint.Bit[0] = True"""
        return _BitView(self, 8)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('B', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class BYTE(ctypes.c_uint8):
    def __new__(cls, value: Any = 0) -> "BYTE":
        instance = ctypes.c_uint8.__new__(cls)
        ctypes.c_uint8.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"BYTE({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint8)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint8)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_byte.Bit[0] = True"""
        return _BitView(self, 8)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('B', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class WORD(ctypes.c_uint16):
    def __new__(cls, value: Any = 0) -> "WORD":
        instance = ctypes.c_uint16.__new__(cls)
        ctypes.c_uint16.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"WORD({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint16)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint16)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_word.Bit[0] = True"""
        return _BitView(self, 16)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('H', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class DWORD(ctypes.c_uint32):
    def __new__(cls, value: Any = 0) -> "DWORD":
        instance = ctypes.c_uint32.__new__(cls)
        ctypes.c_uint32.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"DWORD({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint32)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint32)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_dword.Bit[0] = True"""
        return _BitView(self, 32)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('I', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class REAL(ctypes.c_float):
    def __new__(cls, value: Any = 0.0) -> "REAL":
        instance = ctypes.c_float.__new__(cls)
        ctypes.c_float.__init__(instance, float(value))  # type: ignore
        return instance
    def __float__(self) -> float:
        return float(self.value)
    def __repr__(self) -> str:
        return f"REAL({float(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_float)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_float)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('f', float(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class LREAL(ctypes.c_double):
    def __new__(cls, value: Any = 0.0) -> "LREAL":
        instance = ctypes.c_double.__new__(cls)
        ctypes.c_double.__init__(instance, float(value))  # type: ignore
        return instance
    def __float__(self) -> float:
        return float(self.value)
    def __repr__(self) -> str:
        return f"LREAL({float(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_double)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_double)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('d', float(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class LINT(ctypes.c_int64):
    def __new__(cls, value: Any = 0) -> "LINT":
        instance = ctypes.c_int64.__new__(cls)
        ctypes.c_int64.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"LINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_int64)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_int64)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_lint.Bit[0] = True"""
        return _BitView(self, 64)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('q', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class ULINT(ctypes.c_uint64):
    def __new__(cls, value: Any = 0) -> "ULINT":
        instance = ctypes.c_uint64.__new__(cls)
        ctypes.c_uint64.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"ULINT({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint64)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint64)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_ulint.Bit[0] = True"""
        return _BitView(self, 64)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('Q', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

class LWORD(ctypes.c_uint64):
    def __new__(cls, value: Any = 0) -> "LWORD":
        instance = ctypes.c_uint64.__new__(cls)
        ctypes.c_uint64.__init__(instance, int(value))  # type: ignore
        return instance
    def __int__(self) -> int:
        return int(self.value)
    def __repr__(self) -> str:
        return f"LWORD({int(self.value)})"
    @classmethod
    def sizeof(cls) -> int:
        return ctypes.sizeof(ctypes.c_uint64)
    
    def size(self) -> int:
        return ctypes.sizeof(ctypes.c_uint64)
    
    @property
    def Bit(self) -> _BitView:
        """Ermöglicht Bit-Zugriff: my_lword.Bit[0] = True"""
        return _BitView(self, 64)
    def to_bytes(self, order: str = 'big') -> bytes:
        return _pack_bytes('Q', int(self.value), order)
    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes(order)
    def toString(self) -> str:
        return str(int(self.value))    

# -------------------------
# TypeAlias - Öffentliche Namen (erlauben primitive Zuweisungen in IEC_Struct)
# -------------------------

class INTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = INT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to INT ctypes value."""
        return INT(self.value)
    
    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    @property
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', INT))

    # ----------------------------------------------------------------------
    # GetBytes - Return the enum value as bytes in specified byte order.
    # ----------------------------------------------------------------------
    def GetBytes(self, order: str = 'big') -> bytes:
        return INT(self.value).GetBytes(order)


class DINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = DINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to DINT ctypes value."""
        return DINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', DINT))

    def GetBytes(self, order: str = 'big') -> bytes:
        return DINT(self.value).GetBytes(order)

class SINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    Value : int
    
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj
    
    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = SINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to SINT ctypes value."""
        return SINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"
        
        
    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', SINT))

    def GetBytes(self, order: str = 'big') -> bytes:
        return SINT(self.value).GetBytes(order)

class UINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = UINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to UINT ctypes value."""
        return UINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', UINT))
    
    def GetBytes(self, order: str = 'big') -> bytes:
        return UINT(self.value).GetBytes(order)

class UDINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = UDINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to UDINT ctypes value."""
        return UDINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', UDINT))
    
    def GetBytes(self, order: str = 'big') -> bytes:
        return UDINT(self.value).GetBytes(order)

class USINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = USINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to USINT ctypes value."""
        return USINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', USINT))
    
    def GetBytes(self, order: str = 'big') -> bytes:
        return USINT(self.value).GetBytes(order)

class BYTEEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = BYTE(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to BYTE ctypes value."""
        return BYTE(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', BYTE))

    def GetBytes(self, order: str = 'big') -> bytes:
        return BYTE(self.value).GetBytes(order)

class WORDEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = WORD(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to WORD ctypes value."""
        return WORD(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', WORD))

    def GetBytes(self, order: str = 'big') -> bytes:
        return WORD(self.value).GetBytes(order)

class DWORDEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = DWORD(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to DWORD ctypes value."""
        return DWORD(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', DWORD))
    
    def GetBytes(self, order: str = 'big') -> bytes:
        return DWORD(self.value).GetBytes(order)

class LINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = LINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to LINT ctypes value."""
        return LINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', LINT))
    
    def GetBytes(self, order: str = 'big') -> bytes:
        return LINT(self.value).GetBytes(order)

class ULINTEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = ULINT(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to ULINT ctypes value."""
        return ULINT(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', ULINT))

    def GetBytes(self, order: str = 'big') -> bytes:
        return ULINT(self.value).GetBytes(order)

class LWORDEnum(IntEnum):
    # --------------------------------------------------------------------------------------
    # __new__ Constructor - Create a new enum instance with its corresponding integer value.
    # --------------------------------------------------------------------------------------
    def __new__(cls, value: int):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # ----------------------------------------------------------------------------------------
    # __init__ Initializer - Initialize the enum instance with its corresponding ctypes value.
    # -------------------------------------_--------------------------------------------------
    def __init__(self, value: int):
        self.ctypes_value = LWORD(value)

    # ----------------------------------------------------------------------
    # TypeValue - Return the enum as the type specific ctype value.
    # ----------------------------------------------------------------------
    @property
    def TypeValue(self) :
        """Convert enum to LWORD ctypes value."""
        return LWORD(self.value)

    # ----------------------------------------------------------------------
    # toString - Return the enum name and value as a string, e.g. "INFO (5)".
    # ----------------------------------------------------------------------
    def toString(self):
        return f"{self.name} ({self.value})"

    @classmethod
    def sizeof(cls):
        return ctypes.sizeof(getattr(cls, 'ctypes_type', LWORD))

    def GetBytes(self, order: str = 'big') -> bytes:
        return LWORD(self.value).GetBytes(order)


# -------------------------
# Proxy für Feldzugriff (Instanz-Wrapper, KEIN Descriptor)
# -------------------------
#T = TypeVar('T')

class _FieldProxy(Generic[T]):
    """
    Proxy, der auf ein Feld im ctypes-Storage zeigt.
    Wird pro Instanz erzeugt; ersetzt nicht die Klassenannotation.
    Generic[T] erlaubt Pylance, den Typ des Feldes zu verfolgen.
    """
    __slots__ = ("_storage", "_field", "_decl_type")

    def __init__(self, storage: ctypes.Structure, field: str, declared_type: Optional[type] = None):
        self._storage = storage
        self._field = field
        self._decl_type = declared_type


    @property
    def value(self) -> Any:
        """
        Gibt rekursiv den echten Wert des Feldes zurück (z.B. int bei DWORD, str bei IEC_String).
        Entpackt verschachtelte .value-Ketten bis zum Python-Primitive.
        """
        val = getattr(self._storage, self._field)
        # Rekursiv entpacken, bis ein echtes Python-Primitive erreicht ist
        while hasattr(val, "value") and not isinstance(val, (int, float, str, bool, bytes)):
            val = val.value
        return val

    @value.setter
    def value(self, v: Any) -> None:
        # akzeptiere ctypes, primitives, unsere ctypes-Subklassen, andere FieldProxy oder Enum-Werte
        # FieldProxy -> echten Wert entnehmen
        if isinstance(v, _FieldProxy):
            v = v.value
        # IEC-Typen mit .value auf ihr primitives entpacken
        if hasattr(v, "value") and not isinstance(v, (int, float, str, bool, bytes)):
            try:
                v = v.value
            except Exception:
                pass
        # Enums: wenn deklariert, in int konvertieren
        try:
            import enum as _enum
            if self._decl_type is not None and isinstance(self._decl_type, type) and issubclass(self._decl_type, _enum.IntEnum):
                if isinstance(v, self._decl_type):
                    setattr(self._storage, self._field, int(v))
                    return
        except Exception:
            pass
        setattr(self._storage, self._field, v)

    @property
    def field_type(self) -> type:
        """
        Gibt den Typ des Feldes zurück (z.B. DWORD, INT, ...)
        """
        val = getattr(self._storage, self._field)
        return type(val)
    def __radd__(self, other: Any) -> Any:
        try:
            return int(other) + int(self.value)
        except Exception:
            return NotImplemented

    def __sub__(self, other: Any) -> Any:
        try:
            return int(self.value) - int(other)
        except Exception:
            return NotImplemented

    def __rsub__(self, other: Any) -> Any:
        try:
            return int(other) - int(self.value)
        except Exception:
            return NotImplemented

    def __mul__(self, other: Any) -> Any:
        try:
            return int(self.value) * int(other)
        except Exception:
            return NotImplemented

    def __rmul__(self, other: Any) -> Any:
        try:
            return int(other) * int(self.value)
        except Exception:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        try:
            return int(self.value) == int(other)
        except Exception:
            return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        try:
            return int(self.value) < int(other)
        except Exception:
            return False

    def __le__(self, other: Any) -> bool:
        try:
            return int(self.value) <= int(other)
        except Exception:
            return False

    def __gt__(self, other: Any) -> bool:
        try:
            return int(self.value) > int(other)
        except Exception:
            return False

    def __ge__(self, other: Any) -> bool:
        try:
            return int(self.value) >= int(other)
        except Exception:
            return False

    def __repr__(self) -> str:
        return f"FieldProxy({self._field}={getattr(self._storage, self._field)})"

    # --- Enum helpers ---
    def toString(self) -> str:
        """Falls es sich um ein Enum-Feld handelt, gib den formatierten Namen zurück."""
        try:
            import enum as _enum
            if self._decl_type is not None and isinstance(self._decl_type, type) and issubclass(self._decl_type, _enum.IntEnum):
                try:
                    enum_val = self._decl_type(int(self.value))
                    if hasattr(enum_val, 'toString'):
                        return enum_val.toString()  # type: ignore
                    return f"{enum_val.name} ({int(enum_val)})"
                except Exception:
                    return str(int(self.value))
        except Exception:
            pass
        # Fallback: String-Repräsentation des zugrunde liegenden Werts
        return str(self.value)

    # --- Typed value accessor for enum-backed fields ---
    @property
    def TypeValue(self) -> Any:
        """Gibt den Wert als zugrundeliegenden ctypes-Typ zurück, falls Enum deklariert.

        Für Nicht-Enums wird der rohe Wert zurückgegeben.
        """
        try:
            import enum as _enum
            if self._decl_type is not None and issubclass(self._decl_type, _enum.IntEnum):
                ctype = getattr(self._decl_type, 'ctypes_type', None)
                if ctype is not None:
                    return ctype(int(self.value))
                try:
                    enum_val = self._decl_type(int(self.value))
                    tv = getattr(enum_val, 'TypeValue', None)
                    if tv is not None:
                        return tv
                except Exception:
                    pass
        except Exception:
            pass
        return self.value

    @TypeValue.setter
    def TypeValue(self, v: Any) -> None:
        """Setzt den Feldwert über ctypes, Primitive oder Enuminstanz.

        Entpackt `.value`-Ketten und speichert den zugrunde liegenden numerischen Wert.
        """
        # Enuminstanz -> int speichern
        try:
            import enum as _enum
            if self._decl_type is not None and issubclass(self._decl_type, _enum.IntEnum):
                if isinstance(v, self._decl_type):
                    self.value = int(v)
                    return
        except Exception:
            pass
        # Proxies/ctypes entpacken
        val = v
        try:
            while hasattr(val, 'value') and not isinstance(val, (int, float, str, bool, bytes)):
                val = val.value
        except Exception:
            pass
        try:
            self.value = int(val)
        except Exception:
            self.value = val

    # --- Casting helpers so code can do int(proxy), float(proxy), bool(proxy), str(proxy) ---
    def __int__(self) -> int:
        try:
            return int(self.value)
        except Exception:
            # best-effort: try enum reconstruction
            try:
                import enum as _enum
                if self._decl_type is not None and issubclass(self._decl_type, _enum.IntEnum):
                    return int(self._decl_type(int(self.value)))
            except Exception:
                pass
            raise

    def __float__(self) -> float:
        return float(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)

    def __str__(self) -> str:
        # For enums prefer their toString
        try:
            import enum as _enum
            if self._decl_type is not None and issubclass(self._decl_type, _enum.IntEnum):
                return self.toString()
        except Exception:
            pass
        return str(self.value)

    def sizeof(self) -> int:
        """Gibt die Größe des Feldes in Bytes zurück"""
        field_obj = getattr(self._storage, self._field)
        return ctypes.sizeof(field_obj)

    @property
    def Bit(self) -> _BitView:
        """
        Ermöglicht Bit-Zugriff auf Integer-Felder.
        Leitet zum Bit-Property des zugrundeliegenden IEC-Typ-Objekts weiter.
        
        Beispiel:
            e.Value.Bit[2] = True  # Setze Bit 2 von e.Value
        """
        field_obj = getattr(self._storage, self._field)
        # Prüfe ob das Feld ein Bit-Property hat
        if hasattr(field_obj, 'Bit'):
            return field_obj.Bit  # type: ignore
        else:
            raise AttributeError(f"Field '{self._field}' does not support bit access")

    # expose underlying ctypes object for serialization
    def _ctypes_obj(self) -> Any:
        return getattr(self._storage, self._field)

# -------------------------
# STRING / ARRAY (keine Änderung nötig, Beispiel minimal)
# -------------------------
class IEC_String:
    def __init__(self, max_len: int, value: bytes | str = ""):
        self.max_len = int(max_len)
        self.set(value)
    def fromBytes(self, data: bytes | bytearray) -> "IEC_String":
        """Fill this IEC_String from raw bytes using the instance capacity.

        - If fewer bytes than capacity are given, pads with 0x00.
        - If more bytes are given, truncates to capacity so the last byte is the terminator.
        - Always guarantees a trailing 0x00 terminator and total size `Size`.
        """
        buf = bytes(data)
        content = buf[: self.max_len]
        # pad content to capacity with zeros (content area only)
        content_padded = content.ljust(self.max_len, b"\x00")
        # store with explicit terminator at the end
        self._data = content_padded + b"\x00"
        return self
    def set(self, v: bytes | str) -> None:
        if isinstance(v, str):
            b = v.encode("ascii", errors="replace")
        else:
            b = bytes(v)
        b = b[:self.max_len]
        raw = b + b"\x00"
        self._data = raw.ljust(self.max_len + 1, b"\x00")
    # convenient aliases for setting value
    def assign(self, v: bytes | str) -> None:
        self.set(v)
    def __call__(self, v: bytes | str) -> "IEC_String":
        self.set(v)
        return self
    def to_bytes(self) -> bytes:
        return self._data
    def sizeof(self) -> int:
        return self.max_len + 1
    def __str__(self) -> str:
        return self._data.split(b"\x00",1)[0].decode("ascii", errors="replace")
    def __repr__(self) -> str:
        return f"IEC_String('{str(self)}')"
    @property
    def Size(self) -> int:
        """Total byte size including null terminator (capacity + 1)."""
        return self.max_len + 1
    @property
    def Len(self) -> int:
        """Current string length (characters, without terminator)."""
        return len(self)
    
    # String-ähnliche Methoden für Kompatibilität
    def __len__(self) -> int:
        """Gibt die Länge des Strings zurück (ohne Null-Terminator)"""
        return len(str(self))
    
    def __eq__(self, other: Any) -> bool:
        """Vergleich mit anderen Strings oder IEC_Strings"""
        if isinstance(other, IEC_String):
            return str(self) == str(other)
        elif isinstance(other, str):
            return str(self) == other
        return False
    
    def __add__(self, other: Any) -> str:
        """String-Konkatenation"""
        return str(self) + str(other)
    
    def __radd__(self, other: Any) -> str:
        """Umgekehrte String-Konkatenation"""
        return str(other) + str(self)
    
    def toString(self) -> str:
        """Gibt den String-Wert zurück (Kompatibilität)"""
        return str(self)

    def GetBytes(self, order: str = 'big') -> bytes:
        return self.to_bytes()
    

class STRING(IEC_String):
    def __init__(self, max_len: int, value: bytes | str = ""):
        super().__init__(max_len, value)
        self.private_name: Optional[str] = None
    def __set_name__(self, owner: type, name: str) -> None:
        self.private_name = "_" + name
    @overload
    def __get__(self, obj: None, objtype: Optional[type] = None) -> "STRING": ...
    @overload
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> IEC_String: ...
    def __get__(self, obj: Any, objtype: Optional[type] = None) -> "STRING | IEC_String":
        if obj is None:
            # As a descriptor accessed via class, return the descriptor itself
            return self
        assert self.private_name is not None
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, IEC_String(self.max_len))
        result: IEC_String = getattr(obj, self.private_name)
        return result
    def __set__(self, obj: Any, value: bytes | str | IEC_String | 'STRING') -> None:
        assert self.private_name is not None
        if isinstance(value, (IEC_String, STRING)):
            s = IEC_String(self.max_len, str(value))
            setattr(obj, self.private_name, s)
        else:
            setattr(obj, self.private_name, IEC_String(self.max_len, value))
    def byte_size(self) -> int:
        return self.max_len + 1
    def to_ctypes_field(self, instance: Any) -> Tuple[Type[ctypes.Array], ctypes.Array]:
        assert self.private_name is not None
        s = getattr(instance, self.private_name)
        c_array_type = ctypes.c_char * (self.max_len + 1)
        c_array = c_array_type(*s.to_bytes())
        return c_array_type, c_array
    
    def toString(self) -> str:
        return str(self)


class ARRAY(Generic[T]):
    def __init__(self, lower: int, upper: int, element_type: Any, ctor_args: tuple = (), data: Optional[List[Any]] = None):
        self.lower = int(lower)
        self.upper = int(upper)
        self.element_type = element_type
        self.ctor_args = ctor_args
        self._is_type = isinstance(element_type, type)
        if not self._is_type:
            self._template = element_type
        # Initialisiere das Array wie im ARRAY-Descriptor
        if data is not None:
            self._data: List[Any] = data
        else:
            length = self.upper - self.lower + 1
            if self._is_type:
                # element_type is a class; construct default elements
                try:
                    import enum as _enum
                    if issubclass(self.element_type, _enum.Enum):
                        # For Enum types, default to first member or ctor_args[0]
                        if self.ctor_args:
                            first = self.ctor_args[0]
                            if isinstance(first, self.element_type):
                                default_member = first
                            else:
                                try:
                                    default_member = self.element_type(first)
                                except Exception:
                                    # fallback to first defined enum member
                                    default_member = next(iter(self.element_type))
                        else:
                            default_member = next(iter(self.element_type))
                        self._data = [default_member for _ in range(length)]
                    else:
                        self._data = [self.element_type(*self.ctor_args) for _ in range(length)]
                except Exception:
                    # conservative fallback
                    self._data = [self.element_type(*self.ctor_args) for _ in range(length)]
            else:
                if isinstance(self._template, STRING):
                    self._data = [IEC_String(self._template.max_len) for _ in range(length)]
                else:
                    self._data = [type(self._template)() for _ in range(length)]
    def __getitem__(self, idx: int) -> T:
        if not (self.lower <= idx <= self.upper):
            raise IndexError
        return self._data[idx - self.lower]  # type: ignore[return-value]
    def __setitem__(self, idx: int, value: Any) -> None:
        if not (self.lower <= idx <= self.upper):
            raise IndexError
        if self._is_type:
            if isinstance(value, self.element_type):  # type: ignore
                self._data[idx - self.lower] = value
            else:
                if self.ctor_args:
                    self._data[idx - self.lower] = self.element_type(*self.ctor_args, value)  # type: ignore
                else:
                    self._data[idx - self.lower] = self.element_type(value)  # type: ignore
        else:
            if hasattr(self, '_template') and isinstance(self._template, STRING):
                # accept str/IEC_String; coerce to IEC_String
                if isinstance(value, IEC_String):
                    # copy string content respecting target max_len
                    self._data[idx - self.lower] = IEC_String(self._template.max_len, str(value))
                else:
                    self._data[idx - self.lower] = IEC_String(self._template.max_len, value)  # type: ignore[arg-type]
            else:
                elem_type = type(self._template)
                self._data[idx - self.lower] = elem_type(value)  # type: ignore
    def __len__(self) -> int:
        return len(self._data)
    def __iter__(self) -> Iterator[T]:
        # typing: underlying storage is List[Any]; cast for type checkers
        return iter(self._data)  # type: ignore[return-value]
    def __repr__(self) -> str:
        return f"IECArray[{self.lower}..{self.upper}]({self._data})"
    
    def Size(self) -> int:
        """Gibt die Größe des Arrays zurück"""
        return len(self._data)

# -------------------------
# IEC_Struct: storage creation + proxies + ergonomic __setattr__
# -------------------------
class IEC_Struct:
    _storage_types: Dict[Type["IEC_Struct"], Type[ctypes.Structure]] = {}
    
    def __init_subclass__(cls) -> None:
        """Passe Annotationen an, um primitive Typen für Zuweisungen zu erlauben."""
        super().__init_subclass__()
        if hasattr(cls, '__annotations__'):
            # Erstelle neue Annotations mit Union für IEC-Typen
            new_annotations = {}
            for name, annotation in cls.__annotations__.items():
                # Prüfe ob es ein IEC-Typ ist und erweitere mit primitive type
                if annotation == BOOL or (isinstance(annotation, type) and issubclass(annotation, BOOL)):
                    new_annotations[name] = Union[BOOL, bool]
                elif annotation == INT or (isinstance(annotation, type) and issubclass(annotation, INT)):
                    new_annotations[name] = Union[INT, int]
                elif annotation == DINT or (isinstance(annotation, type) and issubclass(annotation, DINT)):
                    new_annotations[name] = Union[DINT, int]
                elif annotation == SINT or (isinstance(annotation, type) and issubclass(annotation, SINT)):
                    new_annotations[name] = Union[SINT, int]
                elif annotation == UINT or (isinstance(annotation, type) and issubclass(annotation, UINT)):
                    new_annotations[name] = Union[UINT, int]
                elif annotation == UDINT or (isinstance(annotation, type) and issubclass(annotation, UDINT)):
                    new_annotations[name] = Union[UDINT, int]
                elif annotation == USINT or (isinstance(annotation, type) and issubclass(annotation, USINT)):
                    new_annotations[name] = Union[USINT, int]
                elif annotation == LINT or (isinstance(annotation, type) and issubclass(annotation, LINT)):
                    new_annotations[name] = Union[LINT, int]
                elif annotation == ULINT or (isinstance(annotation, type) and issubclass(annotation, ULINT)):
                    new_annotations[name] = Union[ULINT, int]
                elif annotation == BYTE or (isinstance(annotation, type) and issubclass(annotation, BYTE)):
                    new_annotations[name] = Union[BYTE, int]
                elif annotation == WORD or (isinstance(annotation, type) and issubclass(annotation, WORD)):
                    new_annotations[name] = Union[WORD, int]
                elif annotation == DWORD or (isinstance(annotation, type) and issubclass(annotation, DWORD)):
                    new_annotations[name] = Union[DWORD, int]
                elif annotation == LWORD or (isinstance(annotation, type) and issubclass(annotation, LWORD)):
                    new_annotations[name] = Union[LWORD, int]
                elif annotation == REAL or (isinstance(annotation, type) and issubclass(annotation, REAL)):
                    new_annotations[name] = Union[REAL, float]
                elif annotation == LREAL or (isinstance(annotation, type) and issubclass(annotation, LREAL)):
                    new_annotations[name] = Union[LREAL, float]
                else:
                    new_annotations[name] = annotation
            cls.__annotations__ = new_annotations

    @classmethod
    def _ensure_storage_type(cls) -> Type[ctypes.Structure]:
        if cls in IEC_Struct._storage_types:
            return IEC_Struct._storage_types[cls]
        hints = get_type_hints(cls)
        fields: List[Tuple[str, Any]] = []
        for name, annotation in hints.items():
            # skip descriptors (STRING, ARRAY)
            attr = getattr(cls, name, None)
            if hasattr(attr, "__get__") and hasattr(attr, "to_ctypes_field"):
                continue

            # Extrahiere den ctypes-Typ aus Union[Type, primitive] Annotations
            actual_type = annotation
            if hasattr(annotation, '__origin__') and annotation.__origin__ is Union:
                # Union-Typ: nimm das erste Argument das ein ctypes-Typ ist
                for arg in annotation.__args__:
                    try:
                        ctypes.sizeof(arg)
                        actual_type = arg
                        break
                    except:  #noqa: E722
                        continue

            # Enum mit .ctypes_type als Speicherfeld berücksichtigen
            import enum
            if isinstance(actual_type, type) and issubclass(actual_type, enum.IntEnum):
                # Prüfe auf eigenes Attribut ctypes_type
                ctype = getattr(actual_type, 'ctypes_type', None)
                if ctype is not None:
                    fields.append((name, ctype))
                    continue

            # IEC scalar types (ctypes-subclasses)
            try:
                ctypes.sizeof(actual_type) #type: ignore
                # actual_type is a ctypes type or subclass
                fields.append((name, actual_type))
                continue
            except Exception:
                pass
            # nested IEC_Struct
            if isinstance(annotation, type) and issubclass(annotation, IEC_Struct):
                nested = annotation._ensure_storage_type()
                fields.append((name, nested))
                continue
        #Storage = type(f"{cls.__name__}_Storage", (ctypes.Structure,), {"_fields_": fields})
        Storage = type( f"{cls.__name__}_Storage", (ctypes.Structure,), {"_pack_": 1, "_fields_": fields})
        IEC_Struct._storage_types[cls] = Storage
        return Storage

    def __init__(self, **kwargs: Any) -> None:
        Storage = self._ensure_storage_type()
        self._storage = Storage()  # zero-initialized
        # init IEC descriptors (avoid triggering @property getters)
        for name, attr in self.__class__.__dict__.items():
            try:
                if hasattr(attr, "__get__") and hasattr(attr, "to_ctypes_field"):
                    getattr(self, name)
            except Exception:
                pass
        # create proxies for annotated scalar fields (no change to class annotations)
        hints = get_type_hints(self.__class__)
        for name, annotation in hints.items():
            attr = getattr(self.__class__, name, None)
            if hasattr(attr, "__get__") and hasattr(attr, "to_ctypes_field"):
                continue
            
            # Extrahiere den ctypes-Typ aus Union[Type, primitive] Annotations
            actual_type = annotation
            if hasattr(annotation, '__origin__') and annotation.__origin__ is Union:
                # Union-Typ: nimm das erste Argument das ein ctypes-Typ ist
                for arg in annotation.__args__:
                    try:
                        ctypes.sizeof(arg)
                        actual_type = arg
                        break
                    except:#noqa: E722
                        continue
            
            # if actual_type is ctypes-compatible (scalar or nested storage), create proxy or nested wrapper
            try:
                ctypes.sizeof(actual_type)
                # scalar or ctypes-structure field
                super().__setattr__(name, _FieldProxy(self._storage, name, declared_type=None))
                continue
            except Exception:
                pass
            # enums: map to underlying storage but still expose proxy on attribute
            try:
                import enum as _enum
                if isinstance(actual_type, type) and issubclass(actual_type, _enum.IntEnum):
                    super().__setattr__(name, _FieldProxy(self._storage, name, declared_type=actual_type))
                    continue
            except Exception:
                pass
            if isinstance(actual_type, type) and issubclass(actual_type, IEC_Struct):
                # nested: wrap existing storage field
                nested_storage = getattr(self._storage, name)
                nested_obj = actual_type()
                # copy storage pointer: create nested_obj with existing storage
                nested_obj._storage = nested_storage
                super().__setattr__(name, nested_obj)
                continue
        
        # apply class-level default values to proxies/nested structs (no child __init__ needed)
        try:
            class_dict = self.__class__.__dict__
            for name in hints.keys():
                if name in class_dict:
                    default_val = class_dict[name]
                    # skip descriptors like ARRAY/STRING etc.
                    if hasattr(default_val, "__get__"):
                        continue
                    # write into storage via existing proxy/nested instance
                    try:
                        setattr(self, name, default_val)
                    except Exception:
                        # ignore defaults that cannot be applied safely
                        pass
        except Exception:
            pass
        
        # Apply initial values from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        # if attribute exists and is FieldProxy -> set its value
        existing = self.__dict__.get(name, None)
        if isinstance(existing, _FieldProxy):
            existing.value = value
            return
        # nested IEC_Struct replacement: copy bytes
        if isinstance(existing, IEC_Struct) and isinstance(value, IEC_Struct):
            ctypes.memmove(ctypes.addressof(existing._storage), ctypes.addressof(value._storage), ctypes.sizeof(existing._storage))
            return
        # default
        super().__setattr__(name, value)
    
    def set(self, **kwargs: Any) -> None:
        """Alternative zu direkter Zuweisung - vermeidet Pylance-Fehler.
        
        Beispiel:
            e.set(Flag=True, Counter=123)
        """
        for name, value in kwargs.items():
            setattr(self, name, value)

    @classmethod
    def sizeof(cls) -> int:
        size = 0
        # descriptors
        for name, attr in cls.__dict__.items():
            if hasattr(attr, "byte_size"):
                size += attr.byte_size()
        Storage = cls._ensure_storage_type()
        size += ctypes.sizeof(Storage)
        return size

    def to_payload(self) -> bytes:
        parts: List[bytes] = []
        # descriptors first
        for name, attr in self.__class__.__dict__.items():
            if hasattr(attr, "to_ctypes_field"):
                ctype, cval = attr.to_ctypes_field(self)
                parts.append(bytes(cval))
        # then storage bytes
        parts.append(ctypes.string_at(ctypes.addressof(self._storage), ctypes.sizeof(self._storage)))
        return b"".join(parts)


IEC_POU = IEC_Struct

# -------------------------
# IEC 61131-3 Type Conversion Functions

def TO_BOOL(value: Any) -> BOOL:
    return BOOL(value)

def TO_BYTE(value: Any) -> BYTE:
    return BYTE(value)

def TO_WORD(value: Any) -> WORD:
    return WORD(value)

def TO_DWORD(value: Any) -> DWORD:
    return DWORD(value)

def TO_SINT(value: Any) -> SINT:
    return SINT(value)

def TO_USINT(value: Any) -> USINT:
    return USINT(value)

def TO_INT(value: Any) -> INT:
    return INT(value)

def TO_UINT(value: Any) -> UINT:
    return UINT(value)

def TO_DINT(value: Any) -> DINT:
    return DINT(value)

def TO_UDINT(value: Any) -> UDINT:
    return UDINT(value)

def TO_REAL(value: Any) -> REAL:
    return REAL(value)

def TO_LREAL(value: Any) -> LREAL:
    return LREAL(value)

def TO_LINT(value: Any) -> LINT:
    return LINT(value)

def TO_ULINT(value: Any) -> ULINT:
    return ULINT(value)

def TO_LWORD(value: Any) -> LWORD:
    return LWORD(value)

# TIME type (DWORD in milliseconds)
TIME = UDINT

def TO_TIME(value: Any) -> UDINT:
    return UDINT(value)

# Date and Time types
DATE_AND_TIME = UDINT
DT = UDINT
TIME_OF_DAY = UDINT



class DATE(UINT):
    def to_date(self) -> datetime.date:
        """
        Converts the DATE value (days since 1970-01-01) to a Python datetime.date object.
        """
        import datetime
        epoch = datetime.date(1970, 1, 1)
        return epoch + datetime.timedelta(days=int(self.value))

    def to_string(self) -> str:
        """
        Returns the DATE as ISO string (YYYY-MM-DD).
        """
        return self.to_date().isoformat()



class TOD(UDINT):
    def to_time(self) -> datetime.time:
        """
        Converts the TOD value (ms since midnight) to a Python datetime.time object.
        """
        import datetime
        ms_total = int(self.value)
        seconds, ms = divmod(ms_total, 1000)
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return datetime.time(hour=hours, minute=minutes, second=seconds, microsecond=ms*1000)

    def to_string(self) -> str:
        """
        Returns the TOD as string (HH:MM:SS.mmm).
        """
        return self.to_time().strftime('%H:%M:%S.%f')[:-3]