import unittest
import sys

sys.path.insert(1, "./utils")
from pdata import calc_table_size


class Test_Base(unittest.TestCase):
    def test_table_size_base(self):
        secrets = [0, 1]
        epsilon = 1
        table_size = calc_table_size(secrets, epsilon)

        self.assertEqual(table_size, 4)

    def test_table_size_odd(self):
        secrets = [0, 1, 3]
        epsilon = 1
        table_size = calc_table_size(secrets, epsilon)

        self.assertEqual(table_size, 8)


if __name__ == "__main__":
    unittest.main()
