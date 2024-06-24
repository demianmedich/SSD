from abc import ABC, abstractmethod

from ssd.shell.api import Shell


class ShellCommandInterface(ABC):
    def __init__(self, api: Shell, args: list[str]):
        self.api = api
        self.args = args

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
