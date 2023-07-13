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
                if val_of(term.is_infinity) != False:
                    print("idx", X)
                    print("n", n)
                    print("error at", i, "term", term)
                    assert val_of(term.is_infinity) == False
                
                if val_of(result.is_infinity) != False:
                    print("idx", X)
                    print("n", n)
                    print("error at", i, "term", term)
                    assert val_of(result.is_infinity) == False
                result = result.add(term) #Error occurs here when X (index in the table) is 2

        return result

    return polynomial