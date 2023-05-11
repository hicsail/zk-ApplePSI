from curvepoint import CurvePoint

def lagrange_interpolation(points:list[CurvePoint], x, p):
    n = len(points)
    result = CurvePoint(False, 0, 0, p)

    for i in range(n):
        term = points[i].y
        for j in range(n):
            if j != i:
                term *= (x - points[j].x) / (points[i].x - points[j].x)
        result.y += term

    return result