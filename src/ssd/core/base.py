# coding=utf-8
from abc import ABC, abstractmethod


class SSDInterface(ABC):

    @abstractmethod
    def read(self):
        raise NotImplementedError()

    @abstractmethod
    def write(self):
        raise NotImplementedError()
