"""
TODO
    1. Command 패턴 적용?
    - 모든 명령 default 에서 관리
    - 모든 에러 catch 해서 print
"""

import cmd
import os
from pathlib import Path

from ssd.shell.api import ResultReader, Shell
from ssd.shell.app.script_manager import ScriptManager
from ssd.shell.cmd.factory import ShellCommandFactory
from ssd.util.logger import Logger


class SsdTestShellApp(cmd.Cmd):
    intro = "Welcome to the SSD Test Shell. Type help to list commands.\n"
    prompt = "> "

    def __init__(self, ctrl: Shell):
        super().__init__()
        self.ssd_ctrl = ctrl
        self.logger = Logger()
        self._cmd_factory = ShellCommandFactory(api=self.ssd_ctrl)
        self._script_manager = ScriptManager()

    def do_exit(self, args):
        return True

    def do_help(self, args):
        """
        Notice
        `help` 입력 시 self.default()로 가지 않고 super.do_help()가 실행되기에
        별도로 HelpCommand 만들지 않고 override 했습니다.
        """
        self.ssd_ctrl.help()

    def default(self, args: str):
        try:
            cmd_object = self._cmd_factory.parse(args)
            cmd_object.execute()
            return
        except ValueError:
            pass

        try:
            script_path = self._script_manager.find(args)
        except FileNotFoundError:
            self.logger.print("INVALID COMMAND")
            return

        try:
            ret = self._script_manager.execute(script_path)
            self.logger.print("Pass" if ret else "Fail")
        except Exception as e:
            self.logger.print(e)

    def emptyline(self):
        pass


if __name__ == "__main__":
    app = SsdTestShellApp(Shell(ResultReader(Path(os.getcwd()))))
    app.cmdloop()
