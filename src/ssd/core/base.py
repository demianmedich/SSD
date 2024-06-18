# coding=utf-8
from abc import ABC, abstractmethod


class SSDInterface(ABC):

    @abstractmethod
    def read(self, lba_pos: int):
        raise NotImplementedError()

    @abstractmethod
    def write(self, lba_pos: int, value: str):
        raise NotImplementedError()
