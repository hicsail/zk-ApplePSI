import unittest
import sys
from ecdsa import SECP256k1

sys.path.insert(1, "./apple_psi")
from cuckoo_table import CuckooTable


class ModifiedCuckooTable(CuckooTable):
    def __init__(self, secrets: list, table_size: int, p):
        super().__init__(secrets, table_size, p)

    def hash_one(self, item):
        return item % self.table_size

    def hash_two(self, item):
        return (1 + item) % self.table_size


class Test_Base(unittest.TestCase):
    def test_eviction(self):
        secrets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        table_size = len(secrets) - 1
        p = SECP256k1.curve.p()
        cuckoo_table = ModifiedCuckooTable(secrets, table_size, p)
        print("Result:", cuckoo_table.table)
        self.assertEqual(cuckoo_table.table, [9, 0, 11, 2, 3, 4, 5, 6, 7, 8])


if __name__ == "__main__":
    unittest.main()
