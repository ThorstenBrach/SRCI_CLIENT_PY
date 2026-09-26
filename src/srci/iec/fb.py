"""Base class of the transpiled function blocks."""

from __future__ import annotations

from typing import Any

__all__ = ["FunctionBlock"]


class FunctionBlock:
    """Initialisation like Codesys: first all variables of the whole class hierarchy
    (``_init_vars_`` of every class, base first), then ``FB_init`` of every class that
    defines it (base first; Codesys calls the FB_init of the base implicitly).
    """

    def __init__(self) -> None:
        from srci.library_parameters import _mark_instance_created

        _mark_instance_created()
        mro = type(self).__mro__[::-1]
        for cls in mro:
            init_vars = cls.__dict__.get("_init_vars_")
            if init_vars is not None:
                init_vars(self)
        for cls in mro:
            fb_init = cls.__dict__.get("FB_init")
            if fb_init is not None:
                fb_init(self, bInitRetains=False, bInCopyCode=False)

    def __call__(self, **inputs: Any) -> None:  # pragma: no cover - overridden
        raise NotImplementedError
