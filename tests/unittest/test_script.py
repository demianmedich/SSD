import unittest
from unittest.mock import Mock


class TestScriptTestCase(unittest.TestCase):
    def fullwrite_side_effect(self, value):
        for lba in range(100):
            self.shell.write(lba, value)

    def fullread_side_effect(self):
        return [self.shell.read(lba) for lba in range(100)]

    def test_testapp1(self):
        self.shell = Mock()
        self.shell.fullwrite.side_effect = self.fullwrite_side_effect("0x00000000")
        self.shell.fullread.side_effect = self.fullread_side_effect()
        self.shell.fullwrite("0x00000000")
        self.shell.fullread()

    def test_testapp2(self):
        self.shell = Mock()
        self.shell.fullwrite.side_effect = self.fullwrite_side_effect("0x00000000")
        self.shell.fullread.side_effect = self.fullread_side_effect()
        for _ in range(30):
            for lba in range(6):
                self.shell.write(lba, "0xAAAABBBB")
        for lba in range(6):
            self.shell.write(lba, "0x12345678")

        self.shell.read.return_value = "0x12345678"
        for lba in range(6):
            self.assertEqual(self.shell.read(lba), "0x12345678")


if __name__ == "__main__":
    unittest.main()
