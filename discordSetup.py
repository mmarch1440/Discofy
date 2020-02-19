from discord.ext.commands import Bot
from securityCredentials import DCTOKEN
# Discord config
URL = "http://maps.googleapis.com/maps/api/geocode/json"
BOT_PREFIX = "!"
client = Bot(command_prefix=BOT_PREFIX)

def run():
    client.run(DCTOKEN)