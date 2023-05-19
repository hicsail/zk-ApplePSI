from picozk import *

def pedersen_commitment(G, secret, blinding_factor, H):
    return secret * G + blinding_factor * H

def verify_commitment(G, commitment, secret, blinding_factor, H):
    x_cor = SecretInt((secret * G + blinding_factor * H).x())
    return assert0(commitment.x - x_cor)