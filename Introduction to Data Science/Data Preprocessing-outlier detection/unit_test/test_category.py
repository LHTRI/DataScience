import unittest
import pandas as pd
import numpy as np
import sys
from view_point.category import check_category


class MyTest(unittest.TestCase):
    """
    Test category
    """

    def test_check_category_with_valid_value(self):
        data_col = pd.Series(['a', 'b', 'a', 'a', 'b', 'b', 'b', 'a', 'c', 'c', 'c', 'c'])
        # TODO: call your function to check data_col with threshold=0.9
        result, _, out_line = check_category(data_col, 0.9)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)

    def test_check_category_with_empty_value(self):
        data_col = pd.Series([])
        # TODO: call your function to check data_col with threshold=0.9
        result, _, out_line = check_category(data_col, 0.9)
        self.assertEqual(result, 'NA')
        self.assertEqual(len(out_line), 0)

    # TODO: write your other unittest function here

    def test_check_category_with_one_value(self):
        data_col = pd.Series(['A'])
        # Check data_col with threshold=0.9
        result, _, out_line = check_category(data_col, 0.9)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)

    def test_check_category(self):
        A = pd.Series(['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a',
                       'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'b',
                       'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'a', 'c'])
        # Check A array with threshold=0.9
        result, _, out_line = check_category(A, 1)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)
        self.assertEqual(out_line, {})
        # Check B array with threshold=0.5
        result, _, out_line = check_category(A, 0.5)
        self.assertEqual(result, 'NG')
        self.assertEqual(len(out_line), 2)
        self.assertEqual(out_line, {21: 'b', 32: 'c'})

        B = pd.Series([1, 2])
        # Check B array with threshold=0
        result, _, out_line = check_category(B, 0)
        self.assertEqual(result, 'OK')
        self.assertEqual(len(out_line), 0)
        self.assertEqual(out_line, {})


if __name__ == '__main__':
    unittest.main()
