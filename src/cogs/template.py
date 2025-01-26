from classes import Bot, Cog, Context

import discord
from discord import app_commands
from discord.ext import commands

class Example(Cog):
    """Example cog."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.emoji = "🥺"
        self.short_description = "Example cog"
        
        # Define context menus by our own because discord.py doesn't support adding
        # context menus in cogs automatically to the tree yet.
        self.message_context_menu = app_commands.ContextMenu(
            name = "Example message context menu",
            callback = self.message_context_menu_callback,
            allowed_installs = app_commands.AppInstallationType(guild=True, user=True),
            allowed_contexts = app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
        )
        self.bot.tree.add_command(self.message_context_menu)
        
        self.user_context_menu = app_commands.ContextMenu(
            name = "Example user context menu",
            callback = self.user_context_menu_callback,
            allowed_installs = app_commands.AppInstallationType(guild=True, user=True),
            allowed_contexts = app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True)
        )
        self.bot.tree.add_command(self.message_context_menu)
    
    async def cog_unload(self) -> None:
        # Remove context menus on cog unload to not clog up the tree inconsistently
        self.bot.tree.remove_command(self.message_context_menu.name, type=self.message_context_menu.type)
        self.bot.tree.remove_command(self.user_context_menu.name, type=self.user_context_menu.type)
    
    @commands.command()
    async def example(self, ctx: Context) -> None:
        """Example command"""
        await ctx.send("Hello world!")
    
    @app_commands.command()
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def slash_example(self, interaction: discord.Interaction) -> None:
        """Example slash command"""
        await interaction.response.send_message("Hello world!")
    
    # Triggered when a message is right-clicked and the command in `Apps` category is used.
    async def message_context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:
        """Example message context menu"""
        await interaction.response.send_message("Hello world!")
    
    # Triggered when a user is right-clicked and the command in `Apps` category is used.
    async def user_context_menu_callback(self, interaction: discord.Interaction, user: discord.Member | discord.User) -> None:
        """Example user context menu"""
        await interaction.response.send_message("Hello world!")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Example(bot))