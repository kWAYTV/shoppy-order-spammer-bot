import yaml
from yaml import SafeLoader

class Config():
    def __init__(self):
        with open("config.yaml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
            self.shoppy_logo = "https://i.imgur.com/Nfocsma.png"
            self.discord_token = self.config["discord_token"]
            self.bot_prefix = self.config["bot_prefix"]
            self.logs_channel = int(self.config["logs_channel"])
            self.loading_green_emoji_id = self.config["loading_green_emoji_id"]
            self.loading_red_emoji_id = self.config["loading_red_emoji_id"]
            self.green_tick_emoji_id = self.config["green_tick_emoji_id"]