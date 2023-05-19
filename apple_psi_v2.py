from picozk import *
from ecdsa import SECP256k1
from random import randrange
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation
from pedersen_commitment import pedersen_commitment
from pedersen_commitment import verify_commitment

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


# Instantiate EC: Curve & generator parameters
G = SECP256k1.generator
p = SECP256k1.curve.p()
n = SECP256k1.order
H = n * G
alpha = randrange( 1, p )


with PicoZKCompiler('picozk_test', field=[p,n]):

    # User input
    num_elem = 2
    secrets = remove_duplicates([randrange( 1, p ) for _ in range(num_elem)])
    print("secrets", secrets)
    
    # Make a Cuckoo table
    table_size = 2**num_elem
    cuckoo_table = CuckooTable(secrets, table_size, p)

    cuckoo_table.verify_hash() # ZK proof for the hash functions


    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_empty = cuckoo_table.get_non_empty_indices()
    for i in range(len(non_empty)):
        idx, secret = non_empty[i]
        commitment = pedersen_commitment(G, secret, alpha, H)
        x_cor = SecretInt(commitment.x())
        y_cor = SecretInt(commitment.y())
        map_elem = CurvePoint(False, x_cor, y_cor, p)
        cuckoo_table.replace_at(idx, map_elem)
        cuckoo_table.set_non_emplist(i, (idx, map_elem))

        verify_commitment(G, map_elem, secret, alpha, H) # ZK proof for the pedersen hash
    
    
    # Make bots by polynomial interpolation with all true elements
    non_empty = cuckoo_table.get_non_empty_indices()
    empty = cuckoo_table.get_empty_indices()
    for bot_idx in empty:
        bot_elem = lagrange_interpolation(non_empty, bot_idx, p)
        cuckoo_table.replace_at(bot_idx, bot_elem)
        exp_bot = cuckoo_table.get_item_at(bot_idx)

        assert0(bot_elem.y-exp_bot.y) # ZK proof for the interpolation for the bots