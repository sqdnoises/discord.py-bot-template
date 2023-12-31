import logging
import discord
from classes import Bot
from discord.ext import commands

class Events(commands.Cog):
    """All bot events"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("ready to handle commands")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        print(f"{member}: {before.channel} -> {after.channel}")
        if (before.channel is not None and after.channel is None) \
           or (before.channel is not None and after.channel is not None and before.channel != after.channel): # left the voice or changed voice
            print (1)
            if member.guild.voice_client and member.guild.voice_client.channel == before.channel:
                print (2)
                binding = self.bot.get_binding(member=member, voice_client=member.guild.voice_client)
                if binding:
                    print (3)
                    await self.bot.unbind_from(member.guild.voice_client)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))