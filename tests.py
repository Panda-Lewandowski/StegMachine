import unittest

class TestTestCase(unittest.TestCase):
    def test_hello_world(self):
        test_str = "hello world"
        self.assertEqual(test_str, "hello world")


if __name__ == '__main__':
    unittest.main()