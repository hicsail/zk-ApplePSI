from picozk import *
from picozk.poseidon_hash import PoseidonHash
import random
import ecdsa
from ecdsa import SECP256k1
import time
import pandas as pd
import os
import gc
import sys

sys.path.insert(1, ".")
from apple_psi.curvepoint import CurvePoint
from apple_psi.pdata import make_Cuckoo
from apple_psi.psi_main import apple_psi
from apple_psi.helper import remove_duplicates, make_secret, count_rel


def main(size, csv_file, lagrange):
    ttl_start_time = time.time()

    p = SECP256k1.curve.p()  # p = 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
    n = SECP256k1.order
    g = ecdsa.ecdsa.generator_secp256k1
    scale = int(size)
    # Apple input: Curve & generator parameters
    apple_secrets = make_secret(scale, p)
    apple_secrets = remove_duplicates(apple_secrets)
    ncmec_secrets = apple_secrets

    def generate_consts():
        a_i = random.randrange(1, n)  # Random number in the range [1, n-1]
        g_i = g * a_i  # Raise the base point, g, by a_i
        return (g_i.x(), g_i.y())

    G1_x, G1_y = generate_consts()
    G2_x, G2_y = generate_consts()
    G3_x, G3_y = generate_consts()
    G4_x, G4_y = generate_consts()
    G5_x, G5_y = generate_consts()

    file_path = "irs/picozk_test_" + lagrange + "_" + str(size)
    # Simulating Apple confirming their data is same as NCMEC image data
    with PicoZKCompiler(file_path, field=[p, n]):
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
        print(f"\nRunning with Larange Interpolation by {lagrange}")
        print(f"Making Cuckoo", end="\r", flush=True)
        ck_start_time = time.time()
        cuckoo_table, non_emplist, lagrange_bases, poly_degree = make_Cuckoo(
            apple_secrets, p, Points, alpha, epsilon, lagrange
        )
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
        # This one for perm map access
        _apple_secrets = ZKList(apple_secrets)
        # This one for Poseidon Hash
        apple_secrets = [SecretInt(c) for c in apple_secrets]
        perm_map = [
            SecretInt(sec_idx)
            for sec_idx in cuckoo_table.perm_map
            if sec_idx is not None
        ]
        # Make it unaccessible perm map
        cuckoo_table.perm_map = None
        non_emplist = [(idx, SecretInt(elm)) for (idx, elm) in non_emplist]
        time_res = apple_psi(
            p,
            alpha,
            apple_secrets,
            _apple_secrets,
            ncmec_digest,
            Points,
            cuckoo_table,
            non_emplist,
            perm_map,
            lagrange_bases,
            poly_degree,
        )

        ttl_end_time = time.time()
        ttl_elapsed = ttl_end_time - ttl_start_time
        line_count = count_rel(file_path)

        version = lagrange

        if lagrange_bases != None:
            output_statement = f"\n TTL: {ttl_elapsed} seconds to run (Poseidon: {elapsed_time_poseidon}, Cuckoo: {ck_time}, true data check {time_res[0]}, bots check {time_res[1]}) - {line_count}M lines in .rel"
            new_data = [
                size,
                ttl_elapsed,
                ck_time,
                elapsed_time_poseidon,
                time_res[0],
                time_res[1],
                line_count,
                version,
            ]
        else:
            output_statement = f"\n TTL: {ttl_elapsed} seconds to run (Poseidon: {elapsed_time_poseidon}, Cuckoo: {ck_time}, true data check {time_res[0]}) - {line_count}M lines in .rel"
            new_data = [
                size,
                ttl_elapsed,
                ck_time,
                elapsed_time_poseidon,
                time_res[0],
                "-",
                line_count,
                version,
            ]

        print(output_statement)

        res_list.append(new_data)
        new_row = pd.DataFrame(
            [new_data],
            columns=[
                "Scale",
                "Time-Total",
                "Time-Cuckoo",
                "Time-Poseidon",
                "Time-TrueDataCheck",
                "Time-BotsCheck",
                "Lines",
                "Version",
            ],
        )

        # Check if the CSV file exists
        if not os.path.isfile(csv_file):
            # If not, create it with header
            new_row.to_csv(csv_file, index=False)
        else:
            # If it exists, append without writing the header
            new_row.to_csv(csv_file, mode="a", header=False, index=False)


if __name__ == "__main__":
    # Importing ENV Var & Checking if prime meets our requirement
    res_list = []
    csv_file = "Apple_analysis.csv"
    sizes = [500, 1000]

    lagrangeMethods = ["NoLagrange"]
    for size in sizes:
        for lagrange in lagrangeMethods:
            print("\n* Running:", size, f"Lagerange Type: {lagrange}")
            gc.collect()
            main(size, csv_file, lagrange)
