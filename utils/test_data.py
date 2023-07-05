from cuckoo_table import CuckooTable
from pedersen_hash import pedersen_hash
from interpolation import lagrange_polynomial

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
    for i in range(len(non_emplist)):
        idx, _ = non_emplist[i]
        secret = cuckoo_table.get_item_at(idx)
        elm = pedersen_hash(secret, Points, p)
        # elm = elm.scale(alpha) #TODO: Exponentiate the group element by alpha
        cuckoo_table.set_table_at(idx, elm)

    # Make x list and y list
    xs = []
    ys = []

    for idx, _ in cuckoo_table.non_emplist:
        gelm = cuckoo_table.get_item_at(idx)
        xs.append(idx)
        ys.append(gelm[1]) # TODO: Change this to group operation

    # Construct polynomial
    poly = lagrange_polynomial(xs, ys) # TODO: Change this to group operation

    # Calculate bots by the polynomial above
    emptyList = cuckoo_table.get_empty_indices()
    for bot_idx in emptyList:
        p = poly.subs('x', bot_idx)
        cuckoo_table.set_table_at(bot_idx, p)

    return cuckoo_table, poly