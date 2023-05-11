from picozk import *
import ecdsa
from random import randrange
from ecdsa import numbertheory
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation

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
    return x_n - r, xy

# Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
def map_on_eliptic(secret, g, p, n):

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
        result, xy = verify(sig_r, sig_s, secret_h, pubkey, p)
        assert0(result)
    return xy


# Instantiate EC: Curve & generator parameters
g = ecdsa.ecdsa.generator_secp256k1
p = g.curve().p()
n = g.order()


# User input
num_elem = 2
secrets = [randrange( 1, n ) for _ in range(num_elem)]
print("secrets", secrets)
print("")

# TODO: v2 Change secrets into SecretInt


# Make a Cuckoo table
size_factor = 0.7
cuckoo_table = CuckooTable(secrets, size_factor)
empty = cuckoo_table.get_empty_indices()
non_empty = cuckoo_table.get_non_empty_indices() 

# Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
for i in range(len(non_empty)):
    idx, val = non_empty[i]
    map_elem = map_on_eliptic(val, g, p, n)
    cuckoo_table.replace_at(idx, map_elem)
    cuckoo_table.set_non_emplist(i, (idx, map_elem))


# TODO: v1 Make bots by polynomial interpolation
print("First")
print(non_empty[0][1].x)
print("")

print("Second")
print(non_empty[1][1].x)
print("")

print("Addition")
print(non_empty[0][1].x-non_empty[1][1].x)


# res = lagrange_interpolation([non_empty[0][1], non_empty[1][1]], 0, p)
# print("")
# print("")
# print("res", res)

# TODO: v2 verify cuckoo table process
