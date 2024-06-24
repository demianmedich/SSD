from ssd.shell.api import Shell
from ssd.shell.cmd.base import IShellCommand
from ssd.shell.cmd.erase import EraseCommand
from ssd.shell.cmd.erase_range import EraseRangeCommand
from ssd.shell.cmd.full_read import FullReadCommand
from ssd.shell.cmd.full_write import FullWriteCommand
from ssd.shell.cmd.read import ReadCommand
from ssd.shell.cmd.write import WriteCommand


class ShellCommandFactory:
    def __init__(self, api: Shell):
        self.api = api
        self.support_cmds = {
            "read": ReadCommand,
            "write": WriteCommand,
            "fullread": FullReadCommand,
            "fullwrite": FullWriteCommand,
            "erase": EraseCommand,
            "erase_range": EraseRangeCommand,
            # TODO
        }

    def parse(self, cmd_line: str) -> IShellCommand:
        parts = cmd_line.strip().split()

        command_name, args = parts[0], parts[1:]
        if command_name not in self.support_cmds:
            raise ValueError("Unknown command")

        cmd_class = self.support_cmds[command_name]
        return cmd_class(self.api, args)


if __name__ == "__main__":
    # just test
    cf = ShellCommandFactory(Shell(None))
    ret = cf.parse("read 1")
    print(ret.is_valid())
    print(ret.args)
