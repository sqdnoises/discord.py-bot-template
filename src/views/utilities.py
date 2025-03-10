import discord

__all__ = ("InstallView",)


class InstallView(discord.ui.View):
    def __init__(
        self, application_id: int, user_install: bool = True, guild_install: bool = True
    ) -> None:
        super().__init__()
        self.application_id = application_id

        if user_install:
            self.add_item(
                discord.ui.Button(
                    label="Add to your apps",
                    style=discord.ButtonStyle.link,
                    url=f"https://discord.com/oauth2/authorize?client_id={application_id}&integration_type=1&scope=applications.commands",
                )
            )

        if guild_install:
            self.add_item(
                discord.ui.Button(
                    label="Invite to server",
                    style=discord.ButtonStyle.link,
                    url=f"https://discord.com/oauth2/authorize?client_id={application_id}&permissions=8&integration_type=0&scope=applications.commands+bot",
                )
            )
