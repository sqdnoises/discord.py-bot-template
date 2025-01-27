from typing import (
    TYPE_CHECKING, Any,
    Callable, Coroutine,
    TypeVar, ParamSpec
)

if TYPE_CHECKING:
    from .bot import Bot

from discord.ext import commands

__all__ = (
    "Cog",
)

P = ParamSpec("P")
R = TypeVar("R")

class Cog(commands.Cog):
    bot: "Bot"
    emoji: str | None = None
    hidden: bool = False
    short_description: str | None = None
    
    def run(self, f: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, R]:
        return self.bot.loop.run_in_executor(None, lambda: f(*args, **kwargs))  # pyright: ignore[reportReturnType]