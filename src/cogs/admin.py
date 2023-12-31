import utils

from typing import List
import checks
import logging as logger
from classes import Bot, Context
from discord.ext import commands

@checks.is_admin()
class Admin(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=["load_extension"])
    async def load(self, ctx: Context, cog: str):
        """Load a cog"""
        
        ext = "cogs."+cog
        logger.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to load `{ext}`")
        await self.bot.load_extension(ext)
        await ctx.send(f"✅ Loaded the extension: `{ext}`")
        logger.info(f"successfully loaded `{ext}`")

    @commands.command(aliases=["unload_extension"])
    async def unload(self, ctx: Context, cog: str):
        """Unload a cog"""
        
        ext = "cogs."+cog
        logger.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to unload `{ext}`")
        await self.bot.unload_extension(ext)
        await ctx.send(f"✅ Unloaded the extension: `{ext}`")
        logger.info(f"successfully unloaded `{ext}`")

    @commands.command(aliases=["re", "reload_all", "reload_extension", "reload_all_extensions"])
    async def reload(self, ctx: Context, *cogs: str):
        """Reload a or all cogs"""
        
        if len(cogs) == 0:
            extensions = [k for k in self.bot.extensions.keys()]
            
            msg = await ctx.send("🔨 Reloading all extensions...")
            logger.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload all extensions")
        
        else:
            extensions = ["cogs."+cog for cog in cogs]
            
            msg = await ctx.send(f"🔨 Reloading: `{'`, `'.join(extensions)}`")
            logger.warning(f"{ctx.author.display_name} (@{ctx.author}, {ctx.author.id}) wants to reload `{'`, `'.join(extensions)}`")
        
        ext_status = ""
        for ext in extensions:
            try:
                await self.bot.reload_extension(ext)
            
            except Exception as e:
                t = f"failed to reload `{ext}`: `{e.__class__.__name__}`"
                logger.exception(t)
                ext_status += "❌ " + t[0].upper() + t[1:] + "\n"
            
            else:
                t = f"successfully reloaded `{ext}`"
                logger.info(t)
                ext_status += "✅ " + t.capitalize() + "\n"
        
        await msg.edit(content=ext_status)
    
    @commands.command(aliases=["exts", "loaded", "loaded_extensions"])
    async def extensions(self, ctx: Context):
        """List all loaded cogs"""
        
        paginated_list = utils.paginate([f"`{k}`" for k in self.bot.extensions.keys()])
        extensions = [", ".join(group) for group in paginated_list]
        extensions = ",\n".join(extensions)
        
        await ctx.send("All loaded extensions:\n"+
                       extensions)

    @load.error
    @unload.error
    @reload.error
    async def on_extension_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.CheckFailure) or isinstance(error, commands.MissingRequiredArgument):
            return
        
        elif isinstance(error, commands.CommandInvokeError):
            error = error.original
            
            if len(ctx.args) > 2:
                ext = "cogs."+ctx.args[2]
                logger.error(f"failed to {ctx.command.name} `{ext}`: `{error.__class__.__name__}`", exc_info=error)
                await ctx.send(f"❌ Error occured while {ctx.command.name}ing the extension: `{ext}`\n"+
                    utils.code(f"{error.__class__.__name__}: {str(error)}"))

async def setup(bot: Bot) -> None:
    await bot.add_cog(Admin(bot))