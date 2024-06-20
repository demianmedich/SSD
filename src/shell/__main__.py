import sys

from shell.app.cli import SsdTestShellApp
from shell.app.runner import SsdTestRunnerApp
from ssd.util.logger import Logger


def main():
    logger = Logger()
    if len(sys.argv) == 1:
        SsdTestShellApp().cmdloop()
    elif len(sys.argv) == 2:
        SsdTestRunnerApp().execute_runlist(sys.argv[1])
    else:
        logger.print("Invalid number of arguments.")


if __name__ == "__main__":
    """
    HOW TO RUN
        1. cd src
        2.1. python -m shell
        2.2. python -m shell runlist.txt
    """
    main()
