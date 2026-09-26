from RobotLibrary.IEC_Types import (
    TIME, BOOL, INT, DINT, SINT, UINT, USINT, UDINT, LINT, ULINT, BYTE, WORD, DWORD, LWORD, REAL, LREAL, _FieldProxy, IEC_String
)
from RobotLibrary.Constants import OK,RUNNING

from typing import  Union, Optional, Any, overload
from enum import IntEnum


#region Trigger

class R_TRIG:
    """
    IEC 61131-3 konformer R_TRIG (steigende Flanke)
    Aufruf:
        r = R_TRIG()
        r(CLK=True)
        if r.Q: ...
    """

    def __init__(self) -> None:
        self.CLK : bool = False   # Input
        self.Q   : bool = False   # Output
        self.M   : bool = False   # Memory (previous CLK)

    def __call__(self, *, CLK: Optional[bool] = None) -> bool:
        """
        IEC-konformer Aufruf:
            r(CLK = value)
        """
        # Eingang übernehmen
        if (CLK is not None):
            self.CLK = CLK
        else:
            self.CLK = self.CLK

        # steigende Flanke: CLK == TRUE und M == FALSE
        self.Q = (self.CLK) and not (self.M)

        # Speicher aktualisieren
        self.M = self.CLK

        return self.Q
    
class F_TRIG:
    """
    IEC 61131-3 konformer F_TRIG (fallende Flanke)
    Aufruf:
        f = F_TRIG()
        f(CLK=True)
        if f.Q: ...
    """

    def __init__(self) -> None:
        self.CLK : bool = False
        self.Q   : bool = False
        self.M   : bool = False

    def __call__(self, *, CLK: Optional[bool] = None) -> bool:
        # Eingang übernehmen
        if CLK is not None:
            self.CLK = CLK
        else:
            self.CLK = self.CLK

        # fallende Flanke: CLK == FALSE und M == TRUE
        self.Q = (not (self.CLK)) and (self.M)

        # Speicher aktualisieren
        self.M = self.CLK

        return self.Q

#endregion


#region Timer

class TON:
    """
    IEC 61131-3 konformer TON (Timer On-Delay)
    Erzeugt eine verzögerte Einschaltung.
    
    Aufruf:
        timer = TON()
        timer(IN=True, PT=5000.0)  # 5000 ms (5 Sekunden) Verzögerung
        if timer.Q: ...
    """
    
    def __init__(self) -> None:
        self.IN : bool = False    # Input
        self.PT : TIME = TIME(0)            # Preset Time (Sollzeit in Millisekunden)
        self.Q : bool = False     # Output
        self.ET : float = 0.0            # Elapsed Time (Istzeit in Millisekunden)
        self._start_time: Optional[float] = None
    
    def __call__(self, *, IN: bool, PT: TIME, current_time: Optional[float] = None) -> bool:
        """
        IEC-konformer Aufruf:
            timer(IN=True, PT=5000.0, current_time=time.time())
        
        Args:
            IN: Eingang (startet Timer bei steigender Flanke)
            PT: Preset Time in Millisekunden
            current_time: Aktuelle Zeit in Sekunden (default: time.time())
        """
        import time
        if current_time is None:
            current_time = time.time()
        
        self.IN = IN
        self.PT = PT  # in ms
        
        # Steigende Flanke: Timer starten
        if self.IN and self._start_time is None:
            self._start_time = current_time
            self.ET = 0.0
            self.Q = False
        
        # Timer läuft
        elif self.IN and self._start_time is not None:
            elapsed_sec = current_time - self._start_time
            self.ET = elapsed_sec * 1000  # Convert to ms
            if self.ET >= self.PT.value:
                self.ET = self.PT.value
                self.Q = True
        
        # Fallende Flanke: Timer zurücksetzen
        elif not self.IN:
            self._start_time = None
            self.ET = 0.0
            self.Q = False
        
        return self.Q

class TOF:
    """
    IEC 61131-3 konformer TOF (Timer Off-Delay)
    Erzeugt eine verzögerte Ausschaltung.
    
    Aufruf:
        timer = TOF()
        timer(IN=False, PT=5000.0)  # 5000 ms (5 Sekunden) Verzögerung beim Ausschalten
        if timer.Q: ...
    """
    
    def __init__(self) -> None:
        self.IN : bool = False    # Input
        self.PT : TIME = TIME(0)            # Preset Time (Sollzeit in Millisekunden)
        self.Q : bool = False     # Output
        self.ET : float = 0.0            # Elapsed Time (Istzeit in Millisekunden)
        self._start_time: Optional[float] = None
    
    def __call__(self, *, IN:  bool, PT: TIME, current_time: Optional[float] = None) -> bool:
        """
        IEC-konformer Aufruf:
            timer(IN=False, PT=5000.0, current_time=time.time())
        
        Args:
            IN: Eingang
            PT: Preset Time in Millisekunden
            current_time: Aktuelle Zeit in Sekunden (default: time.time())
        """
        import time
        if current_time is None:
            current_time = time.time()
        
        prev_in = self.IN
        self.IN = IN
        self.PT = PT  # in ms
        
        # Steigende Flanke von IN: Ausgang sofort auf True, Timer zurücksetzen
        if self.IN and not prev_in:
            self.Q = True
            self._start_time = None
            self.ET = 0.0
        
        # Eingang bleibt True: Ausgang bleibt True
        elif self.IN:
            self.Q = True
            self._start_time = None
            self.ET = 0.0
        
        # Fallende Flanke: Timer starten (Q bleibt True für PT Zeit)
        elif not self.IN and prev_in and self.Q:
            self._start_time = current_time
            self.ET = 0.0
        
        # Timer läuft
        elif not self.IN and self._start_time is not None:
            elapsed_sec = current_time - self._start_time
            self.ET = elapsed_sec * 1000  # Convert to ms
            if self.ET >= self.PT.value:
                self.ET = self.PT.value
                self.Q = False
                self._start_time = None
        
        return self.Q

class TP:
    """
    IEC 61131-3 konformer TP (Timer Pulse)
    Erzeugt einen Impuls mit fester Zeitdauer.
    
    Aufruf:
        timer = TP()
        timer(IN=True, PT=5000.0)  # 5000 ms (5 Sekunden) Impuls
        if timer.Q: ...
    """
    
    def __init__(self) -> None:
        self.IN = BOOL(False)    # Input
        self.PT = 0.0            # Preset Time (Sollzeit in Millisekunden)
        self.Q = BOOL(False)     # Output
        self.ET = 0.0            # Elapsed Time (Istzeit in Millisekunden)
        self._start_time: Optional[float] = None
        self._triggered = False
    
    def __call__(self, *, IN: Union[BOOL, bool], PT: float, current_time: Optional[float] = None) -> BOOL:
        """
        IEC-konformer Aufruf:
            timer(IN=True, PT=5000.0, current_time=time.time())
        
        Args:
            IN: Eingang (steigende Flanke startet Impuls)
            PT: Preset Time in Millisekunden
            current_time: Aktuelle Zeit in Sekunden (default: time.time())
        """
        import time
        if current_time is None:
            current_time = time.time()
        
        self.IN = BOOL(IN)
        self.PT = float(PT)  # in ms
        
        # Steigende Flanke und noch nicht getriggert: Timer starten
        if self.IN and not self._triggered and self._start_time is None:
            self._start_time = current_time
            self.ET = 0.0
            self.Q = BOOL(True)
            self._triggered = True
        
        # Timer läuft
        if self._start_time is not None:
            elapsed_sec = current_time - self._start_time
            self.ET = elapsed_sec * 1000.0  # Convert to ms
            if self.ET >= self.PT:
                self.ET = self.PT
                self.Q = BOOL(False)
                self._start_time = None
        
        # Eingang fällt: bereit für nächsten Trigger
        if not self.IN:
            self._triggered = False
        
        return self.Q
    
#endregion

#region String Functions

def LEN(IN: str | IEC_String) -> int:
    """
    IEC 61131-3 String Function: LEN
    Gibt die Länge eines Strings zurück.
    
    Args:
        IN: Input String
    
    Returns:
        Länge des Strings
    """
    return len(str(IN))


@overload
def LEFT(IN: str, L: int) -> str: ...
@overload
def LEFT(IN: IEC_String, L: int) -> IEC_String: ...
def LEFT(IN: str | IEC_String, L: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: LEFT
    Gibt die L ersten Zeichen von IN zurück.
    
    Args:
        IN: Input String
        L: Anzahl der Zeichen
    
    Returns:
        Die L ersten Zeichen
    """
    s = str(IN)
    if isinstance(IN, IEC_String):
        return IEC_String(IN.max_len, s[:max(0, int(L))])
    return s[:max(0, int(L))]


@overload
def RIGHT(IN: str, L: int) -> str: ...
@overload
def RIGHT(IN: IEC_String, L: int) -> IEC_String: ...
def RIGHT(IN: str | IEC_String, L: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: RIGHT
    Gibt die L letzten Zeichen von IN zurück.
    
    Args:
        IN: Input String
        L: Anzahl der Zeichen
    
    Returns:
        Die L letzten Zeichen
    """
    s = str(IN)
    if isinstance(IN, IEC_String):
        if L <= 0:
            return IEC_String(IN.max_len, "")
        return IEC_String(IN.max_len, s[-int(L):])
    if L <= 0:
        return ""
    return s[-int(L):]


@overload
def MID(IN: str, Len: int, Pos: int) -> str: ...
@overload
def MID(IN: IEC_String, Len: int, Pos: int) -> IEC_String: ...
def MID(IN: str | IEC_String, Len: int, Pos: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: MID
    Gibt L Zeichen ab Position P zurück.
    
    Args:
        IN: Input String
        L: Anzahl der Zeichen
        P: Startposition (1-basiert, IEC-Standard)
    
    Returns:
        L Zeichen ab Position P
    """
    s = str(IN)
    start = int(Pos) - 1  # Convert 1-based to 0-based
    if start < 0:
        start = 0
    segment = s[start:start + int(Len)]
    if isinstance(IN, IEC_String):
        return IEC_String(IN.max_len, segment)
    return segment


@overload
def CONCAT(IN1: str, IN2: str) -> str: ...
@overload
def CONCAT(IN1: IEC_String, IN2: IEC_String) -> IEC_String: ...
@overload
def CONCAT(IN1: IEC_String, IN2: str) -> IEC_String: ...
@overload
def CONCAT(IN1: str, IN2: IEC_String) -> IEC_String: ...
def CONCAT(IN1: str | IEC_String, IN2: str | IEC_String) -> str | IEC_String:
    """
    IEC 61131-3 String Function: CONCAT
    Fügt zwei Strings zusammen.
    
    Args:
        IN1: Erster String
        IN2: Zweiter String
    
    Returns:
        Konkatenierter String
    """
    s = str(IN1) + str(IN2)
    if isinstance(IN1, IEC_String):
        return IEC_String(IN1.max_len, s)
    if isinstance(IN2, IEC_String):
        return IEC_String(IN2.max_len, s)
    return s


@overload
def INSERT(IN1: str, IN2: str, P: int) -> str: ...
@overload
def INSERT(IN1: IEC_String, IN2: IEC_String | str, P: int) -> IEC_String: ...
def INSERT(IN1: str | IEC_String, IN2: str | IEC_String, P: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: INSERT
    Fügt IN2 in IN1 an Position P ein.
    
    Args:
        IN1: Original String
        IN2: Einzufügender String
        P: Position (1-basiert)
    
    Returns:
        String mit eingefügtem Teil
    """
    s1 = str(IN1)
    s2 = str(IN2)
    pos = int(P) - 1  # Convert 1-based to 0-based
    if pos < 0:
        pos = 0
    if pos > len(s1):
        pos = len(s1)
    res = s1[:pos] + s2 + s1[pos:]
    if isinstance(IN1, IEC_String):
        return IEC_String(IN1.max_len, res)
    return res


@overload
def DELETE(IN: str, L: int, P: int) -> str: ...
@overload
def DELETE(IN: IEC_String, L: int, P: int) -> IEC_String: ...
def DELETE(IN: str | IEC_String, L: int, P: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: DELETE
    Löscht L Zeichen ab Position P aus IN.
    
    Args:
        IN: Input String
        L: Anzahl zu löschender Zeichen
        P: Startposition (1-basiert)
    
    Returns:
        String mit gelöschtem Teil
    """
    s = str(IN)
    start = int(P) - 1  # Convert 1-based to 0-based
    if start < 0:
        start = 0
    res = s[:start] + s[start + int(L):]
    if isinstance(IN, IEC_String):
        return IEC_String(IN.max_len, res)
    return res


@overload
def REPLACE(IN1: str, IN2: str, L: int, P: int) -> str: ...
@overload
def REPLACE(IN1: str, IN2: IEC_String, L: int, P: int) -> str: ...
@overload
def REPLACE(IN1: IEC_String, IN2: str, L: int, P: int) -> IEC_String: ...
@overload
def REPLACE(IN1: IEC_String, IN2: IEC_String, L: int, P: int) -> IEC_String: ...
def REPLACE(IN1: str | IEC_String, IN2: str | IEC_String, L: int, P: int) -> str | IEC_String:
    """
    IEC 61131-3 String Function: REPLACE
    Ersetzt L Zeichen ab Position P in IN1 durch IN2.
    
    Args:
        IN1: Original String
        IN2: Ersetzender String
        L: Anzahl zu ersetzender Zeichen
        P: Startposition (1-basiert)
    
    Returns:
        String mit ersetztem Teil
    """
    s1 = str(IN1)
    s2 = str(IN2)
    start = int(P) - 1  # Convert 1-based to 0-based
    if start < 0:
        start = 0
    res = s1[:start] + s2 + s1[start + int(L):]
    if isinstance(IN1, IEC_String):
        return IEC_String(IN1.max_len, res)
    return res


@overload
def FIND(IN1: str, IN2: str) -> int: ...
@overload
def FIND(IN1: str, IN2: IEC_String) -> int: ...
@overload
def FIND(IN1: IEC_String, IN2: str) -> int: ...
@overload
def FIND(IN1: IEC_String, IN2: IEC_String) -> int: ...
def FIND(IN1: str | IEC_String, IN2: str | IEC_String) -> int:
    """
    IEC 61131-3 String Function: FIND
    Sucht IN2 in IN1 und gibt die Position zurück.
    
    Args:
        IN1: String in dem gesucht wird
        IN2: Zu suchender String
    
    Returns:
        Position (1-basiert) oder 0 wenn nicht gefunden
    """
    s1 = str(IN1)
    s2 = str(IN2)
    pos = s1.find(s2)
    if pos == -1:
        return 0
    return pos + 1  # Convert 0-based to 1-based

@overload
def StrReplace(s: str, sub1: str, sub2: str) -> str: ...
@overload
def StrReplace(s: IEC_String, sub1: str, sub2: str) -> IEC_String: ...
@overload
def StrReplace(s: IEC_String, sub1: IEC_String, sub2: str) -> IEC_String: ...
@overload
def StrReplace(s: IEC_String, sub1: str, sub2: IEC_String) -> IEC_String: ...
@overload
def StrReplace(s: IEC_String, sub1: IEC_String, sub2: IEC_String) -> IEC_String: ...
def StrReplace(s: str | IEC_String, sub1: str | IEC_String, sub2: str | IEC_String) -> str | IEC_String:
    """
    Ersetzt alle Vorkommen von sub1 in s durch sub2.
    Typisierungen verwenden "str" für Pylance-Kompatibilität; interne Funktionen
    akzeptieren sowohl Python-Strings als auch IEC_String via str()-Konvertierung.
    """
    tmp = str(s)
    sub1_str = str(sub1)
    sub2_str = str(sub2)
    while FIND(tmp, sub1_str) > 0:
        tmp = str(REPLACE(tmp, sub2_str, LEN(sub1_str), FIND(tmp, sub1_str)))
    if isinstance(s, IEC_String):
        return IEC_String(s.max_len, tmp)
    return tmp



def LIMIT(LoLim: Any, IN: Any, UpLim: Any) -> Any:
    """
    IEC 61131-3 Function: LIMIT
    Clamp IN to the inclusive range [LoLim, UpLim].

    Supports Python primitives, IEC scalar types, enums (IntEnum), and FieldProxy.
    Returns a value of the same "kind" as IN (same type for IEC types/enums; primitive for primitives).
    """
    # Normalize lower/upper order
    lo, hi = LoLim, UpLim
    try:
        # if swapped accidentally, correct it
        if (float(lo) if isinstance(lo, (float, REAL, LREAL)) else int(lo)) > (float(hi) if isinstance(hi, (float, REAL, LREAL)) else int(hi)):
            lo, hi = hi, lo
    except Exception:
        pass

    def is_float_like(x: Any) -> bool:
        return isinstance(x, (float, REAL, LREAL))

    def to_num(x: Any) -> float | int:
        # FieldProxy
        if isinstance(x, _FieldProxy):
            # decide float vs int by field_type
            t = x.field_type
            if t in (REAL, LREAL):
                return float(x)
            return int(x)
        # IntEnum
        if isinstance(x, IntEnum):
            return int(x)
        # IEC scalars & primitives with casts
        try:
            return float(x) if is_float_like(x) else int(x)
        except Exception:
            # Fallback: try to access .value then cast
            v = getattr(x, 'value', x)
            try:
                return float(v) if is_float_like(v) else int(v)
            except Exception:
                # last resort: raise
                raise

    # Determine numeric domain (float if any arg is float-like)
    use_float = is_float_like(lo) or is_float_like(IN) or is_float_like(hi)
    n_lo = to_num(lo)
    n_in = to_num(IN)
    n_hi = to_num(hi)
    if use_float:
        n_lo = float(n_lo)
        n_in = float(n_in)
        n_hi = float(n_hi)
        n_res: float | int = max(n_lo, min(n_in, n_hi))
    else:
        n_lo = int(n_lo)
        n_in = int(n_in)
        n_hi = int(n_hi)
        n_res = max(n_lo, min(n_in, n_hi))

    def from_num(ref: Any, n: float | int) -> Any:
        # FieldProxy: return appropriate type instance (enum or IEC scalar)
        if isinstance(ref, _FieldProxy):
            decl = getattr(ref, '_decl_type', None)
            if isinstance(decl, type) and issubclass(decl, IntEnum):
                return decl(int(n))
            t = ref.field_type
            try:
                return t(n)  # IEC scalar constructor from number
            except Exception:
                return n
        # Enums: rebuild enum instance
        if isinstance(ref, IntEnum):
            return type(ref)(int(n))
        # IEC scalar instances: preserve type
        for t in (BOOL, INT, DINT, SINT, UINT, USINT, UDINT, LINT, ULINT, BYTE, WORD, DWORD, LWORD, REAL, LREAL):
            if isinstance(ref, t):
                try:
                    return type(ref)(n) #type: ignore
                except Exception:
                    break
        # primitives fall back
        if use_float or isinstance(ref, float):
            return float(n)
        return int(n)

    return from_num(IN, n_res)


def SetTimeout(PT: TIME, Timer : TON) -> int :
    Timer(PT = PT, IN = False) # Reset timer
    Timer(PT = PT, IN = True)  # Start timer
    return OK

def CheckTimeout(Timer : TON) -> int :
    # call timer
    Timer(IN= Timer.IN, PT= Timer.PT)   
    
    if ( Timer.Q) :
        return OK
    else :
        return RUNNING
    
#endregion



def LIMIT( LoLim : int, value : int, UpLim : int) -> int: 

    if value < LoLim :
        value = LoLim
    
    if value > UpLim :
        value = UpLim
    
