# coding=utf-8
from pathlib import Path

from src.ssd.core.base import SSDInterface

DEFAULT_VALUE = 0x00000000

RESULT_FILE = "result.txt"
NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"


class VirtualSSD(SSDInterface):
    _nand_file: Path
    _result_file: Path

    def __init__(self, rootdir: str | Path = Path.cwd()):
        self.set_rootdir(rootdir)

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
        if 0 > addr or addr > 99:
            self.result_file.write_text(f"0x{DEFAULT_VALUE:08X}")
            return

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


class CommandBuffer:
    def __init__(self, ssd: VirtualSSD, rootdir: str | Path = Path.cwd()):
        rootdir = Path(rootdir)
        self._nand_txt_path = rootdir / NAND_FILE
        self._buffer_txt_path = rootdir / BUFFER_TXT
        self._ssd = ssd

        self._make_initial_buffer()

    def flush(self) -> None:
        cmds = self._read_commands_buffer_txt()
        for opcode, addr, value_or_cnt in cmds:
            match opcode:
                case "W":
                    self._ssd.write(addr, value_or_cnt)
                case "E":
                    # TODO: erase 추가 필요.
                    # self._ssd.erase(addr, value_or_cnt)
                    pass
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")

    def read(self, requested_address: int) -> int:
        if requested_address < 0 or requested_address >= 100:
            raise ValueError(f"Invalid address {requested_address}")

        for cmd in self._read_commands_buffer_txt():
            opcode, address, value_or_cnt = cmd.split()

            if int(address) == requested_address:
                match opcode:
                    case "W":
                        return int(value_or_cnt, 16)
                    case "E":
                        return 0
                    case _:
                        raise ValueError(f"Invalid opcode {opcode}")

        raise ValueError(f"Not found data")

    def write(self, cmd: str) -> None:
        commands = self._read_commands_buffer_txt()
        commands.append(cmd)
        changed = self._optimize_commands(commands)

        if changed:
            with open(
                self._buffer_txt_path, mode="wt", encoding="utf-8", newline="\n"
            ) as f:
                f.writelines(f"{cmd}\n" for cmd in commands)
        else:
            with open(
                self._buffer_txt_path, mode="w+", encoding="utf-8", newline="\n"
            ) as f:
                f.write(f"{cmd}\n")

    def _read_commands_buffer_txt(self) -> list[str]:
        commands = self._buffer_txt_path.read_text(encoding="utf-8").split("\n")
        return [cmd for cmd in commands if cmd]
        # return commands

    def _make_initial_buffer(self):
        with open(self._buffer_txt_path, mode="w", encoding="utf-8", newline="\n"):
            pass

    def _optimize_commands(self, commands: list[str]) -> bool:
        """TODO: 최적화 로직을 구현해주세요.

        Returns:
            True: 최적화로 인해 커맨드 변경됐음.
            False: 커맨드 변경사항 없음.
        """
        if not commands:
            return False
        return False
