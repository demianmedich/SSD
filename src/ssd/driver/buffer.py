from pathlib import Path

from ssd.driver.base import SSDInterface

NAND_FILE = "nand.txt"
BUFFER_TXT = "buffer.txt"


class CommandBuffer:
    def __init__(self, ssd: SSDInterface, rootdir: str | Path = Path.cwd()):
        rootdir = Path(rootdir)
        self._buffer_txt_path = rootdir / BUFFER_TXT
        self._ssd = ssd

        if not self._buffer_txt_path.exists():
            self._make_initial_buffer()

    def flush(self) -> None:
        cmds = self._read_commands_buffer_txt()
        for opcode, addr, value_or_cnt in [_.split(" ") for _ in cmds]:
            match opcode:
                case "W":
                    self._ssd.write(addr, data=value_or_cnt)
                case "E":
                    self._ssd.erase(addr, value_or_cnt)
                case _:
                    raise ValueError(f"Invalid opcode {opcode}")
                    self._ssd.erase(addr, size=value_or_cnt)
                # case _:
                #     raise ValueError(f"Invalid opcode {opcode}")
        self._make_initial_buffer()

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
        cmds = self._read_commands_buffer_txt()
        cmds.append(cmd)
        new_cmds = self._optimize_commands(cmds)

        with open(
            self._buffer_txt_path, mode="wt", encoding="utf-8", newline="\n"
        ) as f:
            f.writelines(f"{cmd}\n" for cmd in new_cmds)

        if len(cmds) > 9:
            self.flush()

    def _read_commands_buffer_txt(self) -> list[str]:
        cmds = self._buffer_txt_path.read_text(encoding="utf-8").split("\n")
        return [cmd for cmd in cmds if cmd]

    def _make_initial_buffer(self):
        with open(self._buffer_txt_path, mode="w", encoding="utf-8", newline="\n"):
            pass

    def _merge_erase_commands(self, cmd1, cmd2):
        addr1, size1 = (int(_) for _ in cmd1.split()[1:])
        addr2, size2 = (int(_) for _ in cmd2.split()[1:])
        return f"E {min(addr1, addr2)} {max(addr1 + size1, addr2 + size2) - min(addr1, addr2)}"

    def _split_erase_commands(self, cand: list):
        cmds = []
        if not cand:
            return cmds
        if len(cand) == 1:
            cmds = f"E {cand[0]} 1"
            return cmds

        i = 0
        for j in range(i + 1, len(cand)):
            if cand[j] - cand[j - 1] > 1:
                size = cand[j - 1] - cand[i] + 1
                cmds.append(f"E {cand[i]} {size}")
                i = j

        size = cand[-1] - cand[i] + 1
        cmds.append(f"E {cand[i]} {size}")

        return cmds

    def _optimize_commands(self, commands: list[str]):
        updated_commands = False

        i = len(commands) - 1
        while i > 0:
            j = 0
            while j < i:
                if commands[i].startswith("E"):
                    _, addr, size = self._extract_opcode_addr_size_erase(commands[i])
                    if commands[j].startswith("E"):
                        _, ref_addr, ref_size = self._extract_opcode_addr_size_erase(
                            commands[j]
                        )
                        if (ref_addr <= addr <= ref_addr + ref_size) or (
                            addr <= ref_addr <= addr + size
                        ):
                            if (
                                max(addr + size, ref_addr + ref_size)
                                - min(addr, ref_addr)
                                <= 10
                            ):
                                commands[j] = self._merge_erase_commands(
                                    commands[i], commands[j]
                                )
                                del commands[i]
                                i = 0

                    if commands[j].startswith("W"):
                        _, write_addr, _ = self._extract_opcode_addr_size_write(
                            commands[j]
                        )

                        if addr <= write_addr < addr + size:
                            candidate = list(range(addr, addr + size))
                            candidate.remove(write_addr)
                            del commands[j]
                            for _ in self._split_erase_commands(candidate)[::-1]:
                                commands.insert(j, _)
                            i = 0

                if commands[i].startswith("W"):
                    _, addr, data = self._extract_opcode_addr_size_write(commands[i])
                    if commands[j].startswith(f"W {addr}"):
                        del commands[j]

                    elif commands[j].startswith("E"):
                        _, erase_addr, erase_size = (
                            self._extract_opcode_addr_size_write(commands[j])
                        )
                        if erase_addr <= addr < erase_addr + erase_size:
                            candidate = list(range(erase_addr, erase_addr + erase_size))
                            candidate.remove(addr)
                            del commands[j]

                            for _ in self._split_erase_commands(candidate)[::-1]:
                                commands.insert(j, _)
                            i = 0

        return commands

    def _extract_opcode_addr_size_erase(self, command):
        opcode = command.split()[0]
        addr = int(command.split()[1])
        size = int(command.split()[2])
        return opcode, addr, size

    def _extract_opcode_addr_size_write(self, command):
        opcode = command.split()[0]
        addr = int(command.split()[1])
        data = int(command.split()[2], 16)
        return opcode, addr, data
