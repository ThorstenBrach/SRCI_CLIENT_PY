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
it reads the PLC->RC telegram, computes the answer with ``handler`` (e.g. a simulated robot controller) and
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
from srci.transport.opcua_config import OpcUaConfig, OpcUaDirection, expand_nodes

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
        per_byte: bool = False,
    ) -> None:
        """
        Args:
            handler: computes the RC->PLC telegram from the PLC->RC telegram (once per cycle).
            request_size: bytes of the PLC->RC telegram.
            response_size: bytes of the RC->PLC telegram.
            port: TCP port, 0 = a free port.
            cycle: cycle time of the simulated robot controller in seconds.
            encoding: data type of the nodes, ``"ByteString"`` or an array type (``"Byte"``,
                ``"Double"`` ...); with ``per_byte`` the scalar type of each node (``"Byte"``
                if ``"ByteString"`` is given).
            per_byte: one node per byte like a robot controller that maps its PROFINET I/O to
                OPC UA: ``SRCI.PlcToRob.%IB<8*n>`` (written) and ``SRCI.RobToPlc.%QB<8*n>``
                (read); see :meth:`config` and :attr:`out_nodes`.
        """
        self.per_byte = per_byte
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
        self._out_bytes: list[Any] = []
        self._in_bytes: list[Any] = []
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

    @property
    def out_template(self) -> str:
        """``per_byte``: template of the PLC->RC nodes (``{bit}`` = 8 * byte number)."""
        return f"ns={self.namespace_index};s={OUT_NAME}.%IB{{bit}}"

    @property
    def in_template(self) -> str:
        """``per_byte``: template of the RC->PLC nodes."""
        return f"ns={self.namespace_index};s={IN_NAME}.%QB{{bit}}"

    @property
    def out_nodes(self) -> str | list[str]:
        """What :class:`OpcUaTransport` takes as ``out_node``: one NodeId or one per byte."""
        if not self.per_byte:
            return self.out_node
        return expand_nodes(self.out_template, self.request_size)

    @property
    def in_nodes(self) -> str | list[str]:
        if not self.per_byte:
            return self.in_node
        return expand_nodes(self.in_template, self.response_size)

    def config(self) -> OpcUaConfig:
        """Configuration of a client for this server (as a configuration file would give it)."""
        out_nodes, in_nodes = self.out_nodes, self.in_nodes
        return OpcUaConfig(
            endpoint=self.endpoint,
            plc_to_rc=OpcUaDirection(
                out_nodes if isinstance(out_nodes, str) else tuple(out_nodes), self.request_size
            ),
            rc_to_plc=OpcUaDirection(
                in_nodes if isinstance(in_nodes, str) else tuple(in_nodes), self.response_size
            ),
            name="SRCI RC simulator",
        )

    def start(self) -> Self:
        ua = self._asyncua.ua
        server = self._asyncua.sync.Server()
        server.set_endpoint(f"{self.endpoint}/")
        server.set_server_name("SRCI RC simulator")
        server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        self.namespace_index = server.register_namespace(NAMESPACE)
        folder = server.nodes.objects.add_folder(self.namespace_index, "SRCI")
        if self.per_byte:
            self._add_byte_nodes(folder)
        else:
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

    def _scalar_type(self) -> Any:
        ua = self._asyncua.ua
        return (
            ua.VariantType.Byte if self.encoding == "ByteString" else getattr(ua.VariantType, self.encoding)
        )

    def _scalar(self, value: int) -> Any:
        vtype = self._scalar_type()
        return self._asyncua.ua.Variant(float(value) if vtype.name in ("Float", "Double") else value, vtype)

    def _add_byte_nodes(self, folder: Any) -> None:
        idx = self.namespace_index
        plc_to_rob = folder.add_folder(idx, OUT_NAME)
        rob_to_plc = folder.add_folder(idx, IN_NAME)
        self._out_bytes = []
        for node_id in expand_nodes(self.out_template, self.request_size):
            node = plc_to_rob.add_variable(node_id, node_id.split(".")[-1], self._scalar(0))
            node.set_writable()
            self._out_bytes.append(node)
        self._in_bytes = [
            rob_to_plc.add_variable(node_id, node_id.split(".")[-1], self._scalar(0))
            for node_id in expand_nodes(self.in_template, self.response_size)
        ]

    def _read_request(self) -> bytes:
        if self.per_byte:
            # straight from the address space: hundreds of nodes per cycle
            server = self._server.aio_obj
            return bytes(
                int(server.read_attribute_value(node.nodeid).Value.Value) & 0xFF for node in self._out_bytes
            )
        value = self._out.read_value()
        return bytes(value) if isinstance(value, bytes) else bytes(int(v) & 0xFF for v in value)

    def _write_answer(self, answer: bytes) -> None:
        ua = self._asyncua.ua
        if self.per_byte:
            server = self._server.aio_obj
            values = [
                (node.nodeid, ua.DataValue(self._scalar(byte)))
                for node, byte in zip(self._in_bytes, answer, strict=True)
            ]

            async def write_all() -> None:  # one task on the server loop for all bytes
                for nodeid, data_value in values:
                    await server.write_attribute_value(nodeid, data_value)

            self._server.tloop.post(write_all())
        else:
            self._in.write_value(ua.DataValue(self._variant(answer)))

    def _run(self) -> None:
        next_cycle = time.monotonic()
        while not self._stop.is_set():
            try:
                request = self._read_request()
                if len(request) == self.request_size:
                    answer = bytes(self.handler(request))
                    if len(answer) == self.response_size:
                        self._write_answer(answer)
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
