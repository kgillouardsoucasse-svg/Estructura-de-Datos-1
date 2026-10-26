import random
import unittest

from MyLinkedList import MyLinkedList


class TestMyLinkedList(unittest.TestCase):
    def assert_structure(self, linked, expected):
        node = linked._head
        last = None
        for value in expected:
            self.assertIsNotNone(node)
            self.assertEqual(node.data, value)
            last = node
            node = node.next
        self.assertIsNone(node)
        self.assertIs(linked._tail, last)
        self.assertEqual(len(linked), len(expected))
        self.assertEqual(linked.is_empty(), len(expected) == 0)

    def test_empty(self):
        linked = MyLinkedList()
        self.assert_structure(linked, [])
        self.assertEqual(str(linked), "None")
        self.assertEqual(linked.search(4), -1)
        with self.assertRaises(ValueError):
            linked.remove(4)

    def test_insert_and_update(self):
        linked = MyLinkedList()
        linked.insert(0, 20)
        linked.prepend(10)
        linked.append(40)
        linked.insert(2, 30)
        linked.insert(4, 50)
        linked.set(1, 25)
        self.assert_structure(linked, [10, 25, 30, 40, 50])
        self.assertEqual(linked.get(1), 25)
        self.assertEqual(list(linked), [10, 25, 30, 40, 50])
        self.assertEqual(str(linked), "10 -> 25 -> 30 -> 40 -> 50 -> None")

    def test_delete_and_reuse(self):
        linked = MyLinkedList([10, 20, 30, 40])
        self.assertEqual(linked.delete(1), 20)
        self.assertEqual(linked.delete(2), 40)
        self.assertEqual(linked.delete(0), 10)
        self.assertEqual(linked.delete(0), 30)
        self.assert_structure(linked, [])
        linked.append(99)
        self.assert_structure(linked, [99])

    def test_duplicates_and_none(self):
        linked = MyLinkedList([None, 8, 8])
        self.assertEqual(linked.search(None), 0)
        self.assertIn(None, linked)
        self.assertNotIn(9, linked)
        self.assertEqual(linked.remove(8), 8)
        self.assert_structure(linked, [None, 8])
        self.assertEqual(linked.search(8), 1)

    def test_invalid_indices(self):
        for linked in (MyLinkedList(), MyLinkedList([1, 2])):
            for index in (-1, len(linked), len(linked) + 1):
                with self.assertRaises(IndexError):
                    linked.get(index)
                with self.assertRaises(IndexError):
                    linked.set(index, 7)
                with self.assertRaises(IndexError):
                    linked.delete(index)
            for index in (-1, len(linked) + 1):
                with self.assertRaises(IndexError):
                    linked.insert(index, 7)
            for index in ("0", 1.5, None):
                with self.assertRaises(TypeError):
                    linked.get(index)
                with self.assertRaises(TypeError):
                    linked.insert(index, 7)

    def test_clear_and_reuse(self):
        linked = MyLinkedList([1, 2, 3])
        linked.clear()
        linked.clear()
        self.assert_structure(linked, [])
        linked.prepend(5)
        linked.append(6)
        self.assert_structure(linked, [5, 6])

    def test_random_operations_against_reference(self):
        rng = random.Random(42)
        linked = MyLinkedList()
        reference = []  
        for _ in range(500):
            operation = rng.choice(("append", "prepend", "insert", "delete", "set", "remove"))
            value = rng.randrange(10)
            if operation == "append":
                linked.append(value)
                reference.append(value)
            elif operation == "prepend":
                linked.prepend(value)
                reference.insert(0, value)
            elif operation == "insert":
                index = rng.randrange(len(reference) + 1)
                linked.insert(index, value)
                reference.insert(index, value)
            elif operation == "delete" and reference:
                index = rng.randrange(len(reference))
                self.assertEqual(linked.delete(index), reference.pop(index))
            elif operation == "set" and reference:
                index = rng.randrange(len(reference))
                linked.set(index, value)
                reference[index] = value
            elif operation == "remove":
                if value in reference:
                    self.assertEqual(linked.remove(value), value)
                    reference.remove(value)
                else:
                    with self.assertRaises(ValueError):
                        linked.remove(value)
            self.assert_structure(linked, reference)


if __name__ == "__main__":
    unittest.main()
