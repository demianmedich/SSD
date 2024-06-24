from ssd.shell.api import Shell
from ssd.shell.cmd.base import IShellCommand


class EraseRangeCommand(IShellCommand):
    def __init__(self, api: Shell, args: list[str]):
        super().__init__(api, args)
        self.start_addr = 0
        self.end_addr = 0

    def is_valid(self) -> bool:
        if (
            len(self.args) != 2
            or not self.args[0].isdigit()
            or not self.args[1].isdigit()
        ):
            return False
        self.start_addr, self.end_addr = map(int, self.args)
        return True

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
            return
        self.api.erase_range(self.start_addr, self.end_addr)
