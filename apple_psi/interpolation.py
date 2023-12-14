from picozk import *
import numpy as np


def calc_bary_weights(xs, ys, p):
    xs = np.array(xs)
    ys = np.array(ys)
    n = len(xs)

    # Vectorized computation of differences
    diffs = xs.reshape((n, 1)) - xs
    np.fill_diagonal(diffs, 1)  # Avoid division by zero

    # Non-vectorized computation of weights due to modular inverse
    bary_weights = np.array([modular_inverse(np.prod(diffs[j, :]) % p, p) for j in range(n)])
    return bary_weights


# https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form
def calc_lagrange_terms_bary(xs, ys, cuckoo_table, p):
    bary_weights = calc_bary_weights(xs, ys, p)
    
    xs = np.array(xs)
    ys = np.array(ys, dtype=object)  # Assuming ys are custom objects that support vectorized operations
    n = len(xs)

    # Precompute modular inverses for all unique differences
    unique_diffs = set()
    for x, _ in enumerate(cuckoo_table.table):
        for xi in xs:
            diff = (x - xi) % p
            if diff != 0:  # We only need inverses for non-zero differences
                unique_diffs.add(diff)

    precomputed_inverses = {diff: modular_inverse(diff, p) for diff in unique_diffs}

    # Compute denominators
    denominators = np.zeros(len(cuckoo_table.table), dtype=object)
    for x, _ in enumerate(cuckoo_table.table):
        if x in xs:
            denominators[x] = 1
        else:
            inverse_diffs = np.array([precomputed_inverses[(x - xm) % p] for xm in xs], dtype=object)
            denominators[x] = np.sum(bary_weights * inverse_diffs) % p

    # Compute terms
    lagrange_bases = {}
    for x, _ in enumerate(cuckoo_table.table):
        if x in xs:
            index = np.where(xs == x)[0][0]
            lagrange_bases[x] = [ys[index]]
        else:
            inverse_diffs = np.array([precomputed_inverses[(x - xj) % p] for xj in xs], dtype=object)
            nums = (bary_weights * inverse_diffs) % p
            scalers = (nums * modular_inverse(denominators[x], p)) % p
            terms = [y.scale(scaler) for y, scaler in zip(ys, scalers)]
            lagrange_bases[x] = terms

    return lagrange_bases, n - 1



def calc_polynomial(idx, lagrange_bases):
    result = None
    terms = lagrange_bases[idx]
    for term in terms:
        if result is None:
            result = term
        else:
            if result.x != term.x or result.y != term.y:
                result = result.add(term)
            else:
                result = result.scale(2)
    return result
