# coding=utf-8
"""
Module of Filter and Filters
"""


from collections import UserDict
from typing import Callable, Any, List, Optional


class Filters(UserDict):
    """
    Filters manager
    """
    def apply(self, value: Any, filters: Optional[List[str]] = None) -> bool:
        """
        Apply all or certain registered filters
        """
        # if not specified then apply all
        if filters is None:
            return self.__apply_all(value)
        # or aplly specified
        return self.__apply_many(value, filters)

    def __apply_all(self, value: Any):
        """
        Apply all registered filters
        """
        for _filter in self.values():
            if not _filter.apply(value):
                return False
        return True

    def __apply_many(self, value: Any, filters: Optional[List[str]] = None) -> bool:
        """
        Apply certain registered filters
        """
        for filter_name in (filters or []):
            if filter_name in self and not self[filter_name].apply(value):
                return False
        return True


# pylint: disable=too-few-public-methods
class Filter:
    """
    Class of single filter
    """
    def __init__(self, validator: Callable, *args, **kwargs):
        self.validator = validator
        self.args = args
        self.kwargs = kwargs

    def apply(self, value) -> bool:
        """
        Apply the filter for given value
        """
        return self.validator(value, *self.args, **self.kwargs)
