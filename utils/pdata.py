from cuckoo_table import CuckooTable
from pedersen_hash_field import pedersen_hash_field
from interpolation import lagrange_poly
from curvepoint import CurvePoint
from picozk import *


def make_index_lists(cuckoo_table):
    non_emplist = []
    emptyList = list(range(cuckoo_table.table_size))
    for index in range(len(cuckoo_table.table)):
        if cuckoo_table.table[index] is not None:
            non_emplist.append((index, cuckoo_table.table[index]))
            emptyList.remove(index)
    return non_emplist, emptyList

def make_Cuckoo(secrets, p, Points, alpha, epsilon):

    # Make a Cuckoo table
    table_size = len(secrets)*(1+epsilon)
    cuckoo_table = CuckooTable(secrets, table_size, p)
    non_emplist, emptyList = make_index_lists(cuckoo_table)
        
    # Map each element in the Cuckoo Table onto an elliptic curve and exponentiate each element
    for idx, secret in non_emplist:
        _gelm = pedersen_hash_field(secret, Points, p)
        _gelm = CurvePoint(False, _gelm[0], _gelm[0], p)
        _gelm = _gelm.scale(alpha)
        cuckoo_table.set_table_at(idx, _gelm)
    
    # Make x list and y list
    xs = []
    ys = []

    for idx, _ in non_emplist:
        gelm = cuckoo_table.get_item_at(idx)
        xs.append(idx)
        ys.append(gelm)

    # Calculate bots by the polynomial above
    poly = lagrange_poly(xs, ys, p)
    for bot_idx in emptyList:
        bot, _ = poly(bot_idx)
        cuckoo_table.set_table_at(bot_idx, bot)

    # Open values and save as normal group elements
    for idx in range(len(cuckoo_table.table)):
        _gelm = cuckoo_table.get_item_at(idx)
        gelm = (val_of(_gelm.x),val_of(_gelm.y))
        cuckoo_table.set_table_at(idx, gelm)

    return cuckoo_table, non_emplist, poly