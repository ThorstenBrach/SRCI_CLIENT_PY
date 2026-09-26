from datetime import UTC, datetime, timedelta, timezone

from srci.functions.Convert import DT
from srci.iec.clock import FakeClock
from srci.runtime import system_time_now
from srci.types import IEC_TIMESTAMP, SystemTime


def date(y: int, m: int, d: int) -> int:
    return int(datetime(y, m, d, tzinfo=UTC).timestamp())


def test_iec_date_is_days_since_1990() -> None:
    assert DT.DATE_TO_IEC_DATE(date(1990, 1, 1)) == 0
    assert DT.DATE_TO_IEC_DATE(date(1990, 1, 2)) == 1
    assert DT.DATE_TO_IEC_DATE(date(2026, 9, 26)) == (datetime(2026, 9, 26) - datetime(1990, 1, 1)).days
    assert DT.IEC_DATE_TO_DATE(DT.DATE_TO_IEC_DATE(date(2026, 9, 26))) == date(2026, 9, 26)


def test_timestamps() -> None:
    st = SystemTime(SystemDate=date(2026, 9, 26), SystemTime=12 * 3_600_000 + 500)
    ts = DT.SYSTEMTIME_TO_IEC_TIMESTAMP(st)
    assert isinstance(ts, IEC_TIMESTAMP) and ts.IEC_TIME == 12 * 3_600_000 + 500
    assert DT.IEC_TIMESTAMP_TO_SYSTEMTIME(ts) == st
    assert DT.IEC_TIMESTAMP_TO_DT(ts) == date(2026, 9, 26) + 12 * 3600
    assert DT.TIME_TO_IEC_TIME(5) == DT.IEC_TIME_TO_TIME(5) == 5


def test_system_time_from_clock() -> None:
    clock = FakeClock(wall=datetime(2026, 9, 26, 14, 30, 5, 250_000, tzinfo=UTC))
    st = system_time_now(clock, UTC)
    assert st.SystemDate == date(2026, 9, 26)
    assert st.SystemTime == ((14 * 60 + 30) * 60 + 5) * 1000 + 250
    cest = timezone(timedelta(hours=2))
    assert system_time_now(clock, cest).SystemTime == ((16 * 60 + 30) * 60 + 5) * 1000 + 250
    local = system_time_now(clock)  # local zone of the machine
    assert 0 <= local.SystemTime < 86_400_000
