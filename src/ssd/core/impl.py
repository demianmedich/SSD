# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

RESULT_FILE = "result.txt"
NAND_FILE = "nand.txt"


class VirtualSSD(SSDInterface):

    def __init__(self, ssd_dir: Path):
        self._nand_file = ssd_dir / NAND_FILE
        self._result_file = ssd_dir / RESULT_FILE

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    @property
    def result_file(self) -> Path:
        return self._result_file

    def read(self, lba_pos: int):
        self.result_file.write_text("0x00000000")

    def write(self, lba_pos: int, value: str):
        """TODO: Please implement me"""
