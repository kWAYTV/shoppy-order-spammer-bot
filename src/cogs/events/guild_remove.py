import sys
from discord.ext import commands
from src.util.logger import Logger

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class GuildRemove(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(self.bot)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.logger.log("INFO", f"The guild {guild.name} has been removed from the bot.")
        await self.logger.discord_log(f"The guild {guild.name} has been removed from the bot.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GuildRemove(bot))
    return Logger().log("INFO", "On guild leave event registered!")