"""Functions/Convert/DT of the PLC library.

Codesys representation: ``DATE``/``DT`` = seconds since 1970-01-01, ``TOD`` = ms since
midnight. SRCI: ``IEC_DATE`` = days since 1990-01-01 (UINT), ``IEC_TIME`` = ms since
midnight (spec table 5-82).
"""

from __future__ import annotations

from srci.types import IEC_TIMESTAMP, SystemTime

__all__ = [
    "DATE_TO_IEC_DATE",
    "IEC_DATE_TO_DATE",
    "IEC_TIMESTAMP_TO_DT",
    "IEC_TIMESTAMP_TO_SYSTEMTIME",
    "IEC_TIME_TO_TIME",
    "SYSTEMTIME_TO_IEC_TIMESTAMP",
    "TIME_TO_IEC_TIME",
]

_DATE_1990 = 631_152_000  # DATE#1990-01-01 in seconds since 1970
_DAY = 86_400


# ST-Source: Functions/Convert/DT/DATE_TO_IEC_DATE.st  sha256: 7a1e453258b9a4dc
def DATE_TO_IEC_DATE(Value: int) -> int:
    """Days since 1990-01-01 (UDINT_TO_UINT: modulo 65536 like in ST)."""
    return ((Value - _DATE_1990) // _DAY) & 0xFFFF


# ST-Source: Functions/Convert/DT/IEC_DATE_TO_DATE.st  sha256: 6cd1c6f4cdcfbfca
def IEC_DATE_TO_DATE(Value: int) -> int:
    return _DATE_1990 + Value * _DAY


# ST-Source: Functions/Convert/DT/IEC_TIME_TO_TIME.st  sha256: f9592fecd60fae75
def IEC_TIME_TO_TIME(Value: int) -> int:
    return Value


# ST-Source: Functions/Convert/DT/TIME_TO_IEC_TIME.st  sha256: 24e5fbd3ccf43fd1
def TIME_TO_IEC_TIME(Value: int) -> int:
    return Value


# ST-Source: Functions/Convert/DT/IEC_TIMESTAMP_TO_DT.st  sha256: 12807afa0d9c4d0b
def IEC_TIMESTAMP_TO_DT(Value: IEC_TIMESTAMP) -> int:
    """DT (seconds since 1970). ST builds it via strings; the result is the same."""
    return IEC_DATE_TO_DATE(Value.IEC_DATE) + IEC_TIME_TO_TIME(Value.IEC_TIME) // 1000


# ST-Source: Functions/Convert/DT/IEC_TIMESTAMP_TO_SYSTEMTIME.st  sha256: e44d488ae7155d6b
def IEC_TIMESTAMP_TO_SYSTEMTIME(Value: IEC_TIMESTAMP) -> SystemTime:
    return SystemTime(
        SystemDate=IEC_DATE_TO_DATE(Value.IEC_DATE), SystemTime=IEC_TIME_TO_TIME(Value.IEC_TIME)
    )


# ST-Source: Functions/Convert/DT/SYSTEMTIME_TO_IEC_TIMESTAMP.st  sha256: efd39b4ec7a0ce1c
def SYSTEMTIME_TO_IEC_TIMESTAMP(SystemTime: SystemTime) -> IEC_TIMESTAMP:
    return IEC_TIMESTAMP(
        IEC_DATE=DATE_TO_IEC_DATE(SystemTime.SystemDate), IEC_TIME=TIME_TO_IEC_TIME(SystemTime.SystemTime)
    )
