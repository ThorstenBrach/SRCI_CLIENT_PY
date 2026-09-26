"""Runner: executes the program cyclically and exchanges the telegrams.

One cycle (in one thread, like a PLC task)::

    queued calls from other threads
    RobotInData  <- transport.exchange(RobotOutData of the previous cycle)
    program.cycle(ctx)   # e.g. MC_RobotTaskFB + function blocks, fills RobotOutData

If the transport fails, the program still runs with the last valid ``RobotInData``
(like PROFINET inputs that keep their last value) and ``ctx.communication_ok`` is FALSE.
The SRCI LifeSign supervision of the RobotTask detects a lasting communication loss.
"""

from __future__ import annotations

import logging
import math
import queue
import threading
from collections.abc import Callable
from concurrent.futures import Future
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Protocol, Self, TypeVar, runtime_checkable

from srci.iec.clock import Clock, get_clock, use_clock
from srci.runtime.monitor import CycleMonitor
from srci.transport.base import Transport, TransportError

__all__ = ["CycleContext", "Program", "Runner"]

log = logging.getLogger("srci.runtime")
T = TypeVar("T")


@dataclass
class CycleContext:
    cycle: int
    RobotInData: bytes
    RobotOutData: bytearray
    communication_ok: bool
    transport_error: TransportError | None
    clock: Clock


@runtime_checkable
class Program(Protocol):
    def cycle(self, ctx: CycleContext) -> None: ...


ProgramLike = Program | Callable[[CycleContext], None]


class Runner:
    """Cyclic execution of a program with a transport."""

    def __init__(
        self,
        transport: Transport,
        program: ProgramLike,
        cycle_time: float = 0.01,
        *,
        clock: Clock | None = None,
        lifesign_timeout: float | None = None,
        on_warning: Callable[[str], None] | None = None,
    ) -> None:
        if cycle_time <= 0:
            raise ValueError("cycle_time must be > 0")
        self.transport = transport
        self._program: Callable[[CycleContext], None] = (
            program.cycle if isinstance(program, Program) else program
        )
        self.cycle_time = cycle_time
        self.clock: Clock = clock or get_clock()
        self.monitor = CycleMonitor(cycle_time, lifesign_timeout, on_warning=on_warning)
        self.cycle = 0
        self.communication_ok = False
        self.last_error: TransportError | None = None
        self._in = bytes(transport.recv_size)
        self._out = bytearray(transport.send_size)
        self._calls: queue.SimpleQueue[Callable[[], None]] = queue.SimpleQueue()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._exception: BaseException | None = None

    # ------------------------------------------------------------------ one cycle

    def step(self) -> CycleContext:
        """Execute exactly one cycle (no waiting)."""
        with use_clock(self.clock):
            start = self.clock.monotonic()
            self._run_calls()
            error: TransportError | None = None
            try:
                self._in = self.transport.exchange(self._out)
            except TransportError as exc:
                error = exc
                if self.communication_ok:
                    log.warning("communication lost: %s", exc)
            if error is None and not self.communication_ok and self.cycle > 0:
                log.info("communication restored")
            self.communication_ok = error is None
            self.last_error = error
            ctx = CycleContext(self.cycle, self._in, self._out, self.communication_ok, error, self.clock)
            self._program(ctx)
            self.cycle += 1
            self.monitor.record(start, self.clock.monotonic())
            return ctx

    # ------------------------------------------------------------------ loop

    def run(self, cycles: int | None = None) -> None:
        """Run in the calling thread until :meth:`stop` (or ``cycles`` cycles)."""
        t0 = self.clock.monotonic()
        slot = 0
        done = 0
        while not self._stop.is_set() and (cycles is None or done < cycles):
            self.step()
            done += 1
            now = self.clock.monotonic()
            slot += 1
            next_start = t0 + slot * self.cycle_time
            if now > next_start:  # overrun: skip the missed slots, no burst of catch-up cycles
                slot = math.floor((now - t0) / self.cycle_time) + 1
                next_start = t0 + slot * self.cycle_time
            self.clock.sleep(next_start - now)

    def start(self) -> Self:
        """Run in a background thread."""
        if self._thread is not None:
            raise RuntimeError("runner already started")
        self._stop.clear()

        def target() -> None:
            try:
                self.run()
            except BaseException as exc:  # re-raised in stop()
                self._exception = exc
                log.exception("runner stopped by an exception")

        self._thread = threading.Thread(target=target, name="srci-runner", daemon=True)
        self._thread.start()
        return self

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the background thread; re-raises an exception of the program."""
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout)
            self._thread = None
        if self._exception is not None:
            exc, self._exception = self._exception, None
            raise exc

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.stop()

    # ------------------------------------------------------------------ calls from other threads

    def call_soon(self, fn: Callable[[], Any]) -> None:
        """Execute ``fn`` in the runner thread at the start of the next cycle."""
        self._calls.put(fn)

    def call(self, fn: Callable[[], T], timeout: float | None = 5.0) -> T:
        """Execute ``fn`` in the runner thread and return its result (blocking)."""
        if threading.current_thread() is self._thread:
            return fn()
        future: Future[T] = Future()

        def wrapper() -> None:
            try:
                future.set_result(fn())
            except BaseException as exc:  # delivered to the caller
                future.set_exception(exc)

        self._calls.put(wrapper)
        return future.result(timeout)

    def _run_calls(self) -> None:
        while True:
            try:
                fn = self._calls.get_nowait()
            except queue.Empty:
                return
            fn()
