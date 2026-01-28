"""CLI entrypoint for Applejack."""

import argparse
import sys
from typing import List, Optional

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="applejack")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    parse_parser = subparsers.add_parser(
        "parse",
        help="Parse Applesoft source.",
    )
    parse_parser.add_argument("source", help="Path to source file.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate Applesoft source.",
    )
    validate_parser.add_argument("source", help="Path to source file.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if args.command is None:
            parser.error("missing command")
        return 0
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 1


if __name__ == "__main__":
    sys.exit(main())
