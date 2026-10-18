# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.opcua.test_opcua_sim
#  Author:      Thorsten Brach
#  Date:        2026-10-18
#
#  Description:
#    OPC UA robot controller simulator; SrciClient over OPC UA against the SDK simulator.
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

"""OPC UA robot controller simulator; SrciClient over OPC UA against the SDK simulator."""

from __future__ import annotations

import time

import pytest

pytest.importorskip("asyncua")

from srci.sim.opcua import OpcUaRcSimulator
from srci.transport import OpcUaTransport

pytestmark = pytest.mark.opcua

SIZE = 64


def echo(request: bytes) -> bytes:
    """Answer: the inverted request."""
    return bytes(b ^ 0xFF for b in request)


@pytest.mark.parametrize("encoding", ["ByteString", "Byte", "Double"])
def test_simulator_answers_in_its_own_cycle(encoding: str) -> None:
    """The simulator answers every cycle; the client sees the answer to its request a few cycles later."""
    with OpcUaRcSimulator(echo, SIZE, SIZE, cycle=0.005, encoding=encoding) as sim:
        with OpcUaTransport(sim.endpoint, sim.out_node, sim.in_node, SIZE, SIZE) as t:
            for n in range(1, 4):
                request = bytes([n]) * SIZE
                deadline = time.monotonic() + 2.0
                while t.exchange(request) != echo(request):
                    assert time.monotonic() < deadline, "no answer to the request"
                    time.sleep(0.005)
        assert sim.cycles > 0
        assert not sim.errors


@pytest.mark.sdk
def test_srci_client_over_opcua_against_sdk() -> None:
    """SDK in the loop over OPC UA: the RobotTask initializes and reads the robot data."""
    sdk = pytest.importorskip("srci_sdk_sim.sdk")
    from srci.api import SrciClient

    try:
        sim = sdk.SdkSimulator()
    except sdk.SdkNotAvailableError as exc:  # pragma: no cover - depends on the machine
        pytest.skip(f"SRCI SDK simulator not available: {exc}")
    size = 256
    try:
        with OpcUaRcSimulator(lambda telegram: sim.exchange(telegram, size), size, size) as rc:
            transport = OpcUaTransport(rc.endpoint, rc.out_node, rc.in_node, size, size)
            with SrciClient(transport) as client:
                client.program.ParCfg.Com.LifeSignTimeOut = 500
                client.wait_initialized(timeout=15.0)
                data = client.program.axes_group.State.RobotData
                assert data.RCManufacturer != ""  # robot data read over OPC UA
                assert transport.statistics.exchanges > 10
            assert not rc.errors
    finally:
        sim.close()
