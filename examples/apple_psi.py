from picozk import *
import ecdsa
from random import randrange
from ecdsa import numbertheory
from dataclasses import dataclass
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable

@dataclass
class CurvePoint:
    is_infinity: BooleanWire
    x: ArithmeticWire
    y: ArithmeticWire
    p: int

    # Mux for a curve point
    def mux(self, cond, other):
        return CurvePoint(mux_bool(cond, self.is_infinity, other.is_infinity),
                          mux(cond, self.x, other.x),
                          mux(cond, self.y, other.y), self.p)

    # Point doubling
    def double(self):
        a = 0
        l = ((3*(self.x*self.x) + a) * modular_inverse(2*self.y, self.p)) % self.p

        x3 = (l * l) - (2 * self.x)
        y3 = (l * (self.x - x3) - self.y)
        return CurvePoint(self.is_infinity, x3 % self.p, y3 % self.p, self.p)

    # Point addition
    def add(self, other):
        assert isinstance(other, CurvePoint)
        assert val_of(self.is_infinity) == False
        assert val_of(self.x) != val_of(other.x) or val_of(self.y) != val_of(other.y)
        l = ((other.y - self.y) * modular_inverse(other.x - self.x, self.p)) % self.p
        x3 = l*l - self.x - other.x
        y3 = l * (self.x - x3) - self.y
        return self.mux(other.is_infinity, CurvePoint(False, x3 % self.p, y3 % self.p, self.p))

    # Point scaling by a scalar via repeated doubling
    def scale(self, s):
        bits = s.to_binary()
        res = CurvePoint(True, 0, 0, self.p)
        temp = self
        for b in reversed(bits.wires):
            res = temp.add(res).mux(b.to_bool(), res)
            temp = temp.double()
        return res

# Verify the ECDSA signature represented by (r, s)
def verify(r, s, hash_val, pubkey, p):
    c = modular_inverse(s, n)
    u1 = hash_val * c
    u2 = r * c

    u1_p = u1.to_binary().to_arithmetic(field=p)
    u2_p = u2.to_binary().to_arithmetic(field=p)

    sg = CurvePoint(False, g.x(), g.y(), p)
    spk = CurvePoint(False, pubkey.point.x(), pubkey.point.y(), p)

    xy1 = sg.scale(u1_p)
    xy2 = spk.scale(u2_p)
    xy = xy1.add(xy2)
    x_n = xy.x.to_binary().to_arithmetic(field=n)

    return x_n - r

# Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
def map_on_eliptic(secret, g):
    # Curve & generator parameters
    p = g.curve().p()
    n = g.order()

    # Generate secret & public keys
    pubkey = ecdsa.ecdsa.Public_key( g, g * secret )
    privkey = ecdsa.ecdsa.Private_key( pubkey, secret )

    # Sign a hash value
    h = 13874918263
    sig = privkey.sign(h, randrange(1,n))

    # Secret signature, secret hash value; public pubkey
    with PicoZKCompiler('picozk_test', field=[p,n]):

        sig_r = SecretInt(sig.r, field=n)
        sig_s = SecretInt(sig.s, field=n)
        secret_h = SecretInt(h, field=n)
        result = verify(sig_r, sig_s, secret_h, pubkey, p)
        assert0(result)
    return sig


# Instantiate EC
g = ecdsa.ecdsa.generator_secp256k1
n = g.order()


# User input
num_elem = 3
secrets = [randrange( 1, n ) for _ in range(num_elem)]


# TODO: v2 Change secrets into SecretInt


# Make a Cuckoo table
size_factor = 0.7
cuckoo_table = CuckooTable(secrets, size_factor)
print("secret", secrets)
print("cuckoo_table", cuckoo_table.get_table())
empty = cuckoo_table.get_empty_indices()
non_empty = cuckoo_table.get_non_empty_indices()


# TODO: v0  Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
for idx, val in non_empty:
    map_elem = map_on_eliptic(val, g)
    cuckoo_table.replace_at(idx, map_elem)


# TODO: v1 Make bots by polynomial interpolation


# TODO: v1 verify cuckoo table process
