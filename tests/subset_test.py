import unittest
from picozk import *


def subset_test(apple_secrets, curr_val):
    final_state = 0
    curr_state = 1
    for i in range(len(apple_secrets)):
        curr_state = mux(
            curr_state == final_state,
            curr_state,
            mux(apple_secrets[i] == curr_val, final_state, curr_state),
        )
    assert0(curr_state)
    return curr_state


class Test_Base(unittest.TestCase):
    def test_subset_test_pass(self):
        apple_secrets = [0, 1, 2]
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        curr_val = 1
        res = subset_test(apple_secrets, curr_val)
        self.assertEqual(val_of(res), 0)

    def test_subset_test_fail(self):
        apple_secrets = [0, 2, 3]
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        curr_val = 1
        res = subset_test(apple_secrets, curr_val)
        self.assertNotEqual(val_of(res), 0)


if __name__ == "__main__":
    p = 11
    n = 2
    with PicoZKCompiler("picozk_test", field=[p, n]):
        unittest.main()
