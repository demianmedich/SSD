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

        if not self._buffer_txt_path.exists():
            self._make_initial_buffer()

    def flush(self) -> None:
        cmds = self._read_commands_buffer_txt()
        for opcode, addr, value_or_cnt in [_.split(" ") for _ in cmds]:
            match opcode:
                case "W":
                    self._ssd.write(addr, data=value_or_cnt)
                case "E":
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
        changed, new_cmds = self._optimize_commands(cmds)

        if changed:
            with open(
                self._buffer_txt_path, mode="wt", encoding="utf-8", newline="\n"
            ) as f:
                f.writelines(f"{cmd}\n" for cmd in cmds)
        else:
            with open(
                self._buffer_txt_path, mode="a+", encoding="utf-8", newline="\n"
            ) as f:
                f.write(f"{cmd}\n")

        if len(cmds) > 9:
            self.flush()

    def _read_commands_buffer_txt(self) -> list[str]:
        cmds = self._buffer_txt_path.read_text(encoding="utf-8").split("\n")
        return [cmd for cmd in cmds if cmd]
        # return cmds

    def _make_initial_buffer(self):
        with open(self._buffer_txt_path, mode="w", encoding="utf-8", newline="\n"):
            pass

    def _optimize_commands(self, commands: list[str]):
        updated_commands = False

        i = len(commands) - 1
        while i > 0:
            changed = False

            j = 0
            while j < i:
                i_updated = False
                opcode = commands[i].split()[0]
                if opcode == "W":
                    i_updated = self.optimize_write_command(commands, i, j)
                else:
                    i_updated = self.optimize_erase_command(commands, i, j)

                if i_updated:
                    i = j
                    j = 0
                    changed = True
                else:
                    j += 1

            if changed:
                i = len(commands) - 1
                updated_commands = True
            else:
                i -= 1

        return updated_commands, commands

    def optimize_erase_command(self, commands, i, j):
        i_updated = False
        opcode, addr, value = commands[i].split()
        addr, value = int(addr), int(value)

        if commands[j].startswith("W"):
            _, write_addr, _ = commands[j].split()

            if addr <= write_addr < addr + value:
                i_updated = True
                del commands[j]

        elif commands[j].startswith("E"):
            _, erase_addr, erase_size = commands[j].split()
            erase_addr, erase_size = int(erase_addr), int(erase_size)
            if (
                erase_addr <= addr <= erase_addr + erase_size
                or erase_addr <= addr + value <= erase_addr + erase_size
            ):

                min_addr = min(addr, erase_addr)
                max_addr = min(addr + value, erase_addr + erase_size)
                if max_addr - min_addr <= 10:
                    i_updated = True
                    commands[i] = "E {min_addr} {max_addr - min_addr}"
        return i_updated

    def optimize_write_command(self, commands, i, j):
        opcode, addr, value = commands[i].split()
        addr, value = int(addr), int(value)

        i_updated = False
        if commands[j].startswith(f"W {addr}"):
            i_updated = True
            del commands[j]
        elif commands[j].startswith("E"):
            _, erase_addr, erase_size = commands[j].split()
            erase_addr, erase_size = int(erase_addr), int(erase_size)
            if erase_addr <= addr < erase_addr + erase_size:
                i_updated = True
                del commands[j]
                if erase_addr + erase_size != addr + 1:
                    commands.insert(
                        j,
                        f"E {addr + 1} {erase_addr + erase_size - addr - 1}",
                    )
                if addr != erase_addr:
                    commands.insert(j, f"E {addr} {addr - erase_addr}")
        return i_updated
