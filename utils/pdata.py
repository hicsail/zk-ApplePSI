from cuckoo_table import CuckooTable
from pedersen_hash import pedersen_hash
from interpolation import lagrange_poly
from picozk import *

def make_Cuckoo(secrets, p, Points, alpha, epsilon):

    # Make a Cuckoo table
    table_size = len(secrets)*(1+epsilon)
    cuckoo_table = CuckooTable(secrets, table_size, p)

    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    non_emplist = cuckoo_table.get_non_emplist()
    for idx, secret in non_emplist:
        secret = secret.to_binary()
        _gelm = pedersen_hash(secret, Points, p)
        _gelm = _gelm.scale(alpha)
        cuckoo_table.set_table_at(idx, _gelm)

    # Make x list and y list
    xs = []
    ys = []

    for idx, _ in cuckoo_table.non_emplist:
        gelm = cuckoo_table.get_item_at(idx)
        xs.append(idx)
        ys.append(gelm)

    # Calculate bots by the polynomial above
    emptyList = cuckoo_table.get_empty_indices()
    poly = lagrange_poly(xs, ys, p)
    for bot_idx in emptyList:
        bot, _ = poly(bot_idx)
        cuckoo_table.set_table_at(bot_idx, bot)

    # Open values and save as normal group elements
    for idx in range(len(cuckoo_table.table)):
        _gelm = cuckoo_table.get_item_at(idx)
        gelm = (val_of(_gelm.x),val_of(_gelm.y))
        cuckoo_table.set_table_at(idx, gelm)

    return cuckoo_table, poly