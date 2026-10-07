# Mourad.Soltani
"""CLI for renewal-copy-gate."""

from __future__ import annotations

import argparse
import json
import sys

from renewal_copy_gate import __version__
from renewal_copy_gate.audit import audit_copy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="renewal-copy-gate",
        description="Audit SaaS billing copy for renewal disclosure gaps.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("file", nargs="?", help="Text file. Reads stdin if omitted.")
    args = parser.parse_args(argv)
    if args.file:
        with open(args.file, encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()
    report = audit_copy(text)
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
