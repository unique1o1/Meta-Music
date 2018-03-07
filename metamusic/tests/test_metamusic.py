import unittest


class Tests(unittest.TestCase):

    def test_unit_test(self):
        got = "hello"
        expected = "hello"
        self.assertEqual(got, expected)


if __name__ == '__main__':
    unittest.main()
