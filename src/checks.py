import discord
import config
from discord.ext import commands
from classes import Context

def guild_only(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.guild:
            return False
        else:
            return True
    return commands.check(predicate)

def is_guild_owner(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.guild:
            return False
        else:
            return True if ctx.guild.owner == ctx.author else False
    return commands.check(predicate)

def is_in_vc(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if not ctx.author.voice:
            return False
        else:
            return True
    return commands.check(predicate)

def is_admin(ctx: Context = None):
    async def predicate(ctx: Context = ctx):
        if await ctx.bot.is_owner(ctx.author) or \
           ctx.author.id in config.ADMIN:
            return True
        else:
            return False
    return commands.check(predicate)