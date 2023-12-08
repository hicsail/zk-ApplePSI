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
from psi_main_coeff import apple_psi
from curvepoint import CurvePoint
from pdata import make_Cuckoo


def count(file_path):
    file_path += ".rel"
    # Initialize a variable to count lines
    line_count = 0

    # Open the file and read line by line
    with open(file_path, "r") as file:
        for line in file:
            line_count += 1

    million = 1000000
    line_count /= million

    # Print the total number of lines
    print(f"\n Total number of lines in the file: {line_count} (* 10^6)")

    return line_count


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


def main(size, csv_file):
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
            cuckoo_table, non_emplist, coeffs = make_Cuckoo(
                apple_secrets, p, Points, alpha, epsilon
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
                coeffs,
            )

            ttl_end_time = time.time()
            ttl_elapsed = ttl_end_time - ttl_start_time

            file_path = "irs/picozk_test"
            line_count = count(file_path)

            print(
                f"\n TTL: {ttl_elapsed} seconds to run (Poseidon: {elapsed_time_poseidon}, Cuckoo: {ck_time}) - {line_count}M lines in .rel"
            )

            new_data = [
                size,
                ttl_elapsed,
                ck_time,
                elapsed_time_poseidon,
                line_count,
                "v3(coeff)",
            ]
            res_list.append(new_data)
            new_row = pd.DataFrame(
                [new_data],
                columns=[
                    "Scale",
                    "Time-Total",
                    "Time-Cuckoo",
                    "Time-Poseidon",
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

        except Exception as e:
            print(f"An error occurred in iteration {size}: {e}")


def plot_twin(df, title):
    # Plotting runtime for apple psi specific experiments
    plt.plot(df["Scale"], df["Time-Total"], label="Time")
    plt.title(title)
    plt.xlabel("Scale")
    plt.ylabel("Time in sec")

    # Create a second y-axis for "Lines"
    ax2 = plt.twinx()
    ax2.plot(df["Scale"], df["Lines"], color="orange", label="Lines")
    ax2.set_ylabel("Number of Lines")

    # Add legends for both plots
    plt.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Other plot settings
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Importing ENV Var & Checking if prime meets our requirement
    res_list = []
    csv_file = "Apple_analysis.csv"
    sizes = [5]

    for size in sizes:
        print("\n* Running:", size)
        gc.collect()
        main(size, csv_file)


    df = pd.read_csv(csv_file)

    # v2_df = df[df["Version"] == "v2"]
    # v2_title = "Runtime and Line (v2)"
    # plot_twin(v2_df, v2_title)

    v3_df = df[df["Version"] == "v3"]
    v3_title = "Runtime and Line (v3)"
    plot_twin(v3_df, v3_title)

    v3c_df = df[df["Version"] == "v3(coeff)"]
    v3c_title = "Runtime and Line (v3(coeff))"
    plot_twin(v3c_df, v3c_title)

