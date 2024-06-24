from ssd.shell.api import Shell
from ssd.shell.cmd.base import ShellCommandInterface


class EraseCommand(ShellCommandInterface):
    def __init__(self, api: Shell, args: list[str]):
        super().__init__(api, args)
        self.address = 0
        self.size = 0

    def is_valid(self) -> bool:
        if (
            len(self.args) != 2
            or not self.args[0].isdigit()
            or not self.args[1].isdigit()
        ):
            return False
        self.address, self.size = map(int, self.args)
        return True

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
            return
        self.api.erase(self.address, self.size)
