from typing import Literal

__all__ = (
    "code",
    "error",
    "cleanup_code",
    "camelize",
    "trim_and_add_suffix",
    "timestamp",
    "format_size",
)

# Define literal types for parameters
BASE_TYPE = Literal["bytes", "bits"]
PREFIX_TYPE = Literal["decimal", "binary"]
UNIT_FORMAT_TYPE = Literal["short", "full"]
CASE_TYPE = Literal["standard", "lowercase", "uppercase", "capitalized"]
RETURN_TYPE = Literal["both", "number", "unit"]

# Define acceptable unit_type values (all lowercase)
UNIT_TYPE = Literal[
    "highest",
    "bytes",
    "bits",
    "b",
    "kb",
    "mb",
    "gb",
    "tb",
    "pb",
    "kib",
    "mib",
    "gib",
    "tib",
    "pib",
    "kbit",
    "mbit",
    "gbit",
    "tbit",
    "pbit",
    "kilobytes",
    "megabytes",
    "gigabytes",
    "terabytes",
    "petabytes",
    "kibibytes",
    "mebibytes",
    "gibibytes",
    "tebibytes",
    "pebibytes",
    "kilobits",
    "megabits",
    "gigabits",
    "terabits",
    "petabits",
]

# Mapping of unit_type to (base, prefix_type, short_unit)
UNIT_MAPPING = {
    # Base units
    "bytes": ("bytes", "decimal", "B"),
    "bits": ("bits", "decimal", "b"),
    "b": ("bytes", "decimal", "B"),  # "b" alone is bytes (B), distinct from "bits"
    # Bytes with decimal prefixes (1000-based)
    "kb": ("bytes", "decimal", "KB"),
    "mb": ("bytes", "decimal", "MB"),
    "gb": ("bytes", "decimal", "GB"),
    "tb": ("bytes", "decimal", "TB"),
    "pb": ("bytes", "decimal", "PB"),
    "kilobytes": ("bytes", "decimal", "KB"),
    "megabytes": ("bytes", "decimal", "MB"),
    "gigabytes": ("bytes", "decimal", "GB"),
    "terabytes": ("bytes", "decimal", "TB"),
    "petabytes": ("bytes", "decimal", "PB"),
    # Bytes with binary prefixes (1024-based)
    "kib": ("bytes", "binary", "KiB"),
    "mib": ("bytes", "binary", "MiB"),
    "gib": ("bytes", "binary", "GiB"),
    "tib": ("bytes", "binary", "TiB"),
    "pib": ("bytes", "binary", "PiB"),
    "kibibytes": ("bytes", "binary", "KiB"),
    "mebibytes": ("bytes", "binary", "MiB"),
    "gibibytes": ("bytes", "binary", "GiB"),
    "tebibytes": ("bytes", "binary", "TiB"),
    "pebibytes": ("bytes", "binary", "PiB"),
    # Bits with decimal prefixes (1000-based)
    "kbit": ("bits", "decimal", "Kb"),
    "mbit": ("bits", "decimal", "Mb"),
    "gbit": ("bits", "decimal", "Gb"),
    "tbit": ("bits", "decimal", "Tb"),
    "pbit": ("bits", "decimal", "Pb"),
    "kilobits": ("bits", "decimal", "Kb"),
    "megabits": ("bits", "decimal", "Mb"),
    "gigabits": ("bits", "decimal", "Gb"),
    "terabits": ("bits", "decimal", "Tb"),
    "petabits": ("bits", "decimal", "Pb"),
    # Bits with binary prefixes (1024-based)
    "kibit": ("bits", "binary", "Kib"),
    "mibit": ("bits", "binary", "Mib"),
    "gibit": ("bits", "binary", "Gib"),
    "tibit": ("bits", "binary", "Tib"),
    "pibit": ("bits", "binary", "Pib"),
    "kibibits": ("bits", "binary", "Kib"),
    "mebibits": ("bits", "binary", "Mib"),
    "gibibits": ("bits", "binary", "Gib"),
    "tebibits": ("bits", "binary", "Tib"),
    "pebibits": ("bits", "binary", "Pib"),
}

# Unit lists for determining "highest" unit
UNIT_LISTS = {
    ("bytes", "decimal"): ["B", "KB", "MB", "GB", "TB", "PB"],
    ("bytes", "binary"): ["B", "KiB", "MiB", "GiB", "TiB", "PiB"],
    ("bits", "decimal"): ["b", "Kb", "Mb", "Gb", "Tb", "Pb"],
    ("bits", "binary"): ["b", "Kib", "Mib", "Gib", "Tib", "Pib"],
}

# Full names for units
FULL_NAMES = {
    "B": "bytes",
    "KB": "kilobytes",
    "MB": "megabytes",
    "GB": "gigabytes",
    "TB": "terabytes",
    "PB": "petabytes",
    "KiB": "kibibytes",
    "MiB": "mebibytes",
    "GiB": "gibibytes",
    "TiB": "tebibytes",
    "PiB": "pebibytes",
    "b": "bits",
    "Kb": "kilobits",
    "Mb": "megabits",
    "Gb": "gigabits",
    "Tb": "terabits",
    "Pb": "petabits",
    "Kib": "kibibits",
    "Mib": "mebibits",
    "Gib": "gibibits",
    "Tib": "tebibits",
    "Pib": "pebibits",
}


def code(
    text: str, language: str | None = None, ignore_whitespace: bool = False
) -> str:
    """Return a code block version of the text provided"""
    if not ignore_whitespace and text.strip() == "":
        return ""

    return f"```{language or ''}\n{text}\n```"


def error(e: BaseException, *, include_module: bool = False) -> str:
    if include_module:
        classname = (
            e.__class__.__module__ + "." if e.__class__.__module__ != "builtins" else ""
        ) + e.__class__.__name__
    else:
        classname = e.__class__.__name__

    error_formatted = f"[ERROR]: {classname}\n" f" -> {e}\n"
    return code(error_formatted, "prolog")


def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

    # remove `foo`
    return content.strip("` \n")


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
        raise ValueError(
            "max_length must be greater than or equal to the length of the suffix."
        )

    if len(input_string) > max_length:
        return input_string[: max_length - len(suffix)] + suffix
    return input_string


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


def format_number(
    number: int, decimal_points: int = 0, *, pad_decimal: bool = False
) -> str:
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


def format_size(
    size_bytes: int,
    decimal_places: int = 2,
    *,
    unit_type: UNIT_TYPE = "highest",
    unit_format: UNIT_FORMAT_TYPE = "short",
    case: CASE_TYPE = "standard",
    separator: str = " ",
    return_type: RETURN_TYPE = "both",
    fix_decimal: bool = False,
) -> str | float:
    """
    Convert a size in bytes to a specified unit type and format.

    Parameters:
    - size_bytes: int, the size in bytes to convert
    - unit_type: UNIT_TYPE, the target unit or "highest" (e.g., "kb", "gigabytes", "kibibits")
    - unit_format: UNIT_FORMAT_TYPE, "short" (e.g., "KB") or "full" (e.g., "kilobytes")
    - case: CASE_TYPE, the case for the unit text
    - separator: str, string between number and unit when return_type="both" (default is " ")
    - return_type: RETURN_TYPE, "both" (number and unit), "number" (float), or "unit" (str)
    - decimal_places: int, number of decimal places for the number (default is 2)
    - fix_decimal: bool, whether to fix decimal places with trailing zeros (default is False)

    Returns:
    - Union[str, float]:
      - "both": str, number and unit (e.g., "1.5 MB")
      - "number": float, the converted value (e.g., 1.5)
      - "unit": str, the unit (e.g., "MB")

    Raises:
    - ValueError: if unit_type is invalid
    """
    if unit_type == "highest":
        # Default to bytes with decimal prefixes when "highest" is specified
        base: BASE_TYPE = "bytes"
        prefix_type: PREFIX_TYPE = "decimal"
    else:
        if unit_type not in UNIT_MAPPING:
            raise ValueError(f"Invalid unit_type '{unit_type}'")
        base, prefix_type, short_unit = UNIT_MAPPING[
            unit_type
        ]  # pyright: ignore[reportAssignmentType]

    # Get the unit list for the base and prefix_type
    unit_list = UNIT_LISTS[(base, prefix_type)]
    base_value = 1000 if prefix_type == "decimal" else 1024
    size_in_base = size_bytes if base == "bytes" else size_bytes * 8

    if unit_type == "highest":
        # Find the highest appropriate unit
        for i in range(len(unit_list) - 1, -1, -1):
            multiplier = base_value**i
            if size_in_base >= multiplier:
                selected_unit = unit_list[i]
                value = size_in_base / multiplier
                break
        else:
            selected_unit = unit_list[0]
            value = float(size_in_base)
    else:
        # Use the specific unit from UNIT_MAPPING
        selected_unit = UNIT_MAPPING[unit_type][2]
        index = unit_list.index(selected_unit)
        multiplier = base_value**index
        value = size_in_base / multiplier

    # Format the unit string
    unit_str = FULL_NAMES[selected_unit] if unit_format == "full" else selected_unit
    if case == "lowercase":
        unit_str = unit_str.lower()
    elif case == "uppercase":
        unit_str = unit_str.upper()
    elif case == "capitalized":
        unit_str = unit_str.capitalize()
    # "standard" keeps the unit as is

    # Handle return_type
    if return_type == "number":
        return value
    elif return_type == "unit":
        return unit_str

    # Format the number for "both"
    if decimal_places == 0:
        num_str = str(int(value))
    else:
        num_str = f"{value:.{decimal_places}f}"
        if not fix_decimal:
            num_str = num_str.rstrip("0").rstrip(".")
        # If fix_decimal is True, keep the full precision with trailing zeros

    return num_str + separator + unit_str
