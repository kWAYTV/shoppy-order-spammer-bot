import logging, sys
from discord.ext import commands
from src.util.logger import Logger
from pystyle import Colors, Colorate, Center

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

logo = """
███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗    ███████╗██████╗  █████╗ ███╗   ███╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║
███████╗███████║██║   ██║██████╔╝██████╔╝ ╚████╔╝     ███████╗██████╔╝███████║██╔████╔██║
╚════██║██╔══██║██║   ██║██╔═══╝ ██╔═══╝   ╚██╔╝      ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
███████║██║  ██║╚██████╔╝██║     ██║        ██║       ███████║██║     ██║  ██║██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝        ╚═╝       ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝"""


class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(self.bot)

    def print_logo(self):
        self.logger.clear()
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "-----------------------------------------------------------\n\n", 1)))

    @commands.Cog.listener()
    async def on_ready(self):
        self.print_logo()
        self.logger.log("INFO", f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}.")

        logging.basicConfig(handlers=[logging.FileHandler('shoppy_spammer_bot.log', 'a+', 'utf-8')], level=logging.ERROR, format='%(asctime)s: %(message)s')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return Logger().log("INFO", "On ready event registered!")