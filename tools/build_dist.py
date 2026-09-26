"""Offline build of the wheel and the sdist (``python -m tools.build_dist [--outdir dist]``).

The normal build is ``python -m build`` (backend hatchling, see pyproject.toml). This script
produces equivalent distributions without any build dependency, e.g. on machines without
access to a package index. The package is pure Python: the wheel is ``py3-none-any``.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import re
import tarfile
import time
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {"__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def _project() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]  # type: ignore[no-any-return]


def _version() -> str:
    text = (ROOT / "src" / "srci" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]+)"', text, flags=re.M)
    if match is None:
        raise SystemExit("no __version__ in src/srci/__init__.py")
    version: str = match.group(1)
    if version != _project()["version"]:
        raise SystemExit(f"version mismatch: pyproject {_project()['version']} / srci {version}")
    return version


def _files(base: Path) -> list[Path]:
    return sorted(
        p
        for p in base.rglob("*")
        if p.is_file() and not EXCLUDE_DIRS & set(p.parts) and p.suffix not in EXCLUDE_SUFFIXES
    )


def metadata(version: str) -> str:
    project = _project()
    lines = [
        "Metadata-Version: 2.4",
        f"Name: {project['name']}",
        f"Version: {version}",
        f"Summary: {project['description']}",
        "License-Expression: MIT",
        "License-File: LICENSE",
        f"Requires-Python: {project['requires-python']}",
    ]
    lines += [f"Author: {a['name']}" for a in project.get("authors", [])]  # type: ignore[attr-defined]
    lines += [f"Classifier: {c}" for c in project.get("classifiers", [])]  # type: ignore[attr-defined]
    lines += [f"Project-URL: {k}, {v}" for k, v in project.get("urls", {}).items()]  # type: ignore[attr-defined]
    for extra, deps in project.get("optional-dependencies", {}).items():  # type: ignore[attr-defined]
        lines.append(f"Provides-Extra: {extra}")
        lines += [f"Requires-Dist: {d}; extra == '{extra}'" for d in deps]
    lines += ["Description-Content-Type: text/markdown", ""]
    return "\n".join(lines) + "\n" + (ROOT / "README.md").read_text(encoding="utf-8")


def _record_hash(data: bytes) -> str:
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()


def build_wheel(outdir: Path, version: str) -> Path:
    name = "srci_client"
    dist_info = f"{name}-{version}.dist-info"
    path = outdir / f"{name}-{version}-py3-none-any.whl"
    entries: list[tuple[str, bytes]] = []
    for file in _files(ROOT / "src" / "srci"):
        entries.append((file.relative_to(ROOT / "src").as_posix(), file.read_bytes()))
    entries.append((f"{dist_info}/METADATA", metadata(version).encode()))
    entries.append(
        (
            f"{dist_info}/WHEEL",
            b"Wheel-Version: 1.0\nGenerator: tools.build_dist\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
        )
    )
    entries.append((f"{dist_info}/licenses/LICENSE", (ROOT / "LICENSE").read_bytes()))
    record = io.StringIO()
    writer = csv.writer(record, lineterminator="\n")
    for arcname, data in entries:
        writer.writerow([arcname, _record_hash(data), len(data)])
    writer.writerow([f"{dist_info}/RECORD", "", ""])
    entries.append((f"{dist_info}/RECORD", record.getvalue().encode()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, data in entries:
            info = zipfile.ZipInfo(arcname, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, data)
    return path


def build_sdist(outdir: Path, version: str) -> Path:
    base = f"srci_client-{version}"
    path = outdir / f"{base}.tar.gz"
    include = ["src/srci", "examples", "docs", "README.md", "LICENSE", "pyproject.toml"]
    with tarfile.open(path, "w:gz") as tar:

        def add(arcname: str, data: bytes) -> None:
            info = tarfile.TarInfo(f"{base}/{arcname}")
            info.size = len(data)
            info.mtime = int(time.time())
            info.mode = 0o644
            tar.addfile(info, io.BytesIO(data))

        add("PKG-INFO", metadata(version).encode())
        for item in include:
            src = ROOT / item
            files = [src] if src.is_file() else _files(src)
            for file in files:
                add(file.relative_to(ROOT).as_posix(), file.read_bytes())
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.build_dist", description=__doc__)
    ap.add_argument("--outdir", type=Path, default=ROOT / "dist")
    args = ap.parse_args(argv)
    args.outdir.mkdir(parents=True, exist_ok=True)
    version = _version()
    for path in (build_wheel(args.outdir, version), build_sdist(args.outdir, version)):
        print(
            f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}  ({path.stat().st_size // 1024} KiB)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
