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

    def _extract_addr_from_cmd(self, command):
        return int(command.split()[1])

    def _extract_size_from_cmd(self, command):
        return int(command.split()[2])

    def _extract_data_from_cmd(self, command):
        return int(command.split()[2], 16)

    def _extract_opcode_from_cmd(self, commands):
        return commands.split()[0]

    def _merge_write_cmd(self, later_cmd, older_cmd):
        older_addr = self._extract_addr_from_cmd(older_cmd)
        later_addr = self._extract_addr_from_cmd(later_cmd)
        if self._extract_opcode_from_cmd(later_cmd) == "E":
            later_size = self._extract_size_from_cmd(later_cmd)
        else:
            later_size = 1

        if later_addr <= older_addr < later_addr + later_size:
            return later_cmd, None

        return later_cmd, older_cmd

    def _merge_erase_cmd(self, later_cmd, older_cmd):
        older_addr = self._extract_addr_from_cmd(older_cmd)
        older_size = self._extract_size_from_cmd(older_cmd)
        later_addr = self._extract_addr_from_cmd(later_cmd)
        later_size = self._extract_size_from_cmd(later_cmd)

        if older_addr in range(
            later_addr, later_addr + later_size + 1
        ) or later_addr in range(older_addr, older_addr + older_size + 1):
            new_addr = min(older_addr, later_addr)
            new_size = max(older_addr + older_size, later_addr + later_size) - new_addr
            if new_size <= 10:
                return None, f"E {new_addr} {new_size}"

        return later_cmd, older_cmd

    def _split_erase_cmd(self, later_cmd, older_cmd):
        older_addr = self._extract_addr_from_cmd(older_cmd)
        older_size = self._extract_size_from_cmd(older_cmd)
        later_addr = self._extract_addr_from_cmd(later_cmd)

        if not (older_addr <= later_addr < older_addr + older_size):
            return later_cmd, None

        split_cmds = []
        j = list(range(older_addr, older_addr + older_size)).index(later_addr)
        if j == 0:
            split_cmds.append(f"E {older_addr + 1} {older_size - 1}")
        elif j == older_size:
            split_cmds.append(f"E {older_addr} {older_size - 1}")
        else:
            split_cmds.append(f"E {older_addr} {j}")
            split_cmds.append(f"E {later_addr + 1} {older_size - j - 1}")

        split_cmds.reverse()

        return later_cmd, split_cmds

    def _optimize_commands(self, commands: list[str]):
        i = len(commands) - 1

        while i >= 0:
            i_opcode = self._extract_opcode_from_cmd(commands[i])
            ref_commands = commands.copy()

            j = i - 1
            while j >= 0:
                j_opcode = self._extract_opcode_from_cmd(commands[j])
                # i is later, j is older
                if j_opcode == "W":
                    commands[i], _ = self._merge_write_cmd(commands[i], commands[j])
                    if _ is None:
                        commands.pop(j)
                        break

                if j_opcode == "E" and i_opcode == "E":
                    _, commands[j] = self._merge_erase_cmd(commands[i], commands[j])
                    if _ is None:
                        commands.pop(i)
                        break

                if j_opcode == "E" and i_opcode == "W":
                    commands[i], _ = self._split_erase_cmd(commands[i], commands[j])
                    if _ is not None:
                        commands.pop(j)
                        for __ in _:
                            commands.insert(j, __)
                        break

                j -= 1

            i = i - 1 if ref_commands == commands else (len(commands) - 1)
        return commands
