import math
from dataclasses import dataclass

def remove_duplicates(secret:list): 
    _secret = []
    [_secret.append(x) for x in secret if x not in _secret]
    return _secret

@dataclass
class CuckooTable:
    def __init__(self, secrets:list, size_factor:float):
        secrets = remove_duplicates(secrets)
        self.size_factor = size_factor
        self.table_size = math.ceil(len(secrets)*(1+size_factor))
        self.table = [None] * self.table_size
        self.empty_indices = list(range(self.table_size))
        self.non_empty_indices = []
        self.bulk_set(secrets)

    # As nature of Cuckoo Table, it gives each element multiple choices for positions
    def hash_one(self, item):
        return item % self.table_size

    def hash_two(self, item):
        return (item // self.table_size) % self.table_size

    def set_item(self, item): 
        index_h1 = self.hash_one(item)
        loop_history = 0
        evicted_item = self.table[index_h1] if self.table[index_h1]!=None else None

        while evicted_item is not None:
            loop_history += 1
            if loop_history == self.table_size * 2: # give up if stuck in loop
                return False

            index_h2 = self.hash_two(evicted_item)

            if index_h1 == index_h2:
                index_h2 = (index_h1 + 1) % self.table_size
            ''' In case of collition even after two rounds of hashing, a new element take the place
                and the old element looks for a new place in the next iterations.
                It gives up if loop takes place twice as many time as the size of table, which indicates
                inifinite loop.
            '''

            old_evict_elem = evicted_item
            evicted_item = self.table[index_h2]

            self.table[index_h2] = old_evict_elem
            self.update_indices(index_h2, old_evict_elem)
            index_h1 = index_h2

        self.table[index_h1] = item
        self.update_indices(index_h1, item)
        return True

    def get_item_at(self, index):
        return self.table[index]

    def replace_at(self, index, item):
        self.table[index]=item

    def update_indices(self, index, item):
        if index in self.empty_indices:
            self.empty_indices.remove(index)
        self.non_empty_indices = [(i, self.table[i]) for i in range(self.table_size) if self.table[i] is not None]

    def bulk_set(self, secret):
        for item in secret:
            if not self.set_item(item):
                print(f"Failed to add item {item} due to hash collisions.")

    def get_table(self):
        return self.table

    def get_empty_indices(self):
        return self.empty_indices

    def get_non_empty_indices(self):
        return self.non_empty_indices


# Test the class
# secret = [1, 18, 3, 20, 37, 6, 7, 8, 9, 10] # The algorithm does not work if more than two 
# size=0.7
# table = CuckooTable(secret, size)
# print("")
# print("input", secret)
# output = table.get_table()
# print("output", output)
# print("empty indices", table.get_empty_indices())
# print("non-empty", table.get_non_empty_indices())

# empty = table.get_empty_indices()
# non = table.get_non_empty_indices()

# for e in empty:
#     if output[e]!=None:
#         print("False:empty at", e)
# print("passed")

# for n in non:
#     if output[n[0]]!=n[1]:
#         print("False:non-empty at", n[0])
# print("passed")