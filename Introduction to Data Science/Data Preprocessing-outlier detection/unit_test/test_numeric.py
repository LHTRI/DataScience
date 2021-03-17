import unittest
import pandas as pd
import numpy as np
import sys 
from view_point.numeric import *


class NumericTest(unittest.TestCase):

    def test_check_numeric(self):
        A = pd.Series(
            ['1', ' 2a', '０１２５', 'a', '-2', '-2', '00.0', '000', '0.0000', '2.3', '67', '1213', '-1'])
        B = pd.Series(
            ['1', '2', '3', 'a', '-2', '2', '-2.34', '000', '0.0000', '.2', '0', '-123'])
        C = pd.Series(['1', '2.345', '0', '-1'])

        # TODO: call your function to check A array and threshold = 0.9
        result1, k1, N1, _, out_line = check_numeric(A, 0.9)
        self.assertEqual(result1, 'NA')
        self.assertEqual(k1, 11)
        self.assertEqual(N1, 13)
        self.assertEqual(len(out_line), 0)

        # TODO: call your function to check B array and threshold = 0.9
        result2, k2, N2, _, out_line2 = check_numeric(B, 0.9)
        self.assertEqual(result2, 'NG')
        self.assertEqual(k2, 11)
        self.assertEqual(N2, 12)
        self.assertEqual(len(out_line2), 1)

        # TODO: call your function to check C array and threshold = 0.9
        result3, k3, N3, _, out_line3 = check_numeric(C, 0.9)
        self.assertEqual(result3, 'OK')
        self.assertEqual(k3, 4)
        self.assertEqual(N3, 4)
        self.assertEqual(len(out_line3), 0)

        # TODO: call your function to check A array and threshold = 0
        result10, k10, N10, _, out_line10 = check_numeric(A, 0)
        self.assertEqual(result10, 'NG')
        self.assertEqual(k10, 11)
        self.assertEqual(N10, 13)
        self.assertEqual(len(out_line10), 2)

        # TODO: call your function to check A array and threshold = 1
        result11, k11, N11, _, out_line11 = check_numeric(A, 1)
        self.assertEqual(result11, 'NA')
        self.assertEqual(k11, 11)
        self.assertEqual(N11, 13)
        self.assertEqual(len(out_line11), 0)

    def test_check_numeric_with_empty_value(self):
        A = pd.Series([])

        # Call function to get result and detail error
        result, k, N, _, out_line = check_numeric(A, 0.9)
        self.assertEqual(result, 'NA')
        self.assertEqual(k, 0)
        self.assertEqual(N, 0)
        self.assertEqual(len(out_line), 0)

    # TODO: write your unittest function here

    def test_check_numeric_with_NG_value(self):
        A = pd.Series(['1', 'O', '2.0', '3', '4', '5', '6', '7', '8', '9', 10])
        result, k, N, _, out_line = check_numeric(A, 0.9)
        self.assertEqual(result, 'NG')
        self.assertEqual(k, 10)
        self.assertEqual(N, 11)
        self.assertEqual(len(out_line), 1)
        self.assertEqual(out_line, {1: 'O'})  # {index:value}


if __name__ == '__main__':
    unittest.main()
