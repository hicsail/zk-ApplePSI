import numpy as np
import itertools
from curvepoint import CurvePoint


#Borrowing from picozk
def _extended_gcd(a, b):
   """
   Division in integers modulus p means finding the inverse of the
   denominator modulo p and then multiplying the numerator by this
   inverse (Note: inverse of A is B such that A*B % p == 1) this can
   be computed via extended Euclidean algorithm
   """
   x = 0
   last_x = 1
   y = 1
   last_y = 0
   while b != 0:
       quot = a // b
       a, b = b, a % b
       x, last_x = last_x - quot * x, x
       y, last_y = last_y - quot * y, y
   return last_x, last_y

def modular_inverse(x, p):
   """Compute the inverse of x mod p, i.e. b s.t. x*b mod p = 1"""
   b, _ = _extended_gcd(x, p)
   return b % p


def sym_polynomial(k, xs, p):
    return sum(np.prod(subset) % p for subset in itertools.combinations(xs, k))

'''
Findings:
- g.scale((a-b)/d) != g.scale(a).add(g.(modinv(b))).scale(modinv(d))
- g.scale((a-b)/d) != g.scale(a-b).scale(modinv(d))
- num and denom are always int == float
'''

def lagrange_coefficients(xi, yi, xs, p):
    n = len(xs)
    c_k_values = []
    # denom = modular_inverse(np.prod([xi - x for x in xs if x != xi]) % p, p) % p
    _denom = np.prod([xi - x for x in xs if x != xi]) % p
    
    for k in range(n):
        sigma = sym_polynomial(n - 1 - k, [x for x in xs if x != xi], p) % p
        num = (-1) ** (n - 1 - k) * sigma % p
        mul = num/_denom
        # assert mul == int(mul) #Find a way to scale by fraction
        if yi.is_infinity == False:
            scaled = yi.scale(int(mul))
            c_k_values.append(scaled)
        else:
            c_k_values.append(yi)

    return c_k_values


def lagrange_poly(xs, ys, p):
    n = len(xs)
    c_k_values = [lagrange_coefficients(xs[i], ys[i], xs, p) for i in range(n)]
    lagrange_coeffs = []

    for i in range(n):
        coef = CurvePoint(True, 0, 0, p)
        for c in c_k_values:
            if coef.x != c[i].x or coef.y != c[i].y:
                coef = coef.add(c[i])
            else:
                # assert 1 == 0
                coef = coef.scale(2)
        lagrange_coeffs.append(coef)

    return lagrange_coeffs


def calc_polynomial(x, lagrange_coeffs, p):
    res = CurvePoint(True, 0, 0, p)

    for i, coeff in enumerate(reversed(lagrange_coeffs)):
        scaled = coeff.scale(x**i)

        if scaled.x != res.x or scaled.y != res.y:
            res = res.add(scaled)
        else:
            # assert 1 == 0
            res = res.scale(2)

    return res