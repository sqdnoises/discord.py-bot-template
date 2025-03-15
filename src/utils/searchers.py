"""
Search-related utilities.
"""

import string
from typing import TypeVar, Callable

__all__ = (
    "match",
    "get_matches",
    "get_matches_by_attr",
    "get_identifiable_matches",
)

T = TypeVar("T")


def match(
    query: str | list[str], text: str | list[str], *, splitter: str = string.whitespace
) -> bool:
    """
    Perform a kind-of fuzzy match between query and text by checking if all query fragments are substrings of some text
    fragments, with case-insensitive matching.

    **Behavior:**
    - If both `query` and `text` are strings, first check if the query (lowercased) is a contiguous substring of the text
      (lowercased). If so, return `True` immediately.
    - Then, convert `query` and `text` into lists of lowercased fragments:
      - If `query` is a string, it is lowercased and split by `splitter`.
      - If `query` is a list, each element is lowercased.
      - Similarly for `query`.
    - Check if each lowercased query fragment is a contiguous substring of at least one lowercased text fragment.
    - Return `True` if all query fragments are found, `False` otherwise.

    Args:
        query (str | list[str]): The query to search for. Can be a string or a list of strings.
        text (str | list[str]): The text to search in. Can be a string or a list of strings.
        splitter (str): The delimiter used to split `text` and `query` when they are strings (default: " ").

    Returns:
        bool: `True` if the query matches the text (case-insensitive), `False` otherwise.

    Examples:
        >>> match_space_fuzzy("ell wor", "Hello World")
        True  # "ell" in "hello", "wor" in "world"
        >>> match_space_fuzzy(["Ell", "Wor"], ["Hello", "World"])
        True  # "ell" in "hello", "wor" in "world"
        >>> match_space_fuzzy("WORLD HELLO", "Hello World")
        True  # "world" in "world", "hello" in "hello"
        >>> match_space_fuzzy("xyz", "Hello World")
        False # "xyz" not in "hello" or "world"
    """

    # If both inputs are strings, do a quick substring check in lowercase
    if isinstance(text, str) and isinstance(query, str):
        text_lower = text.lower()
        query_lower = query.lower()
        if query_lower in text_lower:
            return True

    # Convert text and query to lists of lowercased fragments
    text_fragments: list[str] = (
        text.lower().split(splitter)
        if isinstance(text, str)
        else [frag.lower() for frag in text]
    )
    query_fragments: list[str] = (
        query.lower().split(splitter)
        if isinstance(query, str)
        else [frag.lower() for frag in query]
    )

    # Check if each query fragment is a substring of any text fragment
    for query_fragment in query_fragments:
        if not any(query_fragment in text_fragment for text_fragment in text_fragments):
            return False

    return True


def get_matches(query: str, search_list: list[str]) -> list[str]:
    """
    Find strings in `search_list` that "match" the `query` string, where "match" means that all fragments of the string
    are substrings of some fragments of the `query`, using case-insensitive matching.

    **Behavior:**
    - For each string in `search_list`, check if `match(string, query)` returns `True`. Here, `match(string, query)`
      evaluates whether all fragments of the string (split by whitespace) are substrings of at least one fragment of the
      `query` (also split by whitespace), case-insensitively.
    - Collect and return all strings from `search_list` that satisfy this condition, ensuring no duplicates by checking
      membership in the result list.

    Args:
        query (str): The string within which to search for matches; acts as the text that the strings in `search_list`
            are matched against.
        search_list (list[str]): A list of strings to check against the `query`.

    Returns:
        list[str]: A list of unique strings from `search_list` that match the `query`.

    Examples:
        >>> get_matches("Hello World", ["ell", "wor", "foo"])
        ['ell', 'wor']  # "ell" is in "hello", "wor" is in "world", "foo" is not in either
        >>> get_matches("abc def", ["ab", "de", "xyz"])
        ['ab', 'de']    # "ab" is in "abc", "de" is in "def", "xyz" is not in either
    """
    matches: list[str] = []

    # Preprocess query for case-insensitive comparison
    for item in search_list:
        if item not in matches and match(query, item):
            matches.append(item)

    return matches


def get_matches_by_attr(
    query: str,
    search_list: list[T],
    *,
    key: Callable[[T], str | list[str]] = lambda _: str(_)
) -> list[T]:
    """
    Find objects in `search_list` where the fragments extracted by `key` (from a string or list) all match as substrings within the fragments of `query`, using case-insensitive matching.

    **Behavior:**
    - For each object in `search_list`, extract fragments using `key(object)`:
      - If `key(object)` returns a string, it is split into fragments by whitespace.
      - If `key(object)` returns a list of strings, each string is treated as a separate fragment.
    - Use the `match` function to check if all extracted fragments are substrings of at least one whitespace-split fragment of `query`, case-insensitively.
    - Collect and return unique objects from `search_list` where this condition is satisfied.

    Args:
        query (str): The string within which to search for matches.
        search_list (list[T]): A list of objects to check against the `query`.
        key (Callable[[T], str | list[str]], optional): A function that takes an object and returns either a string or a list of strings representing the fragments to match against `query`. Defaults to converting the object to a string using `str()`.

    Returns:
        list[T]: A list of unique objects from `search_list` where all extracted fragments match the `query`.

    Examples:
        >>> class Obj:
        ...     def __init__(self, name: str):
        ...         self.name = name
        ...     def __repr__(self):
        ...         return f"Obj({self.name})"
        >>> objects = [Obj("ell"), Obj("wor"), Obj("foo")]
        >>> get_matches_by_attr("Hello World", objects, key=lambda o: o.name)
        [Obj(ell), Obj(wor)]  # "ell" is in "hello", "wor" is in "world"

        >>> class MultiObj:
        ...     def __init__(self, names: list[str]):
        ...         self.names = names
        ...     def __repr__(self):
        ...         return f"MultiObj({self.names})"
        >>> multi_objects = [MultiObj(["ell", "wor"]), MultiObj(["foo", "bar"]), MultiObj(["hello", "world"])]
        >>> get_matches_by_attr("Hello World", multi_objects, key=lambda o: o.names)
        [MultiObj(['ell', 'wor']), MultiObj(['hello', 'world'])]  # All fragments in ["ell", "wor"] and ["hello", "world"] match
    """
    matches: list[T] = []

    # Preprocess query for case-insensitive comparison
    for item in search_list:
        if item not in matches and match(query, key(item)):
            matches.append(item)

    return matches


def get_identifiable_matches(
    query: str, search_dict: dict[str, T]
) -> list[dict[str, T]]:
    """
    Find entries in `search_dict` where either the key or the value (if it is a string) "matches" the `query` string,
    using case-insensitive matching.

    **Behavior:**
    - For each key-value pair in `search_dict`, evaluate:
      - `match(key, query)` returns `True`, or
      - `value` is a string and `match(value, query)` returns `True`.
    - Here, `match(a, b)` checks if all fragments of `a` (split by whitespace) are substrings of at least one fragment
      of `b` (split by whitespace), case-insensitively.
    - If either condition is true and `value not in matches`, append `{key: value}` to the result list. Note that
      `value not in matches` is typically ineffective since `matches` contains dictionaries, but uniqueness is ensured
      by the distinct keys of `search_dict`.
    - Returns a list of unique `{key: value}` dictionaries for matching pairs.

    Args:
        query (str): The string within which to search for matches.
        search_dict (dict[str, T]): A dictionary with string keys and values of type `T`, where keys and string values
            are matched against the `query`.

    Returns:
        list[dict[str, T]]: A list of dictionaries `{key: value}` for each key-value pair where either the key or the
            value (if a string) matches the `query`.

    Examples:
        >>> search_dict = {"ell": "foo", "bar": "wor", "baz": "xyz"}
        >>> get_identifiable_matches("Hello World", search_dict)
        [{'ell': 'foo'}, {'bar': 'wor'}]  # "ell" matches "Hello", "wor" matches "World"
        >>> search_dict = {"a": "ell", "b": "foo", "c": "wor"}
        >>> get_identifiable_matches("Hello World", search_dict)
        [{'a': 'ell'}, {'c': 'wor'}]  # "ell" matches "Hello", "wor" matches "World"
    """
    matches: list[dict[str, T]] = []

    # Preprocess query for case-insensitive comparison
    for key, value in search_dict.items():
        if value not in matches and (
            match(query, key) or (isinstance(value, str) and match(query, value))
        ):
            matches.append({key: value})

    return matches
