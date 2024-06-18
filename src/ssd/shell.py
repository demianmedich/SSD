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
        self.__max_lba = 100

    def read(self, address: int):
        return self.ssd_accessor.read(address)

    def write(self, address: int, value: int):
        return self.ssd_accessor.write(address, value)

    def help(self):
        raise NotImplementedError

    def fullwrite(self, value):
        for lba in range(self.__max_lba):
            self.write(lba, value)

    def fullread(self):
        for lba in range(self.__max_lba):
            self.read(lba)
