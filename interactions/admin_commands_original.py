import asyncio
from typing import List, Dict

import discord
from discord import Message, Forbidden, Guild, Member, Role, User, NotFound, HTTPException, InvalidArgument

import data
import defs
from interactions import time_ops, reaction_messages, str_ops
from utils import message_ops


async def clear(message: Message, split_content: List[str]):
    limit = 2
    if len(split_content) >= 3:
        if split_content[2].lower() == "all":
            limit = defs.max_delete
        else:
            try:
                limit = int(split_content[2]) + 1
            except ValueError:
                pass

    channel: discord.TextChannel = message.channel
    async for msg in channel.history(limit=limit):
        try:
            await msg.delete()
        except Forbidden:
            pass


async def unban(message: Message, _split_content: List[str]):
    if len(_split_content) <= 2:
        await message.channel.send(f"Wrong command. Correct use is **{data.self_user.mention} unban ID**, "
                                   f"where ID is the user's ID.")
    else:
        try:
            user_id: int = int(_split_content[2])
        except ValueError:
            await message.channel.send("ID should be the user's numeric ID.")
            return
        try:
            user: User = await data.client.fetch_user(user_id)
        except NotFound:
            await message.channel.send(f"Couldn't find user with ID {user_id}")
            return
        try:
            await data.unban(message.guild, user)
        except Forbidden:
            await message.channel.send(f"Couldn't unban {user.mention}. Not enough permissions.")


async def temp_ban(message: Message):
    seconds: int = time_ops.parse_time(message.content)
    if seconds <= 0:
        await message.channel.send(f"Invalid temp ban message, no duration specified")
        return

    bans = []
    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            await message.channel.send(message_ops.parse(defs.temp_ban_message, member))
            try:
                await data.temp_ban(member, seconds)
                bans.append(member)
            except Forbidden:
                await message.channel.send(f"Couldn't temp ban {member.mention}. Not enough permissions.")

    await asyncio.sleep(defs.ban_message_wait)
    await message.channel.send(defs.post_temp_ban_message)


async def ban(message: Message):
    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            await message.channel.send(message_ops.parse(defs.ban_message, member))
            try:
                await message.guild.ban(member)
            except Forbidden:
                await message.channel.send(f"Couldn't ban {member.mention}. Not enough permissions.")

    await asyncio.sleep(defs.ban_message_wait)
    await message.channel.send(defs.post_ban_message)


async def kick(message: Message):
    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            await message.channel.send(message_ops.parse(defs.kick_message, member))
    await asyncio.sleep(defs.kick_message_wait)

    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            try:
                await message.guild.kick(member)
            except Forbidden:
                await message.channel.send(f"Couldn't kick {member.mention}. Not enough permissions.")


async def temp_mute(message: Message):
    guild: Guild = message.guild
    if guild.id in defs.mute_roles:
        role: Role = guild.get_role(defs.mute_roles[guild.id])
        if role is None:
            await message.channel.send(f"Mute role badly configured (couldn't fetch role from ID).")
        else:
            seconds: int = time_ops.parse_time(message.content)
            if seconds <= 0:
                await message.channel.send(f"Invalid temp ban message, no duration specified")
                return
            for member in message.mentions:
                if member != data.self_user and isinstance(member, Member):
                    try:
                        await data.temp_mute(member, role, seconds)
                    except Forbidden:
                        await message.channel.send(f"Couldn't mute {member.mention}. Not enough permissions.")


async def mute(message: Message):
    guild: Guild = message.guild
    if guild.id in defs.mute_roles:
        role: Role = guild.get_role(defs.mute_roles[guild.id])
        if role is None:
            await message.channel.send(f"Mute role badly configured (couldn't fetch role from ID).")
        else:
            for member in message.mentions:
                if member != data.self_user and isinstance(member, Member):
                    try:
                        await member.add_roles(role)
                    except Forbidden:
                        await message.channel.send(f"Couldn't mute {member.mention}. Not enough permissions.")


async def unmute(message: Message):
    guild: Guild = message.guild
    if guild.id in defs.mute_roles:
        role: Role = guild.get_role(defs.mute_roles[guild.id])
        if role is None:
            await message.channel.send(f"Mute role badly configured (couldn't fetch role from ID).")
        else:
            for member in message.mentions:
                if member != data.self_user and isinstance(member, Member):
                    try:
                        await data.unmute(member, role)
                    except Forbidden:
                        await message.channel.send(f"Couldn't unmute {member.mention}. Not enough permissions.")

# GP:
# Function def in its original form: 
# async def warn(message: Message, split_content: List[str]):

async def warn(message: Message, split_content: List[str]):

    # GP: 
    # If the length of our message is less than or equal to 3, 
    # that means that the user didn't enter a warning message, so we'd use a default message
    # e.g., @r warn @e 
    # If less than 4, they didn't enter a reason, so we exit. 

    if len(split_content) <= 4:
        warning = None

        if not split_content[3].startswith("R:"):
            await message.channel.send("Hey! You need to enter a reason for warning me!")
            return  
        
        reason_idx = split_content.index("R:")
        reason = " ".join(split_content[reason_idx:])
        for member in message.mentions:
            if member != data.self_user and isinstance(member, Member):
                if warning is None:
                    await data.warn(member, message_ops.parse(defs.default_warn_message, member))
                else:
                    await data.warn(member, warning)
    # There needs to be a space before and after R: or else
    # the bot will throw an error. 
    else:
        warning = " ".join(split_content[3:reason_idx])
        reason_idx = split_content.index("R:")
        reason = " ".join(split_content[reason_idx:])
        for member in message.mentions:
            if member != data.self_user and isinstance(member, Member):
                if warning is None:
                    await data.warn(member, message_ops.parse(defs.default_warn_message, member))
                else:
                    await data.warn(member, warning)


async def owoify(message: Message, _split_content: List[str]):
    async with data.owoify_lock:
        if message.channel.id in data.owoified_channels:
            data.owoified_channels.remove(message.channel.id)
            await message.channel.send(defs.not_owoifying_message)
        else:
            data.owoified_channels.add(message.channel.id)
            await message.channel.send(defs.owoifying_message)


async def clear_warnings(message: Message):
    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            await data.clear_warnings(member)


async def list_warnings(message: Message):
    mentions: List[Member] = []
    for member in message.mentions:
        if member != data.self_user and isinstance(member, Member):
            mentions.append(member)
    if len(mentions) == 0:
        warning_counts = await data.list_guild_warnings(message.guild)
        if warning_counts is None:
            await message.channel.send(f"No members have warnings on {message.guild}!")
        else:
            msg: List[str] = []
            for key in warning_counts:
                # msg = str_ops.limited_content(f"**<@{key}>** -> {warning_counts[key]} warnings!", msg)
                # If user's warnings aren't greater than or less than 1, use "warning"
                if warning_counts[key] > 1 or warning_counts[key] < 1:
                    msg = str_ops.limited_content(f"**<@{key}>** -> {warning_counts[key]} warnings!", msg)
                else:
                    msg = str_ops.limited_content(f"**<@{key}>** -> {warning_counts[key]} warning!", msg)
            for piece in msg:
                await message.channel.send(piece)
    else:
        for member in mentions:
            warning_counts = await data.list_member_warnings(member)
            if warning_counts is None:
                await message.channel.send(
                    f"{member.mention}'s warnings:\n"
                    "**None!**")
            else:
                await message.channel.send(
                    f"{member.mention}'s warnings:\n--------------------\n" +
                    "\n--------------------\n".join(warning_counts) +
                    "\n--------------------")


async def private_list_warnings(message: Message):
    mention: int
    for mention in message.raw_mentions:
        if mention != data.self_user.id:
            warnings = await data.list_user_warnings(str(mention))
            count = 0
            messages: List[str] = []
            for guild_id, guild_warnings in warnings.items():
                print(guild_id, guild_warnings)
                guild: Guild = await data.client.fetch_guild(int(guild_id))
                count += len(guild_warnings)
                if messages:
                    messages = str_ops.limited_content(f"**====================**\n"
                                                       f"<@{mention}>'s warnings on server {guild.name}:", messages)
                else:
                    messages = str_ops.limited_content(f"<@{mention}>'s warnings on server {guild.name}:", messages)
                for warning in guild_warnings:
                    messages = str_ops.limited_content("====================\n" + warning, messages)
            messages = str_ops.limited_content(f"**====================**\n"
                                               f"<@{mention}>'s total warning count: {count}", messages)
            for msg in messages:
                await message.channel.send(msg)


async def add_reaction_role_corret_format(message: Message, error: str):
    await message.channel.send(f"Error: {error}\n"
                               f"Correct command format: {data.self_mention}` add reaction role role_id emoji`,\n"
                               f"where `role_id` should be the role's ID (a number)\n"
                               f"and `emoji` should be an emoji :white_check_mark:")


async def add_reaction_role(message: Message, split_content: List[str]):
    if len(split_content) < 5:
        await add_reaction_role_corret_format(message, "wrong command size")
        return
    role_id: int
    try:
        role_id = int(split_content[3])
        role: Role = message.guild.get_role(role_id)
        if role is None:
            await message.channel.send(f"Couldn't find role with ID {role_id}")
            return
    except ValueError:
        await add_reaction_role_corret_format(message, f"role_id isn't a number: `{split_content[3]}`")
        return
    emoji: str = split_content[4]
    try:
        await message.add_reaction(emoji)
    except HTTPException or Forbidden or NotFound or InvalidArgument:
        await add_reaction_role_corret_format(message, f"emoji isn't a valid emoji: `{emoji}`")
        return
    emoji = emoji.lower()
    guild_id: str = str(message.guild.id)
    await data.add_reaction_role(guild_id, emoji, str(role_id))
    if await data.should_update_reaction_messages(guild_id):
        await reaction_messages.update_reaction_messages(message.guild)


async def remove_reaction_role(message: Message, split_content: List[str]):
    found_int: bool = False
    for piece in split_content:
        role_id: int
        try:
            role_id = int(piece)
        except ValueError:
            continue
        found_int = True
        guild_id: str = str(message.guild.id)
        await data.remove_reaction_role(guild_id, str(role_id))
        if await data.should_update_reaction_messages(guild_id):
            await reaction_messages.update_reaction_messages(message.guild)
    if not found_int:
        await message.channel.send(f"Correct command format: {data.self_mention}` remove reaction role role_id`,\n"
                                   f"where `role_id` should be the role's ID (a number)")


async def list_reaction_roles(message: Message):
    emoji_roles: Dict[str, str] = await data.list_reaction_roles(str(message.guild.id))
    if emoji_roles is None or not emoji_roles:
        await message.channel.send("No reaction roles configured for this guild!")
    else:
        response: str = "Reaction roles:"
        for emoji, role_id in emoji_roles.items():
            role: Role = message.guild.get_role(int(role_id))
            if role is None:
                response += f"\n{emoji} {role_id} -> **Role not found**"
            else:
                response += f"\n{emoji} {role_id} -> @{role.name}"
        await message.channel.send(response)


async def add_reaction_message(message: Message):
    reaction_message: Message = await message.channel.send(f"{defs.reaction_role_message}\n"
                                                           f"Loading...")
    await data.add_reaction_message(str(reaction_message.guild.id),
                                    reaction_message.channel.id,
                                    reaction_message.id)
    await reaction_messages.update_single_reaction_message(reaction_message)


async def leave_server(message: Message, split_content: List[str]):
    if len(split_content) < 3:
        await message.channel.send("Error: Command too short.\n"
                                   "Correct command format: `leave server server_id`,\n"
                                   "where `server_id` should be the server's ID (a number)")
        return
    guild: Guild
    try:
        guild_id: int = int(split_content[2])
        try:
            guild = await data.client.fetch_guild(guild_id)
        except Forbidden:
            await message.channel.send(f"Bot does not have access to server with ID {guild_id}.")
            return
        except HTTPException:
            await message.channel.send(f"Failed to find server with ID {guild_id}.")
            return
    except ValueError:
        await message.channel.send(f"Error: guild_id isn't a number: `{split_content[3]}`"
                                   "Correct command format: `leave server server_id`,\n"
                                   "where `server_id` should be the server's ID (a number)")
        return
    try:
        await guild.leave()
        await message.channel.send(f"Succesfully left server {guild}.")
    except HTTPException:
        await message.channel.send(f"Failed to leave server {guild}.")


# Looser ones should be on bottom, since it's a very loose check from top to bottom.
# For instance, "ban" should be after "unban" and "temp ban"
loose = {
    "temp ban": temp_ban, "shoot": temp_ban,
    "ban": ban, "kill": ban,
    "kick": kick,
    "temp mute": temp_mute, "arrest": temp_mute,
    "unmute": unmute,
    "mute": mute,
    "remove warn": clear_warnings, "unwarn": clear_warnings,
    "list warn": list_warnings,
    "list reaction role": list_reaction_roles,
    "reaction role message": add_reaction_message
}

private_loose = {
    "list warnings": private_list_warnings,
}

exact = {
    "clear": clear,
    "unban": unban,
    "warn": warn,
    "owoify": owoify
}

starts_with = {
    "add reaction role": add_reaction_role,
    "remove reaction role": remove_reaction_role
}

private_starts_with = {
    "leave server": leave_server
}
