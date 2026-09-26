# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.iec.test_timers
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    IEC standard FBs with a fake clock.
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

"""IEC standard FBs with a fake clock."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from srci.functions.Common import CheckTimeout, SetTimeout
from srci.iec.clock import FakeClock, SystemClock, get_clock, use_clock
from srci.iec.standard import F_TRIG, R_TRIG, TOF, TON, TP
from srci.types import RobotLibraryConstants as C


@pytest.fixture
def clock() -> Iterator[FakeClock]:
    with use_clock(FakeClock()) as c:
        assert isinstance(c, FakeClock)
        yield c


def test_clock_context() -> None:
    assert isinstance(get_clock(), SystemClock)
    fake = FakeClock(start=5.0)
    with use_clock(fake):
        assert get_clock() is fake
        fake.sleep(0.5)
        assert fake.monotonic() == 5.5 and fake.sleeps == [0.5]
    assert isinstance(get_clock(), SystemClock)
    with pytest.raises(ValueError):
        fake.advance(-1)


def test_ton(clock: FakeClock) -> None:
    t = TON()
    t(IN=True, PT=100)
    assert not t.Q and t.ET == 0
    clock.advance(0.099)
    t()
    assert not t.Q and t.ET == 99
    clock.advance(0.001)
    t()
    assert t.Q and t.ET == 100
    clock.advance(1.0)
    t()
    assert t.Q and t.ET == 100  # ET limited to PT
    t(IN=False)
    assert not t.Q and t.ET == 0
    t(IN=True)
    assert not t.Q  # restarts


def test_ton_zero_pt_and_changed_pt(clock: FakeClock) -> None:
    t = TON()
    t(IN=True, PT=0)
    assert t.Q
    t(IN=False)
    t(IN=True, PT=50)
    clock.advance(0.03)
    t(PT=20)  # PT changed while running
    assert t.Q
    with pytest.raises(ValueError):
        t(PT=-1)


def test_tof(clock: FakeClock) -> None:
    t = TOF()
    t(IN=False, PT=100)
    assert not t.Q  # no output before the first TRUE
    t(IN=True)
    assert t.Q
    t(IN=False)
    clock.advance(0.05)
    t()
    assert t.Q and t.ET == 50
    clock.advance(0.05)
    t()
    assert not t.Q and t.ET == 100
    t(IN=True)
    assert t.Q and t.ET == 0


def test_tp(clock: FakeClock) -> None:
    t = TP()
    t(IN=True, PT=100)
    assert t.Q
    t(IN=False)
    clock.advance(0.05)
    t(IN=True)  # not retriggerable
    assert t.Q and t.ET == 50
    clock.advance(0.05)
    t()
    assert not t.Q and t.ET == 100  # IN still TRUE: ET stays
    t(IN=False)
    assert t.ET == 0
    t(IN=True)
    assert t.Q


def test_edges() -> None:
    r, f = R_TRIG(), F_TRIG()
    seq = [False, True, True, False, False, True]
    rq, fq = [], []
    for clk in seq:
        r(CLK=clk)
        f(CLK=clk)
        rq.append(r.Q)
        fq.append(f.Q)
    assert rq == [False, True, False, False, False, True]
    assert fq == [False, False, False, True, False, False]


def test_set_and_check_timeout(clock: FakeClock) -> None:
    timer = TON()
    assert SetTimeout(PT=200, rTimer=timer) == C.OK
    assert CheckTimeout(timer) == C.RUNNING
    clock.advance(0.2)
    assert CheckTimeout(timer) == C.OK
    SetTimeout(PT=200, rTimer=timer)  # restart
    assert CheckTimeout(timer) == C.RUNNING
