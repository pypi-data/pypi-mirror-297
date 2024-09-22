"""
test_grids.py
-------------

This module contains the test cases for `grids.py`.

..autoclass:: RepositoryTestCases

..autoclass:: TestGridRepositoryAdding

..autoclass:: TestGridRepositoryUpdating

..autoclass:: TestGridRepositoryGetting

..autoclass:: TestGridRepositoryDeleting

..autoclass:: TestBuildSmartsheetGrid

..autoclass:: TestBuildDataframe
"""


from unittest import TestCase

from smartsheet_engine.grids import GridRepository
from tests.test_data import (
    sample_object_id,
    sample_object_id_different,
    sample_smartsheet_name,
    sample_smartsheet_name_different,
    sample_invalid_params,
    sample_grid,
    sample_grid_updated,
    sample_grid_id_not_in_repo,
    sample_grid_name_not_in_repo,
)


class RepositoryTestCases:
    """Set up a GridRepository for each TestCase to use"""

    class RepositoryTestCase(TestCase):
        @classmethod
        def setUpClass(cls):
            cls.repo = GridRepository()
            cls.repo.add_grid(sample_grid)

        @classmethod
        def tearDownClass(cls):
            cls.repo.delete_all_grids()


class TestGridRepositoryAdding(RepositoryTestCases.RepositoryTestCase):
    def test_add_grid_not_a_grid_returns_none(self):
        for item in sample_invalid_params:
            status = self.repo.add_grid(item)
            self.assertIsNone(status)

    def test_add_grid_succeeds(self):
        status = self.repo.add_grid(sample_grid)
        self.repo.grids.pop(-1)
        self.assertTrue(status)


class TestGridRepositoryUpdating(RepositoryTestCases.RepositoryTestCase):
    def test_update_grid_succeeds(self):
        status = self.repo.update_grid(sample_grid_updated)
        self.assertTrue(status)

    def test_update_grid_not_a_grid_returns_none(self):
        for item in sample_invalid_params:
            status = self.repo.update_grid(item)
            self.assertIsNone(status)

    def test_update_grid_doesnt_exist_returns_false(self):
        status = self.repo.update_grid(sample_grid_id_not_in_repo)
        self.assertFalse(status)


class TestGridRepositoryUpserting(RepositoryTestCases.RepositoryTestCase):
    def test_upsert_grid_invalid_grid_returns_none(self):
        for param in sample_invalid_params:
            status = self.repo.upsert_grid(param)
            self.assertIsNone(status)

    def test_upsert_grid_valid_grid_not_in_repo_gets_added(self):
        # Confirm that the test grid doesn't already exist in the repository...
        new_grid = sample_grid_id_not_in_repo
        new_grid_from_repo = self.repo.get_grid_by_id(new_grid.sheet_id)
        self.assertIsNone(new_grid_from_repo)
        
        # ...then run the test case
        result = self.repo.upsert_grid(new_grid)
        new_grid_from_repo = self.repo.get_grid_by_id(new_grid.sheet_id)
        self.assertTrue(result)
        self.assertEqual(new_grid, new_grid_from_repo)

    def test_upsert_grid_valid_grid_in_repo_gets_updated(self):
        self.repo.add_grid(sample_grid_id_not_in_repo)
        new_grid = sample_grid_id_not_in_repo
        new_grid.sheet_name = 'new_sheet_name'
        result = self.repo.upsert_grid(new_grid)
        new_grid_from_repo = self.repo.get_grid_by_id(new_grid.sheet_id)
        self.assertTrue(result)
        self.assertEqual(new_grid_from_repo.sheet_name, 'new_sheet_name')

        # Clean up the repository when we're finished
        self.repo.delete_grid_by_id(new_grid.sheet_id)


class TestGridRepositoryGetting(RepositoryTestCases.RepositoryTestCase):
    def test_get_all_grids_succeeds(self):
        grids = self.repo.get_all_grids()
        self.assertEqual(grids, [sample_grid])

    def test_get_grid_by_id_returns_expected_grid(self):
        status = self.repo.get_grid_by_id(sample_object_id)
        self.assertEqual(status, sample_grid)

    def test_get_grid_by_name_returns_expected_grid(self):
        grid = self.repo.get_grid_by_name(sample_smartsheet_name)
        self.assertEqual(grid, sample_grid)

    def test_get_grid_by_id_doesnt_exist_returns_none(self):
        grid = self.repo.get_grid_by_id(sample_object_id_different)
        self.assertIsNone(grid)

    def test_get_grid_by_name_doesnt_exist_returns_none(self):
        grid = self.repo.get_grid_by_name(sample_smartsheet_name_different)
        self.assertIsNone(grid)


class TestGridRepositoryDeleting(RepositoryTestCases.RepositoryTestCase):
    def test_delete_all_grids_succeeds(self):
        self.repo.delete_all_grids()
        grids = self.repo.get_all_grids()
        self.assertEqual(grids, [])
        self.repo.add_grid(sample_grid)

    def test_delete_grid_by_id_succeeds(self):
        self.repo.add_grid(sample_grid_id_not_in_repo)
        status = self.repo.delete_grid_by_id(sample_object_id_different)
        self.assertTrue(status)

    def test_delete_grid_by_id_doesnt_exist_returns_false(self):
        status = self.repo.delete_grid_by_id(sample_object_id_different)
        self.assertFalse(status)

    def test_delete_grid_by_name_succeeds(self):
        self.repo.add_grid(sample_grid_name_not_in_repo)
        status = self.repo.delete_grid_by_name(sample_smartsheet_name_different)
        self.assertTrue(status)

    def test_delete_grid_by_name_doesnt_exist_returns_false(self):
        status = self.repo.delete_grid_by_name(sample_smartsheet_name_different)
        self.assertFalse(status)


# TODO: Write test cases for TestBuildSmartsheetGrid
# TODO: Write test cases for TestBuildDataframe
