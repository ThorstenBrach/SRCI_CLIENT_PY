# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.sim.opcua
#  Author:      Thorsten Brach
#  Date:        2026-10-18
#
#  Description:
#    OPC UA server that behaves like a robot controller with SRCI telegram nodes.
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

"""OPC UA server that behaves like a robot controller with SRCI telegram nodes.

Counterpart of :class:`srci.transport.OpcUaTransport` for tests, demos and the HMI: the server
has two variables, ``ns=<i>;s=SRCI.PlcToRob`` (written by the client) and ``ns=<i>;s=SRCI.RobToPlc``
(read by the client). Like a robot controller it runs its own cycle (default 10 ms): every cycle
it reads the PLC->RC telegram, computes the answer with ``handler`` (e.g. the SDK simulator) and
writes it to the RC->PLC node. There is no lockstep with the client.

Needs ``asyncua`` (``pip install srci-client[opcua]``).
"""

from __future__ import annotations

import contextlib
import socket
import threading
import time
from collections.abc import Callable
from types import TracebackType
from typing import Any, Self

from srci.transport.opcua import load_asyncua

__all__ = ["OpcUaRcSimulator"]

Handler = Callable[[bytes], bytes | bytearray]

NAMESPACE = "urn:srci:rc-simulator"
OUT_NAME = "SRCI.PlcToRob"
IN_NAME = "SRCI.RobToPlc"


class OpcUaRcSimulator:
    """asyncua server with the telegram nodes; ``handler`` answers every cycle."""

    def __init__(
        self,
        handler: Handler,
        request_size: int,
        response_size: int,
        *,
        host: str = "127.0.0.1",
        port: int = 0,
        cycle: float = 0.01,
        encoding: str = "ByteString",
    ) -> None:
        """
        Args:
            handler: computes the RC->PLC telegram from the PLC->RC telegram (once per cycle).
            request_size: bytes of the PLC->RC telegram.
            response_size: bytes of the RC->PLC telegram.
            port: TCP port, 0 = a free port.
            cycle: cycle time of the simulated robot controller in seconds.
            encoding: data type of the nodes, ``"ByteString"`` or an array type (``"Byte"``,
                ``"Double"`` ...).
        """
        self.handler = handler
        self.request_size = request_size
        self.response_size = response_size
        self.host = host
        self.port = port or _free_port(host)
        self.cycle = cycle
        self.encoding = encoding
        self.cycles = 0
        self.errors: list[str] = []
        self._asyncua: Any = load_asyncua()
        self._server: Any = None
        self._out: Any = None
        self._in: Any = None
        self.namespace_index = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="OpcUaRcSimulator", daemon=True)

    # ------------------------------------------------------------------ lifecycle

    @property
    def endpoint(self) -> str:
        return f"opc.tcp://{self.host}:{self.port}"

    @property
    def out_node(self) -> str:
        """NodeId of the PLC->RC telegram (the client writes it)."""
        return f"ns={self.namespace_index};s={OUT_NAME}"

    @property
    def in_node(self) -> str:
        """NodeId of the RC->PLC telegram (the client reads it)."""
        return f"ns={self.namespace_index};s={IN_NAME}"

    def start(self) -> Self:
        ua = self._asyncua.ua
        server = self._asyncua.sync.Server()
        server.set_endpoint(f"{self.endpoint}/")
        server.set_server_name("SRCI RC simulator")
        server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        self.namespace_index = server.register_namespace(NAMESPACE)
        folder = server.nodes.objects.add_folder(self.namespace_index, "SRCI")
        self._out = folder.add_variable(self.out_node, OUT_NAME, self._variant(bytes(self.request_size)))
        self._out.set_writable()
        self._in = folder.add_variable(self.in_node, IN_NAME, self._variant(bytes(self.response_size)))
        server.start()
        self._server = server
        self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout=2.0)
        server, self._server = self._server, None
        if server is not None:
            with contextlib.suppress(Exception):
                server.stop()

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None:
        self.stop()

    # ------------------------------------------------------------------ cycle

    def _variant(self, data: bytes) -> Any:
        ua = self._asyncua.ua
        if self.encoding == "ByteString":
            return ua.Variant(data, ua.VariantType.ByteString)
        vtype = getattr(ua.VariantType, self.encoding)
        values: list[Any] = [float(b) for b in data] if self.encoding in ("Float", "Double") else list(data)
        return ua.Variant(values, vtype, is_array=True)

    def _run(self) -> None:
        ua = self._asyncua.ua
        next_cycle = time.monotonic()
        while not self._stop.is_set():
            try:
                value = self._out.read_value()
                request = bytes(value) if isinstance(value, bytes) else bytes(int(v) & 0xFF for v in value)
                if len(request) == self.request_size:
                    answer = bytes(self.handler(request))
                    if len(answer) == self.response_size:
                        self._in.write_value(ua.DataValue(self._variant(answer)))
                    else:
                        self.errors.append(f"handler returned {len(answer)} bytes")
                else:
                    self.errors.append(f"PlcToRob has {len(request)} bytes")
                self.cycles += 1
            except Exception as exc:  # server stopped, handler error
                if self._stop.is_set():
                    break
                self.errors.append(f"{type(exc).__name__}: {exc}")
            next_cycle += self.cycle
            delay = next_cycle - time.monotonic()
            if delay > 0:
                self._stop.wait(delay)
            else:
                next_cycle = time.monotonic()


def _free_port(host: str) -> int:
    with socket.socket() as s:
        s.bind((host, 0))
        port: int = s.getsockname()[1]
        return port
