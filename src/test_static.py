import unittest, os

from static import copy_static, PUBLIC_PATH, STATIC_PATH


class TestStatic(unittest.TestCase):
    def test_copy_static(self):
        copy_static()
        public_contents = os.listdir(PUBLIC_PATH)
        static_contents = os.listdir(STATIC_PATH)
        self.assertEqual(len(public_contents), len(static_contents))

if __name__ == "__main__":
    unittest.main()