import math
from dataclasses import dataclass
from picozk import *

@dataclass
class CuckooTable:
    def __init__(self, secrets:list, size_factor:float, p):
        self.p = p
        self.size_factor = size_factor
        self.table_size = math.ceil(len(secrets)*(1+size_factor))
        self.table = [None] * self.table_size
        self.empty_indices = list(range(self.table_size))
        self.non_empty_indices = []
        self.bulk_set(secrets)

    def hash_one(self, item):
        return ((99529 * item + 37309) % self.p) % self.table_size
    
    def sec_hash_one(self, item): #FIXME
        numerator = ((99529 * item + 37309) % self.p)
        denomitor=self.table_size
        res = numerator * modular_inverse(denomitor, self.p) % self.p # Result of division
        mod = numerator - denomitor * res
        return  mod
        # return ((99529 * item + 37309) % self.p) % self.table_size

    def hash_two(self, item):
        return ((86837 * item + 40637) % self.p) % self.table_size

    def sec_hash_two(self, item): #FIXME
        numerator = ((86837 * item + 40637) % self.p)
        denomitor=self.table_size
        res = numerator * modular_inverse(denomitor, self.p) % self.p # Result of division
        mod = numerator - denomitor * res
        return  mod
        # return ((86837 * item + 40637) % self.p) % self.table_size

    def set_item(self, item):
        index_h1 = self.hash_one(item)
        index_h2 = self.hash_two(item)
        if self.table[index_h1]==None:
            self.table[index_h1]=item
            self.update_indices(index_h1, item)
        else:
            self.table[index_h2]==item
            self.update_indices(index_h2, item)

    def get_item_at(self, index):
        return self.table[index]

    def replace_at(self, index, item):
        self.table[index]=item
    
    def set_non_emplist(self, index, item):
        self.non_empty_indices[index] = item

    def update_indices(self, index, item):
        if index in self.empty_indices:
            self.empty_indices.remove(index)
        self.non_empty_indices = [(i, self.table[i]) for i in range(self.table_size) if self.table[i] is not None]

    def bulk_set(self, secret):
        for item in secret:
            self.set_item(item)

    def get_table(self):
        return self.table

    def get_empty_indices(self):
        return self.empty_indices

    def get_non_empty_indices(self):
        return self.non_empty_indices
    
    def verify_hash(self):
        for idx, val in self.non_empty_indices:
            idx1 = self.sec_hash_one(SecretInt(val))-idx
            idx2 = self.sec_hash_two(SecretInt(val))-idx
            assert0(idx1*idx2)



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