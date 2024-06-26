from ssd.shell.cmd.base import ShellCommandInterface


class FullWriteCommand(ShellCommandInterface):
    def is_valid(self) -> bool:
        return len(self.args) == 1

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
            return
        self.api.fullwrite(self.args[0])
