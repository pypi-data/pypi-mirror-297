"""
test_utils.py
-------------

This module contains the test cases for `utils.py`.

..autoclass:: TestUtils
"""

from unittest import TestCase

from smartsheet_engine.utils import get_valid_column_subset
from tests.test_data import (
	sample_available_cols,
	sample_subset_cols_none_valid,
    sample_subset_cols_some_valid,
    sample_subset_cols_all_valid,
    sample_invalid_params,
    sample_invalid_params_different,
)


class TestUtils(TestCase):
	def test_get_valid_column_subset_invalid_params_returns_none(self):
		for param_a, param_b in zip(sample_invalid_params,
							  		sample_invalid_params_different):
			cols = get_valid_column_subset(param_a, param_b)
			self.assertIsNone(cols)

	def test_get_valid_column_subset_no_subset_returns_none(self):
		cols = get_valid_column_subset(sample_available_cols,
									   sample_subset_cols_none_valid)
		self.assertIsNone(cols)

	def test_get_valid_column_subset_some_subset_valid_returns_subset(self):
		cols = get_valid_column_subset(sample_available_cols,
									   sample_subset_cols_some_valid)
		self.assertEqual(sorted(cols), sorted(['the', 'fox']))

	def test_get_valid_column_subset_all_subset_valid_returns_subset(self):
		cols = get_valid_column_subset(sample_available_cols,
									   sample_subset_cols_all_valid)
		self.assertEqual(sorted(cols), sorted(['brown', 'fox']))