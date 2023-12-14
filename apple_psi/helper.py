from picozk import *
from picozk.functions import picozk_function
import random


@picozk_function
def subset_test(apple_secrets, curr_val):
    final_state = 0
    curr_state = 1
    for i in range(len(apple_secrets)):
        curr_state = mux(
            curr_state == final_state,
            curr_state,
            mux(apple_secrets[i] == curr_val, final_state, curr_state),
        )
    assert0(curr_state)
    return curr_state


def remove_duplicates(secret: list):
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret


def count_rel(file_path):
    file_path += ".rel"
    # Initialize a variable to count lines
    line_count = 0

    # Open the file and read line by line
    with open(file_path, "r") as file:
        for line in file:
            line_count += 1

    million = 1000000
    line_count /= million

    # Print the total number of lines
    print(f"\n Total number of lines in the file: {line_count} (* 10^6)")

    return line_count


def make_secret(scale, p):
    res = []
    for i in range(scale):
        ent = random.randint(0, p)
        res += [ent]

    return res
