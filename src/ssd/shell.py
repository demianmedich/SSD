# coding=utf-8
import os
from abc import ABC, abstractmethod
from pathlib import Path


class IVirtualSsd(ABC):
    @abstractmethod
    def read(self, address: int):
        raise NotImplementedError

    @abstractmethod
    def write(self, address: int, value: int):
        raise NotImplementedError


class ReadResultAccessor:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
        self.result_path = dir_path / "result.txt"

    def fetch_read_result(self) -> str:
        with open(self.result_path, "r", encoding="utf-8") as fp:
            ret = fp.read()
        return ret


class SsdShell:
    HELP_MESSAGE = (
        f"SSD Shell Commands:\n"
        f"write: Write value (0xXXXXXXXX) to address (0~99)\n"
        f"\twrite [address] [value]\n"
        f"read: Read value of address (0~99)\n"
        f"\tread [address]\n"
        f"exit: Exit shell interface\n"
        f"\texit\n"
        f"help: Print help\n"
        f"\thelp\n"
        f"fullwrite: Write value (0xXXXXXXXX) to entire address\n"
        f"\tfullwrite [value]\n"
        f"fullread: Read value of entire address\n"
        f"\tfullread"
    )

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
