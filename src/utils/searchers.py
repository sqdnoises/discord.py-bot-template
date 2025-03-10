"""
Search-related utilities.
"""

__all__ = ("match_space_fuzzy", "get_matches")


def match_space_fuzzy(text: str, query: str, splitter: str = " ") -> bool:
    """
    Match all query fragments against text words. Words don't need to be in order,
    and fragments can partially match words.
    """
    text_words = text.lower().split(splitter)
    query_fragments = query.lower().split(splitter)
    for fragment in query_fragments:
        # Check if any word in the text starts with or contains the fragment
        if not any(fragment in word for word in text_words):
            return False
    return True


def get_matches(query: str, search_list: list[str]) -> list[str]:
    """
    Finds matches for a query string in a list of strings using direct match, substring match, and fuzzy matching.

    Args:
        query (str): The query string to search for.
        search_list (list[str]): A list of strings to search within.

    Returns:
        list[str]: A list of matched strings.
    """
    matches: list[str] = []

    # Preprocess query for case-insensitive comparison
    query_lower = query.lower()

    for item in search_list:
        item_lower = item.lower()

        # Check for direct match
        if (
            query_lower == item_lower
            or query_lower in item_lower
            or match_space_fuzzy(item, query)
        ) and item not in matches:
            matches.append(item)

    return matches
