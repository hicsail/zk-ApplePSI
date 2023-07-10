from cuckoo_table import CuckooTable
from pedersen_hash import pedersen_hash
from interpolation import lagrange_polynomial, compute_y
from picozk import *

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret

def make_Cuckoo(secrets, p, Points, alpha, epsilon):

    # Make a Cuckoo table
    table_size = len(secrets)*(1+epsilon)
    cuckoo_table = CuckooTable(secrets, table_size, p)

    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_emplist = cuckoo_table.get_non_emplist()
    for idx, secret in non_emplist:
        secret = secret.to_binary()
        gelm = pedersen_hash(secret, Points, p)
        gelm = gelm.scale(SecretInt(alpha))
        cuckoo_table.set_table_at(idx, gelm)

    # Make x list and y list
    xs = []
    ys = []

    for idx, _ in cuckoo_table.non_emplist:
        gelm = cuckoo_table.get_item_at(idx)
        xs.append(idx)
        ys.append(gelm)

    # Construct polynomial
    poly = lagrange_polynomial(xs, ys)

    # Calculate bots by the polynomial above
    emptyList = cuckoo_table.get_empty_indices()
    for bot_idx in emptyList:
        # p = poly.subs('x', bot_idx)
        p = compute_y(bot_idx, poly)
        cuckoo_table.set_table_at(bot_idx, p)

    return cuckoo_table, poly