"""
utils.py
--------

This module contains some miscellaneous helper functions that are used by other modules.

..autofunction:: is_number

..autofunction:: isinstance_all_items

..autofunction:: get_valid_column_subset
"""


from typing import Union, List
from collections.abc import Iterable


def is_number(number) -> bool:
    """Returns True if the given object is either an integer or a float"""
    return type(number) in (float, int)


def isinstance_all_items(iter_obj: object, item_type) -> Union[bool, None]:
    """Returns True if every item in the given iterable is of a given type"""
    if isinstance(iter_obj, Iterable):
        return all(isinstance(obj, item_type) for obj in iter_obj)
    return None


def get_valid_column_subset(
    available_cols: List[str],
    subset_cols: Union[List[str], str],
) -> Union[List[str], None]:
    """Return a subset of columns that appears in a list of available columns
    
    :param available_cols: A list of strings that represent available columns
    :param subset_cols: A string or list of strings that each represent a column
        in `available_cols`
    :returns: A list of any strings in `subset_cols` that also exist
        in `available_cols`; None if 1) `subset_cols` or `available_cols` aren't a
        list of strings, or 2) no strings in `subset_cols` exist in `available_cols`
    """

    if all([isinstance(available_cols, Iterable),
            isinstance_all_items(available_cols, str)]):
        if isinstance(subset_cols, str):
            if subset_cols in available_cols:
                return [subset_cols]
        elif all([isinstance(subset_cols, list),
                isinstance_all_items(subset_cols, str)]):
            subset_cols_available = [c for c in subset_cols if c in available_cols]
            if subset_cols_available:
                return list(set(available_cols) & set(subset_cols_available))
    return None
