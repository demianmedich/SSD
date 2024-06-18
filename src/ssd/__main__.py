# coding=utf-8
import argparse

from src.ssd.core.impl import VirtualSSD


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # TODO: Please implement me to use "args.op", "args.value"
    return parser.parse_args()


def cli_main():
    args = parse_args()
    _do_command(args)


def _do_command(args: argparse.Namespace):
    """TODO: please implement me"""


if __name__ == "__main__":
    cli_main()
