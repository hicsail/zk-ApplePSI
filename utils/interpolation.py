from picozk import *
from curvepoint import CurvePoint

def lagrange_interpolation(points:list[CurvePoint], x, p):
    n = len(points)
    result = CurvePoint(False, x, 0, p)

    for i in range(n):
        term = points[i][1]
        for j in range(n):
            if j != i:
                a = ((x - points[j][1].x) * modular_inverse(points[i][1].x - points[j][1].x, p)) % p
                term = term.scale(a)
        result = result.add(term)

    return result

# def lagrange_interpolation(points:list[CurvePoint], x, p):
#     n = len(points)
#     result = CurvePoint(False, x, 0, p)

#     for i in range(n):
#         term = points[i][1].y
#         for j in range(n):
#             if j != i:
#                 term *= ((x - points[j][1].x) * modular_inverse(points[i][1].x - points[j][1].x, p)) % p
#         result.y = (result.y + term) % p

#     return result