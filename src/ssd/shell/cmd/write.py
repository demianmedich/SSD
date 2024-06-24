from ssd.shell.api import Shell
from ssd.shell.cmd.base import IShellCommand


class WriteCommand(IShellCommand):
    def __init__(self, api: Shell, args: list[str]):
        super().__init__(api, args)
        self.address = 0
        self.value = ""

    def is_valid(self) -> bool:
        if len(self.args) != 2 or not self.args[0].isdigit():
            return False
        self.address = int(self.args[0])
        self.value = self.args[1]
        return True

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
        self.api.write(self.address, self.value)
