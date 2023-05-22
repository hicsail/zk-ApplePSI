from picozk import *

def pedersen_commitment(G, secret, alpha, H):
    return secret * G + alpha * H

def verify_commitment(G, commitment, secret, alpha, H):
    x_cor = SecretInt((secret * G + alpha * H).x())
    return assert0(commitment.x - x_cor)