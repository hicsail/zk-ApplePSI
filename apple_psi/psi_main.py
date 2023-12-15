import time
from picozk import *
from picozk.poseidon_hash import PoseidonHash
from apple_psi.pedersen_hash import pedersen_hash
from apple_psi.interpolation import calc_polynomial


def apple_psi(
    p,
    alpha,
    apple_secrets,
    _apple_secrets,
    ncmec_digest,
    Points,
    cuckoo_table,
    non_emplist,
    perm_map,
    lagrange_bases,
    poly_degree,
):
    # Simulating Apple confirming their data is same as NCMEC image data
    print(f"Reconciling NCMEC Data with Apple Data", end="\r", flush=True)
    poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
    apple_digest = poseidon_hash.hash(apple_secrets)
    assert0(ncmec_digest - val_of(apple_digest))

    tiem_res = []
    print(f"Reconciling True Data in Cuckoo", end="\r", flush=True)
    group_ops_start = time.time()
    
    for perm_idx, (idx, val) in enumerate(non_emplist):
        # Prove that the set non_emplist is a subset of the set apple_secrets
        assert0(_apple_secrets[perm_map[perm_idx]] - val)

        # Prove that each real element exists in hash one or two
        h1 = cuckoo_table.hash_one(val)
        h2 = cuckoo_table.hash_two(val)
        assert0((h1 - idx) * (h2 - idx))

        # Prove that hash_to_curve(val)^alpha is performed appropriately
        val = val.to_binary()
        gelm = pedersen_hash(val, Points, p)
        gelm = gelm.scale(alpha)
        table_elm = cuckoo_table.get_item_at(idx)
        assert0(gelm.x - table_elm.x)
        assert0(gelm.y - table_elm.y)
    group_ops_end = time.time()
    tiem_res.append(group_ops_end - group_ops_start)

    if lagrange_bases != None:
        print(
            f"Validating that bots are drawn from the same curve", end="\r", flush=True
        )
        bots_check_start = time.time()
        # Prove that all elements are on the same curve drawn by lagrange for idx in cuckoo_table.get_empty_indices():
        for idx, val in enumerate(cuckoo_table.table):
            gelm = calc_polynomial(idx, lagrange_bases)
            assert gelm.x == val.x
            assert gelm.y == val.y
        tiem_res.append(group_ops_end - group_ops_start)
        assert poly_degree == len(non_emplist) - 1
        bots_check_end = time.time()
        tiem_res.append(bots_check_end - bots_check_start)

    return tiem_res
