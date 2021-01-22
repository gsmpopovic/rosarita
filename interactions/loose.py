import asyncio
import random

from discord import Message, Guild, Role, Forbidden

import defs
import data


async def lovelace_creed(message: Message):
    if data.creed == 1:
        await message.channel.send("*stares*")
        await asyncio.sleep(3)
    elif data.creed == 2:
        await message.channel.send("**glares**")
        await asyncio.sleep(5)
    elif data.creed >= 3:
        await message.channel.send("*silent stare*")
        return
    await message.channel.send("""\
Una bendición por los vivos, una rama de flor por los muertos.
Con una espada por la justicia, un castigo de muerte para los malvados.
Así llegaremos en el altar de los santos.""")
    data.creed += 1


# This must be a def because lambdas can't be async
async def is_public(message: Message):
    await message.channel.send(f"No. Ask {data.owner.mention}")


async def simp(message: Message):
    await message.channel.send("All simps must die.")
    await message.channel.send(random.choice(defs.simp_images))

    guild: Guild = message.guild
    if guild is not None and guild.id in defs.mute_roles:
        role: Role = guild.get_role(defs.mute_roles[guild.id])
        if role is not None:
            try:
                await data.temp_mute(message.author, role, defs.simp_mute_time)
            except Forbidden:
                pass


mentioned_interactions = {
    "are you a public bot?": is_public,
}

interactions = {
    "what is the lovelace family creed": lovelace_creed,
    "what is your family creed": lovelace_creed,
}

word_interactions = {
    "simp": simp
}
