import os
from typing import Literal, Callable

import discord

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
    return f"```{language}\n{text}\n```"

def paginate(array: list | tuple | set, count: int = 3, debug: bool = False, logger: Callable = print) -> list:
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

def create_activity(name: str, type: Literal["playing", "streaming", "listening", "watching"] = "playing") -> discord.Activity:
    all_activities = {
        "playing":   discord.Game(name=name),
        "streaming": discord.Streaming(name=name),
        "listening": discord.Activity(type=discord.ActivityType.listening, name=name),
        "watching":  discord.Activity(type=discord.ActivityType.watching, name=name)
    }
    return all_activities[type]