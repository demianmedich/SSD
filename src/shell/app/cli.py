"""
TODO
    1. 모든 명령 default 에서 관리
    2. 모든 에러 catch 해서 print
    3. Command Pattern 적용
"""

import cmd


class SsdTestShellApp(cmd.Cmd):
    intro = "Welcome to the SSD Test Shell. Type help to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()

    def do_read(self, args):
        print("read!")

    def do_write(self, args):
        print("Write!")

    def do_exit(self, args):
        return True

    def do_help(self, args):
        print("HELp!")

    def do_fullread(self, args):
        print("FULLREAD")

    def do_fullwrite(self, args):
        print("FULLWRITE")

    def do_erase(self, args):
        print("ERASE!")

    def do_flush(self, args):
        print("FLUSH!")

    def default(self, line):
        print("INVALID COMMAND")

    def emptyline(self):
        pass
