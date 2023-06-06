from dataclasses import dataclass
from picozk import *

@dataclass
class CuckooTable:
    def __init__(self, secrets:list, table_size:int, p):
        self.p = p
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.empty_indices = list(range(self.table_size))
        self.non_emplist = []
        self.bulk_set(secrets)

    def hash_one(self, item):
        return ((99529 * item + 37309) % self.p) % self.table_size
    
    def hash_two(self, item):
        return ((86837 * item + 40637) % self.p) % self.table_size

    def set_item(self, item):
        index_h1 = self.hash_one(item)
        index_h2 = self.hash_two(item)
        if self.table[index_h1]==None:
            self.table[index_h1]=SecretInt(item, self.p)
            self.update_indices(index_h1)
        else:
            self.table[index_h2]=SecretInt(item, self.p)
            self.update_indices(index_h2)

    def get_item_at(self, index):
        return self.table[index]

    def replace_at(self, index, item):
        self.table[index]=item
    
    def set_non_emplist(self, index, item):
        self.non_emplist[index] = item

    def update_indices(self, index):
        if index in self.empty_indices:
            self.empty_indices.remove(index)
        self.non_emplist = [(i, self.table[i]) for i in range(self.table_size) if self.table[i] is not None]

    def bulk_set(self, secrets):
        for item in secrets:
            self.set_item(item)

    def get_table(self):
        return self.table
    
    def get_nonemp_size(self):
        return len(self.non_emplist)

    def get_emp_size(self):
        return len(self.empty_indices)

    def get_size(self):
        return len(self.table)

    def get_empty_indices(self):
        return self.empty_indices

    def get_non_emplist(self):
        return self.non_emplist
    
    def verify_non_emplist(self, secrets):
        curr_state = 1
        final_state = 0
        
        # Proof that each element in the original secret list exists in non-emp list
        for secret in secrets:
            for _, val in self.non_emplist:
                curr_state = mux(curr_state==final_state, final_state, mux(val==secret, final_state, curr_state))
            assert0(curr_state) 
        
        # Each non emptylist element exist in the indexed position of the table
        for idx, val in self.non_emplist:
            assert0(val- self.get_item_at(idx))
        
        # And no other values exists in the non-empty list than original secrets
        assert0(SecretInt(self.get_nonemp_size() - len(secrets)))