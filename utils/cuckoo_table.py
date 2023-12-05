from dataclasses import dataclass
from picozk import *


@dataclass
class CuckooTable:
    def __init__(self, secrets: list, table_size: int, p):
        self.p = p
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.non_emplist = []
        self.bulk_set(secrets)

    def bulk_set(self, secrets):
        for item in secrets:
            self.orig_item = None
            self.set_item(item)

    def hash_one(self, item):
        return ((99529 * item + 37309) % self.p) % self.table_size

    def hash_two(self, item):
        return ((86837 * item + 40637) % self.p) % self.table_size

    def set_item(self, item, second=False):
        loop_history = 0

        while True:
            h_one = self.hash_one(item)
            h_two = self.hash_two(item)

            if h_one == h_two:  # Based on P10
                h_two += 1

            index = h_two if second else h_one

            if self.table[index] is None:
                self.table[index] = item
                evicted_item = None
                break

            elif (
                second is True and (item == self.orig_item or loop_history == self.table_size * 2)
            ):
                # Stop if we've looped back to the original item or exceed p * 2
                break

            else:
                # Swap the item at the index with the new item and try again
                item, self.table[index] = self.table[index], item
                second = True
            loop_history += 1

    def get_item_at(self, index):
        return self.table[index]

    def set_table_at(self, index, item):
        self.table[index] = item

    def get_non_emplist(self):
        return self.non_emplist
