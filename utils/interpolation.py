from picozk import *
import numpy as np
import itertools

def sym_polynomial(k, roots):
    return sum(np.prod(subset) for subset in itertools.combinations(roots, k))

def lagrange_coefficients(ai, bi, roots, p):
    n = len(roots)
    c_k_values = []
    for k in range(n):
        sigma = sym_polynomial(n-1-k, [root for root in roots if root != ai])
        a = ((-1)**(n-1-k) * sigma / np.prod([ai - ak for ak in roots if ak != ai])) % p
        c_k = bi.scale(a) 
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
                s.add(c[i])
        coeffs.append(s)
    
    def polynomial(x):
        res = None
        for i, a in enumerate(reversed(coeffs)):
            if res == None:
                res = a.scale(x**i)
            else:
                res.add(a.scale(x**i))
        return res

    return polynomial


# def lagrange_poly(xs, ys, p):

#     assert(len(xs)==len(ys))
#     n = len(xs)

#     def polynomial(X):
#         result = None

#         for i in range(n):
#             term = ys[i]
#             for j in range(n):
#                 if j != i:
#                     a = ((X - xs[j]) * modular_inverse(xs[i] - xs[j], p)) % p
#                     term = term.scale(a)

#             if result is None:
#                 result = term
#             else:
#                 result = result.add(term)

#         return result

#     return polynomial