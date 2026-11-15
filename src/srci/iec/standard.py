# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.iec.standard
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    IEC 61131-3 standard function blocks used by the PLC library.
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

"""IEC 61131-3 standard function blocks used by the PLC library.

Times (``PT``, ``ET``) are ``TIME`` values in milliseconds, like in the generated types.
The time base is the current clock (:func:`srci.iec.clock.get_clock`) or the clock given
to the constructor.
"""

from __future__ import annotations

from srci.iec.clock import Clock, get_clock

__all__ = ["F_TRIG", "R_TRIG", "TOF", "TON", "TP"]


def _ms(clock: Clock | None) -> int:
    return round((clock or get_clock()).monotonic() * 1000)


class R_TRIG:
    """Rising edge: ``Q`` is TRUE for one call when ``CLK`` changes FALSE -> TRUE."""

    def __init__(self) -> None:
        self.CLK = False
        self.Q = False
        self._M = False

    def __call__(self, CLK: bool | None = None) -> None:
        if CLK is not None:
            self.CLK = bool(CLK)
        self.Q = self.CLK and not self._M
        self._M = self.CLK


class F_TRIG:
    """Falling edge: ``Q`` is TRUE for one call when ``CLK`` changes TRUE -> FALSE.

    The initial state is "CLK was FALSE", so a first call with FALSE gives no edge.
    """

    def __init__(self) -> None:
        self.CLK = False
        self.Q = False
        self._M = True  # = NOT CLK of the previous call

    def __call__(self, CLK: bool | None = None) -> None:
        if CLK is not None:
            self.CLK = bool(CLK)
        self.Q = not self.CLK and not self._M
        self._M = not self.CLK


class _Timer:
    def __init__(self, clock: Clock | None = None) -> None:
        self.IN = False
        self.PT = 0
        self.Q = False
        self.ET = 0
        self._clock = clock
        self._start = 0
        self._prev_in = False

    def _inputs(self, IN: bool | None, PT: int | None) -> int:
        if IN is not None:
            self.IN = bool(IN)
        if PT is not None:
            if PT < 0:
                raise ValueError("PT must not be negative")
            self.PT = int(PT)
        return _ms(self._clock)


class TON(_Timer):
    """On delay: ``Q`` becomes TRUE ``PT`` ms after ``IN`` became TRUE."""

    def __call__(self, IN: bool | None = None, PT: int | None = None) -> None:
        now = self._inputs(IN, PT)
        if self.IN:
            if not self._prev_in:
                self._start = now
            self.ET = min(now - self._start, self.PT)
            self.Q = self.ET >= self.PT
        else:
            self.ET = 0
            self.Q = False
        self._prev_in = self.IN


class TOF(_Timer):
    """Off delay: ``Q`` follows ``IN`` and stays TRUE ``PT`` ms after ``IN`` became FALSE."""

    def __call__(self, IN: bool | None = None, PT: int | None = None) -> None:
        now = self._inputs(IN, PT)
        if self.IN:
            self.Q = True
            self.ET = 0
        else:
            if self._prev_in:
                self._start = now
            if self.Q:
                self.ET = min(now - self._start, self.PT)
                self.Q = self.ET < self.PT
        self._prev_in = self.IN


class TP(_Timer):
    """Pulse: ``Q`` is TRUE for ``PT`` ms after a rising edge of ``IN`` (not retriggerable)."""

    def __call__(self, IN: bool | None = None, PT: int | None = None) -> None:
        now = self._inputs(IN, PT)
        if not self.Q and self.IN and not self._prev_in and self.ET == 0:
            self._start = now
            self.Q = True
        if self.Q:
            self.ET = min(now - self._start, self.PT)
            if self.ET >= self.PT:
                self.Q = False
        elif not self.IN:
            self.ET = 0
        self._prev_in = self.IN
