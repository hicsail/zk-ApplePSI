from picozk import *
from dataclasses import dataclass


@dataclass
class CurvePoint:
    is_infinity: BooleanWire
    x: ArithmeticWire
    y: ArithmeticWire
    p: int

    # Mux for a curve point
    def mux(self, cond, other):
        return CurvePoint(
            mux_bool(cond, self.is_infinity, other.is_infinity),
            mux(cond, self.x, other.x),
            mux(cond, self.y, other.y),
            self.p,
        )

    # Point doubling
    def double(self):
        a = 0
        m = ((3 * (self.x * self.x) + a) * modular_inverse(2 * self.y, self.p)) % self.p

        x3 = (m * m - (2 * self.x)) % self.p
        y3 = (self.y + m * (x3 - self.x)) % self.p
        return CurvePoint(self.is_infinity, x3, y3, self.p)

    # Point addition (self != other)
    def add_nonequal(self, other):
        assert isinstance(other, CurvePoint)
        assert val_of(self.x) != val_of(other.x) or val_of(self.y) != val_of(other.y)

        l = ((other.y - self.y) * modular_inverse(other.x - self.x, self.p)) % self.p
        x3 = l*l - self.x - other.x
        y3 = l * (self.x - x3) - self.y
        return self.mux(other.is_infinity,
                        other.mux(self.is_infinity,
                                  CurvePoint(False, x3 % self.p, y3 % self.p, self.p)))

    # Point addition (general)
    def add(self, other):
        assert isinstance(other, CurvePoint)

        # case 1: self == other
        case1_cond = (self.x == other.x) & (self.y == other.y)
        case1_point = self.double()

        # case 2: self != other
        case2_cond = ~case1_cond
        x_diff = mux(case1_cond, 1, other.x - self.x)
        l = ((other.y - self.y) * modular_inverse(x_diff, self.p)) % self.p
        x3 = l*l - self.x - other.x
        y3 = l * (self.x - x3) - self.y
        case2_point = CurvePoint(False, x3 % self.p, y3 % self.p, self.p)

        return self.mux(other.is_infinity,
                        other.mux(self.is_infinity,
                                  case1_point.mux(case1_cond, case2_point)))

    # Point scaling by a scalar via repeated doubling
    def scale(self, s):
        assert not val_of(self.is_infinity)

        if isinstance(s, ArithmeticWire):
            bits = s.to_binary()
            res = CurvePoint(True, 0, 0, self.p)
            temp = self
            for b in reversed(bits.wires):
                res = temp.add_nonequal(res).mux(b.to_bool(), res)
                temp = temp.double()
            return res
        elif isinstance(s, int):
            bits = util.encode_int(s, s)
            res = CurvePoint(True, 0, 0, self.p)
            temp = self
            for b in reversed(bits):
                if b:
                    res = temp.add_nonequal(res)
                temp = temp.double()
            return res
        else:
            raise Exception('Unsupported exponent:', s)