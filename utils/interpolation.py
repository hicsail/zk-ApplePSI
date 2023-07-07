from picozk import *

# def lagrange_polynomial(x_values, y_values, p):
#     n = len(x_values)
#     coeffs = [None for _ in range(n)]  # Initialize coefficients list

#     for i in range(n):
#         # Compute coefficients of the i-th Lagrange basis polynomial
#         basis_coeffs = [1]
#         for j in range(n):
#             if i != j:
#                 new_coeffs = [0 for _ in range(len(basis_coeffs) + 1)]
#                 for k in range(len(basis_coeffs)):
#                     new_coeffs[k] -= basis_coeffs[k]*x_values[j] / (x_values[i] - x_values[j])
#                     new_coeffs[k + 1] += basis_coeffs[k] / (x_values[i] - x_values[j])
#                 basis_coeffs = new_coeffs
        
#         for k in range(len(basis_coeffs)):
#             coeffs[k] = y_values[i].scale(SecretInt(basis_coeffs[k]%p))

#     return coeffs

#TODO: This is wrong, so modify the above func
def lagrange_polynomial(x_values, y_values):
    n = len(x_values)
    coeffs = [None]*n  # Initialize coefficients list

    for i in range(n):
        for j in range(n):
            if i != j:
                term = 1
                for k in range(n):
                    if k != i and k != j:
                        term *= (x_values[k] - x_values[i]) / (x_values[j] - x_values[i])
                if coeffs[j]==None:
                    coeffs[j] = y_values[i].scale(SecretInt(term))
                else:
                    coeffs[j] = coeffs[j].add(y_values[i].scale(SecretInt(term)))

    return coeffs

def compute_y(x, poly):
    y = None
    for i, coeff in enumerate(poly):
        if y==None:
            y = coeff.scale(SecretInt(x**i))
        else:
            y = y.add(coeff.scale(SecretInt(x**i)))
    return y


# from picozk import *
# from sympy import symbols, expand

# def lagrange_polynomial(x_values, y_values):
#     x = symbols('x')  # define the variable
#     n = len(x_values)
#     L = 0  # Initialize Lagrange polynomial

#     for i in range(n):
#         term = 1
#         for j in range(n):
#             if i != j:
#                 term *= (x - x_values[j]) / (x_values[i] - x_values[j])
#         if L == 0:
#             L = y_values[i]
#         else:
#             L = L.add(y_values[i])
#             # L = L.add(y_values[i].scale(term))
    
#     return expand(L)

# from picozk import *
# from curvepoint import CurvePoint

# def lagrange_interpolation(points:list[CurvePoint], x, p):
#     n = len(points)
#     result = CurvePoint(False, x, 0, p)

#     for i in range(n):
#         term = points[i][1]
#         for j in range(n):
#             if j != i:
#                 a = ((x - points[j][1].x) * modular_inverse(points[i][1].x - points[j][1].x, p)) % p
#                 term = term.scale(a)
#         result = result.add(term)

#     return result