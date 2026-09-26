# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.api.client
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    ``SrciClient``: run a :class:`RobotProgram` step by step from a sequential Python
#    script.
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

"""``SrciClient``: run a :class:`RobotProgram` step by step from a sequential Python script.

A PLC calls its program in a fixed cycle; a Python script wants to write "enable, move,
wait until done". :class:`SrciClient` combines both: it owns the :class:`Runner` and executes
cycles (with the cycle time) whenever the script waits::

    with SrciClient(TcpTransport("192.168.0.10", 5000, 256, 256)) as client:
        client.wait_initialized()
        client.execute(MC_GroupResetFB())
        enable = client.enable(MC_EnableRobotFB())
        move = MC_MoveAxesAbsoluteFB()
        move.ParCmd.JointPosition.J1 = 45.0
        client.execute(move)

All function blocks and their inputs/outputs are the ones of the PLC library (``Execute``,
``Enable``, ``ParCmd``, ``OutCmd``, ``Done``, ``Error``, ``ErrorID`` ...). The helpers only
drive the cycles; nothing runs between two calls of the script (the RobotTask LifeSign
needs a cycle at least every ``LifeSignTimeOut`` ms, default 50 ms) - use :meth:`idle` for
pauses, or :class:`srci.runtime.Runner` in a background thread for long running programs.
"""

from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any, Self, TypeVar

from srci.api.program import RobotProgram
from srci.errors import SrciError
from srci.iec.clock import Clock
from srci.runtime.runner import Runner
from srci.transport.base import Transport

__all__ = ["CommandError", "SrciClient", "WaitTimeoutError"]

FB = TypeVar("FB")


class CommandError(SrciError):
    """A function block ended with ``Error`` (or was aborted)."""

    def __init__(self, block: Any, text: str, error_id: int | None = None) -> None:
        self.block = block
        self.error_id = int(getattr(block, "ErrorID", 0)) if error_id is None else error_id
        super().__init__(f"{type(block).__name__}: {text} (ErrorID 16#{self.error_id:04X})")


class WaitTimeoutError(SrciError, TimeoutError):
    """A condition was not reached within the timeout."""


class SrciClient:
    """Synchronous driver of a :class:`RobotProgram` for sequential scripts."""

    def __init__(
        self,
        transport: Transport,
        program: RobotProgram | None = None,
        *,
        cycle_time: float = 0.01,
        clock: Clock | None = None,
        realtime: bool = True,
    ) -> None:
        self.transport = transport
        self.program = program or RobotProgram(transport.send_size, transport.recv_size)
        self.runner = Runner(transport, self.program, cycle_time, clock=clock)
        self.realtime = realtime

    # ------------------------------------------------------------------ cycles

    @property
    def cycle(self) -> int:
        return self.runner.cycle

    def run(self, cycles: int = 1) -> None:
        """Execute ``cycles`` cycles (with the cycle time if ``realtime``)."""
        clock = self.runner.clock
        for _ in range(cycles):
            start = clock.monotonic()
            self.runner.step()
            if self.realtime:
                clock.sleep(max(0.0, self.runner.cycle_time - (clock.monotonic() - start)))

    def idle(self, seconds: float) -> None:
        """Keep the communication running for ``seconds`` (instead of ``time.sleep``)."""
        self.run(max(1, round(seconds / self.runner.cycle_time)))

    def run_until(self, condition: Callable[[], bool], timeout: float = 10.0, what: str = "") -> int:
        """Execute cycles until ``condition()`` is true; returns the number of cycles."""
        limit = max(1, round(timeout / self.runner.cycle_time))
        for n in range(1, limit + 1):
            self.run()
            if condition():
                return n
        raise WaitTimeoutError(f"timeout after {timeout} s waiting for {what or 'condition'}")

    # ------------------------------------------------------------------ RobotTask

    def wait_initialized(self, timeout: float = 10.0) -> None:
        """Run until the RobotTask is initialized and commands are enabled."""
        rt = self.program.robot_task
        self.run_until(
            lambda: self.program.commands_enabled or bool(rt.Error), timeout, "RobotTask initialization"
        )
        if rt.Error:
            raise CommandError(rt, "initialization failed")

    # ------------------------------------------------------------------ function blocks

    def add(self, block: FB, **inputs: Any) -> FB:
        """Add a function block to the program (it is called in every cycle from now on)."""
        if block not in self.program.blocks:
            self.program.add(block, **inputs)
        else:
            for name, value in inputs.items():
                setattr(block, name, value)
        return block

    def execute(self, block: FB, timeout: float = 30.0, *, check: bool = True, **inputs: Any) -> FB:
        """Execute-type block: rising edge on ``Execute``, run until ``Done`` / ``Error`` /
        ``CommandAborted``, then reset ``Execute``. Raises :class:`CommandError` if ``check``
        and the block did not end with ``Done``."""
        b: Any = self.add(block, **inputs)
        if b.Execute:  # a new rising edge needs one cycle with FALSE
            b.Execute = False
            self.run()
        b.Execute = True
        self.run_until(
            lambda: bool(b.Done or b.Error or getattr(b, "CommandAborted", False)),
            timeout,
            f"{type(b).__name__} Done",
        )
        done, error, aborted = bool(b.Done), bool(b.Error), bool(getattr(b, "CommandAborted", False))
        error_id = int(b.ErrorID)  # the outputs are reset with Execute
        b.Execute = False
        self.run()
        if check and not done:
            raise CommandError(b, "error" if error else "aborted" if aborted else "not done", error_id)
        return block

    def start(self, block: FB, **inputs: Any) -> FB:
        """Execute-type block: only set ``Execute`` (e.g. a motion that runs while the script
        does something else); wait with :meth:`run_until` / :meth:`wait_done`."""
        b: Any = self.add(block, **inputs)
        b.Execute = True
        return block

    def wait_done(self, block: FB, timeout: float = 30.0, *, check: bool = True) -> FB:
        """Wait for a block started with :meth:`start`; resets ``Execute`` afterwards."""
        b: Any = block
        self.run_until(
            lambda: bool(b.Done or b.Error or getattr(b, "CommandAborted", False)),
            timeout,
            f"{type(b).__name__} Done",
        )
        done, error, error_id = bool(b.Done), bool(b.Error), int(b.ErrorID)
        b.Execute = False
        self.run()
        if check and not done:
            raise CommandError(b, "error" if error else "aborted", error_id)
        return block

    def enable(self, block: FB, timeout: float = 10.0, *, check: bool = True, **inputs: Any) -> FB:
        """Enable-type block: set ``Enable`` and run until the block reports that it works
        (``Enabled``, ``Valid``, ``Active`` or ``Done``, whichever the block has) or ``Error``."""
        b: Any = self.add(block, **inputs)
        b.Enable = True
        flags = [n for n in ("Enabled", "Valid", "Active", "Done") if hasattr(b, n)]
        self.run_until(
            lambda: bool(b.Error or any(getattr(b, n) for n in flags)),
            timeout,
            f"{type(b).__name__} Enabled",
        )
        if check and b.Error:
            raise CommandError(b, "error")
        return block

    def disable(self, block: FB, timeout: float = 10.0) -> FB:
        """Enable-type block: reset ``Enable`` and run until it is no longer enabled/busy."""
        b: Any = block
        b.Enable = False
        self.run_until(
            lambda: not getattr(b, "Enabled", False) and not getattr(b, "Busy", False),
            timeout,
            f"{type(b).__name__} disabled",
        )
        return block

    def remove(self, block: Any) -> None:
        self.program.remove(block)

    # ------------------------------------------------------------------ lifecycle

    def close(self) -> None:
        self.transport.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()
