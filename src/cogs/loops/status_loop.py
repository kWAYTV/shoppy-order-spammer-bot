import discord, sys
from itertools import cycle
from src.util.logger import Logger
from discord.ext import commands, tasks

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class StatusLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = Logger()
        self.change_status.start()

    # Dynamic activity
    status = cycle(["shoppy backend crumble", "shoppy backend panic", "shoppy developers sweat", "shoppy backend cry for help", "shoppy backend spin in circles", "shoppy exploits"])
    @tasks.loop(seconds=30)
    async def change_status(self):
        await self.bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=next(self.status)))

    @change_status.before_loop
    async def before_change_status(self) -> None:
        return await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusLoop(bot))
    return Logger().log("INFO", "Status loop loaded!")