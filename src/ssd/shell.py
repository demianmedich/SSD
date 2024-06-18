# coding=utf-8
from abc import ABC, abstractmethod


class IVirtualSsd(ABC):
    @abstractmethod
    def read(self, address: int):
        raise NotImplementedError

    @abstractmethod
    def write(self, address: int, value: int):
        raise NotImplementedError


class ReadCacheAccessor:
    pass


class SsdShell:
    def __init__(self, ssd_accessor: IVirtualSsd):
        self.ssd_accessor = ssd_accessor
        self.read_cache_accessor = ReadCacheAccessor()

    def read(self, address: int):
        if not self._is_valid_address(address):
            raise ValueError  # TODO: 에러? or 출력?
        self.ssd_accessor.read(address)

    @staticmethod
    def _is_valid_address(address):
        return 0 <= address <= 99

    def help(self):
        raise NotImplementedError
