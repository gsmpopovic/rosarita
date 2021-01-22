import discord
from discord import Message

import data


def parse_member(user: discord.abc.User) -> str:
    return "master" if user == data.owner else "member"


async def hi(message: Message):
    await message.channel.send(f"Hello, {parse_member(message.author)}")


async def owo(message: Message):
    await message.channel.send(f"*Notices you dying inside.*\nHello {parse_member(message.author)}.\n**bows**")


interactions = {
    "hey": hi, "hi": hi, "hello": hi,
    "owo": owo, "uwu": owo, "0w0": owo
}
