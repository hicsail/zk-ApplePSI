def pedersen_hash_field(M, Points, p):

    num_bits = M.bit_length()
    
    # Split M into two halves, a and b
    a = M >> (num_bits // 2)
    b = M & ((1 << (num_bits // 2)) - 1)

    # Splitting input into high and low bits
    a_low = a & ((1 << 248) - 1)
    a_high = a >> 248
    b_low = b & ((1 << 248) - 1)
    b_high = b >> 248

    # Calculate the sum
    result_x = Points[0][0]
    result_y = Points[0][1]
    result_x = (result_x + a_low * Points[1][0]) % p
    result_x = (result_x + a_high * Points[2][0]) % p
    result_x = (result_x + b_low * Points[3][0]) % p
    result_x = (result_x + b_high * Points[4][0]) % p

    result_y = (result_y + a_low * Points[1][1]) % p
    result_y = (result_y + a_high * Points[2][1]) % p
    result_y = (result_y + b_low * Points[3][1]) % p
    result_y = (result_y + b_high * Points[4][1]) % p

    # Return the resulting group point 
    return result_x, result_y