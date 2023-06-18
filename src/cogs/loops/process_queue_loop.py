import discord, sys
from itertools import cycle
from src.util.logger import Logger
from src.helper.config import Config
from discord.ext import commands, tasks
from src.handler.queue_handler import QueueHandler

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class ProcessQueueLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = Logger()
        self.config = Config()
        self.queue_handler = QueueHandler()
        self.proccess_queue.start()

    # Proccess the queue
    @tasks.loop(seconds=45)
    async def proccess_queue(self):
        await self.queue_handler.force_check_start()

    @proccess_queue.before_loop
    async def before_proccess_queue(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ProcessQueueLoop(bot))
    return Logger().log("INFO", "Process queue loop loaded!")