"""
Check functions that run to check stuff.
"""

import config
from classes import Context

import discord
from discord.ext import commands

def guild_only(ctx: Context = None):
    def predicate(ctx: Context = ctx):
        if not ctx.guild:
            return False
        else:
            return True
    return commands.check(predicate)

def is_guild_owner(ctx: Context = None):
    def predicate(ctx: Context = ctx):
        if not ctx.guild:
            raise commands.MissingPermissions(missing_permissions=[discord.Permissions.all])
        else:
            return True if ctx.guild.owner == ctx.author else False
    return commands.check(predicate)

def is_in_vc(ctx: Context = None):
    def predicate(ctx: Context = ctx):
        if not ctx.author.voice:
            return False
        else:
            return True
    return commands.check(predicate)

def _is_admin(ctx_or_user: Context  | discord.Interaction | discord.Member | discord.User | int):
    if isinstance(ctx_or_user, Context):
        user = ctx_or_user.author
    elif isinstance(ctx_or_user, discord.Interaction):
        user = ctx_or_user.user
    elif isinstance(ctx_or_user, int):
        user = discord.Object(id=ctx_or_user)
    else:
        user = ctx_or_user
    
    if user.id in config.ADMINS:
        return True
    else:
        return False

def is_admin(ctx: Context = None):
    return commands.check(_is_admin(ctx))