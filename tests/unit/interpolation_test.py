import unittest
import sys
sys.path.insert(1, './utils')
from interpolation import lagrange_interpolation
from curvepoint import CurvePoint

class TestInterpolation(unittest.TestCase):
    def test_interpolation(self):
        p=57287
        first = CurvePoint(False, 10, 130, p)
        second = CurvePoint(False, 30, -50, p)
        result = lagrange_interpolation([first, second], 0, p)
        exp_y=220
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, exp_y)

if __name__ == '__main__':
    unittest.main()
