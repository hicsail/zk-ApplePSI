#TODO: Work on this file later
def hash_message(M):
    # Find the number of bits in M
    num_bits = M.bit_length()
    
    # Split M into two halves, a and b
    a = M >> (num_bits // 2)
    b = M & ((1 << (num_bits // 2)) - 1)
    
    # Hash a and b using the Pedersen hash
    return pedersen_hash(a, b)

def pedersen_hash(a, b, P):
    # Splitting input into high and low bits
    a_low = a & ((1 << 248) - 1)
    a_high = a >> 248
    b_low = b & ((1 << 248) - 1)
    b_high = b >> 248
    
    # Calculate the sum
    result = P[0]
    result += a_low * P[1]
    result += a_high * P[2]
    result += b_low * P[3]
    result += b_high * P[4]
    
    # Return the x-coordinate
    return result
