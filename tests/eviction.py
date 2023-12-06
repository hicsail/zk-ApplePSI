import unittest


class CuckooTable:
    def __init__(self, secrets: list, table_size: int, p):
        self.p = p
        self.table_size = table_size
        self.table = [None] * self.table_size
        self.non_emplist = []
        self.bulk_set(secrets)

    def bulk_set(self, secrets):
        for item in secrets:
            self.orig_item = item
            self.set_item(item)

    # The has functions are made simplier so the test for eviction is simpler
    def hash_one(self, item):
        return item % self.table_size

    def hash_two(self, item):
        return (1 + item) % self.table_size

    def set_item(self, item, second=False):
        print("curr orig", self.orig_item)
        loop_history = 0

        while True:
            h_one = self.hash_one(item)
            h_two = self.hash_two(item)

            if h_one == h_two:  # Based on P10
                h_two += 1

            index = h_two if second else h_one

            if self.table[index] is None:
                self.table[index] = item
                print(f"Set item: {item} at: {index} table: {self.table}")
                break

            elif (
                second is True and (item == self.orig_item or loop_history == self.table_size * 2)
            ):
                if item == self.orig_item:
                    print("Back to original")
                else:
                    print("Exceeded table size * 2")
                # Stop if we've looped back to the original item or exceed p * 2
                break
            
            else:
                # Swap the item at the index with the new item and try again
                item, self.table[index] = self.table[index], item
                second = True
                print(
                    f"Set item: {self.table[index]} at: {index} Evicting: {item} table: {self.table}"
                )

            loop_history += 1


class Test_Base(unittest.TestCase):
    def test_eviction(self):
        secrets = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11]
        table_size = len(secrets) - 1
        p = 3
        cuckoo_table = CuckooTable(secrets, table_size, p)
        print("Result:", cuckoo_table.table)
        self.assertEqual(cuckoo_table.table, [9, 0, 1, 2, 3, 4, 5, 6, 7, 8])


if __name__ == "__main__":
    unittest.main()
