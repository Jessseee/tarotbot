import discord


class Confirm(discord.ui.View):
    def __init__(self, confirm_message="Yes please!", cancel_message="No thanks"):
        super().__init__()
        self.confirmed = None
        self.confirm_label = confirm_message
        self.cancel_message = cancel_message

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = self.confirm_label
        await interaction.response.edit_message(view=None)
        self.confirmed = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.label = self.cancel_message
        await interaction.response.edit_message(view=None)
        self.confirmed = False
        self.stop()
