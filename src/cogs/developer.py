import io
import os
import sys
import copy
import json
import time
import random
import asyncio
import datetime
import textwrap
import pkg_resources
from typing import Literal, Optional
from contextlib import redirect_stdout, redirect_stderr

from .. import utils
from .. import checks
from .. import config
from ..utils import get_logger
from ..classes import Bot, Cog, Context

import discord
from discord import app_commands
from discord.ext import commands

logger = get_logger(__name__)


class Developer(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._last_result = None

    async def cog_check(self, ctx: Context) -> bool:
        return checks.is_admin(ctx)

    @commands.command(aliases=["load-extension"])
    async def load(self, ctx: Context, cog: str) -> None:
        """Load a cog"""
        ext = "cogs." + cog
        logger.warning(
            f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to load `{ext}`"
        )
        await self.bot.load_extension(ext)
        await ctx.send(f"✅ Loaded the extension: `{ext}`")
        logger.info(f"successfully loaded `{ext}`")

    @commands.command(aliases=["unload-extension"])
    async def unload(self, ctx: Context, cog: str) -> None:
        """Unload a cog"""
        ext = "cogs." + cog
        logger.warning(
            f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to unload `{ext}`"
        )
        await self.bot.unload_extension(ext)
        await ctx.send(f"✅ Unloaded the extension: `{ext}`")
        logger.info(f"successfully unloaded `{ext}`")

    @commands.command(
        aliases=["r", "re", "reload-all", "reload-extension", "reload-all-extensions"]
    )
    async def reload(self, ctx: Context, *cogs: str) -> None:
        """Reload an or all cogs"""
        if len(cogs) == 0:
            extensions = [k for k in self.bot.extensions.keys()]

            msg = await ctx.send("🔨 Reloading all extensions...")
            logger.warning(
                f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload all extensions"
            )

        else:
            extensions = ["cogs." + cog for cog in cogs]

            msg = await ctx.send(f"🔨 Reloading: `{'`, `'.join(extensions)}`")
            logger.warning(
                f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload `{'`, `'.join(extensions)}`"
            )

        ext_status = ""
        for ext in extensions:
            try:
                await self.bot.reload_extension(ext)

            except Exception as e:
                t = f"failed to reload `{ext}`: `{e.__class__.__name__}`"
                logger.error(t, exc_info=e)
                ext_status += "❌ " + t[0].upper() + t[1:] + "\n"

            else:
                t = f"successfully reloaded `{ext}`"
                logger.info(t)
                ext_status += "✅ " + t.capitalize() + "\n"

        await msg.edit(content=ext_status)

    @commands.command(aliases=["exts", "loaded", "loaded-extensions"])
    async def extensions(self, ctx: Context) -> None:
        """List all loaded cogs"""
        paginated_list = utils.paginate([f"`{k}`" for k in self.bot.extensions.keys()])
        extensions = [", ".join(group) for group in paginated_list]
        extensions = ",\n".join(extensions)

        await ctx.send("All loaded extensions:\n" + extensions)

    @load.error
    @unload.error
    @reload.error
    async def on_extension_error(
        self, ctx: Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CheckFailure) or isinstance(
            error, commands.MissingRequiredArgument
        ):
            return

        elif isinstance(error, commands.CommandInvokeError):
            e = error.original

            if ctx.command and len(ctx.args) > 2:
                ext = "cogs." + ctx.args[2]
                logger.error(
                    f"failed to {ctx.command.name} `{ext}`: `{error.__class__.__name__}`",
                    exc_info=error,
                )
                await ctx.send(
                    f"❌ Error occurred while {ctx.command.name}ing the extension: `{ext}`\n"
                    + utils.code(f"{e.__class__.__name__}: {str(e)}")
                )

            else:
                raise error

        else:
            raise error

    @commands.command()
    async def restart(self, ctx: Context) -> None:
        """Restart the bot"""
        logger.warning(
            f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) is restarting the bot"
        )

        if self.bot.log_channel is not None:
            logger.warning("informing logs channel")
            try:
                await self.bot.log_channel.send(
                    f"**{ctx.author.display_name}** is restarting the bot\n"
                    f"-# {ctx.author.name} ({ctx.author.id})"
                )
            except Exception as e:
                logger.error(
                    "couldn't inform logs channel, ignoring and restarting", exc_info=e
                )
        else:
            logger.warning(
                "log_channel is not set, restarting without informing logs channel..."
            )

        try:
            await ctx.react("🫠")
        except Exception as e:
            logger.error(
                "couldn't react to message, ignoring and restarting", exc_info=e
            )

        logger.warning(
            "closing bot and replacing current process with a new one by running:\n"
            f"`{' '.join([sys.executable] + sys.argv)}` in os.execv()"
        )
        await self.bot.close()
        os.execv(sys.executable, ["python"] + sys.argv)

    @commands.command()
    async def shutdown(self, ctx: Context) -> None:
        """Shutdown the bot"""
        logger.warning(
            f"{ctx.author.display_name} (@{ctx.author}, id: {ctx.author.id}) is shutting down the bot"
        )

        if self.bot.log_channel is not None:
            logger.warning("informing logs channel")
            try:
                await self.bot.log_channel.send(
                    f"**{ctx.author.display_name}** is shutting down the bot\n"
                    f"-# {ctx.author.name} ({ctx.author.id})"
                )
            except Exception as e:
                logger.error(
                    "couldn't inform logs channel, ignoring and shutting down",
                    exc_info=e,
                )

        else:
            logger.warning(
                "log_channel is not set, shutting down without informing logs channel..."
            )

        try:
            await ctx.react("🫀")
        except Exception as e:
            logger.error(
                "couldn't react to message, ignoring and shutting down", exc_info=e
            )

        logger.warning("shutting down")
        await self.bot.close()

    @commands.command(name="generate-invite", aliases=["invite"])
    async def generate_invite(self, ctx: Context) -> None:
        """Generate a bot invite link for testing purposes"""
        await ctx.send(
            f"**[Click to invite me to a server](https://discord.com/oauth2/authorize?client_id={self.bot.application_id}&permissions=8&scope=bot+applications.commands)**"
        )

    @commands.command()
    async def sudo(
        self,
        ctx: Context,
        channel: Optional[discord.TextChannel],
        who: discord.Member | discord.User,
        *,
        command: str,
    ) -> None:
        """Run a command as another user optionally in another channel"""

        assert ctx.prefix is not None

        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)

    @commands.command(name="exec", aliases=["eval", "run"])
    async def _exec(self, ctx: Context, *, code: str) -> None:
        """Execute async code"""
        bot = self.bot

        logger.warning(
            f"{ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})"
        )

        env = {
            "bot": bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "user": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "log_channel": bot.log_channel,
            "_": self._last_result,
            "os": os,
            "sys": sys,
            "json": json,
            "time": time,
            "random": random,
            "asyncio": asyncio,
            "datetime": datetime,
            "config": config,
            "discord": discord,
            "commands": commands,
            "app_commands": app_commands,
        }

        env.update(globals())

        code = utils.cleanup_code(code)
        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(code, '    ')}"

        async with ctx.typing():
            t = time.monotonic()

            try:
                exec(to_compile, env)

            except Exception as e:
                t = time.monotonic() - t  # in seconds
                if t < 1:
                    t = round(t * 1000)  # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t / 60, 2)  # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2)  # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try:
                    await ctx.failure()
                except:
                    pass

                embed = discord.Embed(
                    title="Execution Failed at exec()",
                    description=utils.error(e, include_module=True),
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow(),
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(
                    version=sys.version_info
                )
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name="System Info",
                    value=f"Python `{version}`\n" f"discord.py `{dpy_version}`",
                )

                embed.add_field(
                    name="Execution Info",
                    value=f"Took `{time_text}`\n" f"Return Type: `{type(e)}`",
                )

                embed.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.display_avatar,
                )

                self._last_result = e
                logger.error(
                    f"failed at `exec()` ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))",
                    exc_info=e,
                )
                try:
                    await ctx.send(embed=embed)
                except Exception as e:
                    error = utils.error(e, include_module=True)
                    await ctx.send(f"An error occurred.\n" f"{error}")
                    logger.error(
                        "error occurred while sending exec() failed embed", exc_info=e
                    )

            func = env["func"]
            try:
                with redirect_stdout(stdout), redirect_stderr(stdout):
                    ret = await func()

            except Exception as e:
                t = time.monotonic() - t  # in seconds
                if t < 1:
                    t = round(t * 1000)  # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t / 60, 2)  # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2)  # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try:
                    await ctx.failure()
                except:
                    pass

                output = stdout.getvalue()

                embed = discord.Embed(
                    title="Execution Failed",
                    description=f"### Output:\n"
                    f"{utils.code(output or 'No output recorded.', 'prolog')}",
                    color=discord.Color.red(),
                    timestamp=discord.utils.utcnow(),
                )

                embed.add_field(
                    name="Error",
                    value=utils.error(e, include_module=True),
                    inline=False,
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(
                    version=sys.version_info
                )
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name="System Info",
                    value=f"Python `{version}`\n" f"discord.py `{dpy_version}`",
                )

                embed.add_field(
                    name="Execution Info",
                    value=f"Took `{time_text}`\n" f"Return Type: `{type(e)}`",
                )

                embed.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.display_avatar,
                )

                self._last_result = e

                output = f"{output}\n" f"Time taken: {time_text}"

                logger.error(
                    f"EXECUTION FAILED! output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                    f"{output}"
                )
                logger.error(
                    f"execution failed ({ctx.clean_prefix}exec by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}))",
                    exc_info=e,
                )

                try:
                    await ctx.send(embed=embed)
                except discord.HTTPException:
                    await ctx.send("Embed too big to send. Check console.")
                except Exception as e:
                    error = utils.error(e)
                    await ctx.send(f"An error occurred.\n" f"{error}")
                    logger.error(
                        "error occurred while sending execution failed embed",
                        exc_info=e,
                    )

            else:
                t = time.monotonic() - t  # in seconds
                if t < 1:
                    t = round(t * 1000)  # in milliseconds and round
                    time_text = f"{t}ms"

                elif t > 60:
                    t = round(t / 60, 2)  # in minutes and round to 2 decimal places
                    time_text = f"{t}m"

                else:
                    t = round(t, 2)  # if in seconds then round to 2 decimal places
                    time_text = f"{t}s"

                try:
                    await ctx.success()
                except:
                    pass

                output = stdout.getvalue()

                output_embed = utils.code(
                    (output or "No output recorded.")
                    + (f"\n-- {repr(ret)}" if ret is not None else ""),
                    "prolog",
                )

                embed = discord.Embed(
                    title="Execution Successful",
                    description=f"### Output:\n" f"{output_embed}",
                    color=discord.Color.green(),
                    timestamp=discord.utils.utcnow(),
                )

                version = "{version.major}.{version.minor}.{version.micro}".format(
                    version=sys.version_info
                )
                dpy_version = pkg_resources.get_distribution("discord.py").version
                embed.add_field(
                    name="System Info",
                    value=f"Python `{version}`\n" f"discord.py `{dpy_version}`",
                )

                embed.add_field(
                    name="Execution Info",
                    value=f"Took `{time_text}`\n" f"Return Type: `{type(ret)}`",
                )

                embed.set_footer(
                    text=f"Requested by {ctx.author}",
                    icon_url=ctx.author.display_avatar,
                )

                self._last_result = ret

                output = (
                    f"{output}\n"
                    f"Returned: {repr(ret)}\n"
                    f"Type: {type(ret)}\n"
                    f"Time taken: {time_text}"
                )

                logger.info(
                    f"execution successful; output of `exec` {ctx.clean_prefix}exec called by {ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id})\n"
                    f"{output}"
                )

                try:
                    if ctx.out:
                        await ctx.send(embed=embed)
                except discord.HTTPException:
                    await ctx.send("Embed too big to send. Check console.")
                except Exception as e:
                    error = utils.error(e)
                    await ctx.send(f"An error occurred.\n" f"{error}")
                    logger.error(
                        "error occurred while sending exec successful embed", exc_info=e
                    )

    @commands.guild_only()
    @commands.command()
    async def sync(
        self,
        ctx: Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """
        Sync slash commands (Umbra's Sync Command)
        https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
        """

        assert ctx.guild is not None

        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands{' globally' if spec is None else ' to the current guild'}."
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Developer(bot))
