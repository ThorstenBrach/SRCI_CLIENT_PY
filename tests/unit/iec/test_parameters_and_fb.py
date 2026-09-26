"""Library parameters (srci.configure) and the base class of the transpiled FBs."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

import srci
from srci import library_parameters as params_module
from srci.iec import rt
from srci.iec.fb import FunctionBlock
from srci.types import AxesGroupStateDataChanged, RobotLibraryParameter, iec


@pytest.fixture
def restore() -> Iterator[None]:
    old = srci.parameters()
    created = params_module._instances_created
    yield
    params_module._instances_created = False
    values: dict[str, Any] = {k: v for k, v in old.items() if k != "MESSAGE_TEXT_LEN"}
    srci.configure(**values)
    params_module._instances_created = created


def test_parameter_values() -> None:
    p = srci.parameters()
    assert p["TOOL_MAX"] == RobotLibraryParameter.TOOL_MAX
    assert p["SWAP_BYTE_ORDER"] is True


@pytest.mark.usefixtures("restore")
def test_configure_changes_array_sizes() -> None:
    params_module._instances_created = False
    srci.configure(TOOL_MAX=4, FRAME_MAX=3)
    changed = AxesGroupStateDataChanged()
    assert len(changed.Tool) == 4 and len(changed.Frame) == 3
    t = iec.ArrayType(0, iec.Param("TOOL_MAX", -1), iec.BOOL)
    assert t.count == 4 and rt.type_size(t) == 4
    srci.configure(TOOL_MAX=6)
    assert t.count == 6 and rt.type_size(t) == 6  # caches are cleared
    assert repr(iec.Param("TOOL_MAX", -1)) == "RobotLibraryParameter.TOOL_MAX - 1"
    assert repr(iec.Param("TOOL_MAX")) == "RobotLibraryParameter.TOOL_MAX"
    assert iec.array_len(1, iec.Param("TOOL_MAX")) == 6


@pytest.mark.usefixtures("restore")
def test_configure_errors() -> None:
    params_module._instances_created = False
    with pytest.raises(KeyError):
        srci.configure(UNKNOWN=1)
    with pytest.raises(ValueError):
        srci.configure(MESSAGE_TEXT_LEN=100)
    with pytest.raises(TypeError):
        srci.configure(TOOL_MAX=1.5)
    with pytest.raises(ValueError):
        srci.configure(TOOL_MAX=0)
    srci.configure(ACR_USAGE_WARNING_LIMIT=90)  # int for a REAL parameter is fine
    params_module._instances_created = True
    with pytest.raises(RuntimeError):
        srci.configure(TOOL_MAX=8)
    srci.configure(TOOL_MAX=RobotLibraryParameter.TOOL_MAX)  # unchanged value is fine
    srci.configure(force=True, TOOL_MAX=8)
    assert RobotLibraryParameter.TOOL_MAX == 8


class Base(FunctionBlock):
    def _init_vars_(self) -> None:
        self.order: list[str] = ["vars Base"]
        self.x = 1

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        self.order.append(f"FB_init Base (Derived vars: {getattr(self, 'y', None)})")
        return False


class Derived(Base):
    def _init_vars_(self) -> None:
        self.order.append("vars Derived")
        self.y = 2

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        self.order.append("FB_init Derived")
        return False


def test_function_block_initialisation_order() -> None:
    """Codesys: all variables first, then FB_init of the base, then FB_init of the derived FB."""
    d = Derived()
    assert d.order == ["vars Base", "vars Derived", "FB_init Base (Derived vars: 2)", "FB_init Derived"]
    with pytest.raises(NotImplementedError):
        d()


def test_new_instance_of_struct_members() -> None:
    from srci.types import AxesGroup

    ag: Any = AxesGroup()
    assert type(ag.State.OnlineChange_R).__name__ == "R_TRIG"
    assert type(ag.Acyclic.ActiveCommandRegister).__name__ == "ActiveCommandRegisterFB"
    assert ag.MessageLog.ExternalLogger is None  # interface reference
