import unittest
import sys
from picozk import *
from ecdsa import SECP256k1

sys.path.insert(1, "./apple_psi")
from pdata import make_Cuckoo
from interpolation import calc_polynomial
from helper import remove_duplicates


class Test_Base(unittest.TestCase):
    def test_interpolation(self):
        apple_secrets = [
            114303190253219474269384419659897947128561637493978467700760475363248655921884,
            47452005787557361733223600541610643778646485287733815210507547468435601040849,
        ]
        apple_secrets = remove_duplicates(apple_secrets)

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

        p = SECP256k1.curve.p()
        n = SECP256k1.order

        Points = [(G1_x, G1_y), (G2_x, G2_y), (G3_x, G3_y), (G4_x, G4_y), (G5_x, G5_y)]

        with PicoZKCompiler("picozk_test", field=[p, n]):
            alpha = 5
            epsilon = 1
            test_d = [
                (
                    113385371939531752299224346207750022137654760827455900656495118238958475899557,
                    62771483501060366068701852540103935202269405130243161002237027326815060845421,
                ),
                (
                    10157760668567613465900040494733225921671659909870612417809483248097326335880,
                    37674699084873029594178945979420673592754951593511996333384002113009473249380,
                ),
                (
                    17136757849927752745205382383109844381056385676206962696615894972524613244840,
                    51205854624749739556354727798176745738753011491453557497102975187014090965090,
                ),
                (
                    68009475676132699416480739324647426793996838463973604256669248866160408522929,
                    37305274461364918522140623956686657783961262461356198153573712844878370500562,
                ),
            ]

            lagrange = "Standard"  # Chose from Standard, BaryCentric, No Lagrange
            print(f"\nRunning with Larange Interpolation by {lagrange}")
            cuckoo_table, non_emplist, lagrange_bases, poly_degree = make_Cuckoo(
                apple_secrets, p, Points, alpha, epsilon, lagrange
            )

            for idx, val in enumerate(cuckoo_table.table):
                _gelm = calc_polynomial(idx, lagrange_bases)
                gelm = (val_of(_gelm.x), val_of(_gelm.y))
                assert gelm == test_d[idx]

            lagrange = "BaryCentric"  # Chose from Standard, BaryCentric, No Lagrange
            print(f"\nRunning with Larange Interpolation by {lagrange}")
            cuckoo_table, non_emplist, lagrange_bases, poly_degree = make_Cuckoo(
                apple_secrets, p, Points, alpha, epsilon, lagrange
            )

            for idx, val in enumerate(cuckoo_table.table):
                _gelm = calc_polynomial(idx, lagrange_bases)
                gelm = (val_of(_gelm.x), val_of(_gelm.y))
                assert gelm == test_d[idx]


if __name__ == "__main__":
    unittest.main()
