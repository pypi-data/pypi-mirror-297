"""
test_client.py
--------------

This module contains the test cases for `client.py`.

..autoclass:: TestSDKWrappersExceptionReturnsNone

..autoclass:: TestSDKWrappersInvalidParamsReturnsNone

..autoclass:: TestSDKWrappersSucceedReturnExpectedObjects

..autoclass:: TestSDKObjectGenerators

Dependencies
------------
- smartsheet-python-sdk
"""


from unittest import TestCase

from smartsheet import models

from smartsheet_engine.client import (
	generate_rows_to_append,
	generate_rows_to_update,
	generate_rows_to_delete,
)
from tests.test_data import (
    SmartsheetMocks,
	sample_object_id,
	sample_sheet,
	sample_share,
	sample_invalid_params,
	sample_id_list,
	sample_column_list,
	sample_column,
	sample_row_list,
	sample_grid,
	sample_add_rows_list_dict,
	sample_update_rows_list_dict,
	sample_delete_rows_list,
	sample_delete_rows_list_some_missing,
	sample_df,
	sample_df_some_rows_missing_id,
	sample_df_all_rows_missing_id,
	sample_df_empty,
	sample_df_no_matching_cols,
)


class TestSDKWrappersExceptionReturnsNone(SmartsheetMocks.MockSDK):
	"""Test that the SDK wrappers return None when the SDK raises an Exception"""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()

		# TODO: Figure out how to mock `smartsheet.exceptions.ApiError` and capture that
		# that exception specifically, instead of a generic `Exception`
		cls.mock_home.list_all_contents.side_effect = Exception
		cls.mock_home.create_sheet.side_effect = Exception
		cls.mock_sheets.get_sheet.side_effect = Exception
		cls.mock_sheets.share_sheet.side_effect = Exception
		cls.mock_sheets.update_rows.side_effect = Exception
		cls.mock_sheets.add_rows.side_effect = Exception
		cls.mock_sheets.delete_rows.side_effect = Exception
		cls.mock_sheets.add_columns.side_effect = Exception
		cls.mock_sheets.update_column.side_effect = Exception
		cls.mock_folders.create_sheet.side_effect = Exception
		cls.mock_workspaces.create_sheet.side_effect = Exception

	def test_smartsheet_get_home_api_error_returns_none(self):
		home = self.api_client.smartsheet_get_home()
		self.mock_home.list_all_contents.assert_called()
		self.assertIsNone(home)

	def test_smartsheet_get_sheet_api_error_returns_none(self):
		sheet = self.api_client.smartsheet_get_sheet(sample_object_id)
		self.mock_sheets.get_sheet.assert_called_once_with(sample_object_id)
		self.assertIsNone(sheet)

	def test_smartsheet_create_sheet_in_home_api_error_returns_none(self):
		resp = self.api_client.smartsheet_create_sheet_in_home(sample_sheet)
		self.mock_home.create_sheet.assert_called_once_with(sample_sheet)
		self.assertIsNone(resp)

	def test_smartsheet_create_sheet_in_folder_api_error_returns_none(self):
		resp = self.api_client.smartsheet_create_sheet_in_folder(sample_object_id,
														   		 sample_sheet)
		self.mock_folders.create_sheet.assert_called_once_with(sample_object_id,
														  	   sample_sheet)
		self.assertIsNone(resp)

	def test_smartsheet_create_sheet_in_workspace_api_error_returns_none(self):
		resp = self.api_client.smartsheet_create_sheet_in_workspace(sample_object_id,
															  		sample_sheet)
		self.mock_workspaces.create_sheet.assert_called_once_with(sample_object_id,
													   		 	  sample_sheet)
		self.assertIsNone(resp)

	def test_smartsheet_share_sheet_api_error_returns_none(self):
		resp = self.api_client.smartsheet_share_sheet(sample_object_id, sample_share)
		self.mock_sheets.share_sheet.assert_called_once_with(sample_object_id,
												  	    	 sample_share,
															 send_email=False)
		self.assertIsNone(resp)

	def test_smartsheet_update_rows_api_error_returns_none(self):
		resp = self.api_client.smartsheet_update_rows(sample_object_id, sample_row_list)
		self.mock_sheets.update_rows.assert_called_once_with(sample_object_id,
													   		 sample_row_list)
		self.assertIsNone(resp)

	def test_smartsheet_add_rows_api_error_returns_none(self):
		resp = self.api_client.smartsheet_add_rows(sample_object_id, sample_row_list)
		self.mock_sheets.add_rows.assert_called_once_with(sample_object_id,
														  sample_row_list)
		self.assertIsNone(resp)

	def test_smartsheet_delete_rows_api_error_returns_none(self):
		resp = self.api_client.smartsheet_delete_rows(sample_object_id, sample_id_list)
		self.mock_sheets.delete_rows.assert_called_once_with(sample_object_id,
													   		 sample_id_list)
		self.assertIsNone(resp)

	def test_smartsheet_add_columns_column_list_api_error_returns_none(self):
		resp = self.api_client.smartsheet_add_columns(sample_object_id,
													  sample_column_list)
		self.mock_sheets.add_columns.assert_called_with(sample_object_id,
													   	sample_column_list)
		self.assertIsNone(resp)
	
	def test_smartsheet_add_columns_one_column_api_error_returns_none(self):
		resp = self.api_client.smartsheet_add_columns(sample_object_id, sample_column)
		self.mock_sheets.add_columns.assert_called_with(sample_object_id,
													   	sample_column)
		self.assertIsNone(resp)

	def test_smartsheet_update_column_column_list_api_error_returns_none(self):
		resp = self.api_client.smartsheet_update_column(sample_object_id,
									   					sample_object_id,
														sample_column_list)
		self.mock_sheets.update_column.assert_called_with(sample_object_id,
														  sample_object_id,
														  sample_column_list)
		self.assertIsNone(resp)

	def test_smartsheet_update_column_one_column_api_error_returns_none(self):
		resp = self.api_client.smartsheet_update_column(sample_object_id,
									   					sample_object_id,
														sample_column)
		self.mock_sheets.update_column.assert_called_with(sample_object_id,
														  sample_object_id,
														  sample_column)
		self.assertIsNone(resp)


class TestSDKWrappersInvalidParamsReturnsNone(SmartsheetMocks.MockSDK):
	"""Test that the SDK wrappers return None when invalid parameter types are given"""
	
	# TODO: Update the tests that take 2 or more arguments to test for every combination
	# of `sample_invalid_params` for arg1, arg2, argN
	def test_smartsheet_get_sheet_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			sheet = self.api_client.smartsheet_get_sheet(param)
			self.assertIsNone(sheet)

	def test_smartsheet_create_sheet_in_home_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_create_sheet_in_home(param)
			self.assertIsNone(resp)

	def test_smartsheet_create_sheet_in_folder_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_create_sheet_in_folder(param, param)
			self.assertIsNone(resp)
		
	def test_smartsheet_create_sheet_in_workspace_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_create_sheet_in_workspace(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_share_sheet_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_share_sheet(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_update_rows_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_update_rows(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_add_rows_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_add_rows(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_delete_rows_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_delete_rows(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_add_columns_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_add_columns(param, param)
			self.assertIsNone(resp)

	def test_smartsheet_update_column_invalid_params_returns_none(self):
		for param in sample_invalid_params:
			resp = self.api_client.smartsheet_update_column(param, param, param)
			self.assertIsNone(resp)


class TestSDKWrappersSucceedReturnExpectedObjects(SmartsheetMocks.MockSDK):
	"""Test that the SDK wrappers return the expected SDK objects when inputs are a
	valid type"""

	def test_smartsheet_get_home_returns_home(self):
		home = self.api_client.smartsheet_get_home()
		self.mock_home.list_all_contents.assert_called()
		self.assertIsInstance(home, models.Home)

	def test_smartsheet_get_sheet_returns_sheet(self):
		sheet = self.api_client.smartsheet_get_sheet(sample_object_id)
		self.mock_sheets.get_sheet.assert_called_once_with(sample_object_id)
		self.assertIsInstance(sheet, models.Sheet)
	
	def test_smartsheet_create_sheet_in_home_succeeds(self):
		resp = self.api_client.smartsheet_create_sheet_in_home(sample_sheet)
		self.mock_home.create_sheet.assert_called_once_with(sample_sheet)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_create_sheet_in_folder_succeeds(self):
		resp = self.api_client.smartsheet_create_sheet_in_folder(sample_object_id,
														   		 sample_sheet)
		self.mock_folders.create_sheet.assert_called_once_with(sample_object_id,
														 	   sample_sheet)
		self.assertIsInstance(resp, models.Result)	
	
	def test_smartsheet_create_sheet_in_workspace_succeeds(self):
		resp = self.api_client.smartsheet_create_sheet_in_workspace(sample_object_id,
															  	    sample_sheet)
		self.mock_workspaces.create_sheet.assert_called_once_with(sample_object_id,
																  sample_sheet)
		self.assertIsInstance(resp, models.Result)
	
	def test_smartsheet_share_sheet_succeeds(self):
		resp = self.api_client.smartsheet_share_sheet(sample_object_id, sample_share)
		self.mock_sheets.share_sheet.assert_called_once_with(sample_object_id,
												  	    	 sample_share,
															 send_email=False)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_update_rows_succeeds(self):
		resp = self.api_client.smartsheet_update_rows(sample_object_id, sample_row_list)
		self.mock_sheets.update_rows.assert_called_once_with(sample_object_id,
													   		 sample_row_list)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_add_rows_succeeds(self):
		resp = self.api_client.smartsheet_add_rows(sample_object_id, sample_row_list)
		self.mock_sheets.add_rows.assert_called_once_with(sample_object_id,
														  sample_row_list)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_delete_rows_succeeds(self):
		resp = self.api_client.smartsheet_delete_rows(sample_object_id, sample_id_list)
		self.mock_sheets.delete_rows.assert_called_once_with(sample_object_id,
													   		 sample_id_list)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_add_columns_column_list_succeeds(self):
		resp = self.api_client.smartsheet_add_columns(sample_object_id,
													  sample_column_list)
		self.mock_sheets.add_columns.assert_called_with(sample_object_id,
													   	sample_column_list)
		self.assertIsInstance(resp, models.Result)
	
	def test_smartsheet_add_columns_one_column_succeeds(self):
		resp = self.api_client.smartsheet_add_columns(sample_object_id,
													  sample_column)
		self.mock_sheets.add_columns.assert_called_with(sample_object_id,
													   	sample_column)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_update_column_column_list_succeeds(self):
		resp = self.api_client.smartsheet_update_column(sample_object_id,
									   					sample_object_id,
														sample_column_list)
		self.mock_sheets.update_column.assert_called_with(sample_object_id,
														  sample_object_id,
														  sample_column_list)
		self.assertIsInstance(resp, models.Result)

	def test_smartsheet_update_column_one_column_succeeds(self):
		resp = self.api_client.smartsheet_update_column(sample_object_id,
									   					sample_object_id,
														sample_column)
		self.mock_sheets.update_column.assert_called_with(sample_object_id,
														  sample_object_id,
														  sample_column)
		self.assertIsInstance(resp, models.Result)
	

class TestSDKObjectGenerators(TestCase):
	"""Test that the SDK object generators return the expected values when valid inputs
	are given, and return None when're given invalid inputs"""

	def test_genenerate_rows_to_append_empty_df_returns_none(self):
		rows = generate_rows_to_append(sample_grid, sample_df_empty)
		self.assertIsNone(rows)

	def test_genenerate_rows_to_append_no_existing_columns_returns_none(self):
		rows = generate_rows_to_append(sample_grid, sample_df_no_matching_cols)
		self.assertIsNone(rows)

	def test_genenerate_rows_to_append_invalid_include_cols_ignored(self):
		for param in sample_invalid_params:
			rows = generate_rows_to_append(sample_grid, sample_df, include_cols=param)
			rows_dicts = [row.to_dict() for row in rows]
			self.assertEqual(rows_dicts, sample_add_rows_list_dict)

	def test_genenerate_rows_to_append_invalid_exclude_cols_ignored(self):
		for param in sample_invalid_params:
			rows = generate_rows_to_append(sample_grid, sample_df, exclude_cols=param)
			rows_dicts = [row.to_dict() for row in rows]
			self.assertEqual(rows_dicts, sample_add_rows_list_dict)

	def test_genenerate_rows_to_append_returns_expected_rows(self):
		rows = generate_rows_to_append(sample_grid, sample_df)
		rows_dicts = [row.to_dict() for row in rows]
		self.assertEqual(rows_dicts, sample_add_rows_list_dict)

	def test_genenerate_rows_to_update_empty_df_returns_none(self):
		rows = generate_rows_to_update(sample_grid, sample_df_empty)
		self.assertIsNone(rows)

	def test_genenerate_rows_to_update_no_existing_columns_returns_none(self):
		rows = generate_rows_to_update(sample_grid, sample_df_no_matching_cols)
		self.assertIsNone(rows)

	def test_genenerate_rows_to_update_invalid_include_cols_ignored(self):
		for param in sample_invalid_params:
			rows = generate_rows_to_update(sample_grid, sample_df, include_cols=param)
			rows_dicts = [row.to_dict() for row in rows]
			self.assertEqual(rows_dicts, sample_update_rows_list_dict)

	def test_genenerate_rows_to_update_invalid_exclude_cols_ignored(self):
		for param in sample_invalid_params:
			rows = generate_rows_to_update(sample_grid, sample_df, exclude_cols=param)
			rows_dicts = [row.to_dict() for row in rows]
			self.assertEqual(rows_dicts, sample_update_rows_list_dict)

	def test_genenerate_rows_to_update_all_rows_missing_row_id_returns_none(self):
		rows = generate_rows_to_delete(sample_grid, sample_df_all_rows_missing_id)
		self.assertEqual(rows, [])

	def test_genenerate_rows_to_update_some_rows_missing_row_id_returns_expected_rows(self):
		rows = generate_rows_to_delete(sample_grid, sample_df_some_rows_missing_id)
		self.assertEqual(rows, sample_delete_rows_list_some_missing)

	def test_genenerate_rows_to_update_returns_expected_rows(self):
		rows = generate_rows_to_update(sample_grid, sample_df)
		rows_dicts = [row.to_dict() for row in rows]
		self.assertEqual(rows_dicts, sample_update_rows_list_dict)

	def test_genenerate_rows_to_delete_empty_df_returns_none(self):
		rows = generate_rows_to_delete(sample_grid, sample_df_empty)
		self.assertIsNone(rows)

	def test_genenerate_rows_to_delete_returns_expected_list(self):
		rows = generate_rows_to_delete(sample_grid, sample_df)
		self.assertEqual(rows, sample_delete_rows_list)
