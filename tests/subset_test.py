import sys
import unittest
from picozk import *

sys.path.insert(1, "./apple_psi")
from helper import subset_test


class Test_Base(unittest.TestCase):
    def test_subset_test_pass(self):
        apple_secrets = [0, 1, 2]
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        curr_val = 1
        res = subset_test(apple_secrets, curr_val)
        self.assertEqual(val_of(res), 0)


if __name__ == "__main__":
    p = 11
    n = 2
    with PicoZKCompiler("picozk_test", field=[p, n]):
        unittest.main()
