# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.st2py.__main__
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    CLI: ``python -m tools.st2py [--check] [--only NAME ...]``.
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

"""CLI: ``python -m tools.st2py [--check] [--only NAME ...]``.

Transpiles the function blocks and functions of the PLC library (RobotLibrary.xml) to
Python modules below ``src/srci`` (``fb``, ``functions``, ``interfaces``).
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from tools.file_header import GENERATED_DATE, render
from tools.plcopen_gen.emitter import Generator
from tools.plcopen_gen.overrides import apply_overrides
from tools.plcopen_gen.parser import parse_library

from .config import CONFIG, Config, PouClone
from .decl import parse_interface
from .emit import EmitError
from .library import Body, Method, Pou, load_pous
from .module import ModuleEmitter
from .registry import Target, build_registry, generated_packages
from .sem import TypeEnv

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_XML = ROOT / "third_party" / "robotlibrary" / "RobotLibrary.xml"
SRC = ROOT / "src"
MANIFEST = SRC / "srci" / "_st2py_manifest.txt"


class PatchError(Exception):
    pass


def clone_pou(pous: dict[str, Pou], clone: PouClone) -> None:
    source = pous.get(clone.source.upper())
    target = pous.get(clone.target.upper())
    if source is None or target is None:
        raise PatchError(f"clone {clone.source} -> {clone.target}: POU not found")

    def fix(text: str) -> str:
        for old, new in clone.replacements:
            text = text.replace(old, new)
        return text

    for old, _ in clone.replacements:
        texts = [source.decl, source.body.src] + [m.decl + m.body.src for m in source.methods.values()]
        if not any(old in t for t in texts):
            raise PatchError(f"clone {clone.target}: replacement {old!r} not found - remove it")
    decl = fix(source.decl)
    if clone.target_decl is not None:
        decl = target.decl
        for old, new in clone.target_decl:
            if old not in decl:
                raise PatchError(f"clone {clone.target}: declaration text {old!r} not found")
            decl = decl.replace(old, new)
    itf = parse_interface(decl)
    pou = Pou(itf.header, itf.vars, Body(fix(source.body.src)), target.folder, decl=decl)
    keep = {m.upper() for m in clone.keep_methods}
    for name in keep:
        if name not in target.methods:
            raise PatchError(f"clone {clone.target}: method {name} to keep not found")
        pou.methods[name] = target.methods[name]
        target.methods[name].owner = pou
    for method in source.methods.values():
        if method.name.upper() in keep:
            continue
        m_itf = parse_interface(fix(method.decl))
        pou.methods[method.name.upper()] = Method(
            m_itf.header, m_itf.vars, Body(fix(method.body.src)), pou, decl=fix(method.decl)
        )
    pous[clone.target.upper()] = pou


def apply_patches(pous: dict[str, Pou], cfg: Config) -> None:
    for clone in cfg.clones:
        clone_pou(pous, clone)
    for var in cfg.variables:
        pou = pous.get(var.pou.upper())
        if pou is None:
            raise PatchError(f"variable target {var.pou} not found")
        added = parse_interface(f"FUNCTION_BLOCK {var.pou}\n{var.decl}").vars
        names = {v.name.upper() for v in pou.vars}
        for v in added:
            if v.name.upper() in names:
                raise PatchError(f"variable {var.pou}.{v.name} exists already - remove the VarAppend")
        pou.vars.extend(added)
    for patch in cfg.patches:
        pou = pous.get(patch.pou.upper())
        if pou is None:
            raise PatchError(f"patch target {patch.pou} not found")
        body = pou.body if patch.method is None else pou.methods[patch.method.upper()].body
        if patch.regex:
            new = patch.new if patch.template else patch.new.replace("\\", "\\\\")
            body.src, count = re.subn(patch.old, new, body.src)
            if count == 0:
                raise PatchError(f"patch for {patch.pou}.{patch.method} is obsolete (no match) - remove it")
        elif patch.old not in body.src:
            raise PatchError(f"patch for {patch.pou}.{patch.method} is obsolete (text not found) - remove it")
        else:
            body.src = body.src.replace(patch.old, patch.new)
        body._parsed = None
    for append in cfg.appends:
        pou = pous.get(append.pou.upper())
        if pou is None or append.method.upper() not in pou.methods:
            raise PatchError(f"append target {append.pou}.{append.method} not found")
        body = pou.methods[append.method.upper()].body
        body.src = body.src.rstrip() + "\n\n" + append.text
        body._parsed = None


def load(xml: Path, cfg: Config) -> tuple[TypeEnv, dict[str, Target]]:
    lib = parse_library(xml)
    apply_overrides(lib)
    digest = hashlib.sha256(xml.read_bytes()).hexdigest()
    gen = Generator(lib, digest)
    pous = load_pous(xml)
    apply_patches(pous, cfg)
    env = TypeEnv(gen, pous)
    reg = build_registry(pous)
    return env, reg


def module_path(module: str) -> Path:
    return SRC / Path(*module.split(".")).with_suffix(".py")


def generate(xml: Path, cfg: Config, only: set[str] | None = None) -> tuple[dict[Path, str], list[str]]:
    env, reg = load(xml, cfg)
    files: dict[Path, str] = {}
    errors: list[str] = []
    for key, pou in sorted(env.pous.items()):
        target = reg.get(key)
        if target is None or target.hand:
            continue
        if only is not None and pou.name not in only:
            continue
        emitter = ModuleEmitter(env, reg, pou, cfg)
        try:
            files[module_path(target.module)] = emitter.emit_module()
        except EmitError as exc:
            errors.append(f"{pou.name}: {exc}")
        except Exception as exc:  # pragma: no cover - reported with the POU name
            errors.append(f"{pou.name}: {type(exc).__name__}: {exc}")
    if only is None:
        for pkg in sorted(generated_packages(reg)):
            init = module_path(pkg).with_suffix("") / "__init__.py"
            if not init.exists():
                name = pkg.rsplit(".", 1)[-1]
                files[init] = (
                    render(name, GENERATED_DATE, "generated package") + f'"""{name} (generated package)."""\n'
                )
        files[SRC / "srci" / "fb" / "_registry.py"] = registry_module(env, reg)
        files[SRC / "srci" / "fb" / "__init__.pyi"] = registry_stub(env, reg)
    return files, errors


def registry_module(env: TypeEnv, reg: dict[str, Target]) -> str:
    lines = [
        render("srci.fb._registry", GENERATED_DATE, "Python modules of the function blocks (generated)"),
        '"""Python modules of the function blocks of the PLC library (generated by tools.st2py)."""',
        "",
        "FB_MODULES: dict[str, str] = {",
    ]
    for key, t in sorted(reg.items()):
        pou = env.pous.get(key)
        if pou is not None and pou.kind == "FUNCTION_BLOCK":
            lines.append(f'    "{t.name}": "{t.module}",')
    lines.append("}")
    return "\n".join(lines) + "\n"


def registry_stub(env: TypeEnv, reg: dict[str, Target]) -> str:
    """Type stub of ``srci.fb``: the function blocks that ``srci.fb.__getattr__`` loads lazily."""
    lines = [
        render("srci.fb", GENERATED_DATE, "Type stub of the function blocks (generated)"),
        '"""Function blocks of the PLC library (generated by tools.st2py)."""',
        "",
        "# ruff: noqa",
    ]
    for key, t in sorted(reg.items()):
        pou = env.pous.get(key)
        if pou is not None and pou.kind == "FUNCTION_BLOCK":
            lines.append(f"from {t.module} import {t.name} as {t.name}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.st2py", description=__doc__)
    ap.add_argument("--xml", type=Path, default=DEFAULT_XML)
    ap.add_argument("--check", action="store_true", help="fail if the generated files are out of date")
    ap.add_argument("--only", nargs="*", help="only these POUs")
    args = ap.parse_args(argv)
    files, errors = generate(args.xml, CONFIG, set(args.only) if args.only else None)
    for e in errors:
        print("ERROR", e, file=sys.stderr)
    if args.check:
        stale = [p for p, s in files.items() if not p.exists() or p.read_text("utf-8") != s]
        if stale or errors:
            for p in stale:
                print("out of date:", p.relative_to(ROOT), file=sys.stderr)
            print("run: python -m tools.st2py", file=sys.stderr)
            return 1
        print(f"{len(files)} generated files are up to date")
        return 0
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_text("utf-8") != text:
            path.write_text(text, encoding="utf-8", newline="\n")
    print(f"{len(files)} files, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
