from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1
from random import randrange
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


#  Apple input: Curve & generator parameters
G = SECP256k1.generator
p = SECP256k1.curve.p()
print('field size:', p) #p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
n = SECP256k1.order

s = 5
H = s*G #TODO:FIXME Replace with the real pedersen hash

t = 2
alpha = 5
# poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
secrets = remove_duplicates(secrets)

# Simulating Apple confirming their data is same as NCMEC image data
with PicoZKCompiler('picozk_test', field=[p,n]):
    # TODO:FIXME Uncomment
    secret_data = [SecretInt(c) for c in secrets]
    # digest = poseidon_hash.hash(secret_data)
    # assert0(digest - val_of(digest)) # Simulating Apple confirming their data is same as NCMEC image data


    # Make a Cuckoo table
    table_size = 2**len(secrets)
    cuckoo_table = CuckooTable(secrets, table_size, p)

    # ZK proof for the hash functions and that the non-empty is made out of the original secrets
    cuckoo_table.verify_non_emplist(secret_data)


    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_emplist = cuckoo_table.get_non_emplist()
    x_cor = SecretInt(G.x())
    y_cor = SecretInt(G.y())
    for i in range(len(non_emplist)):
        idx, _ = non_emplist[i]
        secret = cuckoo_table.get_item_at(idx)*alpha
        _secret = secret.to_binary().to_arithmetic(field=p)
        map_elem = CurvePoint(False, x_cor, y_cor, p)
        exp_elem = map_elem.scale(_secret) # TODO:FIXME we probably need more strict hash function
        cuckoo_table.replace_at(idx, exp_elem)
        cuckoo_table.set_non_emplist(i, (idx, exp_elem))
    
    # Make bots by polynomial interpolation with all true elements
    non_emplist = cuckoo_table.get_non_emplist()
    emptyList = cuckoo_table.get_empty_indices()
    for bot_idx in emptyList:
        bot_elem = lagrange_interpolation(non_emplist, bot_idx, p)
        cuckoo_table.replace_at(bot_idx, bot_elem)
        exp_bot = cuckoo_table.get_item_at(bot_idx)
        # ZK proof for the interpolation for the bots
        check_bots = bot_elem.x-exp_bot.x
        assert0(SecretInt(check_bots))
    
    # Permutation proof
    permutation=cuckoo_table.get_size()-(len(non_emplist)+len(emptyList))
    assert0(SecretInt(permutation))


    # TODO: Add table vs table assertion (Both bots and real values)

    # TODO: Modularize the function so apple cn plug in secrets, alpha, G and H
