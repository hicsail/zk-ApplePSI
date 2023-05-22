from picozk import *
from picozk.poseidon_hash import PoseidonHash
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


# Instantiate the field for poseidon hash and creating a list of secrets that fits in the field
num_elem = 2 # User input
_p = 2**61-1
t = 3
secrets = remove_duplicates([randrange( 1, _p ) for _ in range(num_elem)])
poseidon_hash = PoseidonHash(_p, alpha = 17, input_rate = t, t = t)


# Simulating Apple confirming their data is same as NCMEC image data
with PicoZKCompiler('picozk_test'):
    secret_data = [SecretInt(c) for c in secrets]
    digest = poseidon_hash.hash(secret_data)
    assert0(digest - val_of(digest))


# Instantiate EC: Curve & generator parameters
G = SECP256k1.generator
p = SECP256k1.curve.p() #p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
n = SECP256k1.order
H = n * G
alpha = randrange( 1, p )


# Confirm that the field size from which the secret is generated is smaller than the field size of the eliptic curve
assert(_p <= p)


# The actual zk proof block
with PicoZKCompiler('picozk_test', field=[p,n]):
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