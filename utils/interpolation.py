from picozk import *

def lagrange_interpolation(xs:list, ys:list, x, p):
    assert(len(xs)==len(ys))
    n = len(xs)
    result = None

    for i in range(n):
        term = ys[i]
        for j in range(n):
            if j != i:
                a = ((x - xs[j]) * modular_inverse(xs[i] - xs[j], p)) % p
                term = term.scale(SecretInt(a))

        if result is None:
            result = term
        else:
            result = result.add(term)

    return result