"""Clocks: real time for operation, :class:`FakeClock` for deterministic tests.

IEC timers and the runtime take the time from the *current clock*
(:func:`get_clock`), which can be replaced with :func:`use_clock`.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Protocol

__all__ = ["Clock", "FakeClock", "SystemClock", "get_clock", "set_clock", "use_clock"]


class Clock(Protocol):
    def monotonic(self) -> float:
        """Monotonic time in seconds (timers, cycle timing)."""
        ...

    def time(self) -> float:
        """Wall clock time, seconds since 1970-01-01 UTC (SystemTime)."""
        ...

    def sleep(self, seconds: float) -> None: ...


class SystemClock:
    """The real clock."""

    def monotonic(self) -> float:
        return time.monotonic()

    def time(self) -> float:
        return time.time()

    def sleep(self, seconds: float) -> None:
        if seconds > 0:
            time.sleep(seconds)


class FakeClock:
    """Manually advanced clock; ``sleep`` advances the time immediately."""

    def __init__(self, start: float = 1000.0, wall: datetime | None = None) -> None:
        self._now = start
        self._wall_offset = (wall or datetime(2026, 1, 1, tzinfo=UTC)).timestamp() - start
        self.sleeps: list[float] = []

    def monotonic(self) -> float:
        return self._now

    def time(self) -> float:
        return self._now + self._wall_offset

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.advance(max(0.0, seconds))

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("time cannot go backwards")
        self._now += seconds


_SYSTEM_CLOCK = SystemClock()
_current: ContextVar[Clock] = ContextVar("srci_clock", default=_SYSTEM_CLOCK)


def get_clock() -> Clock:
    return _current.get()


def set_clock(clock: Clock) -> None:
    _current.set(clock)


@contextmanager
def use_clock(clock: Clock) -> Iterator[Clock]:
    token = _current.set(clock)
    try:
        yield clock
    finally:
        _current.reset(token)
