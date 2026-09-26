# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.runtime.test_runner
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Runner: deterministic with FakeClock, plus short real-time runs.
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

"""Runner: deterministic with FakeClock, plus short real-time runs."""

from __future__ import annotations

import threading
import time

import pytest

from srci.iec.clock import FakeClock, SystemClock, get_clock
from srci.iec.standard import TON
from srci.runtime import CycleContext, Runner
from srci.sim.gateway import PlcGatewaySimulator
from srci.transport import (
    Fault,
    FaultInjectingTransport,
    FaultPlan,
    LoopbackTransport,
    TcpTransport,
    TransportTimeoutError,
)


def counter_transport() -> LoopbackTransport:
    """RC side: answers with the first byte of the request + 1."""
    return LoopbackTransport(lambda out: bytes([(out[0] + 1) % 256, 0, 0, 0]), send_size=2, recv_size=4)


class CountingProgram:
    """Writes the last received counter into the next telegram."""

    def __init__(self, clock: FakeClock | None = None, exec_time: float = 0.0) -> None:
        self.seen: list[tuple[int, int, bool]] = []
        self.clock = clock
        self.exec_time = exec_time

    def cycle(self, ctx: CycleContext) -> None:
        self.seen.append((ctx.cycle, ctx.RobotInData[0], ctx.communication_ok))
        ctx.RobotOutData[0] = ctx.RobotInData[0]
        if self.clock is not None and self.exec_time:
            self.clock.advance(self.exec_time)


def test_step_order_exchange_then_program() -> None:
    prog = CountingProgram()
    r = Runner(counter_transport(), prog, cycle_time=0.01, clock=FakeClock())
    for _ in range(4):
        r.step()
    # cycle 0 sends zeros -> receives 1, program echoes 1 -> cycle 1 receives 2 ...
    assert prog.seen == [(0, 1, True), (1, 2, True), (2, 3, True), (3, 4, True)]


def test_callable_program_and_clock_context() -> None:
    fake = FakeClock()
    seen: list[object] = []
    r = Runner(counter_transport(), lambda ctx: seen.append(get_clock()), clock=fake)
    r.step()
    assert seen == [fake]
    assert isinstance(get_clock(), SystemClock)  # restored after the cycle
    with pytest.raises(ValueError):
        Runner(counter_transport(), lambda ctx: None, cycle_time=0)


def test_transport_error_keeps_last_input() -> None:
    inner = counter_transport()
    t = FaultInjectingTransport(inner, FaultPlan(at={2: Fault.TIMEOUT, 3: Fault.TIMEOUT}))
    prog = CountingProgram()
    r = Runner(t, prog, clock=FakeClock())
    for _ in range(5):
        r.step()
    assert [ok for _, _, ok in prog.seen] == [True, True, False, False, True]
    assert prog.seen[2][1] == prog.seen[1][1]  # stale input during the error
    assert isinstance(r.last_error, type(None)) and r.communication_ok


def test_error_context() -> None:
    t = FaultInjectingTransport(counter_transport(), FaultPlan(at={0: Fault.TIMEOUT}))
    r = Runner(t, lambda ctx: None, clock=FakeClock())
    ctx = r.step()
    assert not ctx.communication_ok and isinstance(ctx.transport_error, TransportTimeoutError)
    assert ctx.RobotInData == bytes(4)


def test_fixed_period_without_drift() -> None:
    fake = FakeClock(start=0.0)
    prog = CountingProgram(fake, exec_time=0.003)
    r = Runner(counter_transport(), prog, cycle_time=0.01, clock=fake)
    r.run(cycles=100)
    s = r.monitor.statistics
    assert s.cycles == 100 and s.overruns == 0 and s.late == 0
    assert s.period_min == pytest.approx(0.01) and s.period_max == pytest.approx(0.01)
    assert fake.monotonic() == pytest.approx(1.0)  # 100 cycles x 10 ms, no drift
    assert s.exec_mean == pytest.approx(0.003)


def test_overrun_skips_missed_slots() -> None:
    fake = FakeClock(start=0.0)

    def program(ctx: CycleContext) -> None:
        fake.advance(0.025 if ctx.cycle == 3 else 0.001)

    r = Runner(counter_transport(), program, cycle_time=0.01, clock=fake)
    r.run(cycles=6)
    s = r.monitor.statistics
    assert s.overruns == 1 and s.late == 1
    assert s.period_max == pytest.approx(0.03)  # next free slot, no catch-up burst
    assert s.period_min == pytest.approx(0.01)


def test_lifesign_warning() -> None:
    fake = FakeClock(start=0.0)
    warnings: list[str] = []

    def program(ctx: CycleContext) -> None:
        fake.advance(0.06 if ctx.cycle == 2 else 0.0)

    r = Runner(
        counter_transport(), program, 0.01, clock=fake, lifesign_timeout=0.1, on_warning=warnings.append
    )
    r.run(cycles=5)
    assert r.monitor.statistics.lifesign_warnings == 1
    assert "LifeSign timeout (100 ms)" in warnings[0]


def test_timers_in_program_use_runner_clock() -> None:
    fake = FakeClock(start=0.0)
    ton = TON()
    states: list[bool] = []

    def program(ctx: CycleContext) -> None:
        ton(IN=True, PT=50)
        states.append(ton.Q)

    Runner(counter_transport(), program, cycle_time=0.01, clock=fake).run(cycles=7)
    assert states == [False] * 5 + [True, True]


def test_calls_from_other_threads() -> None:
    prog = CountingProgram()
    with Runner(counter_transport(), prog, cycle_time=0.002) as r:
        names: list[str] = []
        r.call_soon(lambda: names.append(threading.current_thread().name))
        cycle = r.call(lambda: r.cycle)
        assert isinstance(cycle, int)
        with pytest.raises(ZeroDivisionError):
            r.call(lambda: 1 / 0)
        assert r.running
    assert names == ["srci-runner"]
    assert not r.running


def test_exception_in_program_is_raised_by_stop() -> None:
    def program(ctx: CycleContext) -> None:
        if ctx.cycle == 3:
            raise RuntimeError("boom")

    r = Runner(counter_transport(), program, cycle_time=0.001).start()
    deadline = time.monotonic() + 2
    while r.running and time.monotonic() < deadline:
        time.sleep(0.005)
    with pytest.raises(RuntimeError, match="boom"):
        r.stop()
    r.stop()  # second stop is fine
    with pytest.raises(RuntimeError):
        r.start().start()


@pytest.mark.tcp
def test_real_time_run_over_tcp() -> None:
    """10 ms cycle against the gateway simulator on localhost."""
    size = 256
    with PlcGatewaySimulator(lambda b: bytes([b[0]]) + bytes(size - 1), size, size) as sim:
        t = TcpTransport("127.0.0.1", sim.port, size, size, response_timeout=0.2)
        prog = CountingProgram()
        r = Runner(t, lambda ctx: prog.cycle(ctx), cycle_time=0.01)
        r.start()
        time.sleep(0.5)
        r.stop()
        t.close()
    s = r.monitor.statistics
    assert s.cycles >= 30
    assert all(ok for _, _, ok in prog.seen)
    assert s.period_max < 0.05, f"period max {s.period_max * 1000:.1f} ms"
