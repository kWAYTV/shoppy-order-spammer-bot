import discord, sys
from datetime import datetime
from src.util.logger import Logger
from src.helper.config import Config
from discord.ext import commands, tasks
from src.handler.queue_handler import QueueHandler

# Try not to create .pyc trash files.
sys.dont_write_bytecode = True

class UpdateQueueLoop(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = Logger()
        self.config = Config()
        self.queue_handler = QueueHandler()
        self.update_queue_embed.start()

    # Update queue embed message
    @tasks.loop(seconds=10)
    async def update_queue_embed(self):

        # Fetch the message and channel
        queue_channel = self.bot.get_channel(Config().queue_embed_channel_id)
        queue_message = await queue_channel.fetch_message(Config().queue_embed_message_id)

        # Get the queue data and length
        data = self.queue_handler.get_queue_data()
        length = self.queue_handler.get_queue_length()

        # Create the embed
        description = "`User`/`Amount`/`Product ID`\n"
        for index, order in enumerate(data):
            amount = order['amount']
            product_id = order['product_id']
            requested_by = order['requested_by']
            emoji = self.config.loading_green_emoji_id if index == 0 else self.config.loading_red_emoji_id
            description = description + f" > • {emoji} <@{requested_by}> • `{amount}`/`{product_id}`\n"
        embed = discord.Embed(title="📝 Shoppy Queue.", description=description, color=0xb34760)
        embed.set_footer(text=f"Shoppy Order Spammer • Total: {length}")
        embed.set_thumbnail(url=self.config.shoppy_logo)
        embed.timestamp = datetime.utcnow()

        # Edit the message
        await queue_message.edit(embed=embed)

    @update_queue_embed.before_loop
    async def before_update_queue_embed(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UpdateQueueLoop(bot))
    return Logger().log("INFO", "Update queue loop loaded!")
