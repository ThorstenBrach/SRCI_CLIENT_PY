"""Command line of tools.test_report (see the package docstring)."""

from __future__ import annotations

import argparse
import sys

from tools.test_report import catalog, registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.test_report")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("update", help="assign IDs to new tests, retire removed tests")
    sub.add_parser("check", help="exit code 1 if the registry or docs/TestCases.md is out of date")
    sub.add_parser("catalog", help="write docs/TestCases.md")
    args = parser.parse_args(argv)

    functions = registry.scan()
    entries = registry.load()
    if args.command == "update":
        updated = registry.update(entries, functions)
        new = len([e for e in updated if e not in entries])
        registry.save(updated)
        print(f"{len(updated)} test cases, {new} new/changed -> {registry.REGISTRY}")
        return 0
    if args.command == "catalog":
        text = catalog.render(entries, catalog.collect_counts())
        catalog.TARGET.write_text(text, encoding="utf-8", newline="\n")
        print(f"-> {catalog.TARGET}")
        return 0
    problems = registry.problems(entries, functions)
    if catalog.TARGET.read_text(encoding="utf-8") != catalog.render(entries, catalog.collect_counts()):
        problems.append("docs/TestCases.md out of date: python -m tools.test_report catalog")
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
