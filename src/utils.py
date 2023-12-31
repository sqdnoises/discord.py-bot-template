import os
from typing import Callable, List

import aiohttp

def mprint(text: str = "", end: str = "\n", flush: bool = False):
    """Print text in the middle of the terminal if possible, and normally if not"""
    
    try:
        width = os.get_terminal_size().columns
    
    except:
        print(text, end=end, flush=flush)
    
    else:
        text = str(text)
        text_length = len(text)
        if text_length < width:
            spaces = " " * (int(width/2) - int(text_length/2))
        
        else:
            spaces = ""
        
        print(spaces+text, end=end, flush=flush)

def code(text: str, language: str = "py"):
    """Return a code block version of the text provided"""
    return f"```{language}\n{text}\n```"

def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

def paginate(array: list | tuple | set, count: int = 3, debug: bool = False, logger: Callable = print) -> list:
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

def detect_platform():
    """Detect what platform the code is being run at"""

    if "ANDROID_ARGUMENT" in os.environ:
        return "android"
    elif os.name == "nt":
        return "windows"
    elif os.name == "posix":
        return "linux"
    else:
        return "other"

def slice(text: str, max: int = 2000) -> List[str]:
    """Slice a message up into multiple messages"""
    return [text[i:i+max] for i in range(0, len(text), max)]

async def get_raw_content_data(url: str, *args, **kwargs):
    """Get raw content like files and media as bytes"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=True if url.lower().startswith("https") else False, *args, **kwargs) as response:
            return await response.content.read()