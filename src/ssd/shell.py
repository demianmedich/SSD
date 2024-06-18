# coding=utf-8
import os
from abc import ABC, abstractmethod


class IVirtualSsd(ABC):
    @abstractmethod
    def read(self, address: int):
        raise NotImplementedError

    @abstractmethod
    def write(self, address: int, value: str):
        raise NotImplementedError


class Shell:
    def __init__(self, ssd_accessor: IVirtualSsd):
        self.ssd_accessor = ssd_accessor

    def is_valid(self, address, value):
        if 0 > address or address > 99:
            return False

        if value[:2] != "0x":
            return False
        for s in value[2:]:
            if (s < "A" or "F" < s) and (s < "0" or "9" < s):
                return False

        return True

    def write(self, address: int, value: str):
        if not self.is_valid(address, value):
            self.help()
            return

        cmd = f"ssd W {address} {value}"
        os.system(cmd)

    def read(self, lba_pos: int):
        pass

    def exit(self):
        os.system("exit")

    def help(self):
        pass

    def full_write(self, value):
        pass

    def full_read(self):
        pass
