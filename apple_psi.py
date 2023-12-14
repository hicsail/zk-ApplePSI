import sys
import random
import ecdsa
from ecdsa import SECP256k1
from picozk import *
from picozk.poseidon_hash import PoseidonHash

sys.path.insert(1, "./apple_psi")
from apple_psi.curvepoint import CurvePoint
from apple_psi.pdata import make_Cuckoo
from apple_psi.psi_main import apple_psi


def remove_duplicates(secret: list):
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


def main():
    # Apple input: Curve & generator parameters
    apple_secrets = [
        114303190253219474269384419659897947128561637493978467700760475363248655921884,
        47452005787557361733223600541610643778646485287733815210507547468435601040849,
        47452005787557361733223600541610643778646485287733815210507547468435601040848,
    ]
    apple_secrets = remove_duplicates(apple_secrets)

    ncmec_secrets = [
        114303190253219474269384419659897947128561637493978467700760475363248655921884,
        47452005787557361733223600541610643778646485287733815210507547468435601040849,
        47452005787557361733223600541610643778646485287733815210507547468435601040848,
    ]
    ncmec_secrets = remove_duplicates(ncmec_secrets)

    p = SECP256k1.curve.p()  # p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
    n = SECP256k1.order
    g = ecdsa.ecdsa.generator_secp256k1
    
    def generate_consts():
        a_i = random.randrange(1, n) # Random number in the range [1, n-1]
        g_i = g * a_i # Raise the base point, g, by a_i
        return (g_i.x(), g_i.y())
    
    G1_x, G1_y = generate_consts()
    G2_x, G2_y = generate_consts()
    G3_x, G3_y = generate_consts()
    G4_x, G4_y = generate_consts()
    G5_x, G5_y = generate_consts()

    ''' 
        HAZMAT WARNING: The following code involves cryptographic operations
        that include randomized elements. This approach, while functional,
        may not adhere to standard cryptographic practices and might introduce
        risks if used in security-sensitive applications. The randomness
        introduced in the point generation (G1, G2, G3, G4, G5) could impact
        the deterministic nature and reproducibility of cryptographic operations.
        Use this code with caution, and only after thorough review and understanding
        of its implications in the context of your specific use case.
    '''

    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler("irs/picozk_test", field=[p, n]):
        poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
        ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
        ncmec_digest = poseidon_hash.hash(ncmec_secret_data)
        Points = [(G1_x, G1_y), (G2_x, G2_y), (G3_x, G3_y), (G4_x, G4_y), (G5_x, G5_y)]

        # Make Cuckoo Table
        alpha = 5
        epsilon = 1
        cuckoo_table, non_emplist, lagrange_bases = make_Cuckoo(
            apple_secrets, p, Points, alpha, epsilon
        )

        Points = [
            CurvePoint(False, G1_x, G1_y, p),
            CurvePoint(False, G2_x, G2_y, p),
            CurvePoint(False, G3_x, G3_y, p),
            CurvePoint(False, G4_x, G4_y, p),
            CurvePoint(False, G5_x, G5_y, p),
        ]

        # Make Secrets
        alpha = SecretInt(alpha)
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        non_emplist = [(idx, SecretInt(elm)) for (idx, elm) in non_emplist]
        apple_psi(
            p,
            alpha,
            apple_secrets,
            ncmec_digest,
            Points,
            cuckoo_table,
            non_emplist,
            lagrange_bases,
        )


if __name__ == "__main__":
    main()
