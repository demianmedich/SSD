import os
import sys
from pathlib import Path

from ssd.shell.api import ResultReader, Shell

sys.path.append(str(Path(__file__).parent.parent))

api = Shell(ResultReader(Path(os.getcwd())))
default_value = "0x00000000"
test_value = "0x1234567A"
api.fullwrite(test_value)
data = api.fullread()

for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

api.erase(10, 4)
api.erase(40, 5)
api.write(12, "0xABCD1234")
api.write(13, "0x4BCD1234")
data = api.read(13)
if data != "0x4BCD1234":
    sys.exit(1)

api.erase(50, 1)
api.erase(40, 5)
api.write(50, "0x4BCD1234")
data = api.read(50)
if data != "0x4BCD1234":
    sys.exit(1)

sys.exit(0)
