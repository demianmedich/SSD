# coding=utf-8
from abc import ABC, abstractmethod


class SSDInterface(ABC):

    @abstractmethod
    def read(self, addr):
        raise NotImplementedError()

    @abstractmethod
    def write(self, addr, data):
        raise NotImplementedError()
