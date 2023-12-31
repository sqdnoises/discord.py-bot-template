import os
import sys
import pkg_resources
from dotenv import load_dotenv

import config
from utils import mprint

import logging
import discord
from classes import Bot

discord.utils.setup_logging()
logging.info("logging initiated")

load_dotenv()
logging.info("loaded environmental variables")

try:
    terminal = os.get_terminal_size()
except:
    logging.warning("could not detect terminal size")
else:
    logging.info(f"detected current terminal size: {terminal.columns}x{terminal.lines}")

bot = Bot(command_prefix=config.PREFIX)

async def setup_hook():
    mprint()
    mprint("~ TEMPLATE BOT ~")
    mprint(f"running on python {sys.version.split()[0]}; discord.py {pkg_resources.get_distribution('discord.py').version}")
    mprint()
    
#    loaded = []
#    exclude = config.COGS_EXCLUDE
#    for ext in os.listdir("cogs"):
#        if ext in exclude: continue
#        if ext.endswith(".py"):
#            extension = "cogs."+ext[:-3]
#            loaded.append(extension)
#            await bot.load_extension(extension)
    
    #logging.info("the following cogs have #been loaded:\n"+
#      (" "*34)+ f"{', '.join(loaded)}")
    
    logging.info("logged in successfully")
    logging.info(f"user: {bot.user} ({bot.user.id})")

bot.setup_hook = setup_hook

logging.info("starting heardle bot")

@bot.command()
async def hello(ctx):
    await ctx.send("hello")

bot.run(os.getenv("TOKEN"), log_handler=None)