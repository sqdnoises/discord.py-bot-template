"""
This module contains all the utilities that would be needed in the bot.
"""

import os
import re
import sys
import socket
import asyncio
import pkgutil
import platform
from typing    import (
    Any, TypeVar,
    Iterable, Sequence,
    Callable, Awaitable
)
from itertools import islice

__all__ = (
    "format_number",
    "list_modules",
    "mprint",
    "camelize",
    "timestamp",
    "trim_and_add_suffix",
    "strip_color",
    "code",
    "error",
    "cleanup_code",
    "match_space_fuzzy",
    "paginate",
    "clamp",
    "detect_platform",
    "slice",
    "prevent_ratelimit"
)

T = TypeVar("T")

def format_number(number: int, decimal_points: int = 0, *, pad_decimal: bool = False) -> str:
    """
    Formats a large number with suffixes like K, M, B, etc. based on its magnitude.
    
    Parameters:
    - number (int): The number to be formatted.
    - decimal_points (int): The number of decimal places to display. Default is 0.
    - pad_decimal (bool): If True, adds trailing zeroes to decimals if needed. Default is False.
    
    Returns:
    - str: The formatted string with appropriate suffix and decimal places.
    
    Example:
    >>> format_number(1000000)
    '1M'
    >>> format_number(123456, decimal_points=2)
    '123.46K'
    >>> format_number(123000, decimal_points=2, pad_decimal=False)
    '123K'
    """
    
    if number < 1000:
        return str(number)
    
    suffixes = ["K", "M", "B", "T"]
    magnitude = 0
    num = number
    
    while num >= 1000 and magnitude < len(suffixes):
        magnitude += 1
        num /= 1000
    
    # Round the number to the specified decimal places
    if decimal_points:
        formatted_number = f"{num:.{decimal_points}f}"
    else:
        formatted_number = str(int(num))
    
    # Remove trailing decimals if pad_decimal is False
    if not pad_decimal and decimal_points:
        formatted_number = formatted_number.rstrip("0").rstrip(".")
    
    return f"{formatted_number}{suffixes[magnitude-1]}"

def list_modules(package: str | Any) -> list[str]:
    if type(package) == str:
        package = __import__(package)
    
    modules = []
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__+"."): # pyright: ignore[reportAttributeAccessIssue]
        modules.append(modname)
    
    return modules

def mprint(text: str = "", fillchar: str = " ", end: str = "\n", flush: bool = False):
    """Print text in the middle of the terminal if possible, and normally if not"""
    
    try:
        width = os.get_terminal_size().columns
    
    except:
        print(text, end=end, flush=flush)
    
    else:
        text = str(text)
        color_stripped = strip_color(text)
        
        centered_text = color_stripped.center(width, fillchar).replace(color_stripped, text)
        print(centered_text, end=end, flush=flush)

def camelize(s: str) -> str:
    string = list(s)
    punctuate = True
    for i, c in enumerate(string):
        if punctuate:
            string[i] = c.upper()
        if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            punctuate = True
        else:
            punctuate = False
    return "".join(string)

def timestamp(seconds: int) -> str:
    # Calculate hours, minutes, and seconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    # Determine the format based on the presence of hours
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"

def trim_and_add_suffix(input_string: str, max_length: int, suffix: str = "...") -> str:
    """
    Trims the input string to fit within the max_length, appending the suffix if truncated.

    Args:
        input_string (str): The string to process.
        max_length (int): The maximum allowed length of the result.
        suffix (Optional[str]): The suffix to append if the string is truncated. Defaults to "...".

    Returns:
        str: The processed string.
    """
    if max_length < len(suffix):
        raise ValueError("max_length must be greater than or equal to the length of the suffix.")

    if len(input_string) > max_length:
        return input_string[:max_length - len(suffix)] + suffix
    return input_string

def strip_color(text: str) -> str:
    """Strip all color codes from a string"""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)

def code(text: str, language: str | None = None, ignore_whitespace: bool = False) -> str:
    """Return a code block version of the text provided"""
    if not ignore_whitespace and text.strip() == "":
        return ""
    
    return f"```{language or ''}\n{text}\n```"

def error(e: Exception, *, include_module: bool = False) -> str:
    if include_module:
        classname = (e.__class__.__module__+"." if e.__class__.__module__ != "builtins" else "")+e.__class__.__name__
    else:
        classname = e.__class__.__name__
    
    error_formatted = (
        f"[ERROR]: {classname}\n"
        f" -> {e}\n"
    )
    return code(error_formatted, "prolog")

def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    
    # remove `foo`
    return content.strip('` \n')

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
        if (query_lower == item_lower
            or query_lower in item_lower
            or match_space_fuzzy(item, query)) and item not in matches:
            matches.append(item)
    
    return matches

def paginate(
    array: Iterable[Any],
    count: int = 3,
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

    That was just the basic usage. By default the count variable is set to 3.
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

def clamp(value: int | float, lower_limit: int | float, upper_limit: int | float) -> int | float:
    return max(lower_limit, min(value, upper_limit))

def get_user_and_host():
    """Gets the username and hostname in a cross-platform way.

    Returns:
        tuple: A tuple containing the username (str) and hostname (str), or None for either value if it cannot be retrieved.
    """
    
    username = None
    if platform.system() == "Windows":
        username = os.environ.get("USERNAME")
    
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        username = os.environ.get("USER")
        if not username:  # Try different variable if USER is not present
            username = os.environ.get("LOGNAME")
    
    hostname = None
    try:
        hostname = socket.gethostname()
    except Exception:
        pass  # hostname may not always be available
    
    return username, hostname

def detect_platform():
    """Detect what platform the code is being run at"""
    
    if "ANDROID_ROOT" in os.environ:
        if "TERMUX_APP__APK_RELEASE" in os.environ:
            if os.getenv("TERMUX_APP__APK_RELEASE") == "F_DROID":
                return "android/termux-(f-droid)"
            else:
                return "android/termux-(google play store)"
        return "android"
    
    elif os.name == "nt":
        _, _, build_number, _ = platform.win32_ver()
        release = sys.getwindowsversion().major
        return f"windows {release}/build {build_number}"
    
    elif sys.platform == "darwin":
        version = platform.mac_ver()[0]
        return f"macos {version}"
    
    elif os.name == "posix":
        name = platform.system()
        version = platform.version()
        
        if name and version:
            return f"linux/{name} {version}"
        elif name:
            return f"linux/{name}"
        return "linux/other"
    
    else:
        return "other"

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

async def prevent_ratelimit(
    coros: Sequence[Awaitable[T]],
    max_per_time: int,
    time_period: float,
    *,
    return_exceptions: bool = False
) -> list[T | BaseException]:
    """
    Executes coroutines while respecting rate limits.

    Args:
        coros (Sequence[Awaitable[T]]): A list of multiple coroutine arguments.
        max_per_time (int): Maximum number of coroutines to run in the specified time period.
        time_period (float): The time period in seconds for the rate limit.
        return_exceptions (bool, optional): Whether to return exceptions like `asyncio.gather`. Defaults to False.

    Returns:
        list[T | BaseException]: The results of the coroutines in the same order. If `return_exceptions` is True,
        exceptions are included in the result list; otherwise, they raise normally.
    """
    results: list[T | BaseException] = []
    semaphore = asyncio.Semaphore(max_per_time)
    
    async def limited_execution(coroutine: Awaitable[T]) -> T | BaseException:
        async with semaphore:
            try:
                return await coroutine
            except BaseException as e:
                if return_exceptions:
                    return e
                raise
    
    tasks = [limited_execution(coro) for coro in coros]
    for i in range(0, len(tasks), max_per_time):
        batch = tasks[i:i + max_per_time]
        results.extend(await asyncio.gather(*batch, return_exceptions=True))
        if i + max_per_time < len(tasks):  # Avoid unnecessary sleep after the last batch
            await asyncio.sleep(time_period)
    
    if not return_exceptions:
        # Re-raise exceptions if not handled as results
        for result in results:
            if isinstance(result, BaseException):
                raise result
    
    return results