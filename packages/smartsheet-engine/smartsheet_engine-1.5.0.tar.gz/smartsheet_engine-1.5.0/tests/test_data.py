"""
test_data.py
------------

This module contains a Smartsheet SDK mock and sample data used as test inputs.

..autoclass:: SmartsheetMocks

Dependencies
------------
- pandas
- smartsheet-python-sdk
"""


from unittest import TestCase
from unittest.mock import patch
from datetime import datetime

import pandas as pd
from smartsheet import models
from smartsheet import types

from smartsheet_engine import SmartsheetEngine
from smartsheet_engine.client import SmartsheetAPIClient, SHARE_ACCESS_LEVELS
from smartsheet_engine.grids import SmartsheetGrid


# TODO: Create actual samples for each Smartsheet SDK object, instead of empty objects
invalid_access_levels = [level[::-1] for level in SHARE_ACCESS_LEVELS]
sample_timestamp = datetime(2024, 1, 1, 12, 30, 00)
sample_timestamp_different = datetime(2024, 8, 15, 6, 45, 00)
sample_api_key = 'JDw8QS8e21pBCTbaV0lm40kk9m0reWlYX0CG8'
sample_home = models.Home()
sample_share = models.Share()
sample_result = models.Result()
sample_smartsheet_name = 'test_smartsheet'
sample_smartsheet_name_different = 'unlisted_smartsheet'
sample_object_id = 1234567890123456
sample_object_id_different = 6543210987654321
sample_row_list = [models.Row(), models.Row(), models.Row()]
sample_column = models.Column()
sample_column_list = [models.Column(), models.Column(), models.Column()]
sample_available_cols = ['the', 'quick', 'brown', 'fox', 'jumps']
sample_subset_cols_all_valid = ['brown', 'fox']
sample_subset_cols_some_valid = ['the', 'fast', 'red', 'fox', 'leaps']
sample_subset_cols_none_valid = ['a', 'cool', 'blue', 'hedgehog', 'goes']
sample_empty_list = []
sample_id_list = [sample_object_id for _ in range(5)]
sample_valid_emails_list = ['alice@acme.com', 'bob@acme.com']
sample_valid_emails_str = 'alice@acme.com; bob@acme.com'
sample_invalid_params = [
	str(sample_object_id),
	str(sample_object_id_different),
	[str(id) for id in sample_id_list],
	None,
	True,
	False,
	pd.NaT,
	pd.NA,
	{'hello': 8_675_309},
	('foo', 9_000, 'baz'),
	('foo', 'bar', 'baz'),
]
sample_invalid_params_different = [
	str(sample_object_id + 1234),
	str(sample_object_id_different - 9876),
	[str(id * 2) for id in sample_id_list],
	None,
	True,
	False,
	pd.NaT,
	pd.NA,
	{'hello': 8_675_309},
	('loo', 1_009, 'biz'),
	('oof', 'rab', 'zab'),
    {'test': ['items', 'go', 'here']},
    Exception,
    lambda x: x,
]
sample_dropdown_options = ['High', 'Medium', 'Low']
sample_column_map = {'column_1': sample_object_id, 'column_2': sample_object_id}
sample_df = pd.DataFrame(
				{'_ss_row_id': [sample_object_id] * 3,
				 'column_1':	['foo', 'bar', 'baz'],
				 'column_2': 	['Hello', 'There, ', 'World!'],
				})
sample_df_empty = pd.DataFrame()
sample_df_some_rows_missing_id = pd.DataFrame(
				{'_ss_row_id':	[sample_object_id] * 2 + [8675309],
				'column_1':		['foo', 'bar', 'baz'],
				'column_2': 	['Hello', 'There, ', 'World!'], })
sample_df_all_rows_missing_id = pd.DataFrame(
				{'_ss_row_id':	[8675309] * 3,
				'column_1':		['foo', 'bar', 'baz'],
				'column_2': 	['Hello', 'There, ', 'World!'], })
sample_add_rows_list_dict = [
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'foo'},
		{'columnId': 1234567890123456, 'value': 'Hello'}],
		'toBottom': True},
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'bar'},
		{'columnId': 1234567890123456, 'value': 'There, '}],
		'toBottom': True},
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'baz'},
		{'columnId': 1234567890123456, 'value': 'World!'}],
		'toBottom': True},
]
sample_update_rows_list_dict = [
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'foo'},
		{'columnId': 1234567890123456, 'value': 'Hello'}],
		'id': 1234567890123456},
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'bar'},
		{'columnId': 1234567890123456, 'value': 'There, '}],
		'id': 1234567890123456},
	{'cells': [
		{'columnId': 1234567890123456, 'value': 'baz'},
		{'columnId': 1234567890123456, 'value': 'World!'}],
		'id': 1234567890123456},
]
sample_delete_rows_list = [1234567890123456, 1234567890123456, 1234567890123456]
sample_delete_rows_list_some_missing = [1234567890123456, 1234567890123456]
sample_sheet = models.Sheet(
	{
		'accessLevel': 'OWNER',
 		'columns': [
			{
				 'id': 1234567890123456,
				 'index': 0,
				 'primary': True,
				 'title': 'column_1',
				 'type': 'TEXT_NUMBER',
			},
			{
				'id': 1234567890123456,
				'index': 1,
				'title': 'column_2',
				'type': 'PICKLIST',
			}
		],
		'modifiedAt': sample_timestamp,
		'createdAt': sample_timestamp,
		'id': 1234567890123456,
		'name': sample_smartsheet_name,
		'rows': sample_update_rows_list_dict,
	})
sample_df_no_matching_cols = sample_df.rename(columns={'column_1': 'column_a',
													   'column_2': 'column_b'})
sample_df_empty = pd.DataFrame()
sample_include_cols = ['column_1']
sample_exclude_cols = ['column_2']
sample_grid = SmartsheetGrid(sheet_id=sample_object_id,
							 sheet_name=sample_smartsheet_name,
							 access_level='OWNER',
							 column_map=sample_column_map,
                             sheet_obj=sample_sheet,
                             sheet_df=sample_df,
                             created_at=sample_timestamp,
                             modified_at=sample_timestamp,
                             workspace_id=sample_object_id,
                             workspace_name='test_workspace',
                             folder_id=sample_object_id,
                             folder_name='test_folder',
                             is_in_folder=True,
                             is_in_workspace=True)
sample_grid_updated = SmartsheetGrid(sheet_id=sample_object_id,
							         sheet_name=sample_smartsheet_name,
							         access_level='EDITOR')
sample_grid_id_not_in_repo = SmartsheetGrid(sheet_id=sample_object_id_different,
                                            sheet_name=sample_smartsheet_name,
                                            access_level='OWNER')
sample_grid_name_not_in_repo = SmartsheetGrid(sheet_id=sample_object_id,
                                              sheet_name=sample_smartsheet_name_different,
                                              access_level='OWNER')
sample_sheet = models.Sheet()
sample_row_with_data = models.Row()
sample_row_with_data.cells.append({'column_id': sample_object_id, 'value': 'foo'})
sample_row_with_data.cells.append({'column_id': sample_object_id, 'value': 'bar'})
sample_sheet.rows = types.TypedList(sample_row_with_data)
sample_sheets = types.TypedList(sample_sheet)
sample_home_with_sheets = sample_home
sample_home_with_sheets.sheets = sample_sheets


class SmartsheetMocks:
	"""Mock the Smartsheet Python SDK"""

	class MockSDK(TestCase):
		@classmethod
		def setUpClass(cls):
			cls.mock_api_patcher = patch('smartsheet_engine.client.smartsheet.Smartsheet')
			cls.mock_smart = cls.mock_api_patcher.start().return_value
			
			cls.mock_home = cls.mock_smart.Home
			cls.mock_sheets = cls.mock_smart.Sheets
			cls.mock_folders = cls.mock_smart.Folders
			cls.mock_workspaces = cls.mock_smart.Workspaces

			cls.mock_home.list_all_contents.return_value = sample_home
			cls.mock_home.create_sheet.return_value = sample_result
			cls.mock_sheets.get_sheet.return_value = sample_sheet
			cls.mock_sheets.share_sheet.return_value = sample_result
			cls.mock_sheets.update_rows.return_value = sample_result
			cls.mock_sheets.add_rows.return_value = sample_result
			cls.mock_sheets.delete_rows.return_value = sample_result
			cls.mock_sheets.add_columns.return_value = sample_result
			cls.mock_sheets.update_column.return_value = sample_result
			cls.mock_folders.create_sheet.return_value = sample_result
			cls.mock_workspaces.create_sheet.return_value = sample_result

			cls.api_client = SmartsheetAPIClient(api_key=sample_api_key)
			cls.engine = SmartsheetEngine(api_key=sample_api_key)

		@classmethod
		def tearDownClass(cls):
			cls.mock_api_patcher.stop()
