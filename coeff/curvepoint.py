from picozk import *
from dataclasses import dataclass
from picozk.util import encode_int


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

    # Point addition
    def add(self, other):
        assert isinstance(other, CurvePoint)
        assert val_of(self.x) != val_of(other.x) or val_of(self.y) != val_of(other.y)
        m = ((self.y - other.y) * modular_inverse(self.x - other.x, self.p)) % self.p
        x3 = (m * m - self.x - other.x) % self.p
        y3 = (self.y + m * (x3 - self.x)) % self.p
        return self.mux(
            other.is_infinity,
            other.mux(
                self.is_infinity, CurvePoint(False, x3, y3, self.p)
            ),
        )

    # Point scaling by a scalar via repeated doubling
    def scale(self, s):
        
        if self.is_infinity == True:
            return self
        if isinstance(s, ArithmeticWire):
            bits = s.to_binary()
            res = CurvePoint(True, 0, 0, self.p)
            temp = self
            for b in reversed(bits.wires):
                res = temp.add(res).mux(b.to_bool(), res)
                temp = temp.double()
            return res
        elif isinstance(s, int):
            bits = encode_int(s, s)
            res = CurvePoint(True, 0, 0, self.p)
            temp = self
            for b in reversed(bits):
                if b:
                    res = temp.add(res)
                temp = temp.double()
            return res
        else:
            raise Exception("Unsupported exponent:", s)
