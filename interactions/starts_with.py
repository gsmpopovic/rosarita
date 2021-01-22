from discord import Message


def i_am(size: int):
    async def inner_i_am(message: Message):
        await message.channel.send(f"Hello {message.content[size:]}")

    return inner_i_am


interactions = {
    "i am ": i_am(5),
    "i'm ": i_am(4),
    "im": i_am(3)
}
