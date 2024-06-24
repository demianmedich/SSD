# coding=utf-8
from pathlib import Path

from ssd.driver.base import SSDInterface
from ssd.util.logger import Logger

DEFAULT_VALUE = 0x00000000

RESULT_FILE = "result.txt"
NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"


class VirtualSSD(SSDInterface):
    _nand_file: Path
    _result_file: Path

    def __init__(self, rootdir: str | Path = Path.cwd()):
        self.set_rootdir(rootdir)
        self._logger = Logger()

    def set_rootdir(self, rootdir: str | Path):
        rootdir = Path(rootdir)
        self._nand_file = rootdir / NAND_FILE
        self._result_file = rootdir / RESULT_FILE

        self.make_initial_nand()

    def make_initial_nand(self):
        if not self.nand_file.exists():
            with open(self.nand_file, mode="w", encoding="utf-8", newline="\n") as f:
                f.writelines(self.data_format(i, 0) for i in range(100))

    @property
    def nand_file(self) -> Path:
        return self._nand_file

    @property
    def result_file(self) -> Path:
        return self._result_file

    def read(self, addr: int):
        with open(self.nand_file, mode="rt", encoding="utf-8", newline="\n") as f:
            f.seek(len(f.readline()) * addr)
            data = f.readline().split()[-1].strip()
            self.result_file.write_text(data)

    def write(self, addr: int, data: int):
        with open(self.nand_file, mode="r+", encoding="utf-8", newline="\n") as f:
            f.seek(len(f.readline()) * addr)
            f.write(self.data_format(addr, data))

    def data_format(self, addr: int, data: int) -> str:
        return f"{addr:02}\t0x{data:08X}\n"
