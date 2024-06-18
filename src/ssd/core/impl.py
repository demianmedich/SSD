# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

NAND_FILE = "nand.txt"


class VirtualSSD(SSDInterface):

    def __init__(self, ssd_dir: Path):
        self._nand_file = ssd_dir / NAND_FILE

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    def read(self):
        """TODO: Please implement me"""

    def write(self):
        """TODO: Please implement me"""
