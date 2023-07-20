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
            self.orig_item = None
            self.set_item(item)

    def hash_one(self, item):
        return ((99529 * item + 37309) % self.p) % self.table_size
    
    def hash_two(self, item):
        return ((86837 * item + 40637) % self.p) % self.table_size

    def set_item(self, item, second=False):

        if self.orig_item == None:
            self.orig_item = item
        elif self.orig_item == item:
            return

        index = self.hash_two(item) if second==True else self.hash_one(item)
        if self.table[index] == None:
            self.table[index] = item
            self.orig_item = None
            return
        else:
            _item = self.table[index].copy()
            self.table[index] = item
            self.set_item(_item, second=True)

    def get_item_at(self, index):
        return self.table[index]

    def set_table_at(self, index, item):
        self.table[index]=item

    def get_non_emplist(self):
        return self.non_emplist