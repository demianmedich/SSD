# coding=utf-8
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

    def write(self, address: int, value: str):
        self.ssd_accessor.write(address, value)

    def read(self, lba_pos: int):
        pass

    def exit(self):
        pass

    def help(self):
        pass

    def full_write(self, value):
        pass

    def full_read(self):
        pass
