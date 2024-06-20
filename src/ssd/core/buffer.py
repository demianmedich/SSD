from pathlib import Path

from ssd.core.base import SSDInterface

NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"


class CommandBuffer:
    def __init__(self, ssd: SSDInterface, rootdir: str | Path = Path.cwd()):
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
        changed = False
        for i in range(len(commands)):
            if commands[i].startswith("W"):
                _, addr, value = commands[i].split()

                for j in range(i + 1, len(commands)):
                    if commands[j].startswith(f"W {addr}"):
                        changed = True
                    elif commands[j].startswith("E"):
                        _, erase_addr, erase_size = commands[j].split()
                        if erase_addr <= addr < erase_addr + erase_size:
                            changed = True
                    else:
                        break
                    if changed:
                        del commands[i]
                        i = j
            else:
                _, addr, size = commands[i].split()
                for j in range(i + 1, len(commands)):
                    if commands[j].startswith("W"):
                        _, write_addr, write_value = commands[j].split()
                        if addr <= write_addr < addr + size:
                            changed = True
                            del commands[i]
                            commands.insert(i, f"E {addr} {write_addr - addr}")
                            commands.insert(
                                i + 1,
                                f"E {write_addr + 1} {addr + size - write_addr - 1}",
                            )
                            break
                    elif commands[j].startswith("E"):
                        _, erase_addr, erase_size = commands[j].split()
                        if (
                            erase_addr <= addr < erase_addr + erase_size
                            or erase_addr <= addr + size <= erase_addr + erase_size
                        ):
                            changed = True
                            """ing"""

        return changed
