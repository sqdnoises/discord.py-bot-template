from typing import (
    Any, Iterable,
    Callable, Awaitable,
    TypeVar, ParamSpec
)

from classes.bot         import Bot
from classes.cog         import Cog
from classes.context     import Context
from classes.commandtree import CommandTree

from discord import Message

__all__ = (
    "BotT",
    "CogT",
    "ContextT",
    "ContextT_co",
    "CommandTreeT",
    "BasicPrefix",
    "SyncPrefixFunc",
    "AsyncPrefixFunc",
    "PrefixType"
)

T = TypeVar("T")
P = ParamSpec("P")

MaybeAwaitable     = T | Awaitable[T]
MaybeAwaitableFunc = Callable[P, MaybeAwaitable[T]]

BotT         = TypeVar("BotT",         bound=Bot,        covariant=True)
CogT         = TypeVar("CogT",         bound=Cog                       )
ContextT     = TypeVar("ContextT",     bound=Context                   )
ContextT_co  = TypeVar("ContextT_co",  bound=Context,    covariant=True)
CommandTreeT = TypeVar("CommandTreeT", bound=CommandTree               )

BasicPrefix     = str | Iterable[str]
SyncPrefixFunc  = Callable[[Bot, Message], BasicPrefix]
AsyncPrefixFunc = Callable[[Bot, Message], Awaitable[BasicPrefix]]
PrefixType      = BasicPrefix | SyncPrefixFunc | AsyncPrefixFunc
