"""Cli for Karkas."""

from argparse import Namespace

from karkas.options import make_parser
from karkas.run import Runner


def get_args() -> Namespace:
    """
    Returns the parsed command-line arguments.

    Returns:
        Namespace: The parsed command-line arguments.
    """
    parser = make_parser()
    return parser.parse_args()


def main() -> None:
    """
    Execute the main functionality of the program.

    Returns:
        None
    """
    args = get_args()
    runner = Runner(args.path)
    runner.run()


if __name__ == "__main__":
    main()
