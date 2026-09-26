"""Transports: exchange one telegram per cycle with the robot side.

* :class:`TcpTransport` - PLC gateway via TCP (raw telegrams, lockstep)
* :class:`LoopbackTransport` - in-process handler (tests, SDK simulator)
* :class:`FaultInjectingTransport` - deterministic fault injection for tests
"""

from srci.transport.base import (
    ReconnectPolicy,
    Transport,
    TransportClosedError,
    TransportConnectError,
    TransportError,
    TransportProtocolError,
    TransportState,
    TransportStatistics,
    TransportTimeoutError,
)
from srci.transport.fault import Fault, FaultInjectingTransport, FaultPlan
from srci.transport.loopback import LoopbackTransport
from srci.transport.tcp import TcpTransport

__all__ = [
    "Fault",
    "FaultInjectingTransport",
    "FaultPlan",
    "LoopbackTransport",
    "ReconnectPolicy",
    "TcpTransport",
    "Transport",
    "TransportClosedError",
    "TransportConnectError",
    "TransportError",
    "TransportProtocolError",
    "TransportState",
    "TransportStatistics",
    "TransportTimeoutError",
]
