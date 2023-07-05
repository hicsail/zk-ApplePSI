import unittest
import sys
sys.path.insert(1, './utils')
from interpolation import lagrange_polynomial

class TestInterpolation(unittest.TestCase):
    def test_interpolation(self):
        xs = [0, 1, 2]
        ys = [0, 1, 8]
        poly = lagrange_polynomial(xs, ys)
        test_input = [0, 1, 2]
        res = []
        for t in test_input:
            p = poly.subs('x', t)
            res.append(p)
        exp_res = [0, 1, 8]
        self.assertEqual(res, exp_res)

if __name__ == '__main__':
    unittest.main()
