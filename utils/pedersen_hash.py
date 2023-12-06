import copy
from picozk import *


def pedersen_hash(M, Points, p):
    num_bits = p.bit_length()

    # Split M into two halves, a and b
    k = num_bits // 2
    a = M >> k
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
    result = copy.deepcopy(Points[0])
    result.x = (result.x + (a_low.val * Points[1].x) % p) % p
    result.x = (result.x + (a_high.val * Points[2].x) % p) % p
    result.x = (result.x + (b_low.val * Points[3].x) % p) % p
    result.x = (result.x + (b_high.val * Points[4].x) % p) % p

    result.y = (result.y + (a_low.val * Points[1].y) % p) % p
    result.y = (result.y + (a_high.val * Points[2].y) % p) % p
    result.y = (result.y + (b_low.val * Points[3].y) % p) % p
    result.y = (result.y + (b_high.val * Points[4].y) % p) % p

    return result
