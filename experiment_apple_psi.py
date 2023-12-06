from picozk import *
from picozk.poseidon_hash import PoseidonHash
from picozk.functions import picozk_function
from ecdsa import SECP256k1
import random
import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import gc

import sys

sys.path.insert(1, "./utils")
from utils.curvepoint import CurvePoint
from utils.pedersen_hash import pedersen_hash
from utils.pdata import make_Cuckoo


def make_secret(scale, p):
    res = []
    for i in range(scale):
        ent = random.randint(0, p)
        res += [ent]

    return res


def remove_duplicates(secret: list):
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


@picozk_function
def subset_test(apple_secrets, curr_val):
    final_state = 0
    curr_state = 1
    for i in range(len(apple_secrets)):
        curr_state = mux(
            curr_state == final_state,
            curr_state,
            mux(apple_secrets[i] == curr_val, final_state, curr_state),
        )
    assert0(curr_state)
    return curr_state


def apple_pis(p, alpha, apple_secrets, ncmec_digest, Points, cuckoo_table, non_emplist, poly):
    # Simulating Apple confirming their data is same as NCMEC image data
    print(f"Reconciling NCMEC Data with Apple Data", end="\r", flush=True)
    poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
    apple_digest = poseidon_hash.hash(apple_secrets)
    assert0(ncmec_digest - val_of(apple_digest))

    print(f"Reconciling True Data in Cuckoo", end="\r", flush=True)
    for idx, val in non_emplist:
        # Prove that the set non_emplist is a subset of the set apple_secrets
        subset_test(apple_secrets, val)

        # Prove that each real element exists in hash one or two
        h1 = cuckoo_table.hash_one(val)
        h2 = cuckoo_table.hash_two(val)
        assert0((h1 - idx) * (h2 - idx))

        # Prove that hash_to_curve(val)^alpha is performed appropriately
        val = val.to_binary()
        gelm = pedersen_hash(val, Points, p)
        gelm = gelm.scale(alpha)
        table_elm = cuckoo_table.get_item_at(idx)
        assert0(gelm.x - table_elm.x)
        assert0(gelm.y - table_elm.y)

    print(f"Validating that bots are drawn from the same curve", end="\r", flush=True)
    # Prove that all elements are on the same curve drawn by lagrange for idx in cuckoo_table.get_empty_indices():
    for idx, val in enumerate(cuckoo_table.table):
        gelm, d = poly(idx)
        assert gelm.x == val.x
        assert gelm.y == val.y

    assert d == len(non_emplist) - 1


def run(size, csv_file):
    ttl_start_time = time.time()
    scale = int(size)
    p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
    n = SECP256k1.order

    # Apple input: Curve & generator parameters
    apple_secrets = make_secret(scale, p)
    apple_secrets = remove_duplicates(apple_secrets)
    ncmec_secrets = apple_secrets

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
        try:
            print(f"Building Parameters", end="\r", flush=True)
            start_time = time.time()
            poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
            ncmec_secret_data = [SecretInt(c) for c in ncmec_secrets]
            print(f"Hashing Images", end="\r", flush=True)
            ncmec_digest = poseidon_hash.hash(ncmec_secret_data)
            end_time = time.time()
            elapsed_time_poseidon = end_time - start_time

            Points = [
                (G1_x, G1_y),
                (G2_x, G2_y),
                (G3_x, G3_y),
                (G4_x, G4_y),
                (G5_x, G5_y),
            ]

            # Make Cuckoo Table
            alpha = 5
            epsilon = 1
            print(f"Making Cuckoo", end="\r", flush=True)
            ck_start_time = time.time()
            cuckoo_table, non_emplist, poly = make_Cuckoo(apple_secrets, p, Points, alpha, epsilon)
            ck_end_time = time.time()
            ck_time = ck_end_time - ck_start_time

            Points = [
                CurvePoint(False, G1_x, G1_y, p),
                CurvePoint(False, G2_x, G2_y, p),
                CurvePoint(False, G3_x, G3_y, p),
                CurvePoint(False, G4_x, G4_y, p),
                CurvePoint(False, G5_x, G5_y, p),
            ]

            # Make Secrets
            print(f"Producing Pdata", end="\r", flush=True)
            alpha = SecretInt(alpha)
            apple_secrets = [SecretInt(c) for c in apple_secrets]
            non_emplist = [(idx, SecretInt(elm)) for (idx, elm) in non_emplist]
            apple_pis(
                p,
                alpha,
                apple_secrets,
                ncmec_digest,
                Points,
                cuckoo_table,
                non_emplist,
                poly,
            )

            ttl_end_time = time.time()
            ttl_elapsed = ttl_end_time - ttl_start_time

            other_time = ttl_elapsed - elapsed_time_poseidon

            print(f"\n Poseidon Hash: {elapsed_time_poseidon}, Other: {other_time}, TTL: {ttl_elapsed} seconds to run (ck_time: {ck_time} seconds)")

            new_data = [size, other_time, elapsed_time_poseidon, ttl_elapsed, ck_time]
            res_list.append(new_data)
            new_row = pd.DataFrame(
                [new_data],
                columns=["Scale", "Other-Time", "Time-Poseidon", "Time-Total", "ck_time"],
            )


            # Check if the CSV file exists
            if not os.path.isfile(csv_file):
                # If not, create it with header
                new_row.to_csv(csv_file, index=False)
            else:
                # If it exists, append without writing the header
                new_row.to_csv(csv_file, mode="a", header=False, index=False)

        except Exception as e:
            print(f"An error occurred in iteration {size}: {e}")


if __name__ == "__main__":
    # Importing ENV Var & Checking if prime meets our requirement
    res_list = []
    csv_file = "Apple_analysis.csv"
    sizes = [50, 100, 200, 400, 600, 800]

    if os.path.isfile(csv_file):
        os.remove(csv_file)  # Delete the file
        print(f"File '{csv_file}' has been deleted.")

    for size in sizes:
        print('\n* Running:', size)
        gc.collect()
        run(size, csv_file)

    res_df = pd.read_csv(csv_file)
    # Plotting runtime for apple psi specific experiments
    plt.bar(res_df["Scale"], res_df["Time-Poseidon"], label="Time-Poseidon")
    plt.bar(
        res_df["Scale"],
        res_df["Time-Other"],
        bottom=res_df["Time-Poseidon"],
        label="Time-Other",
    )

    plt.title("Runtime")
    plt.xlabel("Scale")
    plt.ylabel("Time in sec")
    plt.grid(True)
    plt.legend(loc="best")
    plt.show()