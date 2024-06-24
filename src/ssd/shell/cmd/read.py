from ssd.shell.api import Shell
from ssd.shell.cmd.base import IShellCommand


class ReadCommand(IShellCommand):
    def __init__(self, api: Shell, args: list[str]):
        super().__init__(api, args)
        self.address = 0

    def is_valid(self) -> bool:
        if len(self.args) != 1 or not self.args[0].isdigit():
            return False
        self.address = int(self.args[0])
        return True

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
            return
        self.api.read(self.address)
