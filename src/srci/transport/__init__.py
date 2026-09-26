# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.transport
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Transports: exchange one telegram per cycle with the robot side.
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
