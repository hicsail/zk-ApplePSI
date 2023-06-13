from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1

import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation
from pedersen_hash import pedersen_hash
from test_data import make_TestCuckoo

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


def apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, test_cuckoo_table):

    # Simulating Apple confirming their data is same as NCMEC image data
    secret_data = [SecretInt(c) for c in apple_secrets]
    t = 2
    poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
    apple_digest = poseidon_hash.hash(secret_data)
    assert0(ncmec_digest - val_of(apple_digest))


    # Make a Cuckoo table
    table_size = 2**len(apple_secrets)
    cuckoo_table = CuckooTable(apple_secrets, table_size, p)

    # ZK proof for the hash functions, that the non-empty is made out of the original secrets
    cuckoo_table.permutation_proof(secret_data)


    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_emplist = cuckoo_table.get_non_emplist()
    for i in range(len(non_emplist)):
        idx, _ = non_emplist[i]
        secret = cuckoo_table.get_item_at(idx).to_binary()
        exp_elem = pedersen_hash(secret, Points, p)
        exp_elem = exp_elem.scale(SecretInt(alpha))
        cuckoo_table.set_non_emplist(i, (idx, exp_elem))
    

    # Make bots by polynomial interpolation with all true elements
    non_emplist = cuckoo_table.get_non_emplist()
    emptyList = cuckoo_table.get_empty_indices()
    for bot_idx in emptyList:
        bot_elem = lagrange_interpolation(non_emplist, bot_idx, p)
        cuckoo_table.set_table_at(bot_idx, bot_elem)
        exp_bot = cuckoo_table.get_item_at(bot_idx)
        # ZK proof for the interpolation for the bots
        check_bots = (bot_elem.x-exp_bot.x) + (bot_elem.y-exp_bot.y)
        assert0(check_bots)
    

    # table vs table assertion (Both bots and real values)
    cuckoo_table.reconcile(test_cuckoo_table)


def main():
    # Apple input: Curve & generator parameters
    apple_secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
    apple_secrets = remove_duplicates(apple_secrets)

    ncmec_secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
    ncmec_secrets = remove_duplicates(ncmec_secrets)
    
    alpha = 5
    t = 2

    p = SECP256k1.curve.p() #p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
    n = SECP256k1.order

    # Points on the elliptic curve
    G = SECP256k1.generator
    G2 = 2*G
    G3 = 3*G
    G4 = 4*G
    G5 = 5*G

    Points = [CurvePoint(False, G.x(), G.y(), p),
            CurvePoint(False, G2.x(), G2.y(), p),
            CurvePoint(False, G3.x(), G3.y(), p),
            CurvePoint(False, G4.x(), G4.y(), p),
            CurvePoint(False, G5.x(), G5.y(), p)]


    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler('picozk_test', field=[p,n]):
        poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
        ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
        ncmec_digest = poseidon_hash.hash(ncmec_secret_data)

        apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, make_TestCuckoo())

if __name__ == "__main__":
    main()