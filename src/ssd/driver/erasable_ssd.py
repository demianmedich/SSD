# coding=utf-8
from abc import ABC, abstractmethod

from ssd.driver.base import SSDInterface

DEFAULT_VALUE = 0x00000000


class ErasableSSDInterface(SSDInterface, ABC):

    @abstractmethod
    def erase(self, addr: int, size: int):
        raise NotImplementedError()


class ErasableVirtualSSD(ErasableSSDInterface):

    def __init__(self, ssd: SSDInterface):
        self._ssd = ssd

    def read(self, addr: int):
        self._ssd.read(addr)

    def write(self, addr: int, data: int):
        self._ssd.write(addr, data)

    def erase(self, addr: int, size: int):
        for i in range(size):
            self.write(addr + i, DEFAULT_VALUE)
