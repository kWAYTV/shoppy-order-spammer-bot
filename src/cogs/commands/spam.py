import discord, asyncio
from discord.ext import commands
from discord import app_commands
from src.util.logger import Logger
from src.util.utils import Utils
from src.helper.config import Config
from src.shoppy.spammer import Spammer
from concurrent.futures import ThreadPoolExecutor
from src.helper.timeout_manager import TimeoutManager

class Spam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.utils = Utils()
        self.logger = Logger(self.bot)
        self.spammer = Spammer()
        self.timeout_manager = TimeoutManager()

    # Spam bot command  
    @app_commands.command(name="spam", description="Start spamming some shoppy store.")
    @app_commands.checks.has_permissions(administrator=True)
    async def spam_command(self, interaction: discord.Interaction, amount: int, product_id: str):
        await interaction.response.defer(ephemeral=True)

        # Clean the username
        username = await self.utils.clean_discord_username(f"{interaction.user.name}#{interaction.user.discriminator}")

        # Check if the user is in timeout
        is_in_timeout, time_remaining = self.timeout_manager.is_user_in_timeout(interaction.user.id)
        if is_in_timeout:
            minutes, seconds = divmod(time_remaining, 60)
            await self.logger.discord_log(f"⏳ @{username} tried to use the spam command but is in timeout for {int(minutes)} minutes and {int(seconds)} seconds.")
            self.logger.log("INFO", f"⏳ @{username} tried to use the spam command but is in timeout for {int(minutes)} minutes and {int(seconds)} seconds.")
            return await interaction.followup.send(f"{self.config.loading_red_emoji_id} You can only use this command every {self.config.user_timeout} seconds! Please wait {int(minutes)} minutes and {int(seconds)} seconds.", ephemeral=True)

        # Check if the amount is more than 50
        if amount > 50:
            await self.logger.discord_log(f"❌ @{username} tried to spam more than 50 times at once.")
            self.logger.log("INFO", f"❌ @{username} tried to spam more than 50 times at once.")
            return await interaction.followup.send(f"❌ You can't spam more than 50 times at once!", ephemeral=True)
        
        # Tell the user that the bot is working on their order and log it to console and logs channel
        requested_message = await interaction.followup.send(f"{self.config.loading_green_emoji_id} Requested `{amount}` orders to be spammed at product ID: `{product_id}`.", ephemeral=True)
        await self.logger.discord_log(f"⌛ Requested `{amount}` orders to be spammed at product ID: `{product_id}`. Requested by `@{username}`.")
        self.logger.log("INFO", f"⌛ Requested {amount} orders to be spammed at product ID: {product_id}. Requested by @{username}")

        # Use asyncio's run_in_executor to run blocking functions in a thread
        with ThreadPoolExecutor() as executor:
            await asyncio.get_event_loop().run_in_executor(executor, self.spammer.start, amount, product_id)

        # Create an embed to send to the user
        embed = discord.Embed(title="Spamming finished!", description=f"Successfully sent `{amount}` orders at product ID: `{product_id}`.", color=0x00ff00).set_thumbnail(url=self.config.shoppy_logo).set_footer(text=f"Shoppy Order Spammer • Requested by @{username}")

        # Edit the message to send the embed and log it to console and logs channel
        await requested_message.edit(content=f"{self.config.green_tick_emoji_id} Your order has been completed! `{amount}` orders have been sent to product ID: `{product_id}`.", embed=embed)
        await self.logger.discord_log(f"✅ Successfully sent `{amount}` orders at product ID: `{product_id}`. Requested by `@{username}`.")
        self.logger.log("INFO", f"✅ Successfully sent {amount} orders at product ID: {product_id}. Requested by @{username}")

        # Add user to timeout list after they have successfully used the command
        self.timeout_manager.add_user(interaction.user.id)
        await self.logger.discord_log(f"⏳ @{username} has been added to the timeout list for {self.config.user_timeout} seconds.")
        self.logger.log("INFO", f"⏳ @{username} has been added to the timeout list for {self.config.user_timeout} seconds.")

    @spam_command.error
    async def spam_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            return await interaction.response.send_message("❌ You don't have permissions to use this command.", ephemeral=True)
        else:
            return await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Spam(bot))
    return Logger().log("INFO", "Spam command loaded!")