import math
from cuckoo_table import CuckooTable
from pedersen_hash_int import pedersen_hash_int
from interpolation import calc_lagrange_terms, calc_lagrange_terms_bary, calc_polynomial
from curvepoint import CurvePoint
import time


def make_index_lists(cuckoo_table):
    non_emplist = []
    emptyList = list(range(cuckoo_table.table_size))
    for index in range(len(cuckoo_table.table)):
        if cuckoo_table.table[index] is not None:
            non_emplist.append((index, cuckoo_table.table[index]))
            emptyList.remove(index)
    return non_emplist, emptyList


def calc_table_size(secrets, epsilon):
    table_size = len(secrets) * (1 + epsilon)

    if math.log2(table_size).is_integer():
        print("table_size", table_size, "is a power of 2")
    else:
        print(
            "table_size",
            table_size,
            "is not a power of 2, padding it to next power of 2.",
        )
        next_power_of_two = 2 ** math.ceil(math.log2(table_size))
        padded_secrets = [None] * int(
            next_power_of_two
        )  # Padding with None or your preferred placeholder
        table_size = len(padded_secrets)
        print("Final table size:", table_size)
    return table_size


def make_Cuckoo(secrets, p, Points, alpha, epsilon, lagrange):
    # Make a Cuckoo table
    table_size = calc_table_size(secrets, epsilon)
    cuckoo_table = CuckooTable(secrets, table_size, p)
    non_emplist, emptyList = make_index_lists(cuckoo_table)

    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    xs = []
    ys = []
    print(f"Pedersen Hash...", end="\r", flush=True)
    for idx, secret in non_emplist:
        gelm = pedersen_hash_int(secret, Points, p)
        gelm = CurvePoint(False, gelm[0], gelm[1], p)
        gelm = gelm.scale(alpha)
        cuckoo_table.set_table_at(idx, gelm)
        xs.append(idx)
        ys.append(gelm)

    if lagrange == "NoLagrange":
        print(f"Skipping Lagrange Polynomial...")
        lagrange_bases = None
        poly_degree = None
        return cuckoo_table, non_emplist, lagrange_bases, poly_degree

    elif lagrange == "Standard":
        # Calculate bots by the polynomial above
        print(f"Lagrange Polynomial {lagrange} method...")
        start_time = time.time()
        lagrange_bases, poly_degree = calc_lagrange_terms(xs, ys, cuckoo_table, p)
        for bot_idx in emptyList:
            bot = calc_polynomial(bot_idx, lagrange_bases)
            cuckoo_table.set_table_at(bot_idx, bot)
        end_time = time.time()
        print(f"Lagrange Polynomial Done...", end="\r", flush=True)
        lagrange_time = end_time - start_time
        print(f"\n Lagrange Took {lagrange_time} sec")
        return cuckoo_table, non_emplist, lagrange_bases, poly_degree

    elif lagrange == "BaryCentric":
        # Calculate bots by the polynomial above
        print(f"Lagrange Polynomial {lagrange} method...")
        start_time = time.time()
        lagrange_bases, poly_degree = calc_lagrange_terms_bary(xs, ys, cuckoo_table, p)
        for bot_idx in emptyList:
            bot = calc_polynomial(bot_idx, lagrange_bases)
            cuckoo_table.set_table_at(bot_idx, bot)
        end_time = time.time()
        print(f"Lagrange Polynomial Done...", end="\r", flush=True)
        lagrange_time = end_time - start_time
        print(f"\n Lagrange Took {lagrange_time} sec")
        return cuckoo_table, non_emplist, lagrange_bases, poly_degree
