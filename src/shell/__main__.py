import sys

from shell.app.test_runner import SsdTestRunnerApp
from shell.app.test_shell import SsdTestShellApp


def main():
    if len(sys.argv) == 1:
        SsdTestShellApp().cmdloop()
    elif len(sys.argv) == 2:
        SsdTestRunnerApp().run_test_list(sys.argv[1])
    else:
        print("Invalid number of arguments.")


if __name__ == "__main__":
    """
    HOW TO RUN
        python -m shell
        python -m shell runlist.txt
    """
    main()
