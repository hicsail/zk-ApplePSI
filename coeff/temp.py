from picozk import *
from picozk.util import encode_int
from ecdsa import SECP256k1
from curvepoint import CurvePoint
import ecdsa

g = ecdsa.ecdsa.generator_secp256k1
p = SECP256k1.curve.p()  # p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
n = SECP256k1.order

a = 10
b = 1
d = 4

print('\n ex1...')
test = CurvePoint(is_infinity=False, x=g.x(), y=g.y(), p=p)
agg = int((a-b)/d)    
res_test = test.scale(agg)
print('\n ex1 result: ', res_test)


print('\n ex2...')
test = CurvePoint(is_infinity=False, x=g.x(), y=g.y(), p=p)
_d = modular_inverse(d, p)
_agg = (a-b)*_d
_res_test = test.scale(_agg)
print('\n ex2 result: ', _res_test)

print('\n ex3...')
__agg = (a-b)
_num_test = test.scale(__agg)
_denom_test = test.scale(_d)
__res_test = _num_test.add(_denom_test)
print('\n ex3 result: ', __res_test)

print('\n ex4...')
_num_test = test.scale(__agg)
print('\n ex4 result: ', _num_test) 

_b = p-b
first = test.scale(a)
combined = first.scale(_b)
print('\n combined result: ', combined)

assert __res_test.x == _res_test.x and __res_test.y == _res_test.y