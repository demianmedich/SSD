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

    def _merge_erase_commands(self, cmd1, cmd2):
        # cmd1 is older erase cmd, cmd2 is later erase cmd
        o_addr = self._extract_addr_from_cmd(cmd1)
        o_size = self._extract_size_from_cmd(cmd1)
        l_addr = self._extract_addr_from_cmd(cmd2)
        l_size = self._extract_size_from_cmd(cmd2)

        if l_addr in range(o_addr, o_addr + o_size + 1) or o_addr in range(
            l_addr, l_addr + l_size + 1
        ):
            new_addr = min(l_addr, o_addr)
            new_size = max(l_addr + l_size, o_addr + o_size) - new_addr
            if new_size <= 10:
                return f"E {new_addr} {new_size}", None

        return cmd1, cmd2

    def _split_erase_commands(self, cmd1, cmd2):
        # cmd1 is older erase cmd, cmd2 is later write cmd
        o_addr = self._extract_addr_from_cmd(cmd1)
        o_size = self._extract_size_from_cmd(cmd1)
        l_addr = self._extract_addr_from_cmd(cmd2)

        cmds = []
        if o_addr <= l_addr < o_addr + o_size:
            cand = list(range(o_addr, o_addr + o_size))
            cand.remove(l_addr)

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
            cmds.append(cmd1)
        cmds.reverse()
        return cmds

    def _optimize_commands(self, commands: list[str]):
        i = len(commands) - 1
        while i < len(commands):
            j = 0
            while j < i:
                if self._extract_opcode_from_cmd(commands[i]) == "W":
                    i_addr = self._extract_addr_from_cmd(commands[i])

                    if self._extract_opcode_from_cmd(commands[j]) == "W":
                        addr = self._extract_addr_from_cmd(commands[j])
                        if addr == i_addr:
                            del commands[i]
                            i = 0

                    if self._extract_opcode_from_cmd(commands[j]) == "E":
                        addr = self._extract_addr_from_cmd(commands[j])
                        size = self._extract_size_from_cmd(commands[j])
                        if addr <= i_addr < addr + size:
                            del commands[i]
                            i = 0

                if self._extract_opcode_from_cmd(commands[i]) == "E":
                    if self._extract_opcode_from_cmd(commands[j]) == "E":
                        commands[i], commands[j] = self._merge_erase_commands(
                            commands[i], commands[j]
                        )

                    if self._extract_opcode_from_cmd(commands[j]) == "W":
                        for _ in self._split_erase_commands(commands[i], commands[j]):
                            commands.insert(i, _)

            i += 1
        return commands
