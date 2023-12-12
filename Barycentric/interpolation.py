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
                denominator *= (xs[i] - xs[j]) % p
        denominator = modular_inverse(denominator, p)
        denominators.append(denominator)

    numerators = []
    for idx,  _ in enumerate(cuckoo_table.table):
        numerator = 1
        for j in range(n):
            if idx != xs[j]:
                numerator *= idx - xs[j]
        numerators.append(numerator)

    # Calculate terms for all index in the cuckoo table
    for idx, _ in enumerate(cuckoo_table.table):
        terms = []
        temp = 1
        for i in range(n):
            term = ys[i]
            numerator = 1
            for j in range(n):
                if j != i:
                    numerator *= idx - xs[j]
            temp *= numerator * denominators[i] % p
            term = term.scale(temp)
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
