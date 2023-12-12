from picozk import *


# https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form
def calc_lagrange_terms(xs, ys, cuckoo_table, p):
    # Preprocessing Lgrange Polynomial (Only terms)
    lagrange_bases = {}  # idx in cuckoo table (key): terms (value)

    bary_weights = []
    for j in range(len(xs)):
        weight = 1
        for m in range(len(xs)):
            if j != m:
                weight *= (xs[j] - xs[m]) % p
        weight = modular_inverse(weight, p)
        bary_weights.append(weight)

    denominators = []

    for x, _ in enumerate(cuckoo_table.table):
        denom = 0
        for m, weight in enumerate(bary_weights):
            if x != xs[m]:
                inverse_diff = modular_inverse(x - xs[m], p)
                denom += (weight * inverse_diff) % p
            else:
                denom = 1
                break

        denominators.append(denom % p)

    for x, _ in enumerate(cuckoo_table.table):
        terms = []
        for j, (weight, y) in enumerate(zip(bary_weights, ys)):
            # If it's an interpolation node, the value of the polynomial at this node is y
            if x == xs[j]:
                terms = [y]
                break
            else:
                inverse_diff = modular_inverse((x - xs[j]) % p, p)
                num = (weight * inverse_diff) % p
                scaler = num * modular_inverse(denominators[x], p) % p
                scaled_y = y.scale(scaler)
                terms.append(scaled_y)

        lagrange_bases[x] = terms

    return lagrange_bases, len(xs) - 1


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
