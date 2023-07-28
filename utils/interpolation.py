from picozk import *
def lagrange_poly(xs, ys, p):

    assert(len(xs)==len(ys))
    n = len(xs)

    def polynomial(X):
        result = None

        for i in range(n):
            term = ys[i]
            for j in range(n):
                if j != i:
                    a = ((X - xs[j]) * modular_inverse(xs[i] - xs[j], p)) % p
                    term = term.scale(a)

            if result is None:
                result = term
            else:
                if result.x != term.x or result.y != term.y:
                    result = result.add(term)
                else:
                    result = result.scale(2)

        return result, n-1

    return polynomial