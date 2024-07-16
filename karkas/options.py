"""Utility to create the argument parser."""

import argparse
from pathlib import Path

from karkas import __version__


def make_parser() -> argparse.ArgumentParser:
    """
    Create and return an ArgumentParser object for reading in a comic or set of comics.

    Args:
        path: Path of a comic or a folder of comics.

    Returns:
        argparse.ArgumentParser: The ArgumentParser object for parsing command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Read in a comic or set of comics, and return the result.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("path", help="Path of a comic or a folder of comics.", type=Path)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit",
    )

    return parser
