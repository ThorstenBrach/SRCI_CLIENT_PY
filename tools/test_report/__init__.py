"""Test case registry (stable test IDs), test report and test case catalog of SRCI_PY.

python -m tools.test_report update            # assign IDs to new tests (tests/testcases.json)
python -m tools.test_report check             # registry and docs/TestCases.md up to date?
python -m tools.test_report catalog           # write docs/TestCases.md
pytest --tc-report build/test-report          # test report (Markdown + HTML)
"""
