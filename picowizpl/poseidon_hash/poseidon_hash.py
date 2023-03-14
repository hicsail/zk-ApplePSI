import numpy as np
from picowizpl import *
import picowizpl.poseidon_hash.poseidon_round_numbers as rn
import picowizpl.poseidon_hash.poseidon_round_constants as rc
import galois
from math import log2, ceil

class PoseidonHash:
    def __init__(self, p, alpha, input_rate, t, security_level = 128):
        self.p = p
        self.security_level = security_level
        self.prime_bit_len = ceil(log2(p))

        if np.gcd(alpha, p-1) == 1:
            self.alpha = alpha
        else:
            raise RuntimeError("Not available alpha")

        self.input_rate = input_rate
        self.t = t
        self.field_p = galois.GF(p)

        if 2 ** self.security_level > self.p ** self.t:
            raise RuntimeError("Not secure")

        self.full_round, self.partial_round, self.half_full_round = \
          rn.calc_round_numbers(log2(self.p),
                                security_level,
                                self.t, self.alpha, True)

        self.rc_field = rc.calc_round_constants(self.t,
                                                self.full_round,
                                                self.partial_round,
                                                self.p,
                                                self.field_p,
                                                self.alpha,
                                                self.prime_bit_len)
        self.rc_field = [int(x) for x in self.rc_field]
        self.mds_matrix = np.array(rc.mds_matrix_generator(self.field_p, self.t)).astype(int)

        self.state = [0 for _ in range(t)]

    def s_box(self, element):
        return pow(element, self.alpha)

    def full_rounds(self):
        for r in range(0, self.half_full_round):
            for i in range(0, self.t):
                self.state[i] = self.state[i] + self.rc_field[self.rc_counter]
                self.rc_counter += 1

                self.state[i] = self.s_box(self.state[i])

            self.state = np.dot(self.state, self.mds_matrix)

    def partial_rounds(self):
        for r in range(0, self.partial_round):
            for i in range(0, self.t):
                self.state[i] = self.state[i] + self.rc_field[self.rc_counter]
                self.rc_counter += 1
            self.state[0] = self.s_box(self.state[0])

            self.state = np.dot(self.state, self.mds_matrix)

    def hash(self, input_vec):
        self.rc_counter = 0
        padded_input = input_vec + [0 for _ in range(self.t-len(input_vec))]
        self.state = [padded_input[i] + self.state[i] for i in range(self.t)]

        self.full_rounds()
        self.partial_rounds()
        self.full_rounds()

        return self.state[1]
