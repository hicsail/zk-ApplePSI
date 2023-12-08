from picozk import *


def calc_lagrange_terms(xs, ys, cuckoo_table, p):
    assert len(xs) == len(ys)
    n = len(xs)

    # Preprocessing Lgrange Polynomial (Only terms)
    lagrange_bases = {}  # idx in cuckoo table (key): terms (value)

    denominators = []
    for i in range(n):
        denominator = 1
        for j in range(n):
            if j != i:
                denominator *= modular_inverse(xs[i] - xs[j], p)
        denominators.append(denominator)

    # Calculate terms for all index in the cuckoo table
    for idx, _ in enumerate(cuckoo_table.table):
        terms = []
        for i in range(n):
            term = ys[i]
            numerator = 1
            for j in range(n):
                if j != i:
                    numerator *= idx - xs[j]
            term = term.scale(numerator * denominators[i] % p)
            terms.append(term)
        lagrange_bases[idx] = terms
    return lagrange_bases


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
    return result, len(lagrange_bases[0]) - 1
