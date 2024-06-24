# coding=utf-8
from ssd.driver.buffered_ssd import CommandBufferedSSDInterface


class RangeValidationDecorator(CommandBufferedSSDInterface):

    def __init__(self, ssd: CommandBufferedSSDInterface):
        self._ssd = ssd

    def read(self, addr: int):
        if 0 > addr or addr > 99:
            self.print_help()
            return

        self._ssd.read(addr)

    def write(self, addr: int, data: int):
        if 0 > addr or addr > 99:
            self.print_help()
            return

        self._ssd.write(addr, data)

    def erase(self, addr: int, size: int):
        if not ((0 < size <= 10) and (addr + size <= 100) and (0 <= addr)):
            self.print_help()
            return

        self._ssd.erase(addr, size)

    def flush(self):
        self._ssd.flush()

    @property
    def help_message(self) -> str:
        return (
            "Invalid command!"
            "Read:  python -m ssd R {addr}"
            "Write: python -m ssd W {addr} {data}"
            "Erase: python -m ssd E {addr} {size}"
            "Flush: python -m ssd F "
            "addr = [0, 99], data = 0xXXXXXXXX, size = [1, 10]"
        )

    def print_help(self):
        print(self.help_message)
