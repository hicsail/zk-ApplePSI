from dataclasses import dataclass
from picozk import *

@dataclass
class CuckooTable:
    def __init__(self, secrets:list, table_size:int, p):
        self.p = p
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.non_emplist = []
        self.bulk_set(secrets)
    
    def bulk_set(self, secrets):
        for item in secrets:
            self.set_item(item)

    def hash_one(self, item):
        return ((99529 * item + 37309) % self.p) % self.table_size
    
    def hash_two(self, item):
        return ((86837 * item + 40637) % self.p) % self.table_size

    def set_item(self, item):
        for _ in range(self.table_size):  # Limit the number of relocations to avoid infinite loops
            # Calculate the hash values
            index_h1 = self.hash_one(item)
            index_h2 = self.hash_two(item)

            # If either location is available, place the item there
            # If neither location is available, evict and relocate the item in the second
            if self.table[index_h1] == None:
                self.table[index_h1] = SecretInt(item, self.p)
                return
            elif self.table[index_h2] == None:
                self.table[index_h2] = SecretInt(item, self.p)
                return
            else:
                item, self.table[index_h2] = self.table[index_h2], SecretInt(item, self.p)

    def get_item_at(self, index):
        return self.table[index]

    def set_table_at(self, index, item):
        self.table[index]=item

    def get_non_emplist(self):
        return self.non_emplist