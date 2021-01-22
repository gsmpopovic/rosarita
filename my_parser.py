import asyncio
import random
from typing import List

from discord import Message

import data
import defs
from defs import reaction_yes, reaction_no, tea_images, tea_syke_images
from interactions import bot_help, str_ops
from utils import message_ops


async def all_parse(message: Message, content_lower: str,
                    is_owner: bool, is_guild_owner: bool, is_dm: bool, mentioned: bool):
    if mentioned or "roberta" in content_lower:
        if is_guild_owner and not is_dm and ("HELP" in message.content or "HALP" in message.content):
            await message.channel.send(defs.incoming_help)
            await message.channel.send(defs.incoming_img)
            await asyncio.sleep(3)
            split_help: List[str] = bot_help.do_help(is_owner, is_guild_owner, is_dm)
            for help_piece in split_help:
                if help_piece:
                    await message.channel.send(help_piece)
                    await asyncio.sleep(0.3)
            return True
        elif "help" in content_lower or "halp" in content_lower:
            sent_message: Message = await message.channel.send(message_ops.parse(defs.help_question, message.author))
            await sent_message.add_reaction(reaction_yes)
            await sent_message.add_reaction(reaction_no)
            async with data.help_lock:
                data.help_reactions[sent_message.id] = message.author.id
            return True


async def parse(message: Message, content_lower: str) -> bool:
    if "thank" in content_lower:
        async with data.tea_lock:
            if message.author.id in data.tea_waiting_thanks:
                await message.channel.send(random.choice(tea_images))
                await message.channel.send(f"You're welcome, {message.author.mention}")
                data.tea_waiting_thanks.remove(message.author.id)
    elif str_ops.match("tea", content_lower) and (
            str_ops.match("please", content_lower) or
            str_ops.match("pls", content_lower) or
            str_ops.match("kindly", content_lower)):
        if message.author == data.owner:
            await message.channel.send("Yes master")
            await message.channel.send(random.choice(tea_images))
        elif data.client.user in message.mentions:
            await message.channel.send("As you wish\n"
                                       "*pours earl grey tea*")
            async with data.tea_lock:
                if message.author.id in data.tea_waiting_thanks:
                    return True
                data.tea_waiting_thanks.add(message.author.id)
            await asyncio.sleep(10)
            async with data.tea_lock:
                if message.author.id in data.tea_waiting_thanks:
                    await message.channel.send("*takes back tea*\n"
                                               "Since you are ungrateful, I will take it back.")
                    await message.channel.send(random.choice(tea_syke_images))
                    data.tea_waiting_thanks.remove(message.author.id)
        else:
            await message.channel.send("***stares***\n"
                                       "Who are you asking for tea? I have a name, you know? Please use it next time.")
        return True
    else:
        return False
