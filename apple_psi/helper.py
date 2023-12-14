from picozk import *
from picozk.functions import picozk_function


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
