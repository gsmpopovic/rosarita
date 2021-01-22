from discord import Message, Guild, Member, Status

import data
import defs


async def server_stats(message: Message):
    guild: Guild = message.guild
    if guild is None:
        return
    if guild.member_count >= 1000:
        # This can be changed, but it might be too heavy to be worth it
        print("Too many members to count!")
    else:
        members: int = 0
        online: int = 0
        bots: int = 0
        member: Member
        for member in guild.members:
            if member.bot:
                bots += 1
            if member.status != Status.offline:
                online += 1
            members += 1
        await message.channel.send(f"```\n"
                                   f"Members: {members}\n"
                                   f"Online : {online}\n"
                                   f"Bots   : {bots}\n"
                                   f"```")


async def warnings(message: Message):
    member_warnings = await data.list_member_warnings(message.author)
    if member_warnings is None:
        await message.channel.send(defs.no_warning_message)
    else:
        await message.channel.send(
            "Your warnings are:\n--------------------\n" +
            "\n--------------------\n".join(member_warnings) +
            "\n--------------------")


exact = {
    "stats": server_stats,
    "status": server_stats,
    "warnings": warnings
}
