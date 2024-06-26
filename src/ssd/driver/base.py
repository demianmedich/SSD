# coding=utf-8
from abc import ABC, abstractmethod


class SSDInterface(ABC):

    @abstractmethod
    def read(self, addr: int):
        raise NotImplementedError()

    @abstractmethod
    def write(self, addr: int, data: int):
        raise NotImplementedError()
