import os
import unittest


class SSDTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_is_exist_nand_txt(self):
        if not os.path.exists("nand.txt"):
            with self.assertRaises(Exception):
                with open("nand.txt", "r") as f:
                    pass


if __name__ == "__main__":
    unittest.main()
