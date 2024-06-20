import sys

from ssd.shell.app.cli import SsdTestShellApp
from ssd.shell.app.runner import SsdTestRunnerApp
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
        2.1. python -m ssd.shell
        2.2. python -m ssd.shell runlist.txt
    """
    main()
