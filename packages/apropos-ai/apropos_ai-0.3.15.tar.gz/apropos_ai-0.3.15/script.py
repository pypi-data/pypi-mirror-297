import pandas as pd
import numpy as np

# Constants
COLUMNS = ["column1", "column2", "column3", "column4", "column5"]


def task_func(df, dct):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input df is not a DataFrame")
    # Replace values using dictionary mapping
    df = df.replace(dct)

    # Calculate the correlation matrix
    correlation_matrix = np.corrcoef(df.values, rowvar=False)

    return pd.DataFrame(correlation_matrix, columns=df.columns, index=df.columns)


import unittest
import pandas as pd


class TestCases(unittest.TestCase):
    def test_case_1(self):
        # Test with simple numeric DataFrame
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        dct = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}
        result = task_func(df, dct)
        self.assertTrue(result.shape == (2, 2))

    def test_case_2(self):
        # Test with DataFrame containing NaN values
        df = pd.DataFrame({"A": [1, 2, None], "B": [4, None, 6]})
        dct = {1: 10, 2: 20, 4: 40, 6: 60}
        result = task_func(df, dct)
        self.assertTrue(result.isna().sum().sum() > 0)

    def test_case_3(self):
        # Test with DataFrame containing negative values
        df = pd.DataFrame({"A": [-1, -2, -3], "B": [-4, -5, -6]})
        dct = {-1: 1, -2: 2, -3: 3, -4: 4, -5: 5, -6: 6}
        result = task_func(df, dct)
        self.assertTrue(result.shape == (2, 2))

    def test_case_4(self):
        # Test with DataFrame containing mixed data types
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        dct = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5}
        result = task_func(df, dct)
        self.assertTrue(result.shape == (2, 2))

    def test_case_5(self):
        # Test with larger DataFrame
        df = pd.DataFrame({"A": range(10), "B": range(10, 20), "C": range(20, 30)})
        dct = {i: i + 1 for i in range(30)}
        result = task_func(df, dct)
        self.assertTrue(result.shape == (3, 3))

    def test_case_6(self):
        with self.assertRaises(ValueError):
            task_func("non_df", {})
