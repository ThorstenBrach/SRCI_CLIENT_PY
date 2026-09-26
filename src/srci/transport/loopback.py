"""In-process transport: calls a handler instead of a network peer (tests, simulators)."""

from __future__ import annotations

import time
from collections.abc import Callable

from srci.transport.base import (
    Clock,
    Transport,
    TransportClosedError,
    TransportProtocolError,
    TransportState,
)

__all__ = ["LoopbackTransport"]

Handler = Callable[[bytes], bytes | bytearray]


class LoopbackTransport(Transport):
    """``exchange(out)`` returns ``handler(out)`` - e.g. the SDK server function."""

    def __init__(
        self, handler: Handler, send_size: int, recv_size: int, clock: Clock = time.monotonic
    ) -> None:
        super().__init__(send_size, recv_size, clock)
        self.handler = handler

    def connect(self) -> None:
        self._state = TransportState.CONNECTED
        self.statistics.connects += 1

    def close(self) -> None:
        self._state = TransportState.CLOSED

    def _exchange(self, out: bytes) -> bytes:
        if self._state is TransportState.CLOSED:
            raise TransportClosedError("transport was closed")
        if self._state is not TransportState.CONNECTED:
            self.connect()
        answer = bytes(self.handler(out))
        if len(answer) != self.recv_size:
            raise TransportProtocolError(f"handler returned {len(answer)} bytes, expected {self.recv_size}")
        return answer
