# Smartsheet Engine

**A Python library that simplifies Smartsheet API workflows**

Smartsheet Engine lets you perform high-level actions on a Smartsheet, such as updating rows or locking a column, using only one function call. And it represents Smartsheets as dataframes, so it can be seamlessly integrated into existing workflows that use dataframes.

## Table of Contents
- [Smartsheet Engine](#smartsheet-engine)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Current](#current)
    - [Coming Soon](#coming-soon)
  - [Roadmap](#roadmap)
  - [Installation](#installation)
    - [From PyPI](#from-pypi)
    - [From GitHub](#from-github)
    - [From the Alteryx Python Tool](#from-the-alteryx-python-tool)
  - [Usage](#usage)
  - [How-to Guides](#how-to-guides)
    - [Create, Read, Update, and Delete Smartsheet Data](#create-read-update-and-delete-smartsheet-data)
      - [Get a Smartsheet as a Dataframe](#get-a-smartsheet-as-a-dataframe)
      - [Append a Dataframe to a Smartsheet](#append-a-dataframe-to-a-smartsheet)
      - [Update a Smartsheet From a Dataframe](#update-a-smartsheet-from-a-dataframe)
      - [Delete Smartsheet Rows](#delete-smartsheet-rows)
      - [Provision a Smartsheet](#provision-a-smartsheet)
    - [Analyze Smartsheet Data](#analyze-smartsheet-data)
      - [Compare Two Dataframes and Identify Row Changes](#compare-two-dataframes-and-identify-row-changes)
      - [Compare Two Dataframes and Identify Column Changes](#compare-two-dataframes-and-identify-column-changes)
      - [Compare Two Dataframes and Identify Cell Value Changes](#compare-two-dataframes-and-identify-cell-value-changes)
    - [Modify Smartsheet Object Properties](#modify-smartsheet-object-properties)
      - [Set Column Formula](#set-column-formula)
      - [Set Column Dropdown Options](#set-column-dropdown-options)
      - [Set Column Formatting](#set-column-formatting)
      - [Lock or Unlock a Column](#lock-or-unlock-a-column)
      - [Hide or Unhide a Column](#hide-or-unhide-a-column)
      - [Share a Smartsheet](#share-a-smartsheet)
      - [Update a Shared User's Sheet Permissions](#update-a-shared-users-sheet-permissions)
  - [Developer's Guide](#developers-guide)
    - [API Reference](#api-reference)
    - [System Design](#system-design)
      - [Architecture Diagram](#architecture-diagram)
      - [`SmartsheetEngine` Class](#smartsheetengine-class)
      - [`SmartsheetAPIClient` Class](#smartsheetapiclient-class)
      - [`GridRepository` Class](#gridrepository-class)
      - [`SmartsheetGrid` Dataclass](#smartsheetgrid-dataclass)
    - [Testing](#testing)
      - [Current Coverage](#current-coverage)
      - [How to Run the Tests and Generate the Report](#how-to-run-the-tests-and-generate-the-report)
    - [Linting](#linting)
      - [Current Results](#current-results)
      - [How to Run the Linter and Generate the Report](#how-to-run-the-linter-and-generate-the-report)
  - [Acknowledgements](#acknowledgements)
  - [License](#license)
  - [Contributing](#contributing)

## Features
### Current
- **Create, Read, Update, and Delete Smartsheet Data**
  - Get a Smartsheet as a Dataframe
  - Append a Dataframe to a Smartsheet
  - Update a Smartsheet From a Dataframe
  - Delete Smartsheet Rows
- **Modify Smartsheet Object Properties**
  - Set Column Formula
  - Set Column Dropdown Options
  - Lock or Unlock a Column
  - Hide or Unhide a Column
  - Share a Smartsheet
### Coming Soon
- **Create, Read, Update, and Delete Smartsheet Data**
  - Provision a Smartsheet
    - Create a Smartsheet From a Schema
    - Create a Column
- **Analyze Smartsheet Dataframes**
  - Compare Two Dataframes and Identify Row Changes
  - Compare Two Dataframes and Identify Column Changes
  - Compare Two Dataframes and Identify Cell Value Changes
- **Modify Smartsheet Object Properties**
  - Set Column Formatting
  - Change a Shared User's Access Level
- **Other**
  - Command-Line Interface

## Roadmap
See the [roadmap](ROADMAP.md) for the master list of work to be done and features coming soon

## Installation
1. Download and install [Python](https://www.python.org/downloads/) if needed
2. Install `smartsheet-engine`
### From PyPI
```
pip install smartsheet-engine
```
### From GitHub
```
git clone https://github.com/1npo/smartsheet-engine.git
cd smartsheet-engine
pip install .
```
### From the [Alteryx Python Tool](https://knowledge.alteryx.com/index/s/article/How-To-Use-Alteryx-installPackages-in-Python-tool-1583461465434)
```
Alteryx.installPackage(package="smartsheet-engine")
```

## Usage
To use `smartsheet-engine` in your script, Python Tool, or Notebook:

1. Get your Smartsheet API key and save it to a variable, such as `smartsheet_api_key`
2. Import the `SmartsheetEngine` class, and start a `SmartsheetEngine` with your API key:
```python
from smartsheet_engine import SmartsheetEngine

S = SmartsheetEngine(api_key=smartsheet_api_key)
```
3. Use the engine as needed in your workflow (see [How-To Guides](#how-to-guides) for examples)

> [!TIP]
> You don't need to provide an API key to `SmartsheetEngine` if your key is already stored in the `SMARTSHEET_ACCESS_TOKEN` environment variable. 

> [!CAUTION]
> Do not hardcode your API key into your script, Python Tool, or widget. Put it in a secret store or an environment variable instead.

## How-to Guides
### Create, Read, Update, and Delete Smartsheet Data
#### Get a Smartsheet as a Dataframe
```python
# Gets the dataframe for the Smartsheet called `finished_test_grid`
# and prints the dataframe

df = S.get_sheet('finished_test_grid').sheet_df
print(df)
```
```text
         _ss_row_id  number   rating
0   123734752464772     1.0   Lowest
1  7876435046272900     2.0      Low
2  2246935512059780     3.0   Medium
3  2463203892629380     4.0     High
4  6966803519999876     5.0  Highest
```

> [!WARNING]
> When you call `get_sheet()`, `SmartsheetEngine` downloads the contents of that Smartsheet and creates a dataframe from it. Then it adds a `_ss_row_id` column to the dataframe, which contains the ID of the corresponding row in the Smartsheet. This is how `SmartsheetEngine` maps dataframe rows to Smartsheet rows.
>
> **This means:**
> 
> - If you delete the `_ss_row_id` column, you won't be able to use the dataframe to update or delete rows on the Smartsheet.
> - If you update a Smartsheet with the dataframe, the data in each row of the dataframe will be inserted into the Smartsheet row that matches the ID in the `_ss_row_id` column.

> [!WARNING]
> Whenever you call `get_sheet()`, it only downloads the most current Smartsheet once, and then saves the results in a "repository". Every time you call `get_sheet()` after that, it will always give you the version of the Sheet that was initially saved to the "repository". This is to avoid making excessive API calls.
>
> So if your workflow needs to make updates to a Smartsheet, and then use `get_sheet()` to get an updated copy of the Smartsheet, you must provide the `refresh=True` option. This will force `SmartsheetEngine` to download the most current Sheet from the API, instead of getting the initial version from the repository. For example:
>
> ```python
> df = S.get_sheet('finished_test_grid', refresh=True).sheet_df
> print(df)
> ```
>
> **All `SmartsheetEngine` actions call `get_sheet()` before performing their action, so this limitation applies to all actions. But all actions accept the `refresh=True` option as a workaround.**

#### Append a Dataframe to a Smartsheet
```python
# Appends 2 rows from a dataframe to the Smartsheet named `test_grid`

df = pd.DataFrame({
    'number':       [4, 5],
    'rating':       [None, None],
    'missing_col':  ['data', 'ignored'], })

S.append_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Appending</th>
    <th>After Appending</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/append_rows_before.png', alt='Before appending rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/append_rows_after.png', alt='After appending rows'></td>
  </tr>
</table>

> [!NOTE]
> Column values from a dataframe will only be updated on or appended to a Smartsheet if those columns exist in the Smartsheet. The column names need to match exactly. Any dataframe column that doesn't exist in the Smartsheet will be ignored.
> 
> You can choose to only update/append certain columns, or NOT to update/append certain columns, by using the `include_cols` and `exclude_cols` arguments.
> 
> For example, in this how-to guide -- `number` is the only column that will be updated, because `rating` contains no data, and `missing_col` doesn't exist as a column in the Smartsheet.
>
> So you can achieve the same effect as this: 
>
> ```python
> S.append_sheet_rows('test_grid', df)
> ```
> 
> By only including the `number` column:
> 
> ```python
> S.append_sheet_rows('test_grid', df, include_cols=['number'])
> ```
>
> Or excluding the `rating` and `missing_col` columns:
>
> ```python
> S.append_sheet_rows('test_grid', df, exclude_cols=['rating', 'missing_col'])
> ```

#### Update a Smartsheet From a Dataframe
```python
# Gets the dataframe for the Smartsheet named `test_grid`, changes the
# dropdown options for the `rating` column, and then updates the column

import numpy as np

df = S.get_sheet('test_grid').sheet_df

S.update_column_dropdown('test_grid', 'rating', ['Lowest', 'Low', 'Medium', 'High', 'Highest'])

conditions = [
    df['number'] == 1,
    df['number'] == 2,
    df['number'] == 3,
    df['number'] == 4,
    df['number'] == 5,
]
choices = [
    'Lowest',
    'Low',
    'Medium',
    'High',
    'Highest',
]
df['rating'] = np.select(conditions, choices)

S.update_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Updating</th>
    <th>After Updating</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/update_rows_before.png', alt='Before updating rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/update_rows_after.png', alt='After updating rows'></td>
  </tr>
</table>

#### Delete Smartsheet Rows
> [!CAUTION]
> Before you run `S.delete_sheet_rows(sheet_name, df)`, make sure that `df` only includes the rows you want to delete from the Smartsheet. Because when you run that function, every Smartsheet row that has an ID listed in `df._ss_row_id` **will be deleted from the Smartsheet**.
```python
# Gets the dataframe for the Smartshet named `test_grid`, selects
# only the rows that have the number 2 or 3 in the number column,
# and then deletes them

df = S.get_sheet('test_grid').sheet_df

df = df[df['number'].isin([2,3])]

S.delete_sheet_rows('test_grid', df)
```

<table>
  <tr>
    <th>Before Deleting</th>
    <th>After Deleting</th>
  <tr>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/delete_rows_before.png', alt='Before deleting rows'></td>
    <td><img src='https://github.com/1npo/smartsheet-engine/blob/main/img/delete_rows_after.png', alt='After deleting rows'></td>
  </tr>
</table>

#### Provision a Smartsheet
> [!NOTE]
>
> Coming soon!

### Analyze Smartsheet Data
#### Compare Two Dataframes and Identify Row Changes
> [!NOTE]
>
> Coming soon!

#### Compare Two Dataframes and Identify Column Changes
> [!NOTE]
>
> Coming soon!

#### Compare Two Dataframes and Identify Cell Value Changes
> [!NOTE]
>
> Coming soon!

### Modify Smartsheet Object Properties
#### Set Column Formula
```python
# Changes the column formula for the `month_rated` column to "=MONTH([date_rated]@row)"
# on the Smartsheet named `test_grid`.

S.set_column_formula('test_grid', 'month_rated', '=MONTH([date_rated]@row)')
```

#### Set Column Dropdown Options
```python
# Changes the dropdown options for the `rating` column to `Low, Medium, and High` on the
# Smartsheet named `test_grid`, and restricts the column to only allow these values

S.set_column_dropdown('test_grid', 'rating', ['Low', 'Medium', 'High'], restrict_values=True)
```

#### Set Column Formatting
> [!NOTE]
>
> Coming soon!

#### Lock or Unlock a Column
```python
# Locks and then unlock the `rating` column on the Smartsheet
# named `test_grid`

S.lock_column('test_grid', 'rating')
S.unlock_column('test_grid', 'rating')
```

#### Hide or Unhide a Column
```python
# Hide and then unhide the `rating` column on the Smartsheet
# named `test_grid`

S.hide_column('test_grid', 'rating')
S.unhide_column('test_grid', 'rating')
```

#### Share a Smartsheet
```python
# Share a Smartsheet named `test_grid` with a list of email addresses, giving
# those users the EDITOR_SHARE access level, and send them an email notification
# that the sheet has been shared with them

S.share_sheet('test_grid',
              ['alice@acme.com', 'bob@acme.com'],
              'EDITOR_SHARE',
              send_email=True)
```

> [!NOTE]
> - One or more email addresses must be provided as either a string or a list. When providing multiple emails as a string, each email address must be separated by a semicolon.
> - **The default access level is VIEWER** if no access level is specified. See the [Smartsheet API documentation](https://smartsheet.redoc.ly/#section/Security/Access-Levels) for a list of valid Access Levels.
> - `S.share_sheet()` will NOT send email notifications by default. If you want Smartsheet to notify the user(s) that the Sheet has been shared with them, then you MUST set `send_email` to True.

#### Update a Shared User's Sheet Permissions
> [!NOTE]
>
> Coming soon!

## Developer's Guide
> [!NOTE]
> This documentation will be refined, expanded, and eventually migrated into Sphinx docs that will be hosted on [GitHub Pages](https://pages.github.com/).

### API Reference
> [!NOTE]
>
> Coming soon! Will be available as soon as Sphinx docs are configured and generated.

### System Design
#### Architecture Diagram
<div align='center'>
<img src='https://github.com/1npo/smartsheet-engine/blob/main/img/smartsheet_engine_architecture.png' alt='smartsheet-engine system architecture diagram'>
</div>

#### `SmartsheetEngine` Class
*Provides a set of high-level Smartsheet actions, such as appending dataframe rows to a Smartsheet or locking a column*
- Uses the `SmartsheetAPIClient` class to interact with the Smartsheet API
- Uses the `GridRepository` class to manage the Smartsheet SDK Sheet objects that represent all the Smartsheets that are available to the user
  
#### `SmartsheetAPIClient` Class
*Simplifies using Smartsheet's Python SDK*
- Converts dataframes to lists of Smartsheet SDK Row, Column, and Cell objects, and vice-versa
- Sends the lists of SDK objects to the API
- Retrieves data from the API and returns it to the user

#### `GridRepository` Class
*Stores, retrieves, and modifies `SmartsheetGrid` objects*
- Simple in-memory repository
- Stores `SmartsheetGrid`s in a list
- Can create, read, and update `SmartsheetGrid` objects
  
#### `SmartsheetGrid` Dataclass
*Contains a Smartsheet Sheet object, relevant metadata, and a dataframe representation of the Sheet*
- Sheet Name, ID, and user's access level
- Column map (between English column name and Smartsheet Column ID)
- The Smartsheet SDK Sheet object
- The pandas dataframe representation of the Sheet
- Created and modified timestamps
- Flags for whether or not the Sheet exists in a folder or a workspace
- Name and ID of the folder or workspace

### Testing
#### Current Coverage
> [!NOTE]
> Current test coverage is ⭐ **94%** ⭐ (as of commit **170b34a**).

| Name                               |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------- | -------: | -------: | ------: | --------: |
| smartsheet\_engine/\_\_init\_\_.py |      206 |       22 |     89% |125-126, 133-138, 162-168, 214-218, 228, 650, 722-726, 738, 751 |
| smartsheet\_engine/client.py       |      188 |       23 |     88% |97-100, 126, 147-155, 342, 344, 346, 399, 401, 403, 405, 412, 420, 460-463 |
| smartsheet\_engine/grids.py        |       98 |       23 |     77% |207-226, 241-252 |
| smartsheet\_engine/utils.py        |       18 |        1 |     94% |        49 |
| tests/test\_client.py              |      218 |        0 |    100% |           |
| tests/test\_data.py                |       86 |        0 |    100% |           |
| tests/test\_grids.py               |       90 |        0 |    100% |           |
| tests/test\_smartsheet\_engine.py  |      210 |        0 |    100% |           |
| tests/test\_utils.py               |       17 |        0 |    100% |           |
|                          **TOTAL** | **1131** |   **69** | **94%** |           |

#### How to Run the Tests and Generate the Report
To run the tests and generate the coverage reports:
1. Install pytest and coverage: `pip install pytest coverage`
2. Change directory to the `smartsheet-engine` project root
3. Run the tests: `coverage run -m pytest`
4. Generate the Markdown report: `coverage report -m --format=markdown`
5. Generate the HTML report: `coverage html -d docs/test_coverage_html`

### Linting
#### Current Results
> [!NOTE]
> Current Pylint score is ⭐ **9.81/10** ⭐ (as of commit **170b34a**).
> 
> Pylint doesn't check for warning **W0311** in these results because it causes excessive warnings. There are many places where spaces are added after tabs to align code for readability and consistent style, but it triggers warning **W0311**.

#### How to Run the Linter and Generate the Report
See [`pylint_results_170b34a.log`](docs/linting/pylint_results_170b34a.log) for the current Pylint results.

To generate the report:
1. Install pylint: `pip install pylint`
2. Change directory to the `smartsheet-engine` project root
3. Run Pylint: `pylint -d W0311 smartsheet_engine > docs/linting/pylint_results_{commit}.log`

## Acknowledgements
- The architecture diagram was made with [Lucidchart](http://lucidchart.com/)

## License
This library was created by Nick O'Malley and is currently unlicensed.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute to `smartsheet-engine`