"""
Bot-related utilities.
"""

import asyncio
from typing import Sequence, Awaitable, TypeVar, TYPE_CHECKING

from .. import config

if TYPE_CHECKING:
    from ..classes import Bot, BasicPrefix

import discord
from discord.ext import commands

T = TypeVar("T")

__all__ = ("get_prefix", "prevent_ratelimit")


async def get_prefix(bot: "Bot", message: discord.Message) -> "BasicPrefix":
    """Get the prefix for the bot"""
    prefix = config.DEFAULT_PREFIX
    if config.MENTION_IS_ALSO_PREFIX:
        return commands.when_mentioned_or(prefix)(bot, message)
    else:
        return prefix


async def prevent_ratelimit(
    coros: Sequence[Awaitable[T]],
    max_per_time: int,
    time_period: float,
    *,
    return_exceptions: bool = False,
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
        batch = tasks[i : i + max_per_time]
        results.extend(await asyncio.gather(*batch, return_exceptions=True))
        if i + max_per_time < len(
            tasks
        ):  # Avoid unnecessary sleep after the last batch
            await asyncio.sleep(time_period)

    if not return_exceptions:
        # Re-raise exceptions if not handled as results
        for result in results:
            if isinstance(result, BaseException):
                raise result

    return results
