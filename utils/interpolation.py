from picozk import *


def lagrange_poly(xs, ys, cuckoo_table, p):
    assert len(xs) == len(ys)
    n = len(xs)

    # Preprocessing Lgrange Polynomial (Only terms)
    lagrange_bases = {}  # idx in cuckoo table (key): terms (value)

    def calc_terms(obj_idx):
        terms = []
        for i in range(n):
            term = ys[i]
            for j in range(n):
                if j != i:
                    a = ((obj_idx - xs[j]) * modular_inverse(xs[i] - xs[j], p)) % p
                    term = term.scale(a)
            terms.append(term)
        return terms

    # Calculate terms for all index in the cuckoo table
    for idx, _ in enumerate(cuckoo_table.table):
        lagrange_bases[idx] = calc_terms(idx)

    def polynomial(idx):
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

        return result, n - 1

    return polynomial
