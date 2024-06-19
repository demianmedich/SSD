# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

DEFAULT_VALUE = 0x00000000

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

        self.make_initial_nand()

    def make_initial_nand(self):
        if not self.nand_file.exists():
            with open(self.nand_file, mode="w", encoding="utf-8", newline="\n") as f:
                f.writelines(f"{i:02}\t0x{0:08x}\n" for i in range(100))

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    @property
    def result_file(self) -> Path:
        return self._result_file

    def read(self, addr: int):
        if not self.nand_file.exists():
            self.result_file.write_text(f"0x{DEFAULT_VALUE}")
            return

        if 0 > addr or addr > 99:
            self.result_file.write_text(f"0x{DEFAULT_VALUE}")
            return

        with open(self.nand_file, mode="rt", encoding="utf-8", newline="\n") as f:
            line = f.readline()
            len_line = len(line)
            f.seek(len_line * addr)
            data = f.readline().split()[-1].strip()

        self.result_file.write_text(data)

    def write(self, addr: int, data: int):
        if not self.nand_file.exists():
            self.make_initial_nand()

        with open(self.nand_file, mode="r+", encoding="utf-8", newline="\n") as f:
            line = f.readline()
            len_line = len(line)
            f.seek(len_line * addr)
            f.write(f"{addr:02}\t0x{data:08x}\n")
