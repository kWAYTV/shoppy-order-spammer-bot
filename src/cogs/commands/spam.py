import discord, asyncio, sys
from datetime import datetime
from typing import Literal
from discord.ext import commands
from discord import app_commands
from src.util.utils import Utils
from src.util.logger import Logger
from src.helper.config import Config
from concurrent.futures import ThreadPoolExecutor
from src.handler.queue_handler import QueueHandler
from src.manager.timeout_manager import TimeoutManager

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class Spam(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()
        self.utils = Utils()
        self.logger = Logger(self.bot)
        self.timeout_manager = TimeoutManager()
        self.queue_handler = QueueHandler()

    # Spam bot command  
    @app_commands.command(name="spam", description=f"Start spamming some shoppy store with a given product ID. ({Config().user_timeout} seconds timeout)")
    async def spam_command(self, interaction: discord.Interaction, amount: int, product_id: str, payment_method: Literal["Paypal", "Bitcoin", "Litecoin", "Ethereum"]):
        await interaction.response.defer(ephemeral=True)

        if payment_method == "Paypal": payment_method = "PayPal"
        if payment_method == "Bitcoin": payment_method = "BTC"
        if payment_method == "Litecoin": payment_method = "LTC"
        if payment_method == "Ethereum": payment_method = "ETH"

        # Clean the username
        username = await self.utils.clean_discord_username(f"{interaction.user.name}#{interaction.user.discriminator}")

        # Check if the user is in timeout
        is_in_timeout, time_remaining = self.timeout_manager.is_user_in_timeout(interaction.user.id)
        if is_in_timeout:
            minutes, seconds = divmod(time_remaining, 60)
            await self.logger.discord_log(f"⏳ {username} tried to use the spam command but is in timeout for {int(minutes)} minutes and {int(seconds)} seconds.")
            self.logger.log("INFO", f"⏳ {username} tried to use the spam command but is in timeout for {int(minutes)} minutes and {int(seconds)} seconds.")
            return await interaction.followup.send(f"{self.config.loading_red_emoji_id} You can only use this command every {self.config.user_timeout} seconds! Please wait {int(minutes)} minutes and {int(seconds)} seconds.", ephemeral=True)

        # Check if the amount is more than 50
        if amount > 50:
            await self.logger.discord_log(f"❌ {username} tried to spam more than 50 times at once.")
            self.logger.log("INFO", f"❌ {username} tried to spam more than 50 times at once.")
            return await interaction.followup.send(f"❌ You can't spam more than 50 times at once!", ephemeral=True)
        
        # Tell the user that the bot is working on their order and log it to console and logs channel
        requested_message = await interaction.followup.send(f"{self.config.loading_green_emoji_id} Requested `{amount}` orders to be spammed at product ID: `{product_id}`.", ephemeral=True)
        await self.logger.discord_log(f"⌛ Requested `{amount}` orders to be spammed at product ID: `{product_id}`. Requested by `{username}`.")
        self.logger.log("INFO", f"⌛ Requested {amount} orders to be spammed at product ID: {product_id}. Requested by {username}")

        # Create an embed to send to the user
        embed = discord.Embed(title=f"{self.config.loading_green_emoji_id} Successfully added!", description=f"Order added to the queue.\nQueued `{amount}` orders at product ID: `{product_id}`.", color=0x00ff00)
        embed.set_thumbnail(url=self.config.shoppy_logo)
        embed.set_footer(text=f"Shoppy Order Spammer • Requested by {username}")
        embed.timestamp = datetime.utcnow()

        # Edit the message to send the embed and log it to console and logs channel
        await requested_message.edit(content=f"{self.config.loading_green_emoji_id} The order has been added to the queue.", embed=embed)
        await self.logger.discord_log(f"✅ Successfully added `{amount}` orders at product ID: `{product_id}` to the queue. Requested by `{username}`.")
        self.logger.log("INFO", f"✅ Successfully added {amount} orders at product ID: {product_id} to the queue. Requested by {username}")

        self.queue_handler.push_order({'amount': int(amount), 'product_id': str(product_id), 'payment_method': payment_method,'requested_by': int(interaction.user.id)})
        await self.queue_handler.force_check_start()

        # Create an embed to send to the user
        embed = discord.Embed(title=f"{self.config.green_tick_emoji_id} Successfully sent!", description=f"Order successfully sent.\nSent `{amount}` orders at product ID: `{product_id}`.", color=0x00ff00)
        embed.set_thumbnail(url=self.config.shoppy_logo)
        embed.set_footer(text=f"Shoppy Order Spammer • Requested by {username}")
        embed.timestamp = datetime.utcnow()

        # Edit the message to send the embed and log it to console and logs channel
        await requested_message.edit(content=f"{self.config.green_tick_emoji_id} The order has been sent.", embed=embed)
        await self.logger.discord_log(f"✅ Successfully sent `{amount}` orders at product ID: `{product_id}`. Requested by `{username}`.")
        self.logger.log("INFO", f"✅ Successfully sent {amount} orders at product ID: {product_id}. Requested by {username}")

        # Check if the user has any of the roles from the admin roles list or has admin permission
        if interaction.user.guild_permissions.administrator:
            await self.logger.discord_log(f"⚠️  {username} has bypassed the timeout because they have admin permissions.")
            self.logger.log("INFO", f"⚠️  {username} has bypassed the timeout because they have admin permissions.")
        else:
            # Add user to timeout list after they have successfully used the command
            adding = self.timeout_manager.add_user(interaction.user.id)

            # Check if the user is already in the timeout list
            if not adding:
                await self.logger.discord_log(f"❌ The user {username} `already` in the timeout list.")
                self.logger.log("INFO", f"❌ The user {username} already in the timeout list.")
                return await interaction.followup.send(f"{self.config.loading_red_emoji_id} The user {username} `already` in the timeout list.", ephemeral=True)

            
            # Log that the user has been added to the timeout list
            await self.logger.discord_log(f"⏳ {username} has been added to the timeout list for {self.config.user_timeout} seconds.")
            self.logger.log("INFO", f"⏳ {username} has been added to the timeout list for {self.config.user_timeout} seconds.")

    @spam_command.error
    async def spam_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            return await interaction.response.send_message("❌ You don't have permissions to use this command.", ephemeral=True)
        else:
            return await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Spam(bot))
    return Logger().log("INFO", "Spam command loaded!")