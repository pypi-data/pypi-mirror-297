"""
test_smartsheet_engine.py
-------------------------

This module contains the test cases for `__init__.py`.

..autoclass:: TestSmartsheetEngineGetHome

..autoclass:: TestSmartsheetEngineGetSheet

..autoclass:: TestSmartsheetEngineAppendSheetRows

..autoclass:: TestSmartsheetEngineUpdateSheetRows

..autoclass:: TestSmartsheetEngineDeleteSheetRows

..autoclass:: TestSmartsheetEngineSetColumnFormula

..autoclass:: TestSmartsheetEngineSetColumnDropdown

..autoclass:: TestSmartsheetEngineLockColumn

..autoclass:: TestSmartsheetEngineUnLockColumn

..autoclass:: TestSmartsheetEngineHideColumn

..autoclass:: TestSmartsheetEngineUnHideColumn

..autoclass:: TestSmartsheetEngineSetColumnProperty

..autoclass:: TestSmartsheetEngineShareSheet

Dependencies
------------
- smartsheet-python-sdk
"""


from tests.test_data import (
    SmartsheetMocks,
    sample_object_id,
    sample_object_id_different,
    sample_smartsheet_name,
    sample_smartsheet_name_different,
    sample_dropdown_options,
    sample_grid,
    sample_grid_id_not_in_repo,
    sample_grid_name_not_in_repo,
    sample_df,
    sample_df_empty,
    sample_home,
    sample_home_with_sheets,
    sample_invalid_params,
    sample_valid_emails_list,
    invalid_access_levels,
)

from smartsheet import models


class TestSmartsheetEngineGetHome(SmartsheetMocks.MockSDK):
    def test_get_home_contents_non_home_object_received_returns_none(self):
        self.mock_home.list_all_contents.return_value = None
        result = self.engine.get_home_contents()
        self.assertIsNone(result)
    
    def test_get_home_contents_no_sheets_in_home_returns_false(self):
        self.mock_home.list_all_contents.return_value = sample_home
        result = self.engine.get_home_contents()
        self.assertFalse(result)

    def test_get_home_contents_sheets_in_home_returns_true(self):
        self.mock_home.list_all_contents.return_value = sample_home_with_sheets
        self.engine.repo.add_grid(sample_grid_id_not_in_repo)
        result = self.engine.get_home_contents()
        self.assertTrue(result)
        self.engine.repo.delete_grid_by_id(sample_grid_id_not_in_repo)

    # TODO: Determine test cases for _walk_folder_hierarchy_upsert_grids
    # def test__walk_folder_hierarchy_upsert_grids___(self):
    #     pass


class TestSmartsheetEngineGetSheet(SmartsheetMocks.MockSDK):
    def test_get_sheet_gets_empty_grid_sheet_not_available_to_user_returns_none(self):
        grid = self.engine.get_sheet(sample_smartsheet_name_different)
        self.assertIsNone(grid)

    def test_get_sheet_gets_grid_with_sheet_obj_returns_repository_grid(self):
        self.engine.repo.add_grid(sample_grid)
        grid = self.engine.get_sheet(sample_smartsheet_name)
        self.assertEqual(grid, sample_grid)

    def test_get_sheet_invalid_params_returns_none(self):
        for param in sample_invalid_params:
            grid = self.engine.get_sheet(param, include_sheet_id=param, refresh=param)
            self.assertIsNone(grid)


class TestSmartsheetEngineAppendSheetRows(SmartsheetMocks.MockSDK):
    def test_append_sheet_rows_invalid_sheet_name_returns_none(self):
        self.engine.repo.delete_grid_by_name(sample_smartsheet_name_different)
        result = self.engine.append_sheet_rows(sample_smartsheet_name_different,
                                               sample_df)
        self.assertIsNone(result)

    def test_append_sheet_rows_empty_df_returns_none(self):
        result = self.engine.append_sheet_rows(sample_smartsheet_name, sample_df_empty)
        self.assertIsNone(result)

    def test_append_sheet_rows_invalid_params_returns_none(self):
        for param in sample_invalid_params:
            result = self.engine.append_sheet_rows(param,
                                                   param,
                                                   include_cols=param,
                                                   exclude_cols=param,
                                                   refresh=param)
            self.assertIsNone(result)

    def test_append_sheet_rows_valid_params_returns_result(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.append_sheet_rows(sample_smartsheet_name, sample_df)
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineUpdateSheetRows(SmartsheetMocks.MockSDK):
    def test_update_sheet_rows_invalid_sheet_name_returns_none(self):
        self.engine.repo.delete_grid_by_name(sample_smartsheet_name_different)
        result = self.engine.update_sheet_rows(sample_smartsheet_name_different,
                                               sample_df)
        self.assertIsNone(result)

    def test_update_sheet_rows_empty_df_returns_none(self):
        result = self.engine.update_sheet_rows(sample_smartsheet_name, sample_df_empty)
        self.assertIsNone(result)

    def test_update_sheet_rows_invalid_params_returns_none(self):
        for param in sample_invalid_params:
            result = self.engine.update_sheet_rows(param,
                                                   param,
                                                   include_cols=param,
                                                   exclude_cols=param,
                                                   refresh=param)
            self.assertIsNone(result)

    def test_update_sheet_rows_valid_params_returns_result(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.update_sheet_rows(sample_smartsheet_name, sample_df)
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineDeleteSheetRows(SmartsheetMocks.MockSDK):
    def test_delete_sheet_rows_invalid_sheet_name_returns_none(self):
        self.engine.repo.delete_grid_by_name(sample_smartsheet_name_different)
        result = self.engine.delete_sheet_rows(sample_smartsheet_name_different,
                                               sample_df)
        self.assertIsNone(result)

    def test_delete_sheet_rows_empty_df_returns_none(self):
        result = self.engine.delete_sheet_rows(sample_smartsheet_name, sample_df_empty)
        self.assertIsNone(result)

    def test_delete_sheet_rows_invalid_params_returns_none(self):
        for param in sample_invalid_params:
            result = self.engine.delete_sheet_rows(param,
                                                   param,
                                                   refresh=param)
            self.assertIsNone(result)

    def test_delete_sheet_rows_valid_params_returns_result(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.delete_sheet_rows(sample_smartsheet_name, sample_df)
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineSetColumnFormula(SmartsheetMocks.MockSDK):
    def test_set_column_formula_invalid_sheet_name_returns_none(self):
        result = self.engine.set_column_formula(sample_smartsheet_name_different,
                                                'column_a',
                                                '=NOW()')
        self.assertIsNone(result)

    def test_set_column_formula_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.set_column_formula(sample_smartsheet_name,
                                                'invalid_column_name',
                                                '=NOW()')
        self.assertIsNone(result)

    def test_set_column_formula_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.set_column_formula(param, param, param)
            self.assertIsNone(result)

    def test_set_column_formula_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.set_column_formula(sample_smartsheet_name,
                                                'column_1',
                                                '=NOW()')
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineSetColumnDropdown(SmartsheetMocks.MockSDK):
    def test_set_column_dropdown_invalid_sheet_name_returns_none(self):
        result = self.engine.set_column_dropdown(sample_smartsheet_name_different,
                                                  'column_a',
                                                  sample_dropdown_options)
        self.assertIsNone(result)

    def test_set_column_dropdown_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.set_column_dropdown(sample_smartsheet_name,
                                                  'invalid_column_name',
                                                  sample_dropdown_options)
        self.assertIsNone(result)

    def test_set_column_dropdown_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.set_column_dropdown(param, param, param)
            self.assertIsNone(result)

    def test_set_column_dropdown_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.set_column_dropdown(sample_smartsheet_name,
                                                  'column_1',
                                                  sample_dropdown_options)
        self.assertIsInstance(result, models.Result)

    def test_set_column_dropdown_invalid_restrict_values_argument_ignored_returns_result(self):
        for param in sample_invalid_params:
            self.engine.repo.upsert_grid(sample_grid)
            result = self.engine.set_column_dropdown(sample_smartsheet_name,
                                                    'column_1',
                                                    sample_dropdown_options,
                                                    restrict_values=param)
            self.assertIsInstance(result, models.Result)



class TestSmartsheetEngineLockColumn(SmartsheetMocks.MockSDK):
    def test_lock_column_invalid_sheet_name_returns_none(self):
        result = self.engine.lock_column(sample_smartsheet_name_different, 'column_a')
        self.assertIsNone(result)

    def test_lock_column_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.lock_column(sample_smartsheet_name, 'invalid_column_name')
        self.assertIsNone(result)

    def test_lock_column_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.lock_column(param, param)
            self.assertIsNone(result)

    def test_lock_column_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.lock_column(sample_smartsheet_name, 'column_1')
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineUnLockColumn(SmartsheetMocks.MockSDK):
    def test_unlock_column_invalid_sheet_name_returns_none(self):
        result = self.engine.unlock_column(sample_smartsheet_name_different, 'column_a')
        self.assertIsNone(result)

    def test_unlock_column_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.unlock_column(sample_smartsheet_name, 'invalid_column_name')
        self.assertIsNone(result)

    def test_unlock_column_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.unlock_column(param, param)
            self.assertIsNone(result)

    def test_unlock_column_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.unlock_column(sample_smartsheet_name, 'column_1')
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineHideColumn(SmartsheetMocks.MockSDK):
    def test_hide_column_invalid_sheet_name_returns_none(self):
        result = self.engine.hide_column(sample_smartsheet_name_different, 'column_a')
        self.assertIsNone(result)

    def test_hide_column_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.hide_column(sample_smartsheet_name, 'invalid_column_name')
        self.assertIsNone(result)

    def test_hide_column_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.hide_column(param, param)
            self.assertIsNone(result)

    def test_hide_column_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.hide_column(sample_smartsheet_name, 'column_1')
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineUnHideColumn(SmartsheetMocks.MockSDK):
    def test_unhide_column_invalid_sheet_name_returns_none(self):
        result = self.engine.unhide_column(sample_smartsheet_name_different, 'column_a')
        self.assertIsNone(result)

    def test_unhide_column_invalid_column_name_returns_none(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.unhide_column(sample_smartsheet_name, 'invalid_column_name')
        self.assertIsNone(result)

    def test_unhide_column_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.unhide_column(param, param)
            self.assertIsNone(result)

    def test_unhide_column_valid_params_returns_result(self):
        self.engine.repo.upsert_grid(sample_grid)
        result = self.engine.unhide_column(sample_smartsheet_name, 'column_1')
        self.assertIsInstance(result, models.Result)


class TestSmartsheetEngineSetColumnProperty(SmartsheetMocks.MockSDK):
    def test__set_column_property_invalid_grid_object_returns_none(self):
        for param in sample_invalid_params:
            result = self.engine._set_column_property(param, 'column_1', {'locked': True})
            self.assertIsNone(result)

    def test__set_column_property_grid_without_column_map_returns_none(self):
        test_grid = sample_grid
        result_a = self.engine._set_column_property(test_grid,
                                                    'column_1',
                                                    {'locked': True})
        self.assertIsInstance(result_a, models.Result)

        test_grid.column_map = None
        result_b = self.engine._set_column_property(test_grid,
                                                    'column_1',
                                                    {'locked': True})
        self.assertIsNone(result_b)

    def test__set_column_property_column_not_in_column_map_returns_none(self):
        result = self.engine._set_column_property(sample_grid,
                                                  'invalid_column_name',
                                                  {'locked': True})
        self.assertIsNone(result)

    def test__set_column_property_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine._set_column_property(param, param, param)
            self.assertIsNone(result)


class TestSmartsheetEngineShareSheet(SmartsheetMocks.MockSDK):
    def test_share_sheet_invalid_access_level_returns_none(self):
        for level in invalid_access_levels:
            result = self.engine.share_sheet(sample_smartsheet_name,
                                             sample_valid_emails_list,
                                             access_level=level)
            self.assertIsNone(result)

    def test_share_sheet_invalid_params_return_none(self):
        for param in sample_invalid_params:
            result = self.engine.share_sheet(param, param)
            self.assertIsNone(result)

    def test_share_sheet_valid_params_returns_true(self):
        self.engine.repo.add_grid(sample_grid)
        result = self.engine.share_sheet(sample_smartsheet_name, sample_valid_emails_list)
        self.assertTrue(result)

