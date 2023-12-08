import numpy as np
import itertools

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


def _lagrange_coefficients(xi, yi, xs, p):
    n = len(xs)
    c_k_values = []
    denom = modular_inverse(np.prod([xi - x for x in xs if x != xi]) % p, p) % p

    for k in range(n):
        sigma = sym_polynomial(n - 1 - k, [x for x in xs if x != xi], p) % p
        num = (-1) ** (n - 1 - k) * sigma % p
        term = (num * denom) % p
        c_k = yi * int(term)
        c_k_values.append(c_k)

    return c_k_values


def _lagrange_poly(xs, ys, p):
    n = len(xs)
    c_values = [_lagrange_coefficients(xs[i], ys[i], xs, p) for i in range(n)]
    coeffs = []

    for i in range(n):
        coef = 0
        for c in c_values:
            coef += c[i] % p

        coeffs.append(coef)

    return coeffs

def _calc_polynomial(x, coeffs):
    res = 0

    for i, coeff in enumerate(coeffs):
        scaled = coeff*(x**i)
        res += scaled

    return res


xs = [0, 1, 2]
ys = [0, 1, 4]
p = 11  # Example modulus, can be changed or removed if not doing modular arithmetic

coeffs = _lagrange_poly(xs, ys, p)

# Output the coefficients for verification
print("Coefficients:", coeffs)

# Test the polynomial at a new point, for example, x = 2

x_test = 0
y_test = _calc_polynomial(x_test, coeffs) % p
print(f"Polynomial evaluated at x = {x_test}: y = {y_test}")
assert y_test == 0

x_test = 1
y_test = _calc_polynomial(x_test, coeffs) % p
print(f"Polynomial evaluated at x = {x_test}: y = {y_test}")
assert y_test == 1

x_test = 2
y_test = _calc_polynomial(x_test, coeffs) % p
print(f"Polynomial evaluated at x = {x_test}: y = {y_test}")
assert y_test == 4

x_test = 3
y_test = _calc_polynomial(x_test, coeffs) % p
print(f"Polynomial evaluated at x = {x_test}: y = {y_test}")
assert y_test == 9 % p
