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

    def _merge_erase_commands(self, later_cmd, older_cmd):
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

    def _split_erase_commands(self, later_cmd, older_cmd):
        older_addr = self._extract_addr_from_cmd(older_cmd)
        later_addr = self._extract_addr_from_cmd(later_cmd)
        later_size = self._extract_size_from_cmd(later_cmd)

        cmds = []
        if later_addr <= older_addr < later_addr + later_size:
            cand = list(range(later_addr, later_addr + later_size))
            cand.remove(older_addr)

            i = 0
            for j in range(i + 1, len(cand)):
                if cand[j] - cand[j - 1] > 1:
                    size = cand[j - 1] - cand[i] + 1
                    cmds.append(f"E {cand[i]} {size}")
                    i = j

            # last one
            size = cand[-1] - cand[i] + 1
            cmds.append(f"E {cand[i]} {size}")
        else:
            cmds.append(later_cmd)

        cmds.reverse()

        return cmds

    def _optimize_commands(self, commands: list[str]):
        i = len(commands) - 1
        while i < len(commands):
            ref_commands = commands.copy()
            j = 0
            while j < i:
                # i is later, j is older
                if self._extract_opcode_from_cmd(commands[j]) == "W":
                    commands[i], commands[j] = self._merge_write_cmd(
                        commands[i], commands[j]
                    )

                if self._extract_opcode_from_cmd(commands[j]) == "E":
                    if self._extract_opcode_from_cmd(commands[i]) == "E":
                        commands[i], commands[j] = self._merge_erase_commands(
                            commands[i], commands[j]
                        )

                    if self._extract_opcode_from_cmd(commands[i]) == "W":
                        for _ in self._split_erase_commands(commands[i], commands[j]):
                            commands.insert(j, _)

                j += 1

            i = i + 1 if ref_commands == commands else 1
        return commands
