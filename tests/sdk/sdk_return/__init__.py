# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.sdk.sdk_return
#  Author:      Thorsten Brach
#  Date:        2026-10-25
#
#  Description:
#    Test data of the commands added to the SRCI SDK ("SDK return"), one module per group.
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

"""Test data of the commands added to the SRCI SDK ("SDK return"), one module per group.

Every module (``io.py``, ``gen.py``, ...) defines

* ``ADDED``: command types of the group,
* optionally ``PARCMD`` (function block -> ParCmd values for a valid command),
  ``RSP_VALUES`` (function block -> response values the test cannot choose freely),
  ``FW_NOT_PASSED`` (function block -> fields of the telegram the SDK evaluates itself),
  ``ERROR_CASES`` ((function block, ParCmd values, ErrorID, InfoID) of the parameter checks),
  ``KNOWN`` (function block -> reason, xfail strict),
  ``COMPANIONS`` (function block -> callables ``(harness, fb)`` adding function blocks that make the
  condition of a trigger function occur, tests.sdk.trigger_pump.when_buffered).

This package merges them (``tests.sdk.test_sdk_return``).
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import Any

ADDED: dict[str, tuple[int, ...]] = {}
PARCMD: dict[str, dict[str, Any]] = {}
RSP_VALUES: dict[str, dict[str, object]] = {}
FW_NOT_PASSED: dict[str, tuple[str, ...]] = {}
ERROR_CASES: list[tuple[str, tuple[tuple[str, Any], ...], int, int]] = []
KNOWN: dict[str, str] = {}
COMPANIONS: dict[str, tuple[Any, ...]] = {}

for _info in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    _mod = importlib.import_module(f"{__name__}.{_info.name}")
    ADDED[_info.name.upper()] = tuple(_mod.ADDED)
    PARCMD.update(getattr(_mod, "PARCMD", {}))
    RSP_VALUES.update(getattr(_mod, "RSP_VALUES", {}))
    FW_NOT_PASSED.update(getattr(_mod, "FW_NOT_PASSED", {}))
    ERROR_CASES.extend(getattr(_mod, "ERROR_CASES", []))
    KNOWN.update(getattr(_mod, "KNOWN", {}))
    COMPANIONS.update(getattr(_mod, "COMPANIONS", {}))

ADDED_TYPES = {t for types in ADDED.values() for t in types}
