from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pyxis",
        description="Transparent architecture-to-code compiler and Workspace runtime.",
    )
    parser.add_subparsers(dest="command")
    parser.parse_args()
    parser.print_help()


if __name__ == "__main__":
    main()
