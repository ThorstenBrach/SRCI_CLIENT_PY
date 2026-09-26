"""SystemTime (``VAR_INPUT`` of MC_RobotTaskFB) from a clock."""

from __future__ import annotations

from datetime import UTC, datetime, tzinfo

from srci.iec.clock import Clock, get_clock
from srci.types import SystemTime

__all__ = ["system_time_now"]


def system_time_now(clock: Clock | None = None, tz: tzinfo | None = None) -> SystemTime:
    """Current date/time in the client's time zone (spec: ClientDate/ClientTime).

    ``SystemDate`` = DATE (seconds since 1970-01-01 of the local date),
    ``SystemTime`` = TOD (milliseconds since local midnight). ``tz=None`` = local zone.
    """
    ts = (clock or get_clock()).time()
    local = datetime.fromtimestamp(ts, tz) if tz is not None else datetime.fromtimestamp(ts).astimezone()
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0)
    date_seconds = int(datetime(local.year, local.month, local.day, tzinfo=UTC).timestamp())
    tod_ms = int((local - midnight).total_seconds() * 1000)
    return SystemTime(SystemDate=date_seconds, SystemTime=tod_ms)
