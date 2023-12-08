def pedersen_hash_int(M, Points, p):
    num_bits = p.bit_length()
    # Split M into two halves, a and b
    k = num_bits // 2
    a = M >> k
    b = M & ((1 << (num_bits // 2)) - 1)

    # Splitting input into high and low bits
    a_low = (a & ((1 << 248) - 1)) % p
    a_high = (a >> 248) % p
    b_low = (b & ((1 << 248) - 1)) % p
    b_high = (b >> 248) % p

    # Calculate the sum
    result_x = Points[0][0] % p
    result_y = Points[0][1] % p

    result_x = (result_x + (a_low * Points[1][0]) % p) % p
    result_x = (result_x + (a_high * Points[2][0]) % p) % p
    result_x = (result_x + (b_low * Points[3][0]) % p) % p
    result_x = (result_x + (b_high * Points[4][0]) % p) % p

    result_y = (result_y + (a_low * Points[1][1]) % p) % p
    result_y = (result_y + (a_high * Points[2][1]) % p) % p
    result_y = (result_y + (b_low * Points[3][1]) % p) % p
    result_y = (result_y + (b_high * Points[4][1]) % p) % p

    return result_x, result_y
