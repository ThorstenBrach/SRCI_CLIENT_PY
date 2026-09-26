# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      srci.library_parameters
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Library parameters (``RobotLibraryParameter`` of the PLC library).
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

"""Library parameters (``RobotLibraryParameter`` of the PLC library).

In Codesys the parameters of a library are set per project. Here they are set with
:func:`configure` before the first function block (e.g. ``MC_RobotTaskFB``) is created::

    import srci
    srci.configure(TOOL_MAX=20, FRAME_MAX=20, LOAD_MAX=20)

Array sizes of the structures and function blocks follow the parameters (the arrays are
created with the current values). Parameters that define STRING lengths cannot be changed.
"""

from __future__ import annotations

from srci.types import RobotLibraryParameter

__all__ = ["configure", "parameters"]

# STRING lengths are fixed at generation time (StringType descriptors)
_FIXED = {"MESSAGE_TEXT_LEN"}

_instances_created = False


def _mark_instance_created() -> None:
    global _instances_created
    _instances_created = True


def parameters() -> dict[str, object]:
    """Current values of all library parameters."""
    return {
        name: getattr(RobotLibraryParameter, name)
        for name in vars(RobotLibraryParameter)
        if name.isupper() and not name.startswith("_")
    }


def configure(*, force: bool = False, **values: object) -> None:
    """Set library parameters, e.g. ``configure(TOOL_MAX=20)``.

    Must be called before function blocks are created (``force=True`` skips this check;
    already created objects keep their array sizes).
    """
    current = parameters()
    for name, value in values.items():
        if name not in current:
            raise KeyError(f"unknown library parameter {name!r} (known: {', '.join(sorted(current))})")
        if name in _FIXED and value != current[name]:
            raise ValueError(f"library parameter {name} cannot be changed")
        if type(value) is not type(current[name]) and not (
            isinstance(current[name], float) and isinstance(value, int)
        ):
            raise TypeError(f"{name} must be {type(current[name]).__name__}, got {type(value).__name__}")
        if isinstance(value, int) and not isinstance(value, bool) and value < 1 and name.endswith("_MAX"):
            raise ValueError(f"{name} must be >= 1")
    if _instances_created and not force and any(values[n] != current[n] for n in values):
        raise RuntimeError("configure() must be called before the first function block is created")
    for name, value in values.items():
        if isinstance(current[name], float):
            value = float(value)  # type: ignore[arg-type]
        setattr(RobotLibraryParameter, name, value)
    _clear_caches()


def _clear_caches() -> None:
    from srci.iec import rt, sizeof

    sizeof._struct_size.cache_clear()
    rt.type_size.cache_clear()
    rt._zeroer.cache_clear()
