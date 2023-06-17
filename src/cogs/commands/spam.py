import discord, asyncio
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.util.utils import Utils
from src.helper.config import Config
from src.shoppy.spammer import Spammer
from concurrent.futures import ThreadPoolExecutor

class Spam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.utils = Utils()
        self.logger = Logger(self.bot)
        self.spammer = Spammer()

    # Spam bot command  
    @app_commands.command(name="spam", description="Start spamming some shoppy store.")
    @app_commands.checks.has_permissions(administrator=True)
    async def spam_command(self, interaction: discord.Interaction, amount: int, product_id: str):
        await interaction.response.defer(ephemeral=True)

        dirty_user = f"{interaction.user.name}#{interaction.user.discriminator}"
        username = await self.utils.clean_discord_username(dirty_user)

        if amount > 50:
            return await interaction.followup.send("❌ You can't spam more than 50 times at once!", ephemeral=True)
        
        requested_message = await interaction.followup.send(f"⌛ Requested `{amount}` orders to be spammed at product ID: `{product_id}`.", ephemeral=True)
        await self.logger.discord_log(f"⌛ Requested `{amount}` orders to be spammed at product ID: `{product_id}`. Requested by `{username}`.")
        self.logger.log("INFO", f"⌛ Requested {amount} orders to be spammed at product ID: {product_id}. Requested by {username}")

        # Use asyncio's run_in_executor to run blocking functions in a thread
        with ThreadPoolExecutor() as executor:
            await asyncio.get_event_loop().run_in_executor(executor, self.spammer.start, amount, product_id)

        await requested_message.edit(content=f"✅ Successfully sent `{amount}` orders at product ID: `{product_id}`.")
        await self.logger.discord_log(f"✅ Successfully sent `{amount}` orders at product ID: `{product_id}`. Requested by `{username}`.")
        self.logger.log("INFO", f"✅ Successfully sent {amount} orders at product ID: {product_id}. Requested by {username}")

    @spam_command.error
    async def spam_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            return await interaction.response.send_message("❌ You don't have permissions to use this command.", ephemeral=True)
        else:
            return await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Spam(bot))
    return Logger().log("INFO", "Spam command loaded!")