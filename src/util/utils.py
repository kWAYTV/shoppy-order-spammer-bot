import sys

# Try to not create .pyc trash files.
sys.dont_write_bytecode = True

class Utils:

    def __init__(self):
        return

    async def clean_discord_username(self, username: str) -> str:
        username_split = username.split("#")
        if username_split[1] == "0":
            return f"@{username_split[0]}"
        else:
            return username