"""
client.py
---------

This module provides a simplified interface to the Smartsheet Python SDK.

The Smartsheet Python SDK represents Smartsheet data as `Row`, `Column`, and `Cell`
objects. So to send and receive Sheet data via the SDK, you need to construct and
deconstruct lists of these `Row`, `Column`, and `Cell` objects in for loops.

The `generate_*` functions in this module convert a dataframe to a list of these objects,
which can then be used by the SDK to send API requests to Smartsheet.

The `SmartsheetAPIClient` maintains the Smartsheet API session, and adds response handling
to the SDK functions that make API calls (such as `smartsheet.Sheet.get_sheet()`), so that
API failures are logged gracefully.

..autofunction:: handle_smartsheet_response

..autoclass:: SmartsheetTokenError

..autoclass:: SmartsheetAPIClient

..autofunction:: generate_rows_to_append

..autofunction:: generate_rows_to_update

..autofunction:: generate_rows_to_delete

Dependencies
------------
- pandas
- smartsheet-python-sdk

Examples
--------
.. code-block:: python
	:caption: Set up the API client with your API key

	from smartsheet_engine.client import SmartsheetAPIClient
	api = SmartsheetAPIClient(api_key=my_smartsheet_api_key)

.. code-block:: python
	:caption: Update a Smartsheet with the contents of a dataframe

	rows = generate_rows_to_append(grid, updates_df)
	result = api.smartsheet_add_rows(grid.sheet_id, rows)
"""


import os
import logging
from datetime import datetime, date
from typing import Union, List, Callable
from functools import wraps

import pandas as pd
import smartsheet
from smartsheet import models

from smartsheet_engine.grids import SmartsheetGrid, METADATA_FIELDS
from smartsheet_engine.utils import (
	is_number,
	isinstance_all_items,
	get_valid_column_subset,
)

logger = logging.getLogger(__name__)


DEFAULT_SMARTSHEET_RETRIES = 3
DEFAULT_SMARTSHEET_WAIT_TIME = 15
SHARE_ACCESS_LEVELS = [
	"ADMIN",
	"COMMENTER",
	"EDITOR",
	"EDITOR_SHARE",
	"OWNER",
	"VIEWER",
]


def handle_smartsheet_response(func) -> Callable:
	"""Return Smartsheet API response data unless there's an error response, then log
	the error gracefully

	:returns: The Smartsheet SDK response object, or None if the API responded with an
	error
	"""

	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			func_return_value = func(*args, **kwargs)
		except Exception as err:
			if isinstance(err, smartsheet.exceptions.ApiError):
				code = err.error.result.status_code
				message = err.error.result.message
				recommendation = err.error.result.recommendation
				logger.error('Request failed with error code %s: %s %s',
							 code,
							 message,
							 recommendation)
			else:
				logger.error('Request raised an exception (%s): %s', type(err), err)
			return None

		return func_return_value
	return wrapper


class SmartsheetTokenError(Exception):
	"""Raise an Exception when there's an issue with the user's Smartsheet API token

	The exception that will be raised if the user doesn't have a Smartsheet API
	key stored in the "SMARTSHEET_ACCESS_TOKEN" environment variable, or an API
	key isn't provided when initializing an instance of SmartsheetEngine.
	"""

	default_msg = ('A Smartsheet API access token is required to use this method. '
				   'Please get an API token and make sure it\'s assigned to the '
				   '"SMARTSHEET_ACCESS_TOKEN" environment variable, or provided to '
				   'the api_key parameter when initializing a SmartsheetEngine.')

	def __init__(self, message: str = default_msg):
		super().__init__(message)


class SmartsheetAPIClient:
	"""A high-level abstraction for making Smartsheet API requests

	The Smartsheet SDK automatically looks for an API key in the
	SMARTSHEET_ACCESS_TOKEN environment variable. If the user passes an API key, that
	will be used instead. If an API key isn't passed by the user, and there's no API
	key in the environment variable, then an exception will be raised.

	:param api_key: Authenticate with the Smartsheet API using this key
	:raises SmartsheetTokenError: If an API key wasn't provided or found in
		the environment
	"""

	def __init__(self, api_key: str = None):
		if api_key:
			logger.info('Initializing Smartsheet API with user-provided key')
			self.smart = smartsheet.Smartsheet(api_key)
		else:
			try:
				if os.environ['SMARTSHEET_ACCESS_TOKEN']:
					pass
				else:
					raise SmartsheetTokenError()
			except KeyError as err:
				raise SmartsheetTokenError() from err

			self.smart = smartsheet.Smartsheet()
		logger.info('Initialized Smartsheet API with key in environment')
		self.smart.errors_as_exceptions(True)

	##
	## Make API calls and handle the responses
	##

	@handle_smartsheet_response
	def smartsheet_get_home(self) -> Union[models.Home, None]:
		"""Get metadata for all Smartsheets available to the user"""
		return self.smart.Home.list_all_contents(include='source')

	@handle_smartsheet_response
	def smartsheet_get_sheet(self, sheet_id: int) -> Union[models.Sheet, None]:
		"""Get the Smartsheet data for the given Smartsheet ID"""
		if is_number(sheet_id):
			return self.smart.Sheets.get_sheet(sheet_id)
		return None

	@handle_smartsheet_response
	def smartsheet_create_sheet_in_home(
		self,
		sheet_spec: models.Sheet
	) -> Union[models.Result, None]:
		"""Create a new Smartsheet in the user's "Sheets" folder, with the given
		Sheet specification
		"""
		if isinstance(sheet_spec, models.Sheet):
			return self.smart.Home.create_sheet(sheet_spec)
		return None

	@handle_smartsheet_response
	def smartsheet_create_sheet_in_folder(
		self,
		folder_id: int,
		sheet_spec: models.Sheet
	) -> Union[models.Result, None]:
		"""Create a new Smartsheet in the given Folder, with the given
		Sheet specification
		"""
		if isinstance(sheet_spec, models.Sheet) and is_number(folder_id):
			return self.smart.Folders.create_sheet(folder_id, sheet_spec)
		return None

	@handle_smartsheet_response
	def smartsheet_create_sheet_in_workspace(
		self,
		workspace_id: int,
		sheet_spec: models.Sheet
	) -> Union[models.Result, None]:
		"""Create a new Smartsheet in the given Workspace, with the given
		Sheet specification
		"""
		if isinstance(sheet_spec, models.Sheet) and is_number(workspace_id):
			return self.smart.Workspaces.create_sheet(workspace_id, sheet_spec)
		return None

	@handle_smartsheet_response
	def smartsheet_share_sheet(
		self,
		sheet_id: int,
		share_settings: models.Share,
		send_email: bool = False
	) -> Union[models.Result, None]:
		"""Share a Smartsheet to the user(s) defined in the given Share object, and
		optionally send an email to the user(s)
		"""
		if all([is_number(sheet_id),
		  		isinstance(share_settings, models.Share),
				isinstance(send_email, bool)]):
			return self.smart.Sheets.share_sheet(sheet_id,
												 share_settings,
												 send_email=send_email)
		return None

	@handle_smartsheet_response
	def smartsheet_update_rows(
		self,
		sheet_id: int,
		rows: List[models.Row]
	) -> Union[models.Result, None]:
		"""Update the given Rows on a Smartsheet"""
		if all([is_number(sheet_id),
		  		isinstance(rows, list),
				isinstance_all_items(rows, models.Row)]):
			return self.smart.Sheets.update_rows(sheet_id, rows)
		return None

	@handle_smartsheet_response
	def smartsheet_add_rows(
		self,
		sheet_id: int,
		rows: List[models.Row]
	) -> Union[models.Result, None]:
		"""Append the given Rows to a Smartsheet"""
		if all([is_number(sheet_id),
		  		isinstance(rows, list),
				isinstance_all_items(rows, models.Row)]):
			return self.smart.Sheets.add_rows(sheet_id, rows)
		return None

	@handle_smartsheet_response
	def smartsheet_delete_rows(
		self,
		sheet_id: int,
		row_ids: List[int]
	) -> Union[models.Result, None]:
		"""Delete the given Rows from a Smartsheet"""
		if all([is_number(sheet_id),
		  		isinstance(row_ids, list),
				isinstance_all_items(row_ids, int)]):
			return self.smart.Sheets.delete_rows(sheet_id, row_ids)
		return None

	@handle_smartsheet_response
	def smartsheet_add_columns(
		self,
		sheet_id: int,
		columns: Union[models.Column, List[models.Column]]
	) -> Union[models.Result, None]:
		"""Add the given Columns to a Smartsheet"""
		if is_number(sheet_id):
			if isinstance(columns, models.Column):
				return self.smart.Sheets.add_columns(sheet_id, columns)
			if isinstance(columns, list) and isinstance_all_items(columns,
															   		    models.Column):
				return self.smart.Sheets.add_columns(sheet_id, columns)
		return None

	@handle_smartsheet_response
	def smartsheet_update_column(
		self,
		sheet_id: int,
		column_id: int,
		columns: Union[models.Column, List[models.Column]]
	) -> Union[models.Result, None]:
		"""Update the given Columns on a Smartsheet"""
		if isinstance(sheet_id, int) and isinstance(column_id, int):
			if isinstance(columns, models.Column):
				return self.smart.Sheets.update_column(sheet_id, column_id, columns)
			if isinstance(columns, list) and isinstance_all_items(columns,
															   		    models.Column):
				return self.smart.Sheets.update_column(sheet_id, column_id, columns)
		return None

##
## Generate Smartsheet Python SDK Row objects
##

def generate_rows_to_append(
	grid: SmartsheetGrid,
	df: pd.DataFrame,
	include_cols: list = None,
	exclude_cols: list = None
) -> Union[List[models.Row], None]:
	"""Generate a list of Smartsheet SDK Row objects that will be appended to a Sheet

	:param grid: Append Rows to the Sheet represented by this SmartsheetGrid
	:param df: Generate a Row object for each series in this dataframe
	:param include_cols: Only append the values in these columns (default: whatever
		fields exist in both df and grid.sheet_df; invalid columns will be ignored)
	:param exclude_cols: Don't append the values from any of these columns (invalid
		columns will be ignored)
	:returns: A list of Smartsheet Row objects, or None if the dataframe is empty
		or malformed
	"""

	if isinstance(grid, SmartsheetGrid) and not df.empty:
		available_cols = set(df.columns) & set(grid.column_map)
		if not available_cols:
			logger.error((
				'No columns in the dataframe are present in the Smartsheet, '
				'can\'t perform update'))
			return None
		include_cols = get_valid_column_subset(available_cols, include_cols)
		exclude_cols = get_valid_column_subset(available_cols, exclude_cols)

		rows_to_append = []
		records = df.to_dict('records')
		for record in records:
			new_row = models.Row()
			new_row.to_bottom = True
			for key, value in record.items():
				if key in METADATA_FIELDS:
					continue
				if include_cols and key not in include_cols:
					continue
				if exclude_cols and key in exclude_cols:
					continue
				if isinstance(value, (date, datetime)):
					value = value.isoformat()
				if value:
					new_row.cells.append({
						'column_id':    grid.column_map[key],
						'value':        value})
			rows_to_append.append(new_row)
		logger.info('%s (%s): Created %s Row objects to append',
					grid.sheet_name,
					grid.sheet_id,
					len(rows_to_append))
		return rows_to_append
	return None

def generate_rows_to_update(
	grid: SmartsheetGrid,
	df: pd.DataFrame,
	include_cols: list = None,
	exclude_cols: list = None
) -> Union[List[models.Row], None]:
	"""Generate a list of Smartsheet SDK Row objects that will be updated on a Sheet

	:param grid: Update Rows on the Sheet represented by this SmartsheetGrid
	:param df: Generate a Row object for updating each series in this dataframe
	:param include_cols: Only update the values in these columns (default: whatever
		fields exist in both df and grid.sheet_df; invalid columns will be ignored)
	:param exclude_cols: Don't update the values from any of these columns (invalid
		columns will be ignored)
	:returns: A list of Smartsheet Row objects, or None if the dataframe is empty
		or malformed
	"""

	if not df.empty:
		available_cols = set(df.columns) & set(grid.column_map)
		if not available_cols:
			logger.error((
				'No columns in the dataframe are present in the Smartsheet, '
				'can\'t perform update'))
			return None
		include_cols = get_valid_column_subset(available_cols, include_cols)
		exclude_cols = get_valid_column_subset(available_cols, exclude_cols)

		rows_to_update = []
		rows_missing_row_id = []
		records = df.to_dict('records')
		for i, record in enumerate(records):
			row_id = int(record.get('_ss_row_id', 0))
			if row_id:
				new_row = models.Row()
				new_row.id = row_id
				for key, value in record.items():
					if key in METADATA_FIELDS:
						continue
					if include_cols and key not in include_cols:
						continue
					if exclude_cols and key in exclude_cols:
						continue
					if isinstance(value, (date, datetime)):
						value = value.isoformat()
					if not value:
						value = ''
					new_cell = models.Cell()
					new_cell.column_id = grid.column_map[key]
					new_cell.value = value
					new_row.cells.append(new_cell)
				rows_to_update.append(new_row)
			else:
				rows_missing_row_id.append(i)

		logger.info('%s (%s): Created %s Row objects to update',
					grid.sheet_name,
					grid.sheet_id,
					len(rows_to_update))

		if len(rows_missing_row_id) > 0:
			logger.warning((
				'%s (%s): %s rows in the dataframe don\'t have a Smartsheet Row ID. '
				'See dataframe rows: %s'),
				grid.sheet_name,
				grid.sheet_id,
				len(rows_missing_row_id),
				", ".join(rows_missing_row_id))

		return rows_to_update
	return None

def generate_rows_to_delete(
	grid: SmartsheetGrid,
	df: pd.DataFrame
) -> Union[List[int], None]:
	"""Generate a list of Smartsheet Row IDs to delete from a Sheet
	
	:param grid: Delete Rows from the Sheet represented by this SmartsheetGrid
	:param df: Get the list of Row IDs from this dataframe
	:returns: A list of Row IDs, or None if the dataframe is empty or malformed
	"""

	if isinstance(grid, SmartsheetGrid):
		available_rows = [row.id for row in grid.sheet_obj.rows]
		if not df.empty:
			rows_to_remove = []
			records = df.to_dict('records')
			for record in records:
				row_id = int(record.get('_ss_row_id', 0))
				if row_id and row_id in available_rows:
					rows_to_remove.append(row_id)
			logger.info('%s (%s): Created a list of %s Row IDs to delete',
						grid.sheet_name,
						grid.sheet_id,
						len(rows_to_remove))
			return rows_to_remove
		logger.error((
			'A dataframe with rows is required to generate a list of rows to '
			'delete, but none was given'))
		return None
	logger.error((
		'A valid SmartsheetGrid object is required to generate a list of rows to '
		'delete, but one wasn\'t provided'))
	return None
