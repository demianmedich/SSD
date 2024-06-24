# coding=utf-8
import os
from pathlib import Path

from ssd.util.logger import Logger


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
        f"\tfullread"
    )

    def __init__(self, result_reader: ResultReader):
        self.result_reader = result_reader
        self.__min_lba = 0
        self.__max_lba = 99
        self.logger = Logger()

    def is_valid(self, address, value):
        if self.__min_lba > address or address > self.__max_lba:
            return False

        if (
            len(value) == 10
            and value.startswith("0x")
            and all(c in "0123456789ABCDEF" for c in value[2:])
        ):
            return True

        return False

    def write(self, address: int, value: str):
        if not self.is_valid(address, value):
            self.help()
            return

        os.system(f"python -m ssd W {address} {value}")

    def read(self, address: int) -> str:
        if not self._is_valid_address(address):
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
            self.logger.print(f"python -m ssd E {address} {min( 10, size )}")
            os.system(f"python -m ssd E {address} {min( 10, size )}")
            address += min(10, size)
            size -= min(10, size)

    def erase_range(self, start_address: int, end_address: int):
        self.erase(start_address, end_address - start_address)

    def flush(self):
        os.system(f"python -m ssd F")

    @staticmethod
    def _is_valid_address(address):
        return 0 <= address <= 99

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

    def testapp1(self):
        test_value = "0xAAAAAAAA"
        self.fullwrite(test_value)
        data = self.fullread()
        for i in range(len(data)):
            if data[i] != test_value:
                self.logger.print("Fail")
                return
        self.logger.print("Success")

    def testapp2(self):
        test_value1 = "0xAAAABBBB"
        test_value2 = "0x12345678"
        for _ in range(30):
            for lba in range(6):
                self.write(lba, test_value1)

        for lba in range(6):
            self.write(lba, test_value2)

        for lba in range(6):
            data = self.read(lba)
            if data != test_value2:
                self.logger.print("Fail")
                return
        self.logger.print("Success")
