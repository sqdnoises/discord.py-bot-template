import os
import sys
import logging
from typing import Optional, Any

from ..termcolors import *

__all__ = (
    "is_docker",
    "stream_supports_colour",
    "ColourFormatter",
    "setup_logging",
    "get_logger",
)

# code heavily inspired from discord.utils.setup_logging


def is_docker() -> bool:
    path = "/proc/self/cgroup"
    return os.path.exists("/.dockerenv") or (
        os.path.isfile(path) and any("docker" in line for line in open(path))
    )


def stream_supports_colour(stream: Any) -> bool:
    is_a_tty = hasattr(stream, "isatty") and stream.isatty()

    # Pycharm and Vscode support colour in their inbuilt editors
    if "PYCHARM_HOSTED" in os.environ or os.environ.get("TERM_PROGRAM") == "vscode":
        return is_a_tty

    if sys.platform != "win32":
        # Docker does not consistently have a tty attached to it
        return is_a_tty or is_docker()

    # ANSICON checks for things like ConEmu
    # WT_SESSION checks if this is Windows Terminal
    return is_a_tty and ("ANSICON" in os.environ or "WT_SESSION" in os.environ)


class ColourFormatter(logging.Formatter):
    LEVEL_COLORS = [
        (logging.DEBUG, bold + bg_black),
        (logging.INFO, bold + blue),
        (logging.WARNING, bold + yellow),
        (logging.ERROR, bold + red),
        (logging.CRITICAL, bg_rgb(200, 0, 0) + white),
    ]

    def __init__(self, *args, name_color: Optional[str] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.FORMATS = {
            level: logging.Formatter(
                f"{bold + black}%(asctime)s{reset} {color}%(levelname)-8s{reset} {name_color or red}%(name)s{reset} %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            for level, color in self.LEVEL_COLORS
        }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


def setup_logging(
    *,
    name: str,
    name_color: Optional[str] = None,
    handler: Optional[logging.Handler] = None,
    formatter: Optional[logging.Formatter] = None,
    level: Optional[int] = None,
    root: bool = False,
) -> None:
    if level is None:
        level = logging.INFO

    if handler is None:
        handler = logging.StreamHandler()

    if formatter is None:
        if isinstance(handler, logging.StreamHandler) and stream_supports_colour(
            handler.stream
        ):
            formatter = ColourFormatter(name_color=name_color)
        else:
            dt_fmt = "%Y-%m-%d %H:%M:%S"
            formatter = logging.Formatter(
                "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
            )

    if root:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(name)

    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
