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


#  Apple input: Curve & generator parameters
num_elem = 2 
G = SECP256k1.generator
p = SECP256k1.curve.p()
print('field size:', p) #p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
n = SECP256k1.order

s = 5
H = s*G #TODO:FIXME

t = 2
alpha = 5
poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
secrets = remove_duplicates([randrange( 1, p ) for _ in range(num_elem)])

# Simulating Apple confirming their data is same as NCMEC image data
with PicoZKCompiler('picozk_test', field=[p,n]):
    secret_data = [SecretInt(c) for c in secrets]
    digest = poseidon_hash.hash(secret_data)
    assert0(digest - val_of(digest)) # Simulating Apple confirming their data is same as NCMEC image data

    # Make a Cuckoo table
    table_size = 2**num_elem
    cuckoo_table = CuckooTable(secrets, table_size, p)
    print(cuckoo_table.get_non_empty_indices())

    cuckoo_table.verify_hash() # ZK proof for the hash functions


    # # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_empty = cuckoo_table.get_non_empty_indices()
    x_cor = SecretInt(G.x())
    y_cor = SecretInt(G.y())
    for i in range(len(non_empty)):
        idx, _ = non_empty[i]
        secret = cuckoo_table.get_item_at(idx)
        print("secret", secret)
        print("type", type(secret))
        _secret = secret.to_binary().to_arithmetic(field=p)
        map_elem = CurvePoint(False, x_cor, y_cor, p)
        exp_elem = map_elem.scale(_secret) # Map secret on the curve
        cuckoo_table.replace_at(idx, exp_elem)
        cuckoo_table.set_non_emplist(i, (idx, exp_elem))

    assert0(cuckoo_table.get_nonemp_size()-len(secret_data))
    
    # # Make bots by polynomial interpolation with all true elements
    non_empty = cuckoo_table.get_non_empty_indices()
    empty = cuckoo_table.get_empty_indices()
    for bot_idx in empty:
        bot_elem = lagrange_interpolation(non_empty, bot_idx, p)
        cuckoo_table.replace_at(bot_idx, bot_elem)
        exp_bot = cuckoo_table.get_item_at(bot_idx)
        assert0(bot_elem.x-exp_bot.x) # ZK proof for the interpolation for the bots