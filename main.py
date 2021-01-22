from discord import Intents

from defs import bot_token
from rosarita_client import RosaritaClient

intents = Intents.default()
intents.typing = False
intents.members = True
intents.presences = True

client = RosaritaClient(intents=intents)
client.run(bot_token)
