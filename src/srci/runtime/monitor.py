"""Cycle time monitoring."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field

__all__ = ["CycleMonitor", "CycleStatistics"]

log = logging.getLogger("srci.runtime")


@dataclass
class CycleStatistics:
    cycles: int = 0
    period_last: float = 0.0
    period_min: float = float("inf")
    period_max: float = 0.0
    exec_last: float = 0.0
    exec_max: float = 0.0
    exec_total: float = 0.0
    overruns: int = 0  # execution took longer than the cycle time
    late: int = 0  # period longer than 1.5 x cycle time
    lifesign_warnings: int = 0

    @property
    def exec_mean(self) -> float:
        return self.exec_total / self.cycles if self.cycles else 0.0

    @property
    def jitter(self) -> float:
        """Max - min period."""
        return 0.0 if self.cycles < 2 else self.period_max - self.period_min


@dataclass
class CycleMonitor:
    """Collects cycle statistics and warns before the RC LifeSign timeout is reached.

    ``lifesign_timeout`` (s): the RC expects a LifeSign change within this time. A warning
    is raised when a period exceeds ``lifesign_warn_ratio`` of it.
    """

    cycle_time: float
    lifesign_timeout: float | None = None
    lifesign_warn_ratio: float = 0.5
    on_warning: Callable[[str], None] | None = None
    statistics: CycleStatistics = field(default_factory=CycleStatistics)
    _last_start: float | None = field(default=None, init=False, repr=False)

    def record(self, start: float, end: float) -> None:
        s = self.statistics
        s.cycles += 1
        exec_time = end - start
        s.exec_last = exec_time
        s.exec_max = max(s.exec_max, exec_time)
        s.exec_total += exec_time
        if exec_time > self.cycle_time:
            s.overruns += 1
        if self._last_start is not None:
            period = start - self._last_start
            s.period_last = period
            s.period_min = min(s.period_min, period)
            s.period_max = max(s.period_max, period)
            if period > 1.5 * self.cycle_time:
                s.late += 1
            if (
                self.lifesign_timeout is not None
                and period > self.lifesign_timeout * self.lifesign_warn_ratio
            ):
                s.lifesign_warnings += 1
                self._warn(
                    f"cycle period {period * 1000:.1f} ms exceeds {self.lifesign_warn_ratio:.0%} of the "
                    f"LifeSign timeout ({self.lifesign_timeout * 1000:.0f} ms)"
                )
        self._last_start = start

    def reset(self) -> None:
        self.statistics = CycleStatistics()
        self._last_start = None

    def _warn(self, text: str) -> None:
        log.warning(text)
        if self.on_warning is not None:
            self.on_warning(text)
