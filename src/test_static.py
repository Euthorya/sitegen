import unittest

from static import copy_static


class TestStatic(unittest.TestCase):
    def test_copy_static(self):
        x = copy_static()
        self.assertEqual(x, True)

if __name__ == "__main__":
    unittest.main()