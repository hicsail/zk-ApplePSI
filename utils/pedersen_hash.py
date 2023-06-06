from curvepoint import CurvePoint

def pedersen_hash(M,p):

    # Points on the elliptic curve
    P = [CurvePoint(False, 
            2089986280348253421170679821480865132823066470938446095505822317253594081284, 
            1713931329540660377023406109199410414810705867260802078187082345529207694986,
            p),
        CurvePoint(False, 
            996781205833008774514500082376783249102396023663454813447423147977397232763, 
            1668503676786377725805489344771023921079126552019160156920634619255970485781,
            p),
        CurvePoint(False, 
            2251563274489750535117886426533222435294046428347329203627021249169616184184, 
            1798716007562728905295480679789526322175868328062420237419143593021674992973,
            p),
        CurvePoint(False, 
            2138414695194151160943305727036575959195309218611738193261179310511854807447, 
            113410276730064486255102093846540133784865286929052426931474106396135072156,
            p),
        CurvePoint(False, 
            2379962749567351885752724891227938183011949129833673362440656643086021394946, 
            776496453633298175483985398648758586525933812536653089401905292063708816422,
            p)]

    num_bits = len(M.wires)
    
    # Split M into two halves, a and b
    a = M >> (num_bits // 2)
    b = M & ((1 << (num_bits // 2)) - 1)

    # Splitting input into high and low bits
    a_low = a & ((1 << 248) - 1)
    a_high = a >> 248
    b_low = b & ((1 << 248) - 1)
    b_high = b >> 248

    a_low = a_low.to_arithmetic(field=p)
    a_high = a_high.to_arithmetic(field=p)
    b_low = b_low.to_arithmetic(field=p)
    b_high = b_high.to_arithmetic(field=p)

    # Calculate the sum
    result = P[0]
    result.x = result.x + a_low.val * P[1].x
    result.x = result.x + a_high.val * P[2].x
    result.x = result.x + b_low.val * P[3].x
    result.x = result.x + b_high.val * P[4].x

    result.y = result.y + a_low.val * P[1].y
    result.y = result.y + a_high.val * P[2].y
    result.y = result.y + b_low.val * P[3].y
    result.y = result.y + b_high.val * P[4].y

    # Return the resulting group point 
    return result