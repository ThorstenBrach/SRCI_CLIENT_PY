# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.tools.test_build_dist
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    tools.build_dist: offline wheel and sdist.
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

"""tools.build_dist: offline wheel and sdist."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import tarfile
import zipfile
from pathlib import Path

import srci
from tools import build_dist


def test_wheel_and_sdist(tmp_path: Path) -> None:
    assert build_dist.main(["--outdir", str(tmp_path)]) == 0
    wheel = tmp_path / f"srci_client-{srci.__version__}-py3-none-any.whl"
    with zipfile.ZipFile(wheel) as zf:
        names = set(zf.namelist())
        assert "srci/__init__.py" in names and "srci/py.typed" in names and "srci/fb/__init__.pyi" in names
        assert not any(n.startswith(("tests/", "tools/")) or "__pycache__" in n for n in names)
        info = f"srci_client-{srci.__version__}.dist-info"
        meta = zf.read(f"{info}/METADATA").decode()
        assert "Name: srci-client" in meta and f"Version: {srci.__version__}" in meta
        for name, digest, _size in csv.reader(io.StringIO(zf.read(f"{info}/RECORD").decode())):
            if digest:
                data = zf.read(name)
                expected = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
                assert digest == f"sha256={expected}", name
    with tarfile.open(tmp_path / f"srci_client-{srci.__version__}.tar.gz") as tar:
        names = set(tar.getnames())
    base = f"srci_client-{srci.__version__}"
    assert {f"{base}/PKG-INFO", f"{base}/pyproject.toml", f"{base}/src/srci/__init__.py"} <= names
    assert f"{base}/examples/core_profile/core_profile_demo.py" in names
