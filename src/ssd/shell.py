# coding=utf-8
from abc import ABC, abstractmethod


class IVirtualSsd(ABC):
    @abstractmethod
    def read(self, address: int):
        raise NotImplementedError

    @abstractmethod
    def write(self, address: int, value: int):
        raise NotImplementedError


class ReadResultAccessor:
    def fetch_read_result(self):
        return "0x00000000"  # TODO: read real file


class SsdShell:
    HELP_MESSAGE = "help!"

    def __init__(
        self, ssd_accessor: IVirtualSsd, read_res_accessor: ReadResultAccessor
    ):
        self.ssd_accessor = ssd_accessor
        self.read_result_accessor = read_res_accessor

    def read(self, address: int):
        if not self._is_valid_address(address):
            self.help()
            return
        self.ssd_accessor.read(address)
        print(self.read_result_accessor.fetch_read_result())  # TODO: 출력 Format 맞추기

    @staticmethod
    def _is_valid_address(address):
        return 0 <= address <= 99

    def help(self):
        print(SsdShell.HELP_MESSAGE)
