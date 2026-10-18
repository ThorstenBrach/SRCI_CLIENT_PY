# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.transport.opcua
#  Author:      Thorsten Brach
#  Date:        2026-10-18
#
#  Description:
#    OPC UA transport: the telegrams as byte arrays on two nodes of an OPC UA server.
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

"""OPC UA transport: the telegrams as byte arrays on two nodes of an OPC UA server.

For a PLC bridge or a robot controller that offers the SRCI telegrams on an OPC UA server.
Only the medium changes; the SRCI telegrams are the same as over TCP:

* every cycle the PLC->RC telegram (``send_size`` bytes) is **written** to ``out_node`` and the
  RC->PLC telegram (``recv_size`` bytes) is **read** from ``in_node``;
* there is no handshake on the OPC UA level: request and answer are matched by the SRCI
  protocol itself (``SEQ_ACK`` of the sequence header, LifeSign) - like on a PROFINET line,
  where the client and the RC do not run in lockstep either;
* the data type of the nodes is detected on connect: ``ByteString`` or a one dimensional
  array of ``Byte``/``SByte``/``UInt16`` ... or ``Float``/``Double`` (one telegram byte per element,
  value 0 ... 255; robot controllers that publish only number arrays, e.g. a VAL 3 ``num`` array).

Needs the optional dependency ``asyncua`` (``pip install srci-client[opcua]``); it is imported
only when a connection is opened, so ``import srci.transport`` works without it.

:func:`browse` lists the variables of a server (for configuration tools, e.g. the HMI).
"""

from __future__ import annotations

import contextlib
import logging
import time
from dataclasses import dataclass
from typing import Any

from srci.transport.base import (
    Clock,
    ReconnectPolicy,
    Transport,
    TransportClosedError,
    TransportConnectError,
    TransportError,
    TransportProtocolError,
    TransportState,
    TransportTimeoutError,
)

__all__ = ["OpcUaNodeInfo", "OpcUaTransport", "browse", "load_asyncua"]

log = logging.getLogger("srci.transport")

INSTALL_HINT = "OPC UA needs the package asyncua: pip install srci-client[opcua]"

# encodings of a telegram on a node
_BYTESTRING = "ByteString"
_ARRAY = "Array"


def load_asyncua() -> Any:
    """Import ``asyncua`` (``asyncua.sync`` and ``asyncua.ua``) or raise :class:`TransportConnectError`."""
    try:
        import asyncua  # noqa: F401
        from asyncua import sync, ua  # noqa: F401
    except ImportError as exc:  # pragma: no cover - depends on the installation
        raise TransportConnectError(INSTALL_HINT) from exc
    import asyncua as module

    return module


@dataclass(frozen=True)
class OpcUaNodeInfo:
    """A variable of an OPC UA server (result of :func:`browse`)."""

    node_id: str
    """NodeId string, e.g. ``ns=2;s=SRCI.PlcToRob``."""
    path: str
    """Browse path from the start node, e.g. ``Objects/SRCI/PlcToRob``."""
    data_type: str
    """Variant type of the value, e.g. ``ByteString`` or ``Byte``."""
    is_array: bool
    length: int
    """Number of bytes (``ByteString``) or elements (array) of the current value, -1 if unknown."""
    writable: bool

    @property
    def telegram_candidate(self) -> bool:
        """``ByteString`` or an array of a number type: can carry a telegram."""
        return self.data_type == _BYTESTRING or (self.is_array and self.data_type in _ARRAY_TYPES)


_ARRAY_TYPES = {"Byte", "SByte", "UInt16", "Int16", "UInt32", "Int32", "UInt64", "Int64", "Float", "Double"}
_FLOAT_TYPES = {"Float", "Double"}


class OpcUaTransport(Transport):
    """Write the PLC->RC telegram to one node, read the RC->PLC telegram from another."""

    def __init__(
        self,
        endpoint: str,
        out_node: str,
        in_node: str,
        send_size: int,
        recv_size: int,
        *,
        timeout: float = 1.0,
        username: str | None = None,
        password: str | None = None,
        security: str | None = None,
        reconnect: ReconnectPolicy | None = None,
        check_lengths: bool = True,
        clock: Clock = time.monotonic,
    ) -> None:
        """
        Args:
            endpoint: server URL, e.g. ``opc.tcp://192.168.0.254:4840``.
            out_node: NodeId of the PLC->RC telegram (written), e.g. ``ns=2;s=SRCI.PlcToRob``.
            in_node: NodeId of the RC->PLC telegram (read).
            send_size: bytes of the PLC->RC telegram.
            recv_size: bytes of the RC->PLC telegram.
            timeout: timeout of one request (connect, read, write) in seconds.
            username: optional user (anonymous without).
            password: password of ``username``.
            security: optional security string of asyncua, e.g.
                ``"Basic256Sha256,SignAndEncrypt,client_cert.der,client_key.pem"``.
            reconnect: backoff between reconnects after an error.
            check_lengths: check on connect that the nodes carry ``send_size`` / ``recv_size``
                bytes (a node without value is accepted).
        """
        super().__init__(send_size, recv_size, clock)
        self.endpoint = endpoint
        self.out_node_id = out_node
        self.in_node_id = in_node
        self.timeout = timeout
        self.username = username
        self.password = password
        self.security = security
        self.reconnect = reconnect if reconnect is not None else ReconnectPolicy()
        self.check_lengths = check_lengths
        self._client: Any = None
        self._out: Any = None
        self._in: Any = None
        self._out_encoding = _BYTESTRING
        self._out_variant: Any = None
        self._ua: Any = None
        self._user_closed = False

    # ------------------------------------------------------------------ connection

    def connect(self) -> None:
        self._user_closed = False
        self._drop(TransportState.DISCONNECTED)
        asyncua = load_asyncua()
        self._ua = asyncua.ua
        client = asyncua.sync.Client(self.endpoint, timeout=self.timeout)
        try:
            if self.username:
                client.set_user(self.username)
                client.set_password(self.password or "")
            if self.security:
                client.set_security_string(self.security)
            client.connect()
        except Exception as exc:  # asyncua raises many types
            with contextlib.suppress(Exception):
                client.disconnect()
            self.reconnect.failed(self.clock())
            self._state = TransportState.ERROR
            log.warning("cannot connect to %s: %s", self.endpoint, exc)
            raise TransportConnectError(f"cannot connect to {self.endpoint}: {_text(exc)}") from exc
        try:
            self._out, self._out_encoding, self._out_variant = self._telegram_node(
                client, self.out_node_id, self.send_size, "out_node"
            )
            self._in, _, _ = self._telegram_node(client, self.in_node_id, self.recv_size, "in_node")
        except TransportError:
            with contextlib.suppress(Exception):
                client.disconnect()
            self.reconnect.failed(self.clock())
            self._state = TransportState.ERROR
            raise
        self._client = client
        self._state = TransportState.CONNECTED
        self.reconnect.succeeded()
        self.statistics.connects += 1
        log.info("connected to %s (connect #%d)", self.endpoint, self.statistics.connects)

    def _telegram_node(self, client: Any, node_id: str, size: int, name: str) -> tuple[Any, str, Any]:
        """Node, encoding and variant type of a telegram node; checks type and length."""
        ua = self._ua
        try:
            node = client.get_node(node_id)
            value = node.read_data_value().Value
        except Exception as exc:
            raise TransportConnectError(f"{name} {node_id!r}: {_text(exc)}") from exc
        vtype = value.VariantType if value is not None else None
        if vtype is None or (value.Value is None and vtype == ua.VariantType.Null):
            # no value yet: take the declared data type
            try:
                vtype = node.read_data_type_as_variant_type()
            except Exception as exc:
                raise TransportConnectError(f"{name} {node_id!r}: data type unknown: {_text(exc)}") from exc
            current: Any = None
        else:
            current = value.Value
        if vtype == ua.VariantType.ByteString:
            encoding = _BYTESTRING
        elif vtype.name in _ARRAY_TYPES:
            encoding = _ARRAY
        else:
            raise TransportConnectError(
                f"{name} {node_id!r}: data type {vtype.name} cannot carry a telegram (ByteString or a number array expected)"
            )
        if self.check_lengths and current is not None:
            if encoding == _ARRAY and not isinstance(current, (list, tuple)):
                raise TransportConnectError(f"{name} {node_id!r}: {vtype.name} is no array")
            length = len(current) if isinstance(current, (bytes, bytearray, list, tuple)) else -1
            if length not in (0, size):
                raise TransportConnectError(f"{name} {node_id!r} has {length} bytes, the telegram has {size}")
        return node, encoding, vtype

    def close(self) -> None:
        self._user_closed = True
        self._drop(TransportState.CLOSED)

    def _drop(self, state: TransportState) -> None:
        client, self._client = self._client, None
        self._out = self._in = None
        if client is not None:
            with contextlib.suppress(Exception):
                client.disconnect()
        self._state = state

    def _ensure_connected(self) -> None:
        if self._client is not None:
            return
        if self._user_closed:
            raise TransportClosedError("transport was closed")
        if self.statistics.connects > 0 or self._state is TransportState.ERROR:
            if not self.reconnect.enabled:
                raise TransportConnectError("connection lost and reconnect is disabled")
            now = self.clock()
            if not self.reconnect.allowed(now):
                wait = self.reconnect.next_attempt - now
                raise TransportConnectError(f"reconnect to {self.endpoint} delayed ({wait:.3f} s)")
        self.connect()

    # ------------------------------------------------------------------ exchange

    def _encode(self, out: bytes) -> Any:
        ua = self._ua
        if self._out_encoding == _BYTESTRING:
            variant = ua.Variant(out, ua.VariantType.ByteString)
        else:
            values: list[Any] = (
                [float(b) for b in out] if self._out_variant.name in _FLOAT_TYPES else list(out)
            )
            variant = ua.Variant(values, self._out_variant, is_array=True)
        return ua.DataValue(variant)

    def _decode(self, value: Any) -> bytes:
        if value is None:
            data = b""
        elif isinstance(value, (bytes, bytearray)):
            data = bytes(value)
        elif isinstance(value, (list, tuple)):
            try:
                data = bytes(int(v) & 0xFF for v in value)
            except (TypeError, ValueError) as exc:
                raise TransportProtocolError(f"in_node: value is no byte array: {exc}") from exc
        else:
            raise TransportProtocolError(f"in_node: value of type {type(value).__name__} is no byte array")
        if len(data) != self.recv_size:
            raise TransportProtocolError(f"in_node has {len(data)} bytes, expected {self.recv_size}")
        return data

    def _exchange(self, out: bytes) -> bytes:
        self._ensure_connected()
        try:
            self._out.write_value(self._encode(out))
            value = self._in.read_value()
            return self._decode(value)
        except TransportProtocolError:
            raise
        except TransportError as exc:
            self._drop(TransportState.ERROR)
            log.warning("connection dropped: %s", exc)
            raise
        except TimeoutError as exc:
            self._drop(TransportState.ERROR)
            error = TransportTimeoutError(f"no answer of {self.endpoint} within {self.timeout * 1000:.0f} ms")
            log.warning("connection dropped: %s", error)
            raise error from exc
        except Exception as exc:  # connection lost, bad status ...
            self._drop(TransportState.ERROR)
            log.warning("connection dropped: %s", exc)
            raise TransportClosedError(f"OPC UA error: {_text(exc)}") from exc


def browse(
    endpoint: str,
    *,
    start: str | None = None,
    max_depth: int = 6,
    timeout: float = 2.0,
    username: str | None = None,
    password: str | None = None,
    security: str | None = None,
    max_nodes: int = 2000,
) -> list[OpcUaNodeInfo]:
    """Variables below ``start`` (default: the Objects folder), for configuration tools.

    Raises :class:`TransportConnectError` if the server cannot be reached.
    """
    asyncua = load_asyncua()
    ua = asyncua.ua
    client = asyncua.sync.Client(endpoint, timeout=timeout)
    try:
        if username:
            client.set_user(username)
            client.set_password(password or "")
        if security:
            client.set_security_string(security)
        client.connect()
    except Exception as exc:
        with contextlib.suppress(Exception):
            client.disconnect()  # also stops the thread of the client
        raise TransportConnectError(f"cannot connect to {endpoint}: {_text(exc)}") from exc
    result: list[OpcUaNodeInfo] = []
    try:
        root = client.get_node(start) if start else client.nodes.objects
        todo: list[tuple[Any, str, int]] = [(root, start or "Objects", 0)]
        seen: set[str] = set()
        while todo and len(result) < max_nodes:
            node, path, depth = todo.pop(0)
            try:
                children = node.get_children()
            except Exception:  # no access to a folder
                continue
            for child in children:
                key = child.nodeid.to_string()
                if key in seen:
                    continue
                seen.add(key)
                try:
                    name = child.read_browse_name().Name
                    node_class = child.read_node_class()
                except Exception:
                    continue
                child_path = f"{path}/{name}"
                if node_class == ua.NodeClass.Variable:
                    result.append(_node_info(child, key, child_path, ua))
                elif depth + 1 < max_depth and not (start is None and depth == 0 and name == "Server"):
                    todo.append((child, child_path, depth + 1))
    finally:
        with contextlib.suppress(Exception):
            client.disconnect()
    return result


def _node_info(node: Any, key: str, path: str, ua: Any) -> OpcUaNodeInfo:
    data_type, is_array, length, writable = "?", False, -1, False
    with contextlib.suppress(Exception):
        value = node.read_data_value().Value
        data_type = value.VariantType.name
        is_array = bool(value.is_array)
        if isinstance(value.Value, (bytes, bytearray, list, tuple)):
            length = len(value.Value)
    with contextlib.suppress(Exception):
        access = node.read_attribute(ua.AttributeIds.UserAccessLevel).Value.Value
        writable = bool(int(access) & ua.AccessLevel.CurrentWrite.mask)
    return OpcUaNodeInfo(key, path, data_type, is_array, length, writable)


def _text(exc: BaseException) -> str:
    text = str(exc)
    return f"{type(exc).__name__}: {text}" if text else type(exc).__name__
