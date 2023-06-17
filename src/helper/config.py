import yaml
from yaml import SafeLoader

class Config():
    def __init__(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.hypixel_logo = "https://i.imgur.com/Nfocsma.png"
            self.discord_token = self.config["discord_token"]
            self.bot_prefix = self.config["bot_prefix"]
            self.logs_channel = int(self.config["logs_channel"])