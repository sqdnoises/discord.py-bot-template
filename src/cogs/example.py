import logging
import discord
from classes import Bot, Context
from discord.ext import commands
from discord import app_commands

class Example(commands.Cog):
    """Example commands"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def example(self, ctx: Context):
        """Normal command example"""
        await ctx.send("Example")
    
    @app_commands.command(name="slash-example")
    @app_commands.describe(variable="Whatever is in this it says that")
    async def slash_example(interaction: discord.Interaction, variable: str):
        """Slash command example"""
        await interaction.response.send_message(variable)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Example(bot))