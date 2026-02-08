import unittest

class TestBasic(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(1, 1)

    def test_not_equal(self):
        self.assertNotEqual(1, 2)

if __name__ == '__main__':
    unittest.main()