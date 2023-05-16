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

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret

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
    assert0(x_n - r)
    return xy

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
    xy = verify(sig_r, sig_s, secret_h, pubkey, p)
    return xy

# Instantiate EC: Curve & generator parameters
g = ecdsa.ecdsa.generator_secp256k1
p = g.curve().p()
n = g.order()

with PicoZKCompiler('picozk_test', field=[p,n]):

    # User input
    num_elem = 2
    secrets = remove_duplicates([randrange( 1, n ) for _ in range(num_elem)])
    print("secrets", secrets)
    
    # Make a Cuckoo table
    size_factor = 2
    cuckoo_table = CuckooTable(secrets, size_factor, p)

    #TODO: v2 ZK proof for the hash functions
    # cuckoo_table.verify_hash()


    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_empty = cuckoo_table.get_non_empty_indices()
    print("non_empty", non_empty)
    for i in range(len(non_empty)):
        idx, val = non_empty[i]
        print("idx val", idx, val)
        map_elem = map_on_eliptic(val, g, p, n)
        cuckoo_table.replace_at(idx, map_elem)
        cuckoo_table.set_non_emplist(i, (idx, map_elem))
    
    
    non_empty = cuckoo_table.get_non_empty_indices()
    print("non_empty", non_empty)
    # Make bots by polynomial interpolation with all true elements
    empty = cuckoo_table.get_empty_indices()
    for bot_idx in empty:
        print("bot_idx", bot_idx)
        bot_elem = lagrange_interpolation(non_empty, bot_idx, p)
        cuckoo_table.replace_at(bot_idx, bot_elem)
        exp_bot = cuckoo_table.table[bot_idx]
        assert0(bot_elem.y-exp_bot.y)
    
    
        