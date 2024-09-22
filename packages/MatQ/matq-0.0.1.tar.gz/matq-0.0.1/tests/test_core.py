import unittest
from MatQ.core import add, subtract

class TestMathOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(3, 2), 5)

    def test_subtract(self):
        self.assertEqual(subtract(3, 2), 1)

if __name__ == '__main__':
    unittest.main()