# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tools.test_report
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Test case registry (stable test IDs), test report and test case catalog of SRCI_PY.
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

"""Test case registry (stable test IDs), test report and test case catalog of SRCI_PY.

python -m tools.test_report update            # assign IDs to new tests (tests/testcases.json)
python -m tools.test_report check             # registry and docs/TestCases.md up to date?
python -m tools.test_report catalog           # write docs/TestCases.md
pytest --tc-report build/test-report          # test report (Markdown + HTML)
"""
