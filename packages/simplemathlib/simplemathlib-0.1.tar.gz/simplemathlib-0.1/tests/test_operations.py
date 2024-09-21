# tests/test_operations.py

import unittest
from simplemathlib import add, subtract  # Updated import to new package name


class TestOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)


if __name__ == "__main__":
    unittest.main()
