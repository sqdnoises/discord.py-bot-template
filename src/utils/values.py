__all__ = ("clamp",)


def clamp(
    value: int | float, lower_limit: int | float, upper_limit: int | float
) -> int | float:
    return max(lower_limit, min(value, upper_limit))
