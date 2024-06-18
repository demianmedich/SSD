# coding=utf-8
from abc import ABC, abstractmethod


class IVirtualSsd(ABC):
    @abstractmethod
    def read(self, address: int):
        raise NotImplementedError

    @abstractmethod
    def write(self, address: int, value: int):
        raise NotImplementedError


class SsdShell:
    def __init__(self, ssd_accessor: IVirtualSsd):
        self.ssd_accessor = ssd_accessor

    def read(self, lba_pos: int):
        return self.ssd_accessor.read(lba_pos)

    def help(self):
        raise NotImplementedError

    def full_write(self, value):
        pass

    def full_read(self):
        pass
