import unittest
import sys
sys.path.insert(1, './utils')
from cuckoo_table import CuckooTable

class TestCuckoo(unittest.TestCase):
    def test_cuckoo(self):
        # Test the class
        secret = [1, 18, 3, 20, 35, 6, 7, 8, 9, 10] # The algorithm does not work if more than two 
        size=0.7
        table = CuckooTable(secret, size)
        print("")
        print("input", secret)
        output = table.get_table()
        print("output", output)
        print("empty indices", table.get_empty_indices())
        print("non-empty", table.get_non_empty_indices())

        empty = table.get_empty_indices()
        non = table.get_non_empty_indices()
        flag = False
        for e in empty:
            self.assertIsNone(output[e])
            if output[e]!=None:
                flag=True
                print("False:empty at", e)

        for n in non:
            self.assertEqual(output[n[0]], n[1])
            if output[n[0]]!=n[1]:
                flag=True
                print("False:non-empty at", n[0])
        
        if flag:
            print("Failed")
        else:
            print("passed")

if __name__ == '__main__':
    unittest.main()
