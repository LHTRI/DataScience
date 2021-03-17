import unittest
import pandas as pd
import numpy as np
import sys 
from view_point.value_range import check_value_range


class MyTest(unittest.TestCase):

    def test_check_value_range_with_na_value(self):
        data_col = pd.Series(['a', 'b', 'a', 'a', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c'])
        # TODO: call your function to check data_col with threshold_range_z_score = 15, threshold_range_iqr=1.5
        result, _, out_line = check_value_range(data_col, 15, 1.5)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    def test_check_value_range_with_empty_value(self):
        data_col = pd.Series([])
        # TODO: call your function to check data_col with threshold_range_z_score = 15, threshold_range_iqr=1.5
        result, _, out_line = check_value_range(data_col, 15, 1.5)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    # TODO: write your other unittest functions here

    def test_check_value_range_with_one_value(self):
        data_col = pd.Series([0])
        # Call function to check data_col with threshold_range_z_score = 3, threshold_range_iqr=1.5
        result, _, out_line = check_value_range(data_col, 3, 1.5)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)

    def test_check_value_range_with_predictable_values(self):
        data_col = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 10000])
        # Call your function to check data_col with threshold_range_z_score = 3, threshold_range_iqr=1.5
        result, _, out_line = check_value_range(data_col, 3, 1.5)
        self.assertEqual(result, 'NG')
        self.assertEqual(len(out_line), 1)
        self.assertEqual(out_line, {8: 10000})

    def test_check_value_range_with_predictable_values_2(self):
        data_col = pd.Series([100000, 100000, 100000, 0, 100000, 100000, 100000, 100000])
        # Call your function to check data_col with threshold_range_z_score = 3, threshold_range_iqr=1.5
        result, _, out_line = check_value_range(data_col, 3, 1.5)
        self.assertEqual(result, 'NG')
        self.assertEqual(len(out_line), 1)
        self.assertEqual(out_line, {3: 0})


if __name__ == '__main__':
    unittest.main()
