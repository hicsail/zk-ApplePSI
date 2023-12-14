from picozk import *
from picozk.poseidon_hash import PoseidonHash
from apple_psi.pedersen_hash import pedersen_hash
from apple_psi.interpolation import calc_polynomial
from apple_psi.helper import subset_test


def apple_psi(
    p,
    alpha,
    apple_secrets,
    ncmec_digest,
    Points,
    cuckoo_table,
    non_emplist,
    lagrange_bases,
    poly_degree,
):
    # Simulating Apple confirming their data is same as NCMEC image data
    print(f"Reconciling NCMEC Data with Apple Data", end="\r", flush=True)
    poseidon_hash = PoseidonHash(p, alpha=17, input_rate=3)
    apple_digest = poseidon_hash.hash(apple_secrets)
    assert0(ncmec_digest - val_of(apple_digest))

    print(f"Reconciling True Data in Cuckoo", end="\r", flush=True)
    for idx, val in non_emplist:
        # Prove that the set non_emplist is a subset of the set apple_secrets
        subset_test(apple_secrets, val)

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

    print(f"Validating that bots are drawn from the same curve", end="\r", flush=True)
    # Prove that all elements are on the same curve drawn by lagrange for idx in cuckoo_table.get_empty_indices():
    for idx, val in enumerate(cuckoo_table.table):
        gelm = calc_polynomial(idx, lagrange_bases)
        assert gelm.x == val.x
        assert gelm.y == val.y

    assert poly_degree == len(non_emplist) - 1
