"""
TODO
    1. Command 패턴 적용?
    - 모든 명령 default 에서 관리
    - 모든 에러 catch 해서 print
"""

import cmd
import os
from pathlib import Path

from ssd.driver.base import SSDInterface
from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableSSDInterface, ErasableVirtualSSD
from ssd.driver.virtual import VirtualSSD
from ssd.shell.api import ResultReader, Shell
from ssd.shell.app.script_manager import ScriptManager
from ssd.util.logger import Logger


class SsdTestShellApp(cmd.Cmd):
    intro = "Welcome to the SSD Test Shell. Type help to list commands.\n"
    prompt = "> "

    def __init__(self, ctrl: Shell):
        super().__init__()
        self.ssd_ctrl = ctrl
        self.logger = Logger()
        self._script_manager = ScriptManager()

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

    def do_flush(self, args):
        ssd = CommandBufferedSSD(
            ErasableVirtualSSD(
                VirtualSSD(
                    rootdir=Path(Logger.find_git_root()).joinpath("src/ssd/shell/app")
                )
            ),
            rootdir=Path(Logger.find_git_root()).joinpath("src/ssd/shell/app"),
        )

        ssd.flush()

    def default(self, args: str):
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
