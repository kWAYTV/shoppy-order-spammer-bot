import discord, sys
from datetime import datetime
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.helper.config import Config

# Try not to create .pyc trash files.
sys.dont_write_bytecode = True

class QueueEmbed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    # QueueEmbed bot command
    @app_commands.command(name="queue_embed", description="Creates and sets the queue embed.")
    async def queue_embed_command(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not self.config.queue_embed_switch:
            return await interaction.followup.send("❌ Queue embed is disabled in the config! Enable it and restart the bot.", ephemeral=True)
        
        embed = discord.Embed(title="📝 Shoppy Queue.", color=0xb34760)
        embed.set_footer(text="Shoppy Order Spammer")
        embed.set_thumbnail(url=self.config.shoppy_logo)
        embed.timestamp = datetime.utcnow()

        queue_embed_message = await interaction.followup.send(embed=embed)

        self.config.set_queue_embed_channel_id(queue_embed_message.channel.id)
        self.config.set_queue_embed_message_id(queue_embed_message.id)

        await interaction.followup.send("✅ Queue embed created and values set in the config!", ephemeral=True)

    @queue_embed_command.error
    async def queue_embed_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("❌ You don't have permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QueueEmbed(bot))
    return Logger().log("INFO", "Queue embed command loaded!")
