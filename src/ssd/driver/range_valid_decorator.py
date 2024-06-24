# coding=utf-8
from ssd.driver.buffered_ssd import CommandBufferedSSDInterface
from ssd.util.valid import is_valid_address, is_valid_address_and_size


class RangeValidationDecorator(CommandBufferedSSDInterface):

    def __init__(self, ssd: CommandBufferedSSDInterface):
        self._ssd = ssd

    def read(self, addr: int):
        if not is_valid_address(addr):
            self.print_help()
            return

        self._ssd.read(addr)

    def write(self, addr: int, data: int):
        if not is_valid_address(addr):
            self.print_help()
            return

        self._ssd.write(addr, data)

    def erase(self, addr: int, size: int):
        if not is_valid_address_and_size(addr, size):
            self.print_help()
            return

        self._ssd.erase(addr, size)

    def flush(self):
        self._ssd.flush()

    @property
    def help_message(self) -> str:
        return (
            "Invalid command!\n"
            "Read:  python -m ssd R {addr}\n"
            "Write: python -m ssd W {addr} {data}\n"
            "Erase: python -m ssd E {addr} {size}\n"
            "Flush: python -m ssd F \n"
            "addr = [0, 99], data = 0xXXXXXXXX, size = [1, 10]\n"
        )

    def print_help(self):
        print(self.help_message)
