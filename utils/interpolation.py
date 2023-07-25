from picozk import *
import numpy as np
import itertools

def sym_polynomial(k, roots):

    return sum(np.prod(subset) for subset in itertools.combinations(roots, k))


def lagrange_coefficients(ai, bi, roots, p):

    n = len(roots)
    c_k_values = []

    for k in range(n):
        sigma = sym_polynomial(n-1-k, [root for root in roots if root != ai]) % p
        print("sigma", sigma)
        print("(-1)**(n-1-k)", (-1)**(n-1-k))
        print("modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai])), p)", modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai])), p))
        # a = ((-1)**(n-1-k) * sigma * modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai]) % p), p)) % p
        print("(sigma * modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai]), p)) % p)", (sigma * modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai]) % p), p)) % p)
        a = ((-1)**(n-1-k) * (sigma * modular_inverse(int(np.prod([ai - ak for ak in roots if ak != ai]) % p), p)) % p) % p
        print("a", a)
        c_k = bi.scale(int(a))
        c_k_values.append(c_k)
        print("c_k", c_k)
        print("")

    c_k_values.reverse()
    print("c_k_values", c_k_values)
    print("")

    return c_k_values


def lagrange_poly(xs, ys, p):

    n = len(xs)
    c_values = []

    for i in range(n):
        c_values.append(lagrange_coefficients(xs[i], ys[i], xs, p))

    coeffs = []

    for i in range(n):
        s = None
        for c in c_values:
            if s == None:
                s = c[i]
            else:
                s.add(c[i])
        coeffs.append(s)

    return coeffs
    
def calc_polynomial(x, coeffs):

    res = None

    for i, a in enumerate(reversed(coeffs)):

        if res == None:
            res = a.scale(x**i)
        else:
            res.add(a.scale(x**i))
    return res