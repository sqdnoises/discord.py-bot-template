from typing import Optional
import discord
from discord.ext import commands

class Context(commands.Context):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.voice: Optional[discord.VoiceState] = self.author.voice
    
    async def react(self, emoji: discord.Emoji) -> discord.Reaction:
        """Add reaction to a message"""
        return await self.message.add_reaction(emoji)

class Bot(commands.Bot):
    def __init__(self, command_prefix: str, *args, intents: discord.Intents = discord.Intents.all(), **kwargs) -> None:
        super().__init__(command_prefix=command_prefix, intents=intents, *args, **kwargs)
        self.vc_bindings = {} # {discord.Member: discord.VoiceClient}
    
    async def get_context(self, message: discord.Message, *, cls: commands.Context = Context) -> Context:
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)
    
    def get_binding(self, *, member: discord.Member = None, voice_client: discord.VoiceClient = None) -> list:
        """Get voice client for a user or vice versa"""
        
        if member is not None and voice_client is None:
            for m, vc in self.vc_bindings.items():
                if m == member:
                    return [m, vc]
        
        elif member is None and voice_client is not None:
            for m, vc in self.vc_bindings.items():
                if vc == voice_client:
                    return [m, vc]
        
        elif member is not None and voice_client is not None:
            for m, vc in self.vc_bindings.items():
                if m == member and vc == voice_client:
                    return [m, vc]
        
        return [] # if not found or both arguments not specified
    
    async def bind_to(self, member: discord.Member, connect: bool = True) -> bool:
        """Bind a guild voice client to a member in `bot.vc_bindings` variable"""
        
        if not member.guild.voice_client: # if bot is not connected to voice
            if member.voice: # and member is connected to voice
                if connect: # connect to the voice
                    await member.voice.channel.connect()
                    await member.guild.change_voice_state(self_mute=False, self_deafen=True)
                
                self.vc_bindings.update({member: member.guild.voice_client}) # update bindings
                return True # indicate bot has connected to a voice
            
            else: # and member is not connected to voice
                if member in self.vc_bindings: # if member is in vc bindings
                    self.vc_bindings.pop(member) # remove them
                
                return False # indicate bot did not connect to a voice
        
        else: # if bot is connected to voice
            if member.voice: # and the member is connected to voice
                if member.voice.channel == member.guild.voice_client.channel: # and member voice is same as bot voice
                    return True # indicate bot is connected to members voice
                
                else: # and member is not in same voice as the bot
                    binding = self.get_binding(voice_client=member.guild.voice_client) # find the binding of the voice the bot is in
                    if binding: # if the binding exists
                        if binding[0] == member: # if the binding member is the member
                            await member.guild.voice_client.move_to(member.voice.channel) # switch to members voice
                            return True # indicate bot is in members voice
                        
                        else:
                            return False # indicate bot is not connected to members voice
                    
                    else: # if the binding doesn't exist
                        return False # indicate bot is not connected to members voice
            
            else: # if the member is not connected to voice
                return False # indicate bot did not connect to members voice
    
    async def unbind_from(self, voice_client: discord.VoiceClient, disconnect: bool = True) -> bool:
        """Unbind a member from a guild voice client in `bot.vc_bindings` variable"""
        
        binding = self.get_binding(voice_client=voice_client)
        if binding: # if the binding exists
            m, vc = binding
            
            if disconnect and vc.is_connected(): # if voice is connected, disconnect
                await vc.disconnect()
            self.vc_bindings.pop(m)
            
            return True # indicate that the bot unbinded from the voice
                    
        else: # if the binding doesn't exist
            return False # indicate that the bot could not unbind from the voice