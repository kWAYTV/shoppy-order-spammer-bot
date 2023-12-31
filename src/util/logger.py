import discord, sys
from os import system, name
from datetime import datetime
from discord.ext import commands
from colorama import Fore, Style
from src.helper.config import Config

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class Logger:

    def __init__(self, bot: commands.Bot = None):
        self.config = Config()
        # Set the colors for the logs
        self.log_types = {
            "INFO": Fore.CYAN,
            "SUCCESS": Fore.GREEN,
            "OK": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "SLEEP": Fore.YELLOW,
            "ERROR": Fore.RED,
            "BAD": Fore.RED,
            "INPUT": Fore.BLUE,
            "RATELIMIT": Fore.YELLOW,
        }
        self.bot = bot

    # Clear console function
    def clear(self):
        system("cls" if name in ("nt", "dos") else "clear")

    # Function to send logs to the discord channel
    async def discord_log(self, description: str):
        channel = self.bot.get_channel(self.config.logs_channel)
        embed = discord.Embed(title="Shoppy Order Spammer", description=description)
        embed.set_thumbnail(url=self.config.shoppy_logo)
        embed.set_footer(text=f"Shoppy Order Spammer - discord.gg/kws")
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)

    # Function to log messages to the console
    def log(self, type, message):
        color = self.log_types[type]
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y • %H:%M:%S")
        print(f"{Style.DIM}{current_time} • {Style.RESET_ALL}{Style.BRIGHT}{color}[{Style.RESET_ALL}{type}{Style.BRIGHT}{color}] {Style.RESET_ALL}{Style.BRIGHT}{Fore.WHITE}{message}")