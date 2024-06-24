import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from ssd.shell.api import ResultReader, Shell

api = Shell(ResultReader(Path(os.getcwd())))

test_value1 = "0xAAAABBBB"
test_value2 = "0x12345678"
target_lba = list(range(0, 6))

for _ in range(30):
    for lba in target_lba:
        api.write(lba, test_value1)

for lba in target_lba:
    api.write(lba, test_value2)

for lba in target_lba:
    if api.read(lba) != test_value2:
        sys.exit(1)

sys.exit(0)
