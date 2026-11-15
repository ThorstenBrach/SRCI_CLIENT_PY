# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.transport.opcua_config
#  Author:      Thorsten Brach
#  Date:        2026-11-14
#
#  Description:
#    Configuration files (TOML) for the OPC UA transport: endpoint and node layout of a robot.
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

"""Configuration files (TOML) for the OPC UA transport: endpoint and node layout of a robot.

OPC UA servers publish the SRCI telegrams in different ways. A PLC bridge has one node per
direction that carries the whole telegram (``ByteString`` or ``Byte[]``); a robot controller
that maps its PROFINET I/O to OPC UA (e.g. a Staubli CS9) has one node **per byte**. A
configuration file describes the layout once, so nobody has to link hundreds of nodes by hand::

    name = "Staubli CS9 uniVALpi"
    endpoint = "opc.tcp://192.168.2.117:853/Staubli"
    username = "maintenance"          # the password is not stored in the file

    [plc_to_rc]                       # PLC->RC telegram, written by the client
    nodes = "ns=1;s=Robot:Inputs/Outputs:J207J208-SiemensTRL_256:%IB{bit}"
    size = 256                        # bytes of the telegram

    [rc_to_plc]                       # RC->PLC telegram, read by the client
    nodes = "ns=1;s=Robot:Inputs/Outputs:J207J208-SiemensTRL_256:%QB{bit}"
    size = 256

``nodes`` of a direction is

* a NodeId without placeholder: **one** node carries the whole telegram (``size`` bytes);
* a NodeId with the placeholders ``{index}`` (byte number, from ``first``, default 0) and/or
  ``{bit}`` (bit address = 8 * byte number): ``size`` nodes, one per byte;
* a list of NodeIds: one node per byte, ``len(nodes) == size``.

The ready-made files of this package are listed by :func:`profiles` and loaded with
:func:`load_profile`; :meth:`srci.transport.OpcUaTransport.from_config` opens a transport.
This module needs no ``asyncua``.
"""

from __future__ import annotations

import os
import string
import tomllib
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from importlib import resources
from pathlib import Path
from typing import Any

__all__ = [
    "OpcUaConfig",
    "OpcUaConfigError",
    "OpcUaDirection",
    "expand_nodes",
    "load_config",
    "load_profile",
    "parse_config",
    "profiles",
]

PLACEHOLDERS = frozenset({"index", "bit"})
_PROFILE_PACKAGE = "srci.transport.opcua_profiles"


class OpcUaConfigError(ValueError):
    """Invalid OPC UA configuration (file or values)."""


def expand_nodes(template: str, size: int, first: int = 0) -> list[str]:
    """NodeIds of ``size`` bytes from a template with ``{index}`` / ``{bit}``.

    >>> expand_nodes("ns=1;s=IO:%IB{bit}", 3)
    ['ns=1;s=IO:%IB0', 'ns=1;s=IO:%IB8', 'ns=1;s=IO:%IB16']
    """
    names = _placeholders(template)
    if not names:
        raise OpcUaConfigError(f"{template!r} has no placeholder {{index}} or {{bit}}")
    return [template.format(index=first + i, bit=8 * (first + i)) for i in range(size)]


def _placeholders(template: str) -> set[str]:
    try:
        names = {name for _, name, _, _ in string.Formatter().parse(template) if name is not None}
    except ValueError as exc:
        raise OpcUaConfigError(f"{template!r}: {exc}") from exc
    unknown = names - PLACEHOLDERS
    if unknown:
        raise OpcUaConfigError(
            f"{template!r}: unknown placeholder {', '.join(sorted(unknown))} (allowed: {{index}}, {{bit}})"
        )
    return names


@dataclass(frozen=True)
class OpcUaDirection:
    """Node layout of one telegram direction."""

    nodes: str | tuple[str, ...]
    """One NodeId (whole telegram on one node) or one NodeId per byte."""
    size: int
    """Bytes of the telegram."""
    consistency_byte: int | None = None
    """``[plc_to_rc]`` with one node per byte: byte the RC checks for consistency, written in
    three steps (see :class:`srci.transport.OpcUaTransport`)."""

    @property
    def per_byte(self) -> bool:
        return not isinstance(self.nodes, str)

    @property
    def node_ids(self) -> list[str]:
        return [self.nodes] if isinstance(self.nodes, str) else list(self.nodes)


@dataclass(frozen=True)
class OpcUaConfig:
    """Contents of a configuration file; :meth:`OpcUaTransport.from_config` opens a transport."""

    endpoint: str
    plc_to_rc: OpcUaDirection
    rc_to_plc: OpcUaDirection
    name: str = ""
    description: str = ""
    username: str | None = None
    password: str | None = None
    """Only for tests: better give it to ``from_config`` or via ``password_env``."""
    password_env: str | None = None
    """Name of an environment variable with the password (read by :meth:`resolved_password`)."""
    security: str | None = None
    timeout: float = 1.0
    check_lengths: bool = True
    write_changed_only: bool = False
    max_nodes_per_call: int | None = None
    """Nodes per Read/Write request; ``None``: the limit of the server (OperationLimits)."""
    cycle_ms: int | None = None
    """Recommended cycle time of the client (for applications such as the HMI)."""
    lifesign_timeout_ms: int | None = None
    """Recommended LifeSign timeout ``ParCfg.Com.LifeSignTimeOut`` (for applications)."""
    source: str = ""
    """File the configuration was loaded from."""
    extra: Mapping[str, Any] = field(default_factory=dict)
    """Unknown keys of the file (kept for applications)."""

    @property
    def send_size(self) -> int:
        return self.plc_to_rc.size

    @property
    def recv_size(self) -> int:
        return self.rc_to_plc.size

    def resolved_password(self) -> str | None:
        """``password`` or the value of the environment variable ``password_env``."""
        if self.password is not None:
            return self.password
        if self.password_env:
            return os.environ.get(self.password_env)
        return None

    def with_endpoint(self, endpoint: str) -> OpcUaConfig:
        return replace(self, endpoint=endpoint)


_TOP_KEYS: dict[str, type | tuple[type, ...]] = {
    "name": str,
    "description": str,
    "endpoint": str,
    "username": str,
    "password": str,
    "password_env": str,
    "security": str,
    "timeout": (int, float),
    "check_lengths": bool,
    "write_changed_only": bool,
    "max_nodes_per_call": int,
    "cycle_ms": int,
    "lifesign_timeout_ms": int,
}
_DIRECTIONS = ("plc_to_rc", "rc_to_plc")


def parse_config(data: Mapping[str, Any], *, source: str = "") -> OpcUaConfig:
    """Configuration from the parsed contents of a file (a dict)."""
    where = f"{source}: " if source else ""
    values: dict[str, Any] = {}
    extra: dict[str, Any] = {}
    for key, value in data.items():
        if key in _DIRECTIONS:
            continue
        expected = _TOP_KEYS.get(key)
        if expected is None:
            extra[key] = value
            continue
        if (isinstance(value, bool) and expected is not bool) or not isinstance(value, expected):
            raise OpcUaConfigError(f"{where}{key} has the wrong type ({type(value).__name__})")
        values[key] = value
    if "endpoint" not in values:
        raise OpcUaConfigError(f"{where}endpoint is missing")
    if "timeout" in values:
        values["timeout"] = float(values["timeout"])
        if values["timeout"] <= 0:
            raise OpcUaConfigError(f"{where}timeout must be > 0")
    if values.get("max_nodes_per_call", 1) < 1:
        raise OpcUaConfigError(f"{where}max_nodes_per_call must be >= 1")
    return OpcUaConfig(
        plc_to_rc=_direction(data.get("plc_to_rc"), f"{where}[plc_to_rc]"),
        rc_to_plc=_direction(data.get("rc_to_plc"), f"{where}[rc_to_plc]"),
        source=source,
        extra=extra,
        **values,
    )


def _direction(section: Any, where: str) -> OpcUaDirection:
    if not isinstance(section, Mapping):
        raise OpcUaConfigError(f"{where} is missing")
    allowed = {"nodes", "size", "first"} | ({"consistency_byte"} if where.endswith("[plc_to_rc]") else set())
    unknown = set(section) - allowed
    if unknown:
        raise OpcUaConfigError(f"{where}: unknown key {', '.join(sorted(unknown))}")
    size = section.get("size")
    if isinstance(size, bool) or not isinstance(size, int) or size < 1:
        raise OpcUaConfigError(f"{where}: size (bytes of the telegram, >= 1) is missing or invalid")
    guard = section.get("consistency_byte")
    if guard is not None and (isinstance(guard, bool) or not isinstance(guard, int) or not 0 <= guard < size):
        raise OpcUaConfigError(f"{where}: consistency_byte must be a byte number 0 ... {size - 1}")
    direction = _nodes(section, size, where)
    if guard is not None and not direction.per_byte:
        raise OpcUaConfigError(f"{where}: consistency_byte needs one node per byte")
    return OpcUaDirection(direction.nodes, size, guard)


def _nodes(section: Mapping[str, Any], size: int, where: str) -> OpcUaDirection:
    first = section.get("first", 0)
    if isinstance(first, bool) or not isinstance(first, int) or first < 0:
        raise OpcUaConfigError(f"{where}: first must be an integer >= 0")
    nodes = section.get("nodes")
    if isinstance(nodes, str):
        if not nodes.strip():
            raise OpcUaConfigError(f"{where}: nodes is empty")
        if _placeholders(nodes):
            return OpcUaDirection(tuple(expand_nodes(nodes, size, first)), size)
        if "first" in section:
            raise OpcUaConfigError(f"{where}: first needs a template with {{index}} or {{bit}}")
        return OpcUaDirection(nodes, size)
    if isinstance(nodes, list) and nodes and all(isinstance(n, str) and n.strip() for n in nodes):
        if len(nodes) != size:
            raise OpcUaConfigError(f"{where}: {len(nodes)} nodes for {size} bytes")
        if len(set(nodes)) != len(nodes):
            raise OpcUaConfigError(f"{where}: a node is listed twice")
        return OpcUaDirection(tuple(nodes), size)
    raise OpcUaConfigError(f"{where}: nodes must be a NodeId, a template or a list of NodeIds")


def load_config(path: str | os.PathLike[str]) -> OpcUaConfig:
    """Read a configuration file (TOML)."""
    file = Path(path)
    try:
        with file.open("rb") as stream:
            data = tomllib.load(stream)
    except OSError as exc:
        raise OpcUaConfigError(f"{file}: {exc.strerror or exc}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise OpcUaConfigError(f"{file}: {exc}") from exc
    return parse_config(data, source=str(file))


def profiles() -> list[str]:
    """Names of the configuration files shipped with this package (e.g. ``staubli_cs9``)."""
    folder = resources.files(_PROFILE_PACKAGE)
    return sorted(item.name[:-5] for item in folder.iterdir() if item.name.endswith(".toml"))


def load_profile(name: str) -> OpcUaConfig:
    """A configuration file shipped with this package, see :func:`profiles`."""
    if name not in profiles():
        raise OpcUaConfigError(f"no OPC UA profile {name!r} (available: {', '.join(profiles())})")
    item = resources.files(_PROFILE_PACKAGE) / f"{name}.toml"
    try:
        data = tomllib.loads(item.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise OpcUaConfigError(f"profile {name}: {exc}") from exc
    return parse_config(data, source=f"profile {name}")
