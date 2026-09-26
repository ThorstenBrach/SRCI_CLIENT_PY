# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.registry
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Where POUs and functions live in Python (generated or hand written).
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

"""Where POUs and functions live in Python (generated or hand written)."""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass

from .library import Pou


@dataclass(frozen=True)
class Target:
    module: str
    name: str
    hand: bool = False
    params: tuple[tuple[str, str], ...] = ()  # hand written functions: (UPPER ST name, python name)

    def param(self, st_name: str) -> str | None:
        for key, py in self.params:
            if key == st_name.upper():
                return py
        return None


# hand written modules that implement library POUs (scanned for names)
HAND_MODULES = (
    "srci.fb._internal.Send.RobotLibrarySendDataBaseFB",
    "srci.fb._internal.Send.RobotLibrarySendDataFB",
    "srci.fb._internal.Send.RobotLibraryCommandDataFB",
    "srci.fb._internal.Recv.RobotLibraryRecvDataBaseFB",
    "srci.fb._internal.Recv.RobotLibraryRecvDataFB",
    "srci.fb._internal.Recv.RobotLibraryResponseDataFB",
    "srci.functions.Common",
    "srci.functions.Convert.Misc",
    "srci.functions.Convert.DT",
)

STANDARD_MODULE = "srci.iec.standard"


def module_for(pou: Pou) -> str:
    """Python module of a generated POU (mirrors the folder structure of the library)."""
    folder = pou.folder[1:] if pou.folder and pou.folder[0] == "Library" else list(pou.folder)
    if not folder:
        raise ValueError(f"{pou.name}: no folder in the project structure")
    top = {"POUs": "fb", "Functions": "functions", "Interfaces": "interfaces"}.get(folder[0])
    if top is None:
        raise ValueError(f"{pou.name}: unexpected folder {folder}")
    return ".".join(["srci", top, *folder[1:], pou.name])


def _hand_names() -> dict[str, Target]:
    out: dict[str, Target] = {}
    for mod_name in HAND_MODULES:
        mod = importlib.import_module(mod_name)
        for name, obj in vars(mod).items():
            if name.startswith("_") or getattr(obj, "__module__", None) != mod_name:
                continue
            if inspect.isclass(obj):
                out[name.upper()] = Target(mod_name, name, hand=True)
            elif inspect.isfunction(obj):
                params = tuple((p.rstrip("_").upper(), p) for p in inspect.signature(obj).parameters)
                out[name.upper()] = Target(mod_name, name, hand=True, params=params)
    return out


def build_registry(pous: dict[str, Pou]) -> dict[str, Target]:
    hand = _hand_names()
    reg: dict[str, Target] = {}
    for key, pou in pous.items():
        if key in hand:
            reg[key] = hand[key]
        elif pou.kind in ("FUNCTION_BLOCK", "FUNCTION", "INTERFACE"):
            reg[key] = Target(module_for(pou), pou.name)
    for key in ("R_TRIG", "F_TRIG", "TON", "TOF", "TP"):
        reg[key] = Target(STANDARD_MODULE, key, hand=True)
    return reg


def generated_packages(reg: dict[str, Target]) -> set[str]:
    pkgs: set[str] = set()
    for t in reg.values():
        if t.hand:
            continue
        parts = t.module.split(".")
        for i in range(2, len(parts)):
            pkgs.add(".".join(parts[:i]))
    return pkgs


__all__ = ["Target", "build_registry", "generated_packages", "module_for"]
