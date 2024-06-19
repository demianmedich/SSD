import cmd
import os
from pathlib import Path

from src.ssd.shell import ReadResultAccessor, Shell

# TODO: 얘를 shell로 바꾸고 기존 shell.py는 control.py 등으로 변경


class SsdShell(cmd.Cmd):
    prompt = "> "

    def __init__(self, ctrl: Shell):
        super().__init__()
        self.ssd_ctrl = ctrl

    def do_read(self, args):
        self.ssd_ctrl.read(int(args))

    def do_write(self, args):
        addr, value = args.split()
        self.ssd_ctrl.write(int(addr), value)

    def do_exit(self, args):
        return True

    def do_help(self, args):
        self.ssd_ctrl.help()

    def do_fullread(self, args):
        self.ssd_ctrl.fullread()

    def do_fullwrite(self, args):
        self.ssd_ctrl.fullwrite(args)

    def do_testapp1(self, args):
        self.ssd_ctrl.testapp1()

    def do_testapp2(self, args):
        self.ssd_ctrl.testapp2()

    def default(self, line):
        """Handle invalid commands"""
        print("INVALID COMMAND")


if __name__ == "__main__":
    app = SsdShell(Shell(ReadResultAccessor(Path(os.getcwd()))))
    app.cmdloop()
