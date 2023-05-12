from picozk import *
from curvepoint import CurvePoint

def lagrange_interpolation(points:list[CurvePoint], x, p):
    n = len(points)
    result = CurvePoint(False, 0, 0, p)

    for i in range(n):
        term = points[i].y
        for j in range(n):
            if j != i:
                term *= ((x - points[j].x) * modular_inverse(points[i].x - points[j].x, p)) % p
        result.y = (result.y + term) % p

    return result