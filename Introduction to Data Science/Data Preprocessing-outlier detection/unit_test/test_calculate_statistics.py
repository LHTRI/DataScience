import unittest
import pandas as pd
import numpy as np
import sys
from utils.utility import calculate_statistics


class MyTest(unittest.TestCase):
    """
    Test calculate_statistics
    """

    def test_calculate_statistics_empty_value(self):
        data = []
        mean, stdev, z_score_list = calculate_statistics(data)
        self.assertEqual(mean, None)
        self.assertEqual(stdev, None)
        self.assertEqual(z_score_list, None)

    def test_calculate_statistics_one_value(self):
        data = [1]
        mean, stdev, z_score_list = calculate_statistics(data)
        self.assertEqual(mean, None)
        self.assertEqual(stdev, None)
        self.assertEqual(z_score_list, None)

    def test_calculate_statistics_value(self):
        data = [1, 1]
        mean, stdev, z_score_list = calculate_statistics(data)
        self.assertEqual(mean, 1)
        self.assertEqual(stdev, 0)
        self.assertEqual(z_score_list, [0, 0])


if __name__ == '__main__':
    unittest.main()
