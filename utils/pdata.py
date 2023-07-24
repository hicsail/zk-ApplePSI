from cuckoo_table import CuckooTable
from pedersen_hash_int import pedersen_hash_int
from interpolation import lagrange_poly, calc_polynomial
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
        _gelm = pedersen_hash_int(secret, Points, p)
        _gelm = CurvePoint(False, _gelm[0], _gelm[1], p)
        _gelm = _gelm.scale(alpha)
        cuckoo_table.set_table_at(idx, _gelm)
    
    # Make x list and y list
    xs = []
    ys = []

    for idx, _ in non_emplist: #TODO: Consider making it idx, val
        gelm = cuckoo_table.get_item_at(idx)
        xs.append(idx)
        ys.append(gelm)

    # Calculate bots by the polynomial above
    poly_coeffs = lagrange_poly(xs, ys, p)
    print("poly_coeffs", poly_coeffs)
    for bot_idx in emptyList:
        bot = calc_polynomial(bot_idx, poly_coeffs)
        cuckoo_table.set_table_at(bot_idx, bot)

    return cuckoo_table, poly_coeffs