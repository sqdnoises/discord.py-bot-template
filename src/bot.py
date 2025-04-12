"""
## `discord.py` bot template
a discord.py bot template that I use for my bots.

Copyright (c) 2023-present SqdNoises
Licensed under the MIT License
For more information, please check the provided LICENSE file.
"""

import os
import sys

if __name__ == "__main__":
    from termcolors import *

    executable = os.path.split(sys.executable)[-1]
    if executable.endswith(".exe"):
        executable = executable[:-4]

    dirname = os.path.split(os.path.dirname(os.path.abspath(__file__)))[-1]

    print(
        f"{red}Please go back one directory and run:{reset}\n"
        f"{blue}{bold}>{reset} {yellow}{executable} -m {dirname}{reset}",
        flush=True,
    )
    os._exit(1)

import logging
from datetime import datetime

from .config import (
    BOT_NAME,
    ADMINS,
    DEBUG,
    LOGS_FOLDER,
    LOG_FILENAME_TIME_FORMAT,
)
from .utils import (
    get_logger,
    setup_logging,
    get_prefix,
    print_terminal_size,
    print_versions,
)
from .classes import Bot
from .termcolors import *

import discord
from dotenv import load_dotenv

setup_logging(level=logging.DEBUG if DEBUG else None)
discord.utils.setup_logging(root=False)

logger = get_logger()
logger.info("initialising")

if DEBUG:
    logger.debug("Houston, we have a code GRAY (DEBUG)")
    logger.debug("debug mode enabled")

if LOGS_FOLDER:
    os.makedirs(LOGS_FOLDER, exist_ok=True)
    filepath = os.path.join(
        LOGS_FOLDER,
        f"{BOT_NAME} {datetime.now().strftime(LOG_FILENAME_TIME_FORMAT)}.log",
    )

    log_file_formatter = logging.Formatter(
        "{asctime} {levelname:<8} {name} > {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )

    log_file_handler = logging.FileHandler(filepath)
    log_file_handler.setFormatter(log_file_formatter)
    log_file_handler.setLevel(logging.DEBUG)

    logger.addHandler(log_file_handler)
    logger.debug(f"{BOT_NAME} file handler set up")

    logging.getLogger("discord").addHandler(log_file_handler)
    logger.debug("discord.py file handler set up")

print_versions()

load_dotenv()
logger.info("loaded environment variables")

bot = Bot(
    command_prefix=get_prefix,
    strip_after_prefix=True,
    status=discord.Status.idle,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="the world burn"
    ),
)

print_terminal_size()


def start(*args, **kwargs):
    """Start the bot"""
    logger.info(f"starting {BOT_NAME}")

    if not ADMINS:
        logger.critical(
            "no admins found in the config file, please add atleast one user ID"
        )
        return

    token = os.getenv("TOKEN")

    if token:
        bot.run(token, *args, **kwargs)
    else:
        logger.critical(
            "environment variable 'TOKEN' not found. are you sure you have setup your `.env` file correctly?"
        )
