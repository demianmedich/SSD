from ssd.shell.cmd.base import ShellCommandInterface


class FlushCommand(ShellCommandInterface):
    def is_valid(self) -> bool:
        return len(self.args) == 0

    def execute(self) -> None:
        if not self.is_valid():
            self.api.help()
            return
        self.api.flush()
