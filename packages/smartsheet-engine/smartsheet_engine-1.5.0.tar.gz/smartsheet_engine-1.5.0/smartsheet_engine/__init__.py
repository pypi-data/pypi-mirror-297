"""
__init__.py
-----------

This module is the entry-point for smartsheet_engine when it's imported as a library. It
provides the SmartsheetEngine class. This class contains a set of methods that each
perform a high-level action on a Smartsheet (such as appending rows or setting a column
formula). And it's designed to let users interact with Smartsheet data via dataframes.

..autoclass:: SmartsheetEngine

Dependencies
------------
- pandas
- smartsheet-python-sdk

Examples
--------
.. code-block:: python
	:caption: Start the engine

	from smartsheet_engine import SmartsheetEngine
	engine = SmartsheetEngine(api_key=my_smartsheet_api_key)

.. code-block:: python
	:caption: Get the contents of a Smartsheet as a dataframe, and make sure to get the
		most current version of the Sheet from the API

	df = engine.get_sheet('my_smartsheet', refresh=True).sheet_df

.. code-block:: python
	:caption: Append the contents of a dataframe to a Smartsheet

	df = create_df_as_needed()
	engine.append_sheet_rows('my_smartsheet', df)

.. code-block:: python
	:caption: Update the contents of a Smartsheet using a dataframe
		
	df = engine.get_sheet('my_smartsheet').sheet_df
	updated_df = update_df_as_needed(df)
	engine.update_sheet_rows('my_smartsheet', updated_df)

.. code-block:: python
	:caption: Update the dropdown options on a Smartsheet column, and restrict column
		values to only allow these options

	engine.set_column_dropdown('my_smartsheet',
							   'column_a',
							   ['my', 'dropdown', 'options'],
							   restrict_values=True)
"""


import logging
from typing import Union

import pandas as pd
from smartsheet import models, types

from .client import (
    SmartsheetAPIClient,
    SHARE_ACCESS_LEVELS,
	generate_rows_to_append,
	generate_rows_to_update,
	generate_rows_to_delete,
)
from .grids import (
    SmartsheetGrid,
    GridRepository,
    build_smartsheet_grid,
    build_dataframe
)
from .utils import isinstance_all_items

LOG_FORMAT = '%(asctime)s:%(levelname)-8s:%(name)s:%(funcName)s:%(message)s'
logging.basicConfig(format=LOG_FORMAT,
					datefmt='%Y-%m-%d %I:%M%p',
					level=logging.INFO)
logger = logging.getLogger(__name__)

# FOR DEBUGGING - Write logs to file
# ----------------------------------
# LOG_FORMAT = logging.Formatter(LOG_FORMAT)
# file_handler = logging.FileHandler('~/smartsheet_engine_test_run.log')
# file_handler.setFormatter(LOG_FORMAT)
# logger.addHandler(file_handler)


class SmartsheetEngine:
	"""An abstraction that implements high-level Smartsheet operations

	:param api_key: A user-provided API key
	"""

	def __init__(self, api_key: str = None):
		self.api = SmartsheetAPIClient(api_key=api_key)
		self.repo = GridRepository()
		self.get_home_contents()

	def get_home_contents(self) -> Union[bool, None]:
		"""Get a listing of all Smartsheets available to the user, save the metadata
		for each Sheet in a SmartsheetGrid, and upsert each Grid into the GridRepository

		..warning:: Running this function will **overwrite** the `SmartsheetGrid` objects
			currently in the `GridRepository`. In a future version, a `merge_grid`
			function will be added to `GridRepository` so the user can selectively
			update certain fields in each `SmartsheetGrid` object, instead of overwriting
			the entire `SmartsheetGrid`.

		:returns: True if at least one Smartsheet was found in the user's Home; False
			if the user's Home object was received but has no available Smartsheets;
			None if the API/SDK returned None or an object other than a Home (eg a
			Result object)
		"""

		# Get metadata about the Smartsheet content available to the user
		home = self.api.smartsheet_get_home()
		if not isinstance(home, models.Home) or home is None:
			logger.error('Received empty or invalid Smartsheet Home object')
			return None

		# Get Sheets in the user's "Sheets" folder
		for sheet in home.sheets:
			grid = build_smartsheet_grid(sheet)
			self.repo.upsert_grid(grid)

		# Get Sheets in any hierarchy of Folders in the user's "Sheets" folder
		self._walk_folder_hierarchy_upsert_grids(home.folders)

		# Get Sheets in any of the user's Workspaces
		for workspace in home.workspaces:
			for sheet in workspace.sheets:
				grid = build_smartsheet_grid(sheet, workspace=workspace)
				self.repo.upsert_grid(grid)

			# Get Sheets in any hierarchy of Folders in this Workspace
			self._walk_folder_hierarchy_upsert_grids(workspace.folders,
													 workspace=workspace)

		logger.info('Found %s available Smartsheets', len(self.repo.grids))
		if len(self.repo.grids) > 0:
			return True
		return False

	def _walk_folder_hierarchy_upsert_grids(
		self,
		folders: types.TypedList,
		workspace: models.Workspace = None
	):
		"""Walk a hierarchy of Smartsheet Folders, convert each Sheet to a SmartsheetGrid,
		and upsert it into the GridRepository

		:param folders: A TypedList of zero or more Smartsheet SDK Folder objects
		:param workspace: An optional Workspace object to pass to
			`build_smartsheet_grid.
		"""

		if all([isinstance(folders, types.TypedList),
		  		isinstance_all_items(folders, models.Folder)]):
			for folder in folders:
				for sheet in folder.sheets:
					grid = build_smartsheet_grid(sheet,
												 folder=folder,
												 workspace=workspace)
					self.repo.upsert_grid(grid)
				if folder.folders:
					self._walk_folder_hierarchy_upsert_grids(folder.folders, workspace)

	def get_sheet(
		self,
		sheet_name: str,
		include_sheet_id: bool = False,
		refresh: bool = False
	) -> Union[SmartsheetGrid, None]:
		"""Get the `SmartsheetGrid` that has the given Sheet name
		
		This function tries to get the `SmartsheetGrid` object from the `GridRepository`
		first. If it finds a `SmartsheetGrid` that has contains a Sheet in `sheet_obj`,
		then it returns that `SmartsheetGrid`. But if it only contains metadata about the
		Smartsheet (no Sheet in `sheet_obj`), or the user provides `refresh=True`, then
		it will download the most current Sheet object from the API, attach it to the
		`SmartsheetGrid` object, and then upsert that object into the `GridRepository`.

		:param sheet_name: Get the contents of this Smartsheet
		:param include_sheet_id: Include the Sheet ID of this Smartsheet in optional
			`_ss_sheet_id` metadata column
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`
		:returns: A SmartsheetGrid object that contains the data and metadata for the
			given Smartsheet, or None if the Sheet doesn't exist
		"""

		if not isinstance(sheet_name, str):
			logger.error('sheet_name must be a string, but a "%s" was provided',
						 type(sheet_name))
			return None

		grid = self.repo.get_grid_by_name(sheet_name)
		if grid is None:
			# TODO: Rewrite this comment more clearly & concisely
			# If the user tries to get a Sheet that was created after the last time
			# `get_home_contents` was run, the Sheet won't exist in the GridRepository,
			# but it will be available to the user. So we want to re-run
			# `get_home_contents` here, then look for the Sheet in the repository again,
			# to make sure that the Sheet actually does exist and is available.
			self.get_home_contents()
			grid = self.repo.get_grid_by_name(sheet_name)
			if grid is None:
				logger.error('Smartsheet not found: %s', sheet_name)
				return None
		if isinstance(grid, SmartsheetGrid):
			if not grid.sheet_obj or refresh is True:
				grid.sheet_obj = self.api.smartsheet_get_sheet(grid.sheet_id)
				grid.column_map = {col.title: col.id for col in grid.sheet_obj.columns}
				grid.sheet_df = build_dataframe(grid, include_sheet_id)
				self.repo.update_grid(grid)
				logger.info('%s (%s): Got Sheet with %s rows from the API',
							sheet_name,
							grid.sheet_id,
							len(grid.sheet_df.index))
			else:
				logger.info('%s (%s): Got Sheet with %s rows from the GridRepository',
							sheet_name,
							grid.sheet_id,
							len(grid.sheet_df.index))
			return grid
		return None

	def append_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Append dataframe rows to a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to append rows to
		:param df: Append the rows in this dataframe to the Sheet
		:param include_cols: Only append the values in these columns (default: whatever
			fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't append the values from any of these columns
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before appending the rows
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			rows = generate_rows_to_append(grid, df, include_cols, exclude_cols)
			if all([isinstance(rows, list), isinstance_all_items(rows, models.Row)]):
				result = self.api.smartsheet_add_rows(grid.sheet_id, rows)
				if result:
					logger.info('%s (%s): Added %s rows',
								grid.sheet_name,
								grid.sheet_id,
								len(rows))
					return result
		return None

	def update_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		include_cols: list = None,
		exclude_cols: list = None,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Update Rows in a Smartsheet

		:param sheet_name: The name of the Smartsheet to update rows on
		:param df: Update the Sheet with this dataframe
		:param include_cols: Only update the values in these columns (default: whatever
			fields exist in both df and grid.sheet_df)
		:param exclude_cols: Don't update the values from any of these columns
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before updating the rows
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			rows = generate_rows_to_update(grid, df, include_cols, exclude_cols)
			if all([isinstance(rows, list), isinstance_all_items(rows, models.Row)]):
				result = self.api.smartsheet_update_rows(grid.sheet_id, rows)
				if result:
					logger.info('%s (%s): Updated %s rows',
								grid.sheet_name,
								grid.sheet_id,
								len(rows))
					return result
		return None

	def delete_sheet_rows(
		self,
		sheet_name: str,
		df: pd.DataFrame,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Delete Rows in a Smartsheet

		:param sheet_name: The name of the Smartsheet to delete rows from
		:param df: Get the list of Row IDs to delete from this dataframe
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before deleting the rows
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			rows = generate_rows_to_delete(grid, df)
			if all([isinstance(rows, list), isinstance_all_items(rows, int)]):
				result = self.api.smartsheet_delete_rows(grid.sheet_id, rows)
				if result:
					logger.info('%s (%s): Deleted %s rows',
								grid.sheet_name,
								grid.sheet_id,
								len(rows))
					return result
		return None

	def set_column_formula(
		self,
		sheet_name: str,
		column_name: str,
		formula: str,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Set the column formula for a column in a Smartsheet

		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to set the formula on
		:param formula: The new column formula
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before setting the column formula
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				result = self._set_column_property(grid,
									   			   column_name,
												   {'formula': formula})
				if result:
					logger.info('%s (%s): %s: Set the column formula to %s',
								grid.sheet_name,
								grid.sheet_id,
								column_name,
								formula)
					return result
			else:
				logger.error((
					'%s (%s): Unable to set column formula, column "%s" was not found '
					'in the Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to set column formula, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def set_column_dropdown(
		self,
		sheet_name: str,
		column_name: str,
		dropdown_options: list,
		restrict_values: bool = False,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Set the dropdown options for a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to set the dropdown on
		:param dropdown_options: The new values for the column dropdown
		:param restrict_values: Only allow dropdown options to be entered into the column
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before setting the column dropdown
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				settings = {'type': 'PICKLIST', 'options': dropdown_options}
				if restrict_values is True:
					settings.update({'validation': True})
					validation_msg = (' and restricted column to allow dropdown '
					   				  'values only')
				else:
					validation_msg = ''

				result = self._set_column_property(grid, column_name, settings)
				if result:
					logger.info('%s (%s): %s: Set the dropdown values to %s%s',
								grid.sheet_name,
								grid.sheet_id,
								column_name,
								dropdown_options,
								validation_msg)
					return result
			else:
				logger.error((
					'%s (%s): Unable to set column dropdown, column "%s" was not found '
					'in the Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to set column dropdown, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def lock_column(
		self,
		sheet_name: str,
		column_name: str,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Lock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to lock
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before locking the column
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				result = self._set_column_property(grid, column_name, {'locked': True})
				if result:
					logger.info('%s (%s): %s: Locked column',
								grid.sheet_name,
								grid.sheet_id,
								column_name)
					return result
			else:
				logger.error((
					'%s (%s): Unable to lock column, column "%s" was not found in the '
					'Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to lock column, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def hide_column(
		self,
		sheet_name: str,
		column_name: str,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Hide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to hide
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before hiding the column
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				result = self._set_column_property(grid, column_name, {'hidden': True})
				if result:
					logger.info('%s (%s): %s: Hid column',
								grid.sheet_name,
								grid.sheet_id,
								column_name)
					return result
			else:
				logger.error((
					'%s (%s): Unable to hide column, column "%s" was not found in the '
					'Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to hide column, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def unlock_column(
		self,
		sheet_name: str,
		column_name: str,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Unlock a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to unlock
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before unlocking the column
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				result = self._set_column_property(grid, column_name, {'locked': False})
				if result:
					logger.info('%s (%s): %s: Unlocked column',
								grid.sheet_name,
								grid.sheet_id,
								column_name)
					return result
			else:
				logger.error((
					'%s (%s): Unable to unlock column, column "%s" was not found in the '
					'Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to unlock column, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def unhide_column(
		self,
		sheet_name: str,
		column_name: str,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Unhide a column in a Smartsheet
		
		:param sheet_name: The name of the Smartsheet to update
		:param column_name: The name of the column to unhide
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before unhiding the column
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if isinstance(grid, SmartsheetGrid):
			if column_name in grid.column_map:
				result = self._set_column_property(grid, column_name, {'hidden': False})
				if result:
					logger.info('%s (%s): %s: Unhid column',
								grid.sheet_name,
								grid.sheet_id,
								column_name)
					return result
			else:
				logger.error((
					'%s (%s): Unable to unhide column, column "%s" was not found in the '
					'Smartsheet'),
					grid.sheet_name,
					grid.sheet_id,
					column_name)
		else:
			logger.error((
				'Unable to unhide column, Smartsheet "%s" does not exist or is not '
				'available to the user'),
				sheet_name)
		return None

	def _set_column_property(
		self,
		grid: SmartsheetGrid,
		column_name: str,
		setting: dict
	) -> Union[models.Result, None]:
		"""Update a Smartsheet Column property
		
		:param grid: Update the column on the Smartsheet that's represented by this
			SmartsheetGrid object
		:param column_name: Update the property of this column
		:param setting: A dictionary where the key is the name of the Column property,
			and the value is the new setting for the property
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		if not isinstance(grid, SmartsheetGrid):
			logger.error('No SmartsheetGrid provided')
			return None

		if grid.column_map is None:
			logger.error((
				'Can\'t set column property, the given SmartsheetGrid for '
				'Smartsheet "%s" doesn\'t contain a column map. This usually '
				'means that the Sheet data hasn\'t been retrieved from the API. '
				'Run `get_sheet(sheet_name, refresh=True)` and try again.'),
				grid.sheet_name)
			return None

		if column_name not in grid.column_map:
			logger.error('Column "%s" does not exist in the "%s" Smartsheet',
						 column_name,
						 grid.sheet_name)
			return None

		result = self.api.smartsheet_update_column(grid.sheet_id,
										  		   grid.column_map[column_name],
										  		   models.Column(setting))
		return result

	# TODO: Write tests for `create_sheet()`
	# TODO: Convert `create_sheet()` to a private method to be used by
	# `provision_smartsheet()`, which will be the user-facing action for creating a
	# Smartsheet with the engine
	def create_sheet(
		self,
		sheet_name: str,
		sheet_obj: models.Sheet,
		create_in: str = 'home',
		folder_id: int = None,
		workspace_id: int = None
	) -> Union[models.Result, None]:
		"""Create a new Smartsheet
		
		:param sheet_name: The name of the Smartsheet to create
		:param sheet_obj: A list of dictionaries, each containing a Smartsheet
			column specification
		:param create_in: Where to create the Smartsheet (either "home", "folder",
			or "workspace")
		:param folder_id: The ID of the Folder to save the Smartsheet in (required if
			create_in is "folder")
		:param workspace_id: The ID of the Workspace to save the Smartsheet in (required
			if create_in is "workspace")
		"""

		if not sheet_name:
			logger.error(
				'Sheet name required to create a new Smartsheet, but none was provided')
			return None

		valid_create_in = ('home', 'folder', 'workspace')
		if create_in not in valid_create_in:
			logger.error((
				'An invalid option was given for `create_in`: "%s". Please select a '
				'valid location and try again: [%s]'),
				create_in,
				', '.join(valid_create_in))
			return None

		result = None

		if create_in == 'home':
			result = self.api.smartsheet_create_sheet_in_home(sheet_obj)

		elif create_in == 'folder':
			if folder_id:
				result = self.api.smartsheet_create_sheet_in_folder(folder_id, sheet_obj)
			else:
				logger.error((
					'A folder ID must be provided when choosing to create a Smartsheet '
					'in a Folder, but none was provided'))

		elif create_in == 'workspace':
			if workspace_id:
				result = self.api.smartsheet_create_sheet_in_workspace(workspace_id,
														   			   sheet_obj)
			else:
				logger.error((
					'A workspace ID must be provided when choosing to create a '
					'Smartsheet in a Workspace, but none was provided'))

		if result:
			sheet_id = result.result.id
			permalink = result.result.permalink
			logger.info('%s (%s): Created new Smartsheet at %s',
			   			sheet_name,
						sheet_id,
						permalink)
			return result
		return None

	def share_sheet(
		self,
		sheet_name: str,
		share_with: Union[list, str],
		access_level: str = 'VIEWER',
		send_email: bool = False,
		refresh: bool = False
	) -> Union[models.Result, None]:
		"""Share a Smartsheet with one or more users with a given access level

		:param sheet_name: The name of the Smartsheet to share
		:param share_with: A list or semicolon-delimited string of email address(es) to
			share the Sheet with
		:param access_level: The access level that the given email address(es) should have
			(options: ADMIN, COMMENTER, EDITOR, EDITOR_SHARE, OWNER, VIEWER
		:param send_email: Notify the given user(s) by email that the sheet has been
			shared with them (default: Don't send email)
		:param refresh: Get a new Sheet object from the API even if one already exists in
			the `GridRepository`, before sharing the sheet
		:returns: A Smartsheet SDK Response object if the operation succeeded,
			otherwise None
		"""

		if not isinstance(access_level, str):
			logger.error((
				'Access level must be provided as a string, and it must be a valid '
				'option (%s)'),
				", ".join(SHARE_ACCESS_LEVELS))
			return None

		access_level = access_level.upper()
		if access_level not in SHARE_ACCESS_LEVELS:
			logger.error((
				'Invalid access level provided (%s). Please specify a valid option (%s)'),
				access_level,
				", ".join(SHARE_ACCESS_LEVELS))
			return None

		if isinstance(share_with, str):
			if ';' in share_with:
				share_with = [email.strip() for email in share_with.split(';')]
			else:
				share_with = [share_with.strip()]
		elif isinstance(share_with, list):
			share_with = [email.strip() for email in share_with]
		else:
			logger.error((
				'Share email addresses must be provided as either a string or a list '
				'of strings. If providing multiple emails in a string, the string must '
				'be comma-delimited.'))
			return None

		email_notification_str = 'not sending notification email'
		if send_email:
			email_notification_str = 'sending notification email'

		grid = self.get_sheet(sheet_name, refresh=refresh)
		if grid:
			for email in share_with:
				share_settings = models.Share({'access_level': access_level,
								   			   'email': email})
				result = self.api.smartsheet_share_sheet(grid.sheet_id,
													share_settings,
													send_email=send_email)
				if result:
					logger.info('%s (%s): Shared sheet with %s (%s), %s',
								grid.sheet_name,
								grid.sheet_id,
								email,
								access_level,
								email_notification_str)
					return result
		else:
			logger.error(
				'Cannot share sheet: Unable to find Smartsheet named "%s" in the list of '
				'Smartsheets available to the user.',
				sheet_name)
		return None
