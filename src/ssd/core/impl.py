# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

NAND_FILE = "nand.txt"


class VirtualSSD(SSDInterface):

    def __init__(self, ssd_dir: Path):
        self._nand_file = ssd_dir / NAND_FILE

        self.formatSSD()

    def formatSSD(self):
        if not self._nand_file.exists():
            with open(self._nand_file, "w+") as f:
                for _ in range(100):
                    f.write(f"{_:02}\t0x{0:08x}\n")

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    def read(self):
        """TODO: Please implement me"""

    def write(self, addr, data):
        with open(self._nand_file, "r+") as f:
            f.write(f"{addr:02}\t0x{data:08x}\n")
