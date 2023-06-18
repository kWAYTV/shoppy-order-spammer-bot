import os, sys
from src.util.logger import Logger
from src.helper.config import Config

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

defaultConfig = """
# Shoppy order spammer

# Discord bot prefix
bot_prefix: 
# Discord bot token
discord_token: 
# Discord green tick emoji id
green_tick_emoji_id: 
# Discord green loading emoji id
loading_green_emoji_id: 
# Discord red loading emoji id
loading_red_emoji_id: 
# Discord logs channel id
logs_channel: 
# Discord queue embed switch (true/false)
queue_embed_switch: 
# Discord queue embed channel id
queue_embed_channel_id: 
# Discord queue embed message id
queue_embed_message_id: 
# Discord user timeout after order (in seconds)
user_timeout: 

"""

class FileManager():

    def __init__(self):
        self.logger = Logger()
        self.config = Config()

    # Function to check if the input files are valid
    def check_input(self):

        # if there is no config file, create one.
        if not os.path.isfile("config.yaml"):
            self.logger.log("INFO", "Config file not found, creating one...")
            open("config.yaml", "w+").write(defaultConfig)
            self.logger.log("INFO", "Successfully created config.yml, please fill it out and try again.")
            exit()

        # if there's no proxies file, create one.
        if not os.path.isfile("proxies.txt"):
            self.logger.log("INFO", "Proxies file not found, creating one...")
            open("proxies.txt", "w+").write("")
            self.logger.log("INFO", "Successfully created proxies.txt, please fill it out with proxies in user:pass@ip:port format and try again.")
            exit()

        # If the proxies file is empty, exit.
        if os.stat("proxies.txt").st_size == 0:
            self.logger.log("INFO", "Proxies file is empty, please fill it out with proxies in user:pass@ip:port format and try again.")
            exit()

        # If the folder "/src/database" doesn't exist, create it.
        if not os.path.exists("src/database"):
            os.makedirs("src/database")