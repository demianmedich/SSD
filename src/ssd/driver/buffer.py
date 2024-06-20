from pathlib import Path

from ssd.driver.base import SSDInterface

NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"


class CommandBuffer:
    def __init__(self, ssd: SSDInterface, rootdir: str | Path = Path.cwd()):
        rootdir = Path(rootdir)
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
                    self._ssd.erase(addr, value_or_cnt)
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")

    def read(self, requested_address: int) -> str:
        if requested_address < 0 or requested_address >= 100:
            raise ValueError(f"Invalid address {requested_address}")

        for cmd in self._read_commands_buffer_txt():
            opcode, address, value_or_cnt = cmd.split()

            if int(address) == requested_address:
                match opcode:
                    case "W":
                        return value_or_cnt
                    case "E":
                        return "0x00000000"
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
                self._buffer_txt_path, mode="r+", encoding="utf-8", newline="\n"
            ) as f:
                f.write(f"{cmd}\n")

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
