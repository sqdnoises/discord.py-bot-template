"""
Console-related utilities.
"""

import os
import sys
import socket
import platform
import pkg_resources

from .colors import strip_color
from ..logger import logging

__all__ = (
    "mprint",
    "print_versions",
    "print_terminal_size",
    "get_user_and_host",
    "detect_platform",
)


def mprint(text: str = "", fillchar: str = " ", end: str = "\n", flush: bool = False):
    """Print text in the middle of the terminal if possible, and normally if not"""

    try:
        width = os.get_terminal_size().columns

    except:
        print(text, end=end, flush=flush)

    else:
        text = str(text)
        color_stripped = strip_color(text)

        centered_text = color_stripped.center(width, fillchar).replace(
            color_stripped, text
        )
        print(centered_text, end=end, flush=flush)


def print_versions():
    logging.info(f"python {sys.version}")
    logging.info(f"discord.py {pkg_resources.get_distribution('discord.py').version}")


def print_terminal_size():
    try:
        terminal = os.get_terminal_size()
    except:
        logging.warn("could not detect terminal size")
    else:
        logging.info(
            f"detected current terminal size: {terminal.columns}x{terminal.lines}"
        )


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
