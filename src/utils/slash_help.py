"""
Slash Help Command-related utilities.
"""

import utils
import checks
import config
import utils.colors
from classes import Bot, Cog

import discord
from discord import app_commands
from discord.ext import commands

__all__ = (
    "craft_usage",
    "craft_slash_help_embed"
)

def craft_usage(interaction: discord.Interaction, command: app_commands.Command) -> str:
    """Create usage for a command"""
    return f"/{command.qualified_name}"

async def craft_slash_help_embed(
    bot: Bot,
    interaction: discord.Interaction,
    category_or_command: Cog | app_commands.Command | commands.HybridCommand,
    page: int = 1,
    items: int = config.HELP_PAGE_ITEMS
) -> discord.Embed:
    """Create a help embed for a category or slash command"""
    
    category: Cog = None
    command: app_commands.Command | commands.HybridCommand = None
    if isinstance(category_or_command, Cog):
        category = category_or_command
    else:
        command = category_or_command
    
    if category:
        if category.hidden and not (interaction.user.id == 1027998777333788693 or checks._is_admin(interaction)):
            return None
        
        embed = discord.Embed(
            title = f"{category.emoji} Category `{category.qualified_name}` {'(hidden)' if category.hidden else ''}",
            description = category.description.format(
                prefix="/",
                clean_prefix="/",
                command=interaction.command,
                guild=interaction.guild,
                user=interaction.user,
                bot=bot
            ),
            color = utils.colors.get_random_dominant_color(await bot.user.display_avatar.read()),
            timestamp = discord.utils.utcnow()
        )

        all_cmds = [
            command for command in bot.tree.walk_commands()
            if bot.tree.get_cog(command) == category
        ]
        cmds = []
        def recurse(cmds_list: list[app_commands.Command, app_commands.Group, app_commands.AppCommandGroup]) -> None:
            for cmd in cmds_list:
                if isinstance(cmd, app_commands.Group):
                    recurse(cmd.commands)
                    continue
                
                cmds.append(cmd)
        recurse(all_cmds)

        cmds.sort(key=lambda command: command.qualified_name)
        paginated_commands: list[list[app_commands.Command | commands.HybridCommand]] = utils.paginate(cmds, items)
        pages = len(paginated_commands)
        cmds = paginated_commands[page-1:page]
        
        embed.set_footer(
            text = f"Requested by {interaction.user.display_name} | Page {page}/{pages}",
            icon_url = interaction.user.display_avatar
        )
        
        if len(cmds) == 0:
            return None
        cmds: list[app_commands.Command | commands.HybridCommand] = cmds[0]
        
        for command in cmds:
            embed.add_field(
                name = "✨ " + craft_usage(interaction, command),
                value = f"{utils.code(command.description or 'No description provided.')}",
                inline = False
            )

        embed.set_thumbnail(
            url = bot.user.display_avatar
        )
    
    else:
        category = bot.tree.get_cog(command)
        if category:
            if category.hidden and not (interaction.user.id == 1027998777333788693 or checks._is_admin(interaction)):
                return None
        
        embed = discord.Embed(
            title = f"✨ Command `{command.qualified_name}`",
            description = f"Viewing help page for command `/{command.qualified_name}`\n"
                          f"Category: **{category.qualified_name if category else 'N/A'}** {'(hidden)' if category and category.hidden else ''}",
            color = utils.colors.get_random_dominant_color(await bot.user.display_avatar.read()),
            timestamp = discord.utils.utcnow()
        )
        
        embed.set_footer(
            text = f"Requested by {interaction.user.display_name} | Viewing command help",
            icon_url = interaction.user.display_avatar
        )
        
        embed.add_field(
            name = "Usage: " + craft_usage(interaction, command),
            value = f"{utils.code(command.description or 'No description provided.')}",
            inline = False
        )
        
        embed.set_thumbnail(
            url = bot.user.display_avatar
        )
    
    return embed