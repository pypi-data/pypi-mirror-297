"""
grids.py
--------

This module provides a custom `SmartsheetGrid` dataclass that represents a Smartsheet
Sheet, its associated metadata, and a dataframe representation of the Sheet. It also
provides an in-memory repository for storing and retrieving `SmartsheetGrid` objects. And
it provides some functions for building `SmartsheetGrid` objects and dataframe
representations of Sheets.

.. autoclass:: SmartsheetGrid

.. autoclass:: GridRepository

.. autofunction:: build_smartsheet_grid

.. autofunction:: build_dataframe

Dependencies
------------
- pandas
- smartsheet-python-sdk

Examples
--------
.. code-block:: python
	:caption: Set up the repository

	from smartsheet_engine.grids import GridRepository
	repo = GridRepository()

.. code-block:: python
	:caption: Add a grid

	repo.add_grid(grid)

.. code-block:: python
	:caption: Get a grid by name and then update it

	grid = repo.get_grid_by_name('my_smartsheet_grid')
	grid.sheet_df = modified_df
	repo.update_grid(grid)
"""


import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Union

import pandas as pd
from smartsheet import models

logger = logging.getLogger(__name__)


# These fields are added to each dataframe that's created by SmartsheetEngine and
# are used to track Sheet and Row IDs.
METADATA_FIELDS = [
	'_ss_row_id',
	'_ss_sheet_id', # optional -- only added if explicitly requested by the user
]


@dataclass
class SmartsheetGrid:
	"""A Smartsheet SDK Sheet object and associated metadata"""
	sheet_id: int
	sheet_name: str
	access_level: str
	column_map: dict = None
	sheet_obj: models.Sheet = None
	sheet_df: pd.DataFrame = None
	created_at: datetime = None
	modified_at: datetime = None
	workspace_id: int = None
	workspace_name: str = None
	folder_id: int = None
	folder_name: str = None
	is_in_folder: bool = False
	is_in_workspace: bool = False


class GridRepository:
	"""An in-memory repository for `SmartsheetGrid` objects"""

	def __init__(self):
		self.grids = []

	def add_grid(self, grid: SmartsheetGrid) -> bool:
		"""Add a `SmartsheetGrid` to the repository

		:param grid: The `SmartsheetGrid` object to add to the repository
		:returns: True if `grid` was added, False if it was not added, and None if
			`grid` is not a `SmartsheetGrid` object
		"""

		if not isinstance(grid, SmartsheetGrid):
			return None

		self.grids.append(grid)
		return True

	def update_grid(self, grid: SmartsheetGrid) -> bool:
		"""Update the given `SmartsheetGrid` object in the repository

		.. warning:: This function finds the `SmartsheetGrid` in the `GridRepository`
			that has the same `sheet_id` as `grid`, and then **replaces that
			`SmartsheetGrid` with `grid`**, overwriting it.

		:param grid: The `SmartsheetGrid` object to update in the repository
		:returns: True if `grid` was found in the repository and updated, False if `grid`
			was not found in the repository, and None if `grid` is not a
			`SmartsheetGrid` object
		"""

		if not isinstance(grid, SmartsheetGrid):
			return None
		index = next((i for i, g in enumerate(self.grids)
					 if g.sheet_id == grid.sheet_id), None)
		if index is not None:
			self.grids[index] = grid
			return True
		return False

	def upsert_grid(self, grid: SmartsheetGrid):
		"""Convenience function to add a grid to the repository if it doesn't already
		exist, otherwise update the existing grid
		"""

		if isinstance(grid, SmartsheetGrid):
			if self.get_grid_by_id(grid.sheet_id):
				self.update_grid(grid)
			else:
				self.add_grid(grid)
			return True
		return None

	def get_all_grids(self) -> list:
		"""Get a list of all the `SmartsheetGrid` objects in the repository"""
		return self.grids

	def get_grid_by_id(self, sheet_id: int) -> Union[models.sheet.Sheet, None]:
		"""Get the `SmartsheetGrid` with the given Sheet ID from the repository

		:returns: A `SmartsheetGrid` object if the Sheet ID is found in the repository,
			otherwise None
		"""

		grid = next((grid for grid in self.grids if grid.sheet_id == sheet_id), None)
		if grid:
			return grid
		return None

	def get_grid_by_name(self, name: str) -> Union[models.sheet.Sheet, None]:
		"""Get the `SmartsheetGrid` with the given Sheet Name from the repository

		:returns: A `SmartsheetGrid` object if a Sheet with the given name is found in
			the repository, otherwise None
		"""

		grid = next((grid for grid in self.grids if grid.sheet_name == name), None)
		if grid:
			return grid
		return None

	def delete_all_grids(self):
		"""Clear the contents of the repository"""
		self.grids = []

	def delete_grid_by_id(self, sheet_id: int):
		"""Remove the `SmartsheetGrid` with the given ID from the repository"""
		index = next((i for i, g in enumerate(self.grids)
					 if g.sheet_id == sheet_id), None)
		if index is not None:
			self.grids.pop(index)
			return True
		return False

	def delete_grid_by_name(self, name: str):
		"""Remove the `SmartsheetGrid` with the given ID from the repository"""
		index = next((i for i, g in enumerate(self.grids) if g.sheet_name == name), None)
		if index is not None:
			self.grids.pop(index)
			return True
		return False


def build_smartsheet_grid(
	sheet: models.Sheet,
	folder: models.Folder = None,
	workspace: models.Workspace = None
) -> Union[SmartsheetGrid, None]:
	"""Create a `SmartsheetGrid` object and populate it with the metadata from a
	Smartsheet SDK Sheet object

	:param sheet: The Sheet object to convert to a SmartsheetGrid
	:param folder: Set `is_in_folder` and populate `folder_id` and `folder_name` in
		the `SmartsheetGrid` if a Smartsheet Folder object is given
	:param workspace: Set `is_in_workspace` and populate `workspace_id` and
		`workspace_name` in the `SmartsheetGrid` if a Smartsheet Folder object
		is given
	:returns: A populated SmartsheetGrid object if a valid Sheet object was
		provided, otherwise None
	"""

	if not isinstance(sheet, models.Sheet):
		logger.error((
			'Valid Sheet object was not provided, unable to build '
			'SmartsheetGrid'))
		return None

	sheet_grid = SmartsheetGrid(sheet_id=sheet.id,
								sheet_name=sheet.name,
								access_level=sheet.access_level,
								created_at=sheet.created_at,
								modified_at=sheet.modified_at)
	if isinstance(folder, models.Folder):
		sheet_grid.is_in_folder = True
		sheet_grid.folder_id = folder.id
		sheet_grid.folder_name = folder.name
	if isinstance(workspace, models.Workspace):
		sheet_grid.is_in_workspace = True
		sheet_grid.workspace_id = workspace.id
		sheet_grid.workspace_name = workspace.name
	return sheet_grid


def build_dataframe(
	grid: SmartsheetGrid,
	include_sheet_id: bool = False
) -> pd.DataFrame:
	"""Create a dataframe from the Row and Column objects in a Sheet object
	
	:param sheet_name: Build a dataframe for this Smartsheet
	:param include_sheet_id: Include the Sheet ID of this Smartsheet in optional
		`_ss_sheet_id` metadata column
	:returns: The Sheet object as a dataframe
	"""

	sheet_records = []
	for row in grid.sheet_obj.rows:
		# These fields prefixed with _ss are metadata needed for processing when
		# updating, adding, or removing rows
		row_record = {}
		row_record['_ss_row_id'] = row.id
		if include_sheet_id is True:
			row_record['_ss_sheet_id'] = grid.sheet_id
		for col in grid.column_map.keys():
			row_record.update({col: row.get_column(grid.column_map[col]).value})
		sheet_records.append(row_record)
	return pd.DataFrame.from_dict(sheet_records)
