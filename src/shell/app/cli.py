"""
TODO
    1. 모든 명령 default 에서 관리
    2. 모든 에러 catch 해서 print
    3. Command Pattern 적용
"""

import cmd

from ssd.core.logger import Logger


class SsdTestShellApp(cmd.Cmd):
    intro = "Welcome to the SSD Test Shell. Type help to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.LOG = Logger()

    def do_read(self, args):
        self.LOG.print("read!")

    def do_write(self, args):
        self.LOG.print("Write!")

    def do_exit(self, args):
        return True

    def do_help(self, args):
        self.LOG.print("HELp!")

    def do_fullread(self, args):
        self.LOG.print("FULLREAD")

    def do_fullwrite(self, args):
        self.LOG.print("FULLWRITE")

    def do_erase(self, args):
        self.LOG.print("ERASE!")

    def do_flush(self, args):
        self.LOG.print("FLUSH!")

    def default(self, line):
        self.LOG.print("INVALID COMMAND")

    def emptyline(self):
        pass
