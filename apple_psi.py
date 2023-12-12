import sys
from picozk import *
from picozk.poseidon_hash import PoseidonHash
from ecdsa import SECP256k1

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

    # TODO: Update the consts - Points on the elliptic curve
    G1_x, G1_y = (
        2089986280348253421170679821480865132823066470938446095505822317253594081284,
        1713931329540660377023406109199410414810705867260802078187082345529207694986,
    )
    G2_x, G2_y = (
        996781205833008774514500082376783249102396023663454813447423147977397232763,
        1668503676786377725805489344771023921079126552019160156920634619255970485781,
    )
    G3_x, G3_y = (
        2251563274489750535117886426533222435294046428347329203627021249169616184184,
        1798716007562728905295480679789526322175868328062420237419143593021674992973,
    )
    G4_x, G4_y = (
        2138414695194151160943305727036575959195309218611738193261179310511854807447,
        113410276730064486255102093846540133784865286929052426931474106396135072156,
    )
    G5_x, G5_y = (
        2379962749567351885752724891227938183011949129833673362440656643086021394946,
        776496453633298175483985398648758586525933812536653089401905292063708816422,
    )

    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler("irs/picozk_test", field=[p, n]):
        poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
        ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
        ncmec_digest = poseidon_hash.hash(ncmec_secret_data)
        Points = [(G1_x, G1_y), (G2_x, G2_y), (G3_x, G3_y), (G4_x, G4_y), (G5_x, G5_y)]

        # Make Cuckoo Table
        alpha = 5
        epsilon = 1
        cuckoo_table, non_emplist, lagrange_bases, poly_degree = make_Cuckoo(
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
            poly_degree,
        )


if __name__ == "__main__":
    main()
