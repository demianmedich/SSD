"""
    빠른 동작 검증 위한 Dummy Test Script 입니다
"""

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from ssd.shell import ReadResultAccessor, Shell  # noqa

api = Shell(ReadResultAccessor(Path(os.getcwd())))

target_address = 0
value = "0x19930516"
api.write(target_address, value)

read_result = api.read(target_address)  # Todo: Runner로 돌리면 얘도 출력하지 말아야
print(f"나는 Runner로 돌리면 출력되지 않고, Shell로 돌리면 출력되어야 한다.")
print(f"{read_result = }")


if read_result == value:
    sys.exit(0)
else:
    sys.exit(1)
