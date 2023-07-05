from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1

import sys
sys.path.insert(1, './utils')
from curvepoint import CurvePoint
from interpolation import lagrange_polynomial
from pedersen_hash import pedersen_hash
from test_data import make_Cuckoo

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret

def apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, cuckoo_table, poly):

    # TODO: Unncomment - Simulating Apple confirming their data is same as NCMEC image data
    # secret_data = [SecretInt(c) for c in apple_secrets]
    # t = 2
    # poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
    # apple_digest = poseidon_hash.hash(secret_data)
    # assert0(ncmec_digest - val_of(apple_digest))


    # Assert that the set non_emplist is a subset of the set apple_secrets
    non_emplist = cuckoo_table.get_non_emplist()
    final_state = 0
    for _, val in non_emplist:
        curr_state = 1
        for idx in range(len(apple_secrets)):
            curr_state = mux(curr_state==final_state, curr_state, mux(apple_secrets[idx]==val, curr_state, final_state))
        assert0(curr_state)

        #TODO: hash_to_curve(val)^alpha exists in the cuckoo_table at location hash_one(val) or hash_two(val)

    # TODO: Assert that all elements are on the same curve drew by lagrange

    

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

    Points = [G, G2, G3, G4, G5]

    epsilon=1
    cuckoo_table, poly = make_Cuckoo(apple_secrets, p, Points, alpha, epsilon)

    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler('picozk_test', field=[p,n]):
    #     # poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
    #     # ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
    #     # ncmec_digest = poseidon_hash.hash(ncmec_secret_data)
        ncmec_digest = None
        
        # Make Secrets
        alpha=SecretInt(alpha)
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        Points = [CurvePoint(False, G.x(), G.y(), p),
                CurvePoint(False, G2.x(), G2.y(), p),
                CurvePoint(False, G3.x(), G3.y(), p),
                CurvePoint(False, G4.x(), G4.y(), p),
                CurvePoint(False, G5.x(), G5.y(), p)]


        apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, cuckoo_table, poly)

if __name__ == "__main__":
    main()