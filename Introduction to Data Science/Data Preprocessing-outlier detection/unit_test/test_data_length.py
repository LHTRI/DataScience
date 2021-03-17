import unittest
import pandas as pd
import numpy as np
import sys 
from view_point.data_length import check_length


class MyTest(unittest.TestCase):

    def test_check_length_with_valid_value(self):
        data_col = pd.Series(['a', 'b', 'd', 'e', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c'])
        # TODO: call your function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)

    # TODO: write your unittest function here
    def test_check_length_with_number_value(self):
        data_col = pd.Series(['a', 1, 'd', 'e', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c'])
        # Call function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    def test_check_length_with_nan_value(self):
        data_col = pd.Series(['a', np.nan, 'd', 'e', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c'])
        # Call function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    def test_check_length_with_NG_value(self):
        data_col = pd.Series(['a', 'b', 'd', 'NG', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c', '1', '2'])
        # Call function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'NG')
        self.assertEqual(len(out_line), 1)
        self.assertEqual(out_line, {3: 'NG'})  # {index: value}

    def test_check_length_with_empty_value(self):
        data_col = pd.Series([])
        # Call function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    def test_check_length_with_white_space_value(self):
        data_col = pd.Series([''])
        # Call function to check data_col with threshold=0.9
        result, _, out_line = check_length(data_col, 0.9)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)


if __name__ == '__main__':
    unittest.main()
