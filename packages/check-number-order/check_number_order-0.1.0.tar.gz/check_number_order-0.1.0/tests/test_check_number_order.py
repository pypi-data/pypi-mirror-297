import unittest
from check_number_order.check_number_order import check_number_order

class TestCheckNumberOrder(unittest.TestCase):
    def test_increasing_order(self):
        result = check_number_order(12345, "Increasing", "Not Increasing")
        self.assertEqual(result, "Increasing")

    def test_decreasing_order(self):
        result = check_number_order(54321, "Increasing", "Not Increasing")
        self.assertEqual(result, "Increasing")

    def test_no_order(self):
        result = check_number_order(12343, "Increasing", "Not Increasing")
        self.assertEqual(result, "Not Increasing")

if __name__ == '__main__':
    unittest.main()