# coding=utf-8
import os
from pathlib import Path

from ssd.util.logger import Logger
from ssd.util.valid import (
    DEFAULT_LOWER_BOUND,
    DEFAULT_UPPER_BOUND,
    is_8digit_hex_string,
    is_valid_address,
)


class ResultReader:
    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
        self.result_path = dir_path / "result.txt"

    def fetch_read_result(self) -> str:
        with open(self.result_path, "r", encoding="utf-8") as fp:
            ret = fp.read()
        return ret


class Shell:
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
        f"\tfullread\n"
        f"erase: Erase value amount of size from address\n"
        f"\terase [address] [size]\n"
        f"erase_range: Erase value from start (include) to end (exclude)\n"
        f"\terase_range [start address] [end address]\n"
        f"flush: Flush all commands in buffer\n"
        f"\tflush\n"
    )

    def __init__(
        self,
        result_reader: ResultReader,
        address_lower_bound: int = DEFAULT_LOWER_BOUND,
        address_upper_bound: int = DEFAULT_UPPER_BOUND,
    ):
        self.result_reader = result_reader
        self.__min_lba = address_lower_bound
        self.__max_lba = address_upper_bound
        self.logger = Logger()

    def is_valid(self, address, value):
        if not is_valid_address(address):
            return False

        if is_8digit_hex_string(value):
            return True

        return False

    def write(self, address: int, value: str):
        if not self.is_valid(address, value):
            self.help()
            return

        self.logger.print(f"python -m ssd W {address} {value}")
        os.system(f"python -m ssd W {address} {value}")

    def read(self, address: int) -> str:
        if not is_valid_address(address):
            self.help()
            return ""

        os.system(f"python -m ssd R {address}")
        read_result = self.result_reader.fetch_read_result()
        self.logger.print(read_result)
        return read_result

    def erase(self, address: int, size: int):
        if not ((0 < size) and (address + size <= 100) and (0 <= address)):
            self.help()
            return

        while size:
            self.logger.print(f"python -m ssd E {address} {min(10, size)}")
            os.system(f"python -m ssd E {address} {min(10, size)}")
            address += min(10, size)
            size -= min(10, size)

    def erase_range(self, start_address: int, end_address: int):
        self.erase(start_address, end_address - start_address)

    def help(self):
        print(self.HELP_MESSAGE)

    def fullwrite(self, value):
        if not self.is_valid(self.__max_lba, value):
            self.help()
            return

        for lba in range(self.__min_lba, self.__max_lba + 1):
            self.write(lba, value)

    def fullread(self):
        result = []
        for lba in range(self.__min_lba, self.__max_lba + 1):
            result.append(self.read(lba))
        return result

    def flush(self):
        os.system(f"python -m ssd F")
