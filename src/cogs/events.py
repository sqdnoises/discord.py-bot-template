import utils
import aiohttp
import requests
from logger  import logging

import config
from classes import Bot, Cog, Context

import discord
from discord     import app_commands
from discord.ext import commands, tasks

class Events(Cog):
    """All bot events"""
    
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = None
        self.bot.tree.interaction_check = self.app_command_interaction_check
        self.bot.tree.on_error = self.on_app_command_error
        self.activity_loop.start()
    
    @tasks.loop(minutes=15)
    async def activity_loop(self) -> None:
        await self.bot.change_presence(
            activity = self.bot.create_activity(
                name = f"over {len(self.bot.users)} users",
                type = "watching"
            ),
            status = discord.Status.online
        )
    
    @activity_loop.before_loop
    async def before_activity_loop(self) -> None:
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info(f"serving {len(self.bot.guilds)} guilds and {len(self.bot.users)} users")
        logging.info("ready to handle commands")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, exception: commands.CommandError) -> None:
        if isinstance(exception, commands.MissingRequiredArgument):
            if config.MISSING_ARGUMENT_MESSAGE:
                await ctx.send(config.MISSING_ARGUMENT_MESSAGE.format(
                    argument=exception.param.name,
                    type=exception.param.converter.__name__,
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot
                ))
        
        elif isinstance(exception, commands.MissingPermissions):
            if config.NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions),
                    ctx=ctx,
                    bot=ctx.bot
                ))
        
        elif isinstance(exception, commands.BotMissingPermissions):
            if config.BOT_NO_PERMISSIONS_MESSAGE:
                await ctx.send(config.BOT_NO_PERMISSIONS_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.command,
                    message=ctx.message,
                    user=ctx.author,
                    perms=exception.missing_permissions,
                    permissions=exception.missing_permissions,
                    joined_permissions=", ".join(exception.missing_permissions),
                    joined_permissions_code=", ".join(f"`{permission}`" for permission in exception.missing_permissions),
                    ctx=ctx,
                    bot=ctx.bot
                ))
        
        elif isinstance(exception, commands.CommandNotFound):
            if config.LOG_NOT_FOUND_COMMANDS_TO_CONSOLE:
                logging.error(f"{ctx.author.display_name} (@{ctx.author.name}, id: {ctx.author.id}) used {ctx.message.content} but command `{ctx.message.content[len(ctx.prefix or ""):].split()[0]}` doesn't exist!")
            
            if config.COMMAND_NOT_FOUND_MESSAGE:
                await ctx.send(config.COMMAND_NOT_FOUND_MESSAGE.format(
                    prefix=ctx.prefix,
                    clean_prefix=ctx.clean_prefix,
                    command=ctx.message.content[len(ctx.prefix or ""):].split()[0],
                    message=ctx.message,
                    user=ctx.author,
                    ctx=ctx,
                    bot=ctx.bot,
                ))
        
        else:
            raise exception
    
    async def app_command_interaction_check(self, interaction: discord.Interaction) -> bool:
        """Log slash commands to console"""
        if config.LOG_COMMANDS_TO_CONSOLE and interaction.command and interaction.type == discord.InteractionType.application_command:
            logging.info(f"{interaction.user.display_name} (@{interaction.user.name}, id: {interaction.user.id}) used /{interaction.command.qualified_name} "
                        f"in channel: #{interaction.channel} ({interaction.channel.id if interaction.channel else None}) in guild: {interaction.guild} ({interaction.guild.id if interaction.guild else None})")
        return True
    
    # bot.tree.on_error
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        error_txt = f"An error occurred in `/{interaction.command.qualified_name if interaction.command else '???'}`:"
        
        if interaction.command is not None:
            if interaction.command._has_any_error_handlers():
                return
            
            logging.error(f"Ignoring exception in command {interaction.command.name}", exc_info=error)
        else:
            logging.error("Ignoring exception in command tree", exc_info=error)
        
        if isinstance(error, app_commands.CheckFailure):
            return
        
        if isinstance(error, app_commands.CommandInvokeError):
            e = error.original
        else:
            e = error
        
        if isinstance(e, requests.HTTPError) or isinstance(e, aiohttp.ClientError):
            classname = (e.__class__.__module__+"." if e.__class__.__module__ != "builtins" else "")+e.__class__.__name__
            embed = discord.Embed(
                description = str(e),
                color = discord.Color.brand_red()
            ).set_author(
                name = f"❌ {classname}"
            )
            
            # try except hell
            try:
                await interaction.response.send_message(embed=embed)
            except:
                try:
                    await interaction.followup.send(embed=embed)
                except:
                    try:
                        await interaction.edit_original_response(content=None, embed=embed, view=None)
                    except:
                        await interaction.channel.send(f"{interaction.user.mention} {error_txt}", embed=embed) # type: ignore
            
            return
        
        await interaction.channel.send(interaction.user.mention, embed=discord.Embed( # type: ignore
            description = f"{error_txt}\n"
                          f"{utils.error(e, include_module=True)}",
            color = discord.Color.brand_red()
        ))

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))