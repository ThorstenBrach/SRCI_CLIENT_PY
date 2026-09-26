# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.transport.base
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Transport interface: exchanges one telegram per cycle (lockstep).
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

"""Transport interface: exchanges one telegram per cycle (lockstep).

The library core only knows :class:`Transport`. A cycle is one call of
:meth:`Transport.exchange`: the PLC->RC telegram (``RobotOutData``) is sent and exactly
one RC->PLC telegram (``RobotInData``) is returned. Telegram lengths are fixed per
direction by configuration - there is no additional framing.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from types import TracebackType
from typing import Self

from srci.errors import SrciError

__all__ = [
    "Clock",
    "ReconnectPolicy",
    "Transport",
    "TransportClosedError",
    "TransportConnectError",
    "TransportError",
    "TransportProtocolError",
    "TransportState",
    "TransportStatistics",
    "TransportTimeoutError",
]

Clock = Callable[[], float]
"""Monotonic clock in seconds (injectable for tests)."""


class TransportError(SrciError):
    """Base class of transport errors. After an error the next ``exchange`` reconnects."""


class TransportConnectError(TransportError):
    """The connection could not be established (or reconnect is still delayed)."""


class TransportTimeoutError(TransportError):
    """No complete answer within the response timeout."""


class TransportClosedError(TransportError):
    """The peer closed the connection."""


class TransportProtocolError(TransportError):
    """The peer violated the lockstep protocol (e.g. sent more bytes than one telegram)."""


class TransportState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"
    ERROR = "error"
    CLOSED = "closed"


@dataclass
class TransportStatistics:
    exchanges: int = 0
    connects: int = 0
    timeouts: int = 0
    errors: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    last_rtt: float = 0.0
    max_rtt: float = 0.0
    last_error: str = ""

    def record_rtt(self, rtt: float) -> None:
        self.last_rtt = rtt
        self.max_rtt = max(self.max_rtt, rtt)


@dataclass
class ReconnectPolicy:
    """Exponential backoff between reconnect attempts."""

    enabled: bool = True
    initial_delay: float = 0.1
    max_delay: float = 2.0
    factor: float = 2.0
    _delay: float = field(default=0.0, init=False, repr=False)
    _next_attempt: float = field(default=0.0, init=False, repr=False)

    def allowed(self, now: float) -> bool:
        return now >= self._next_attempt

    def failed(self, now: float) -> None:
        self._delay = (
            self.initial_delay if self._delay == 0.0 else min(self._delay * self.factor, self.max_delay)
        )
        self._next_attempt = now + self._delay

    def succeeded(self) -> None:
        self._delay = 0.0
        self._next_attempt = 0.0

    @property
    def next_attempt(self) -> float:
        return self._next_attempt


class Transport(ABC):
    """Exchanges fixed length telegrams in lockstep."""

    def __init__(self, send_size: int, recv_size: int, clock: Clock = time.monotonic) -> None:
        if send_size < 1 or recv_size < 1:
            raise ValueError("telegram sizes must be >= 1")
        self.send_size = send_size
        self.recv_size = recv_size
        self.clock = clock
        self.statistics = TransportStatistics()
        self._state = TransportState.DISCONNECTED

    @property
    def state(self) -> TransportState:
        return self._state

    @property
    def connected(self) -> bool:
        return self._state is TransportState.CONNECTED

    @abstractmethod
    def connect(self) -> None:
        """Establish the connection (raises :class:`TransportConnectError`)."""

    @abstractmethod
    def close(self) -> None:
        """Close the connection. Idempotent."""

    @abstractmethod
    def _exchange(self, out: bytes) -> bytes:
        """Send ``out`` and return exactly ``recv_size`` bytes."""

    def exchange(self, out: bytes | bytearray) -> bytes:
        """One cycle: send the PLC->RC telegram, return the RC->PLC telegram."""
        if len(out) != self.send_size:
            raise ValueError(f"telegram has {len(out)} bytes, expected {self.send_size}")
        start = self.clock()
        try:
            data = self._exchange(bytes(out))
        except TransportError as exc:
            self.statistics.errors += 1
            self.statistics.last_error = f"{type(exc).__name__}: {exc}"
            if isinstance(exc, TransportTimeoutError):
                self.statistics.timeouts += 1
            raise
        if len(data) != self.recv_size:  # pragma: no cover - guarded by implementations
            raise TransportProtocolError(f"received {len(data)} bytes, expected {self.recv_size}")
        self.statistics.exchanges += 1
        self.statistics.bytes_sent += len(out)
        self.statistics.bytes_received += len(data)
        self.statistics.record_rtt(self.clock() - start)
        return data

    def __enter__(self) -> Self:
        self.connect()
        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.close()
