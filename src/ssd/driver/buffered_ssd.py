import os
from abc import ABC, abstractmethod
from pathlib import Path

from ssd.driver.erasable_ssd import ErasableSSDInterface

NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"
RESULT_FILE = "result.txt"


class CommandBufferedSSDInterface(ErasableSSDInterface, ABC):

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError()


class CommandBufferedSSD(CommandBufferedSSDInterface):
    def __init__(self, ssd: ErasableSSDInterface, rootdir: str | Path = Path.cwd()):
        self.rootdir = Path(rootdir)
        self._buffer_txt_path = self.rootdir / BUFFER_TXT
        self._result_txt_path = self.rootdir / RESULT_FILE
        self._ssd = ssd

        if not self._buffer_txt_path.exists():
            self._make_initial_buffer()

    def read(self, addr: int) -> None:
        for cmd in self._read_commands_buffer_txt():
            opcode, address, value_or_cnt = cmd.split()

            if int(address) == addr:
                match opcode:
                    case "W":
                        self._result_txt_path.write_text(value_or_cnt)
                        return
                    case "E":
                        self._result_txt_path.write_text("0x00000000")
                        return
                    case _:
                        raise ValueError(f"Invalid opcode {opcode}")

        self._ssd.read(addr)

    def write(self, addr: int, data: int):
        self._buffer_command(f"W {addr} 0x{data:08X}")

    def erase(self, addr: int, size: int):
        self._buffer_command(f"E {addr} {size}")

    def _buffer_command(self, cmd):
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
                self._buffer_txt_path, mode="r+", encoding="utf-8", newline="\n"
            ) as f:
                f.seek(0, os.SEEK_END)
                f.write(f"{cmd}\n")

    def flush(self) -> None:
        cmds = self._read_commands_buffer_txt()
        for cmd in cmds:
            opcode, addr, value_or_cnt = cmd.split()
            addr = int(addr)
            match opcode:
                case "W":
                    self._ssd.write(int(addr), int(value_or_cnt, 16))
                case "E":
                    self._ssd.erase(int(addr), int(value_or_cnt))
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")

        self._make_initial_buffer()

    def _read_commands_buffer_txt(self) -> list[str]:
        commands = self._buffer_txt_path.read_text(encoding="utf-8").split("\n")
        return [cmd for cmd in commands if cmd]

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
