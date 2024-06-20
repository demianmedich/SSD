import sys

from shell.app.test_runner import SsdTestRunnerApp
from shell.app.test_shell import SsdTestShellApp


def main():
    if len(sys.argv) == 1:
        SsdTestShellApp().cmdloop()
    elif len(sys.argv) == 2:
        SsdTestRunnerApp().execute_runlist(sys.argv[1])
    else:
        print("Invalid number of arguments.")


if __name__ == "__main__":
    """
    HOW TO RUN
        1. cd src
        2.1. python -m shell
        2.2. python -m shell runlist.txt
    """
    main()
