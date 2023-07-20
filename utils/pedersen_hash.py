import copy
from picozk import *
def pedersen_hash(M, Points, p):

    num_bits = len(M.wires)
    
    # Split M into two halves, a and b
    a = M >> (num_bits // 2)
    print("a Secint", val_of(a.to_arithmetic(field=p)))
    b = M & ((1 << (num_bits // 2)) - 1)
    print("b Secint", val_of(b.to_arithmetic(field=p)))

    # Splitting input into high and low bits
    a_low = a & ((1 << 248) - 1)
    a_high = a >> 248
    b_low = b & ((1 << 248) - 1)
    b_high = b >> 248

    a_low = a_low.to_arithmetic(field=p)
    a_high = a_high.to_arithmetic(field=p)
    b_low = b_low.to_arithmetic(field=p)
    b_high = b_high.to_arithmetic(field=p)
    print("b_low secint", val_of(b_low), "b_high", val_of(b_high))

    # Calculate the sum
    result = copy.deepcopy(Points[0])

    result.x = result.x + a_low.val * Points[1].x
    result.x = result.x + a_high.val * Points[2].x
    result.x = result.x + b_low.val * Points[3].x
    result.x = result.x + b_high.val * Points[4].x

    result.y = result.y + a_low.val * Points[1].y
    result.y = result.y + a_high.val * Points[2].y
    result.y = result.y + b_low.val * Points[3].y
    result.y = result.y + b_high.val * Points[4].y

    return result