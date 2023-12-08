from picozk import *
from picozk.util import encode_int
from ecdsa import SECP256k1
from curvepoint import CurvePoint

p = SECP256k1.curve.p()  # p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
n = SECP256k1.order
with PicoZKCompiler("irs/picozk_test", field=[p, n]):
    
    sec_s = SecretInt(5)
    sec_bits = sec_s.to_binary()
    
    int_s = 5
    int_bits = encode_int(int_s, p)

    assert len(sec_bits.wires) == len(int_bits)
    # print(sec_bits.wires, int_bits)

    s_res = CurvePoint(False, 10, 20, p)
    res = CurvePoint(False, 10, 20, p)
    
    s = s_res.scale(sec_s)
    i = res.scale(int_s)

    assert val_of(s.x) == i.x
    assert val_of(s.y) == i.y