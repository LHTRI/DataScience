import unittest
import pandas as pd
import numpy as np
import sys
from utils.utility import calculate_quartile


class MyTest(unittest.TestCase):
    """
    Test calculate_quartile
    """

    def test_calculate_quartile_empty_value(self):
        data = []
        Q1, Q2, Q3, _ = calculate_quartile(data)
        self.assertEqual(Q1, None)
        self.assertEqual(Q2, None)
        self.assertEqual(Q3, None)

    def test_calculate_quartile_one_value(self):
        data = [3]
        Q1, Q2, Q3, _ = calculate_quartile(data)
        self.assertEqual(Q1, 3)
        self.assertEqual(Q2, 3)
        self.assertEqual(Q3, 3)

    def test_calculate_quartile_two_value(self):
        data = [1, 3]
        Q1, Q2, Q3, _ = calculate_quartile(data)
        self.assertEqual(Q1, 1)
        self.assertEqual(Q2, 2)
        self.assertEqual(Q3, 3)

    def test_calculate_quartile_value(self):
        data = [1, 2, 3, 4, 5]
        Q1, Q2, Q3, _ = calculate_quartile(data)
        self.assertEqual(Q1, 1.5)
        self.assertEqual(Q2, 3)
        self.assertEqual(Q3, 4.5)


if __name__ == '__main__':
    unittest.main()
