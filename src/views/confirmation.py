import discord

__all__ = (
    "ConfirmationView",
)

class ConfirmationView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, timeout: int = 30) -> None:
        super().__init__(timeout=timeout)
        self.interaction = interaction
        self.user = interaction.user
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.value = False
        self.stop()
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message(embed=discord.Embed(
                description = "Sorry, but this command wasn't requested by you.",
                color = discord.Color.dark_gold()
            ), ephemeral=True)
            return False
        
        return True
    
    async def on_timeout(self) -> None:
        if self.value is not None:
            return
        
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        
        await self.interaction.edit_original_response(embed=discord.Embed(
            description = "You took too long to respond.",
            color = discord.Color.brand_red()
        ), view=self)