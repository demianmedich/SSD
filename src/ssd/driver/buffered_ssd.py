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
        opcode, value_or_cnt = self._check_in_buffer(addr)
        if opcode == "E":
            self._result_txt_path.write_text("0x00000000")
            return
        if opcode == "W":
            self._result_txt_path.write_text(value_or_cnt)
            return

        self._ssd.read(addr)
        return

    def write(self, addr: int, data: int):
        self._buffer_command(f"W {addr} 0x{data:08X}")

    def erase(self, addr: int, size: int):
        self._buffer_command(f"E {addr} {size}")

    def _check_in_buffer(self, ref_addr):
        for _ in self._read_commands_buffer_txt()[::-1]:
            opcode = self._extract_opcode_from_cmd(_)
            if opcode == "W" and ref_addr == self._extract_addr_from_cmd(_):
                return opcode, self._extract_data_from_cmd(_)
            if opcode == "E" and ref_addr in self._extract_range_from_cmd(_):
                return opcode, 0
        return None, None

    def _buffer_command(self, cmd):
        commands = self._read_commands_buffer_txt()
        commands.append(cmd)
        commands = self._optimize_commands(commands)

        with open(
            self._buffer_txt_path, mode="wt", encoding="utf-8", newline="\n"
        ) as f:
            f.writelines(f"{cmd}\n" for cmd in self._optimize_commands(commands))

        if len(commands) > 10:
            self.flush()

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

    def _extract_range_from_cmd(self, cmd):
        return range(
            self._extract_addr_from_cmd(cmd),
            self._extract_addr_from_cmd(cmd) + self._extract_size_from_cmd(cmd),
        )

    def _extract_addr_from_cmd(self, command):
        return int(command.split()[1])

    def _extract_size_from_cmd(self, command):
        return int(command.split()[2])

    def _extract_data_from_cmd(self, command):
        return command.split()[2]

    def _extract_opcode_from_cmd(self, command):
        return command.split()[0]

    def _merge_write_cmd(self, later_cmd, older_cmd):
        older_addr = self._extract_addr_from_cmd(older_cmd)
        later_addr = self._extract_addr_from_cmd(later_cmd)
        if self._extract_opcode_from_cmd(later_cmd) == "E":
            later_size = self._extract_size_from_cmd(later_cmd)
        else:
            later_size = 1

        if later_addr <= older_addr < later_addr + later_size:
            older_cmd = None

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
                later_cmd = None
                older_cmd = f"E {new_addr} {new_size}"
            else:
                older_cmd = f"E {new_addr} 10"
                later_cmd = f"E {new_addr+10} {new_size-10}"

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
        elif j == older_size - 1:
            split_cmds.append(f"E {older_addr} {older_size - 1}")
        else:
            split_cmds.append(f"E {older_addr} {j}")
            split_cmds.append(f"E {later_addr + 1} {older_size - j - 1}")

        split_cmds = [_ for _ in split_cmds if split_cmds[-1] if int(_.split()[-1]) > 0]
        split_cmds.reverse()

        return later_cmd, split_cmds

    def _optimize_commands(self, commands: list[str]):
        later_idx = len(commands) - 1

        while later_idx >= 0:
            later_opcode = self._extract_opcode_from_cmd(commands[later_idx])
            ref_commands = commands.copy()

            older_idx = later_idx - 1
            while older_idx >= 0:
                older_opcode = self._extract_opcode_from_cmd(commands[older_idx])
                if older_opcode == "W":
                    commands[later_idx], _ = self._merge_write_cmd(
                        commands[later_idx], commands[older_idx]
                    )
                    if _ is None:
                        commands.pop(older_idx)
                        break

                if older_opcode == "E" and later_opcode == "E":
                    _, commands[older_idx] = self._merge_erase_cmd(
                        commands[later_idx], commands[older_idx]
                    )
                    if _ is None:
                        commands.pop(later_idx)
                        break
                    else:
                        commands[later_idx] = _

                if older_opcode == "E" and later_opcode == "W":
                    commands[later_idx], _ = self._split_erase_cmd(
                        commands[later_idx], commands[older_idx]
                    )
                    if _ is not None:
                        commands.pop(older_idx)
                        for __ in _:
                            commands.insert(older_idx, __)
                        break

                older_idx -= 1

            later_idx = (
                (later_idx - 1) if ref_commands == commands else (len(commands) - 1)
            )
        return commands
