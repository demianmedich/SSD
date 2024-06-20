"""
TODO
    1. 모든 명령 default 에서 관리
    2. 모든 에러 catch 해서 print
    3. Command Pattern 적용
    4. ssd.shell 로 이동
"""

import cmd

from ssd.shell.app.util import ScriptManager
from ssd.util.logger import Logger


class SsdTestShellAppOld(cmd.Cmd):
    intro = "Welcome to the SSD Test Shell. Type help to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self._script_manager = ScriptManager()

    def do_read(self, args):
        self.logger.print("read!")

    def do_write(self, args):
        self.logger.print("Write!")

    def do_exit(self, args):
        return True

    def do_help(self, args):
        self.logger.print("HELp!")

    def do_fullread(self, args):
        self.logger.print("FULLREAD")

    def do_fullwrite(self, args):
        self.logger.print("FULLWRITE")

    def do_erase(self, args):
        self.logger.print("ERASE!")

    def do_flush(self, args):
        self.logger.print("FLUSH!")

    def default(self, args: str):
        try:
            script_path = self._script_manager.find(args)
        except FileNotFoundError:
            self.logger.print("INVALID COMMAND")
            return

        try:
            ret = self._script_manager.execute(script_path)
            print("Pass" if ret else "Fail")
        except Exception as e:
            print(e)

    def emptyline(self):
        pass
