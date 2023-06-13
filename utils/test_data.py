from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1

from cuckoo_table import CuckooTable
from curvepoint import CurvePoint
from interpolation import lagrange_interpolation
from pedersen_hash import pedersen_hash

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


def make_TestCuckoo():

    #  Apple input: Curve & generator parameters
    secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
    secrets = remove_duplicates(secrets)
    alpha = 5

    # Other parameters
    G = SECP256k1.generator
    G2 = 2*G
    G3 = 3*G
    G4 = 4*G
    G5 = 5*G

    p = SECP256k1.curve.p()


    # Points on the elliptic curve
    Points = [CurvePoint(False, G.x(), G.y(), p),
            CurvePoint(False, G2.x(), G2.y(), p),
            CurvePoint(False, G3.x(), G3.y(), p),
            CurvePoint(False, G4.x(), G4.y(), p),
            CurvePoint(False, G5.x(), G5.y(), p)]


    # Make a Cuckoo table
    table_size = 2**len(secrets)
    test_cuckoo_table = CuckooTable(secrets, table_size, p)


    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_emplist = test_cuckoo_table.get_non_emplist()
    for i in range(len(non_emplist)):
        idx, _ = non_emplist[i]
        secret = test_cuckoo_table.get_item_at(idx).to_binary()
        exp_elem = pedersen_hash(secret, Points, p)
        exp_elem = exp_elem.scale(SecretInt(alpha))
        test_cuckoo_table.set_non_emplist(i, (idx, exp_elem))


    # Make bots by polynomial interpolation with all true elements
    non_emplist = test_cuckoo_table.get_non_emplist()
    emptyList = test_cuckoo_table.get_empty_indices()
    for bot_idx in emptyList:
        bot_elem = lagrange_interpolation(non_emplist, bot_idx, p)
        test_cuckoo_table.set_table_at(bot_idx, bot_elem)

    return test_cuckoo_table