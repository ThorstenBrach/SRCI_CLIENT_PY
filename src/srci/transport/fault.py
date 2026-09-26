"""Fault injection around any transport - deterministic, for tests."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

from srci.transport.base import (
    Transport,
    TransportClosedError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)

__all__ = ["Fault", "FaultInjectingTransport", "FaultPlan"]


class Fault(Enum):
    """What happens in a cycle."""

    TIMEOUT = "timeout"  # the answer is lost (request was delivered)
    DROP_REQUEST = "drop_request"  # the request is lost, no answer
    DISCONNECT = "disconnect"  # connection breaks
    CORRUPT = "corrupt"  # one bit of the answer flipped
    STALE = "stale"  # the previous answer is delivered again
    PROTOCOL = "protocol"  # lockstep violated


@dataclass
class FaultPlan:
    """Faults per cycle number (0 based) and/or random faults with a fixed seed."""

    at: dict[int, Fault] = field(default_factory=dict)
    probability: float = 0.0
    kinds: tuple[Fault, ...] = tuple(Fault)
    seed: int = 0

    def __post_init__(self) -> None:
        self._rnd = random.Random(self.seed)

    def fault_for(self, cycle: int) -> Fault | None:
        if cycle in self.at:
            return self.at[cycle]
        if self.probability and self._rnd.random() < self.probability:
            return self._rnd.choice(self.kinds)
        return None


class FaultInjectingTransport(Transport):
    """Wraps another transport and injects faults according to a :class:`FaultPlan`."""

    def __init__(self, inner: Transport, plan: FaultPlan) -> None:
        super().__init__(inner.send_size, inner.recv_size, inner.clock)
        self.inner = inner
        self.plan = plan
        self.cycle = 0
        self.injected: list[tuple[int, Fault]] = []
        self._last_answer: bytes | None = None
        self._rnd = random.Random(plan.seed + 1)

    @property
    def state(self) -> TransportState:
        return self.inner.state

    def connect(self) -> None:
        self.inner.connect()

    def close(self) -> None:
        self.inner.close()

    def _exchange(self, out: bytes) -> bytes:
        cycle, self.cycle = self.cycle, self.cycle + 1
        fault = self.plan.fault_for(cycle)
        if fault is not None:
            self.injected.append((cycle, fault))
        if fault is Fault.DROP_REQUEST:
            raise TransportTimeoutError(f"[injected] request of cycle {cycle} lost")
        if fault is Fault.DISCONNECT:
            self.inner.close()
            self.inner.connect()  # a real transport reconnects on the next exchange
            raise TransportClosedError(f"[injected] connection lost in cycle {cycle}")
        answer = self.inner.exchange(out)
        if fault is Fault.TIMEOUT:
            raise TransportTimeoutError(f"[injected] answer of cycle {cycle} lost")
        if fault is Fault.PROTOCOL:
            raise TransportProtocolError(f"[injected] lockstep violated in cycle {cycle}")
        if fault is Fault.STALE and self._last_answer is not None:
            answer = self._last_answer
        elif fault is Fault.CORRUPT:
            data = bytearray(answer)
            pos = self._rnd.randrange(len(data))
            data[pos] ^= 1 << self._rnd.randrange(8)
            answer = bytes(data)
        self._last_answer = answer
        return answer
