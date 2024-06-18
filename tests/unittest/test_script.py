import unittest
from unittest.mock import Mock


class TestScriptTestCase(unittest.TestCase):
    def setUp(self):
        self.shell = Mock()

        def fullwrite_side_effect(value):
            for lba in range(100):
                self.shell.write(lba, value)

        def fullread_side_effect():
            return [self.shell.read(lba) for lba in range(100)]

        self.shell.fullwrite.side_effect = fullwrite_side_effect
        self.shell.fullread.side_effect = fullread_side_effect

    def test_testapp1(self):
        self.shell.fullwrite("0x00000000")
        self.shell.fullwrite.assert_called_once()
        self.shell.fullwrite.assert_called_once_with("0x00000000")

        self.shell.fullread()
        self.shell.fullread.assert_called_once()
        self.assertEqual(self.shell.read.call_count, 100)

    def test_testapp2(self):
        for _ in range(30):
            for lba in range(6):
                self.shell.write(lba, "0xAAAABBBB")
        for lba in range(6):
            self.shell.write(lba, "0x12345678")
        self.assertEqual(self.shell.write.call_count, 186)

        self.shell.read.return_value = "0x12345678"
        for lba in range(6):
            self.assertEqual(self.shell.read(lba), "0x12345678")
        self.assertEqual(self.shell.read.call_count, 6)


if __name__ == "__main__":
    unittest.main()
