import os
import sys
from pathlib import Path

from ssd.shell.api import ResultReader, Shell
from ssd.shell.app.cli import SsdTestShellApp
from ssd.shell.app.runner import SsdTestRunnerApp
from ssd.util.logger import Logger


def main():
    logger = Logger()

    rootdir = Path(os.getcwd())

    truncate_file(rootdir / "result.txt")
    truncate_file(rootdir / "buffer.txt")

    with open(rootdir / "buffer.txt", mode="w", encoding="utf-8", newline="\n"):
        pass

    if len(sys.argv) == 1:
        SsdTestShellApp(Shell(ResultReader(Path(os.getcwd())))).cmdloop()
    elif len(sys.argv) == 2:
        SsdTestRunnerApp().execute_runlist(sys.argv[1])
    else:
        logger.print("Invalid number of arguments.")


def truncate_file(file: Path):
    with open(file, mode="w", encoding="utf-8", newline="\n"):
        pass


if __name__ == "__main__":
    """
    HOW TO RUN
        1. cd src
        2.1. python -m ssd.shell
        2.2. python -m ssd.shell runlist.txt
    """
    main()
