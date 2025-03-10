"""
Iterables-related utilities.
"""

from typing import Any, Iterable, Callable, TypeVar
from itertools import islice

T = TypeVar("T")

__all__ = ("paginate", "slice")


def paginate(
    array: Iterable[Any],
    count: int = 3,
    *,
    debug: bool = False,
    logger: Callable = print
) -> list:
    """Efficient paginator for making a multiple lists out of a list which are sorted in a page-vise order.

    For example:
    ```py
    >>> abc = [1, 2, 3, 4, 5]
    >>> print(paginate(abc, count=2)
    [[1, 2], [3, 4], [5]]
    ```
    """
    array = list(array)
    paginated = []

    temp = []
    for item in array:
        if len(temp) == count:
            paginated.append(temp)
            temp = []

        temp.append(item)

        if debug:
            logger(len(temp), item)

    if len(temp) > 0:
        paginated.append(temp)

    return paginated


def slice(iterable: Iterable[T], max: int = 2000) -> list[list[T]]:
    """Slice an iterable up into multiple lists"""
    result = []
    it = iter(iterable)
    while True:
        chunk = list(islice(it, max))
        if not chunk:
            break
        result.append(chunk)
    return result
