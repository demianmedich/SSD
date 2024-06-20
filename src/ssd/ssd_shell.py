import cmd
import os
from pathlib import Path

from src.ssd.shell import ReadResultAccessor, Shell
from ssd.util.logger import Logger

# TODO: 얘를 shell로 바꾸고 기존 shell.py는 control.py 등으로 변경


class SsdShell(cmd.Cmd):
    prompt = "> "

    def __init__(self, ctrl: Shell):
        super().__init__()
        self.ssd_ctrl = ctrl
        self.logger = Logger()

    def do_erase(self, args):
        try:
            args = args.split()
            if len(args) != 2:
                raise ValueError
            self.ssd_ctrl.erase(int(args[0]), int(args[1]))
        except ValueError:
            self.ssd_ctrl.help()

    def do_erase_range(self, args):
        try:
            args = args.split()
            if len(args) != 2:
                raise ValueError
            self.ssd_ctrl.erase_range(int(args[0]), int(args[1]))
        except ValueError:
            self.ssd_ctrl.help()

    def do_read(self, args):
        try:
            args = args.split()
            if len(args) != 1:
                raise ValueError
            self.ssd_ctrl.read(int(args[0]))
        except ValueError:
            self.ssd_ctrl.help()

    def do_write(self, args):
        try:
            args = args.split()
            if len(args) != 2:
                raise ValueError
            self.ssd_ctrl.write(int(args[0]), args[1])
        except ValueError:
            self.ssd_ctrl.help()

    def do_exit(self, args):
        return True

    def do_help(self, args):
        self.ssd_ctrl.help()

    def do_fullread(self, args):
        self.ssd_ctrl.fullread()

    def do_fullwrite(self, args):
        try:
            args = args.split()
            if len(args) != 1:
                raise ValueError
            self.ssd_ctrl.fullwrite(args[0])
        except ValueError:
            self.ssd_ctrl.help()

    def do_testapp1(self, args):
        self.ssd_ctrl.testapp1()

    def do_testapp2(self, args):
        self.ssd_ctrl.testapp2()

    def default(self, line):
        """Handle invalid commands"""
        self.logger.print("INVALID COMMAND")

    def emptyline(self):
        pass


if __name__ == "__main__":
    app = SsdShell(Shell(ReadResultAccessor(Path(os.getcwd()))))
    app.cmdloop()
