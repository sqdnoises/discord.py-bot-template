"""
## `discord.py` bot template
a discord.py bot template that I use for my bots.

Copyright (c) 2023-present SqdNoises
Licensed under the MIT License
For more information, please check the provided LICENSE file.
"""

from .bot import start
from .termcolors import *

if __name__ == "__main__":
    start()
    print(
        f"{bold}{blue}> {yellow}cya later {green}alligator {magenta}:3{reset}",
        flush=True,
    )
