from picozk import *
import ecdsa
from random import randrange
from ecdsa import numbertheory
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation
import random

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
    sig_r = SecretInt(sig.r, field=n)
    sig_s = SecretInt(sig.s, field=n)
    secret_h = SecretInt(h, field=n)
    result, xy = verify(sig_r, sig_s, secret_h, pubkey, p)
    assert0(result)
    return xy

def select_group_elem(non_empty:list, n):
    random_elems = random.sample(non_empty, n)
    res_elems =[]
    for el in random_elems:
        res_elems.append(el[1])
    return res_elems

# Instantiate EC: Curve & generator parameters
g = ecdsa.ecdsa.generator_secp256k1
p = g.curve().p()
n = g.order()


# User input
num_elem = 2
secrets = [randrange( 1, n ) for _ in range(num_elem)]
print("secrets", secrets)
print("")


with PicoZKCompiler('picozk_test', field=[p,n]):
    
    # TODO: v2 Change secrets into SecretInt


    # Make a Cuckoo table
    size_factor = 0.7
    cuckoo_table = CuckooTable(secrets, size_factor, p)
    empty = cuckoo_table.get_empty_indices()
    non_empty = cuckoo_table.get_non_empty_indices() 

    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    for i in range(len(non_empty)):
        idx, val = non_empty[i]
        map_elem = map_on_eliptic(val, g, p, n)
        cuckoo_table.replace_at(idx, map_elem)
        cuckoo_table.set_non_emplist(i, (idx, map_elem))


    # Make bots by polynomial interpolation
    for i in range(len(empty)):
        bot_idx = empty[i]
        num_elems=2 # The number of elements to iterpolate with
        random_elems = select_group_elem(non_empty, num_elems)
        bot_elem = lagrange_interpolation(random_elems, 0, p)
        cuckoo_table.replace_at(bot_idx, bot_elem)

    print("Resulting Table")
    print(cuckoo_table.get_table())

    # TODO: v2 verify cuckoo table process
