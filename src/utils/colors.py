"""
Color-related utilities.
"""

__all__ = (
    "rgb",
    "hex",
    "int_to_rgb",
    "int_to_hex",
    "rgb_to_hex",
    "hex_to_rgb"
)

def rgb(r: int = 0, g: int = 0, b: int = 0) -> int:
    """Convert RGB to an int hex code."""
    return r << 16 | g << 8 | b

def hex(hex_str: str) -> int:
    """Convert a hex code to an int hex code."""
    hex_str = hex_str.lstrip("#").lower()  # remove leading # and convert to lower case
    
    if len(hex_str) not in (3, 6):
        raise ValueError("Invalid hex code length, it must be 3 or 6 characters long.")
        
    for char in hex_str:
        if char not in "0123456789abcdef":
            raise ValueError("Invalid character in hex code.")

    if len(hex_str) == 3:
        hex_str = hex_str[0] * 2 + hex_str[1] * 2 + hex_str[2] * 2 # expand 3 character string to 6 character string

    return int(hex_str, 16)

def int_to_rgb(int_hex: int) -> tuple[int, int, int]:
    """Convert an int hex code to a `(r, g, b)` tuple."""
    r = int_hex >> 16
    g = int_hex >> 8 & 0xFF
    b = int_hex & 0xFF
    return (r, g, b)

def int_to_hex(int_hex: int, upper: bool = True) -> str:
    """Convert an int hex code to string hex code."""
    return f"#{int_hex:06X}" if upper else f"#{int_hex:06x}"

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert a `(r, g, b)` tuple to a hex code."""
    return int_to_hex(rgb(r, g, b))

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """Convert a hex code to a `(r, g, b)` tuple."""
    return int_to_rgb(hex(hex_str))