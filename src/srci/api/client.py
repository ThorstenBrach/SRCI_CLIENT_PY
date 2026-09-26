# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.api.client
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    ``SrciClient``: run a :class:`RobotProgram` from a sequential Python script
#    (cycle in a background thread).
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

"""``SrciClient``: run a :class:`RobotProgram` from a sequential Python script.

On a PLC the program is called in a fixed cycle, and a sequence only sets inputs and looks at
outputs. :class:`SrciClient` does the same for a Python script: the program runs cyclically
in a background thread (:class:`srci.runtime.Runner`, thread ``srci-runner``), the script
writes "enable, move, wait until done"::

    with SrciClient(TcpTransport("192.168.0.10", 5000, 256, 256)) as client:
        client.wait_initialized()
        client.execute(MC_GroupResetFB())
        enable = client.enable(MC_EnableRobotFB())
        move = MC_MoveAxesAbsoluteFB()
        move.ParCmd.JointPosition.J1 = 45.0
        client.execute(move)
        time.sleep(2.0)  # the cycle (and the RobotTask LifeSign) keeps running

All function blocks and their inputs/outputs are the ones of the PLC library (``Execute``,
``Enable``, ``ParCmd``, ``OutCmd``, ``Done``, ``Error``, ``ErrorID`` ...).

* The cycle thread starts with the first helper call (after the configuration of the program)
  and stops with :meth:`close`.
* The helpers change the inputs in the cycle thread (between two cycles, never in the middle of
  one) and wait until the cycle thread reports the result, so every result belongs to one cycle.
* :meth:`execute` / :meth:`wait_done` / :meth:`disable` remove the finished block from the
  program; :meth:`add`, :meth:`enable` and :meth:`start` add it.
* Outputs can be read at any time; single inputs of an active block (e.g. a jog key) may be
  set directly, several related inputs are set consistently with :meth:`set`.

``background=False`` (default with ``realtime=False`` or an own ``clock``, e.g. ``FakeClock``)
runs the cycles in the calling thread only while the script waits in one of the helpers -
deterministic for tests and simulations; there nothing runs between two calls, so pauses must
use :meth:`idle` (the RobotTask LifeSign needs a cycle at least every ``LifeSignTimeOut`` ms).
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from concurrent.futures import Future
from concurrent.futures import TimeoutError as FutureTimeout
from types import TracebackType
from typing import Any, Self, TypeVar

from srci.api.program import RobotProgram
from srci.errors import SrciError
from srci.iec.clock import Clock
from srci.runtime.runner import CycleContext, Runner
from srci.transport.base import Transport

__all__ = ["CommandError", "SrciClient", "WaitTimeoutError"]

FB = TypeVar("FB")
T = TypeVar("T")

_POLL = 0.1  # s: the waiting script checks this often whether the cycle thread still runs


class CommandError(SrciError):
    """A function block ended with ``Error`` (or was aborted)."""

    def __init__(self, block: Any, text: str, error_id: int | None = None) -> None:
        self.block = block
        self.error_id = int(getattr(block, "ErrorID", 0)) if error_id is None else error_id
        super().__init__(f"{type(block).__name__}: {text} (ErrorID 16#{self.error_id:04X})")


class WaitTimeoutError(SrciError, TimeoutError):
    """A condition was not reached within the timeout."""


class _Waiter:
    """A condition that the cycle thread checks after every cycle."""

    def __init__(self, check: Callable[[], Any], cycles: int) -> None:
        self.check = check
        self.cycles = cycles  # cycles evaluated so far
        self.future: Future[Any] = Future()


def _finished(b: Any) -> bool:
    return bool(b.Done or b.Error or getattr(b, "CommandAborted", False))


def _result(b: Any) -> tuple[bool, bool, bool, int]:
    """Done, Error, CommandAborted, ErrorID of one cycle (reset together with Execute)."""
    return bool(b.Done), bool(b.Error), bool(getattr(b, "CommandAborted", False)), int(b.ErrorID)


class SrciClient:
    """Driver of a :class:`RobotProgram` for sequential scripts (cycle in a background thread)."""

    def __init__(
        self,
        transport: Transport,
        program: RobotProgram | None = None,
        *,
        cycle_time: float = 0.01,
        clock: Clock | None = None,
        realtime: bool = True,
        background: bool | None = None,
    ) -> None:
        self.transport = transport
        self.program = program or RobotProgram(transport.send_size, transport.recv_size)
        self.runner = Runner(transport, self._cycle, cycle_time, clock=clock)
        self.realtime = realtime
        self.background = (realtime and clock is None) if background is None else background
        self._waiters: list[_Waiter] = []
        self._lock = threading.Lock()
        self._closed = False
        self._started = False  # the cycle thread starts with the first wait (after the configuration)

    # ------------------------------------------------------------------ cycle thread

    def _cycle(self, ctx: CycleContext) -> None:
        self.program.cycle(ctx)
        with self._lock:
            waiters = list(self._waiters)
        for w in waiters:
            w.cycles += 1
            try:
                value = w.check()
            except Exception as exc:  # delivered to the waiting script
                self._drop(w)
                w.future.set_exception(exc)
                continue
            if value is not None:
                self._drop(w)
                w.future.set_result(value)

    def _drop(self, w: _Waiter) -> None:
        with self._lock:
            if w in self._waiters:
                self._waiters.remove(w)

    def _do(self, fn: Callable[[], T]) -> T:
        """Execute ``fn`` between two cycles (in the cycle thread in background mode)."""
        if not self.background:
            return fn()
        self._check_running()
        future: Future[T] = Future()

        def call() -> None:
            try:
                future.set_result(fn())
            except BaseException as exc:  # delivered to the script
                future.set_exception(exc)

        self.runner.call_soon(call)
        while True:
            try:
                return future.result(_POLL)
            except FutureTimeout:
                self._check_running()

    def _until(self, check: Callable[[], T | None], timeout: float, what: str) -> tuple[T, int]:
        """Wait until ``check()`` (evaluated after every cycle) returns a value that is not None;
        returns it and the number of cycles."""
        if not self.background:
            limit = max(1, round(timeout / self.runner.cycle_time))
            for n in range(1, limit + 1):
                self._step()
                value = check()
                if value is not None:
                    return value, n
            raise WaitTimeoutError(f"timeout after {timeout} s waiting for {what}")
        self._check_running()
        w = _Waiter(check, 0)
        with self._lock:
            self._waiters.append(w)
        clock = self.runner.clock
        deadline = clock.monotonic() + timeout
        try:
            while True:
                try:
                    return w.future.result(max(0.0, min(_POLL, deadline - clock.monotonic()))), w.cycles
                except FutureTimeout:
                    self._check_running()
                    if clock.monotonic() >= deadline:
                        raise WaitTimeoutError(f"timeout after {timeout} s waiting for {what}") from None
        finally:
            self._drop(w)

    def _check_running(self) -> None:
        if self._closed:
            raise SrciError("client is closed")
        if not self._started:
            self._started = True
            self.runner.start()
        if not self.runner.running:
            self.runner.stop()  # re-raises the exception that stopped the cycle
            raise SrciError("cycle thread is not running")

    def _step(self) -> None:
        clock = self.runner.clock
        start = clock.monotonic()
        self.runner.step()
        if self.realtime:
            clock.sleep(max(0.0, self.runner.cycle_time - (clock.monotonic() - start)))

    # ------------------------------------------------------------------ cycles

    @property
    def cycle(self) -> int:
        return self.runner.cycle

    def run(self, cycles: int = 1) -> None:
        """Wait for ``cycles`` cycles (without ``background``: execute them)."""
        if not self.background:
            for _ in range(cycles):
                self._step()
            return
        count = 0

        def check() -> bool | None:
            nonlocal count
            count += 1
            return True if count >= cycles else None

        self._until(check, 10.0 + cycles * self.runner.cycle_time, f"{cycles} cycles")

    def idle(self, seconds: float) -> None:
        """Pause for ``seconds`` while the communication keeps running (in background mode the
        same as ``time.sleep``)."""
        if self.background:
            self._check_running()
            self.runner.clock.sleep(seconds)
        else:
            self.run(max(1, round(seconds / self.runner.cycle_time)))

    def run_until(self, condition: Callable[[], bool], timeout: float = 10.0, what: str = "") -> int:
        """Wait until ``condition()`` is true (checked after every cycle, in the cycle thread);
        returns the number of cycles."""
        return self._until(lambda: True if condition() else None, timeout, what or "condition")[1]

    # ------------------------------------------------------------------ RobotTask

    def wait_initialized(self, timeout: float = 10.0) -> None:
        """Wait until the RobotTask is initialized and commands are enabled."""
        rt = self.program.robot_task
        error = self._until(
            lambda: bool(rt.Error) if self.program.commands_enabled or rt.Error else None,
            timeout,
            "RobotTask initialization",
        )[0]
        if error:
            raise CommandError(rt, "initialization failed")

    # ------------------------------------------------------------------ function blocks

    def _add(self, block: Any, inputs: dict[str, Any]) -> None:
        if block not in self.program.blocks:
            self.program.add(block, **inputs)
        else:
            for name, value in inputs.items():
                setattr(block, name, value)

    def add(self, block: FB, **inputs: Any) -> FB:
        """Add a function block to the program (it is called in every cycle from now on) and
        set ``inputs``."""
        self._do(lambda: self._add(block, inputs))
        return block

    def set(self, block: FB, **inputs: Any) -> FB:
        """Set several inputs of a block together (between two cycles)."""

        def apply() -> None:
            for name, value in inputs.items():
                setattr(block, name, value)

        self._do(apply)
        return block

    def remove(self, block: Any) -> None:
        """Remove a block from the program (it is no longer called)."""
        self._do(lambda: self.program.remove(block))

    def _rising_edge(self, block: Any, inputs: dict[str, Any]) -> None:
        def prepare() -> bool:
            self._add(block, inputs)
            if block.Execute:  # a new rising edge needs one cycle with FALSE
                block.Execute = False
                return True
            block.Execute = True
            return False

        if self._do(prepare):
            if not self.background:
                self._step()
            self._do(lambda: setattr(block, "Execute", True))

    def _finish(self, block: FB, timeout: float, check: bool) -> FB:
        b: Any = block
        name = type(block).__name__
        try:
            done, error, aborted, error_id = self._until(lambda: _result(b) if _finished(b) else None,
                                                         timeout, f"{name} Done")[0]  # fmt: skip
        except WaitTimeoutError:
            self._release(block)
            raise WaitTimeoutError(
                f"{name} not done within {timeout} s - Execute reset, the command may still run on the RC"
            ) from None
        self._release(block)
        if check and not done:
            raise CommandError(block, "error" if error else "aborted" if aborted else "not done", error_id)
        return block

    def _release(self, block: Any) -> None:
        """Reset ``Execute`` (one cycle, so the block sees the falling edge) and remove the block."""
        self._do(lambda: setattr(block, "Execute", False))
        if not self.background:
            self._step()
        self.remove(block)

    def execute(self, block: FB, timeout: float = 30.0, *, check: bool = True, **inputs: Any) -> FB:
        """Execute-type block: rising edge on ``Execute``, wait for ``Done`` / ``Error`` /
        ``CommandAborted``, reset ``Execute`` and remove the block. Raises
        :class:`CommandError` if ``check`` and the block did not end with ``Done``,
        :class:`WaitTimeoutError` after ``timeout`` (``Execute`` is reset as well)."""
        self._rising_edge(block, inputs)
        return self._finish(block, timeout, check)

    def start(self, block: FB, **inputs: Any) -> FB:
        """Execute-type block: only the rising edge on ``Execute`` (e.g. a motion that runs while
        the script does something else); wait with :meth:`wait_done`."""
        self._rising_edge(block, inputs)
        return block

    def wait_done(self, block: FB, timeout: float = 30.0, *, check: bool = True) -> FB:
        """Wait for a block started with :meth:`start` like :meth:`execute`."""
        return self._finish(block, timeout, check)

    def enable(self, block: FB, timeout: float = 10.0, *, check: bool = True, **inputs: Any) -> FB:
        """Enable-type block: set ``Enable`` and wait until the block reports that it works
        (``Enabled``, ``Valid``, ``Active`` or ``Done``, whichever the block has) or ``Error``.
        The block stays in the program until :meth:`disable`."""
        b: Any = block
        flags = [n for n in ("Enabled", "Valid", "Active", "Done") if hasattr(b, n)]
        self._do(lambda: self._add(b, {**inputs, "Enable": True}))
        error, error_id = self._until(
            lambda: (bool(b.Error), int(b.ErrorID)) if b.Error or any(getattr(b, n) for n in flags) else None,
            timeout,
            f"{type(b).__name__} Enabled",
        )[0]
        if check and error:
            raise CommandError(b, "error", error_id)
        return block

    def disable(self, block: FB, timeout: float = 10.0) -> FB:
        """Enable-type block: reset ``Enable``, wait until it is no longer enabled/busy and
        remove the block."""
        b: Any = block
        self._do(lambda: setattr(b, "Enable", False))
        try:
            self._until(
                lambda: True if not getattr(b, "Enabled", False) and not getattr(b, "Busy", False) else None,
                timeout,
                f"{type(b).__name__} disabled",
            )
        finally:
            self.remove(b)
        return block

    # ------------------------------------------------------------------ lifecycle

    def close(self) -> None:
        """Stop the cycle thread and close the transport."""
        if self._closed:
            return
        self._closed = True
        try:
            if self._started:
                self.runner.stop()
        finally:
            self.transport.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()
