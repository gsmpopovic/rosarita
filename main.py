from discord import Intents
#from defs import bot_token
from rosarita_client import RosaritaClient
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

token = os.getenv("BOT_TOKEN_ONE")
intents = Intents.default()
intents.typing = False
intents.members = True
intents.presences = True

client = RosaritaClient(intents=intents)


client.run(token)
