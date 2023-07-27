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
        num  = (-1)**(n-1-k) * sigma % p
        denom = modular_inverse(np.prod([ai - ak for ak in roots if ak != ai]) % p, p) % p
        term = num * denom % p
        if bi.is_infinity==False:
            c_k = bi.scale(int(term))
        c_k_values.append(c_k)
    c_k_values.reverse()

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
                if s.x != c[i].x or s.y != c[i].y:
                    s = s.add(c[i])
                else:
                    s = s.scale(2)
                    
        coeffs.append(s)
    return coeffs
    
def calc_polynomial(x, coeffs):

    res = None

    for i, coeff in enumerate(reversed(coeffs)):
        scaled = coeff.scale(x**i)
        if res == None:
            res = scaled
        else:
            if scaled.x != res.x or scaled.y != res.y:
                res = res.add(scaled)
            else:
                res = res.scale(2)
    return res