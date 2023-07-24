import unittest
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

    # The has functions are made simplier so the test for eviction is simpler
    def hash_one(self, item):
        return item % self.table_size
    
    def hash_two(self, item):
        return (1+item) % self.table_size
    
    def set_item(self, item, second=False):

        if self.orig_item == None:
            self.orig_item = item
        elif self.orig_item == item:
            print("Giving up:", item)
            return

        index = self.hash_two(item) if second==True else self.hash_one(item)

        if self.table[index] == None:
            self.table[index] = item
            self.orig_item = None
            print("Set item:", item, "at:", index, "table:", self.table)
            return
        else:
            _item = self.table[index]
            self.table[index] = item
            print("Set item:", item, "at:", index, "Evicting:", _item,  "table:", self.table)
            self.set_item(_item, second=True)


class Test_Base(unittest.TestCase):
    def test_eviction(self):
        secrets = [ 0,1,2,3,4,5,6,7,8,9, 11]
        table_size = len(secrets)-1
        p = 3
        cuckoo_table = CuckooTable(secrets, table_size, p)
        print("Result:", cuckoo_table.table)
        self.assertEqual(cuckoo_table.table, [9, 0, 1, 2, 3, 4, 5, 6, 7, 8])

if __name__ == '__main__':
    unittest.main()
