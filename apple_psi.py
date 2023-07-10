from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1

import sys
sys.path.insert(1, './utils')
from curvepoint import CurvePoint
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


    # Prove that the set non_emplist is a subset of the set apple_secrets
    non_emplist = cuckoo_table.get_non_emplist()
    final_state = 0
    for idx, val in non_emplist:
        curr_state = 1
        for idx in range(len(apple_secrets)):
            curr_state = mux(curr_state==final_state, curr_state, mux(apple_secrets[idx]==val, curr_state, final_state))
        assert0(curr_state)

        
        # Prove the element exists at the index of either hash_one or _two
        h1 = cuckoo_table.hash_one(val)
        h2 = cuckoo_table.hash_two(val)
        assert0((h1-idx)*(h2-idx))

        # TODO: hash_to_curve(val)^alpha exists in the cuckoo_table at location hash_one(val) or hash_two(val)
        gelm = pedersen_hash(val.to_binary(), Points, p)
        gelm = gelm.scale(alpha)
        assert0(gelm.x-cuckoo_table.get_item_at(idx).x)
        
    
    # TODO: Prove that all elements are on the same curve drawn by lagrange

    # Assert that len(non_emplist_items) == d+1
    assert(len(non_emplist)-len(poly)==0)
    # TODO: Implment eviction
    

def main():
    # Apple input: Curve & generator parameters
    apple_secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
    apple_secrets = remove_duplicates(apple_secrets)

    ncmec_secrets = [114303190253219474269384419659897947128561637493978467700760475363248655921884, 47452005787557361733223600541610643778646485287733815210507547468435601040849]
    ncmec_secrets = remove_duplicates(ncmec_secrets)
    
    p = SECP256k1.curve.p() #p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
    n = SECP256k1.order

    # Points on the elliptic curve
    G = SECP256k1.generator
    G2_x, G2_y= 996781205833008774514500082376783249102396023663454813447423147977397232763, 1668503676786377725805489344771023921079126552019160156920634619255970485781
    G3_x, G3_y= 2251563274489750535117886426533222435294046428347329203627021249169616184184,1798716007562728905295480679789526322175868328062420237419143593021674992973
    G4_x, G4_y= 2138414695194151160943305727036575959195309218611738193261179310511854807447,113410276730064486255102093846540133784865286929052426931474106396135072156
    G5_x, G5_y= 2379962749567351885752724891227938183011949129833673362440656643086021394946,776496453633298175483985398648758586525933812536653089401905292063708816422

    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler('picozk_test', field=[p,n]):
        alpha = 5
        t = 2
    #     # poseidon_hash = PoseidonHash(p, alpha = alpha, input_rate = t)
    #     # ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
    #     # ncmec_digest = poseidon_hash.hash(ncmec_secret_data)
        ncmec_digest = None

        Points = [CurvePoint(False, G.x(), G.y(), p),
                CurvePoint(False, G2_x, G2_y, p),
                CurvePoint(False, G3_x, G3_y, p),
                CurvePoint(False, G4_x, G4_y, p),
                CurvePoint(False, G5_x, G5_y, p)]

        # Make Cuckoo Table
        epsilon=1
        cuckoo_table, poly = make_Cuckoo(apple_secrets, p, Points, alpha, epsilon)
        
        # Make Secrets
        alpha=SecretInt(alpha)
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, cuckoo_table, poly)

if __name__ == "__main__":
    main()