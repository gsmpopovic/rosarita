from discord import Intents
from defs import bot_token
from rosarita_client import RosaritaClient

intents = Intents.default()
intents.typing = False
intents.members = True
intents.presences = True

client = RosaritaClient(intents=intents)
# client.run(bot_token)

#client.loop.create_task(audio_player_task())

client.run("Nzg5Mjk4NDczNzM1ODE1MTg3.X9wBfA.alTDd3oKYtUAy8Ig88S6Gq1VT1w")
