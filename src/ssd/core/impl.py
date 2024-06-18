# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

RESULT_FILE = "result.txt"
NAND_FILE = "nand.txt"


class VirtualSSD(SSDInterface):
    _nand_file: Path
    _result_file: Path

    def __init__(self, rootdir: Path | None = None):
        if rootdir:
            self.set_rootdir(rootdir)

    def set_rootdir(self, rootdir: Path):
        self._nand_file = rootdir / NAND_FILE
        self._result_file = rootdir / RESULT_FILE

        self.formatSSD()

    def formatSSD(self):
        if not self._nand_file.exists():
            with open(self._nand_file, "w+") as f:
                for _ in range(100):
                    f.write(f"{_:02}\t0x{0:08x}\n")

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    @property
    def result_file(self) -> Path:
        return self._result_file

    def read(self, addr: int):
        if not self.nand_file.exists():
            self.result_file.write_text("0x00000000")
            return

        if 0 > addr or addr > 99:
            self.result_file.write_text("0x00000000")
            return

        self.result_file.write_text("0x00000000")

    def write(self, addr: int, data: str):
        with open(self._nand_file, "r+") as f:
            f.seek((len(f.readline()) + 1) * addr)
            f.write(f"{addr:02}\t0x{data:08x}\n")
