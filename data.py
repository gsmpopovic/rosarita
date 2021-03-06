import asyncio
import json
import time
from datetime import datetime

# 02/05/21
# Import sched
#import sched 

from asyncio.locks import Lock
from typing import Set, Dict, List, Optional

from discord import User, Member, Guild, Role, Client, HTTPException

# 02/05/21
# Import message
from discord import Message 

import defs

client: Client
owner: User
self_user: User
self_mention: str

help_reactions: Dict[int, int] = {}
help_lock: Lock = asyncio.Lock()

tea_waiting_thanks: Set[int] = set()
tea_lock: Lock = asyncio.Lock()

owoified_channels: Set[int] = set()
owoify_lock: Lock = asyncio.Lock()

_data_lock: Lock = asyncio.Lock()
_temp_bans: Dict[str, int] = {}
_temp_mutes: Dict[str, int] = {}
_warnings: Dict[str, Dict[str, List[str]]] = {}
_reaction_roles: Dict[str, Dict[str, str]] = {}
_reaction_messages: Dict[str, List[List[int]]] = {}

# 02/05/21
# Create two lists to hold edited and deleted messages. 

_edits = []
_deletes = []

# 02/21/21
# create a list to hold queued songs.

# _queued = []


creed = 0


def data_locked(func):
    async def wrapper(*args, **kwargs):
        async with _data_lock:
            return await func(*args, **kwargs)

    return wrapper

#02/21/21
# Create queue for queued music 

# @data_locked
# async def queue_music(message, url):
#     _queued.append(url)
#     await _save()
#     return _queued

# 02/05/21
# Record edits 

@data_locked 
async def record_edits(message_before, message_after):
    # _edits.append(message.content)
    author = message_after.author
    key = f"{message_after.created_at}"
    _edits.append(
        {key:{
            "author": author.name,
            "before":message_before.content, 
            "after":message_after.content
            }
    })
    await _save()

# 02/05/21
# Record deletes

@data_locked 
async def record_deletes(deleted_message):
    author = deleted_message.author
    key = f"{deleted_message.created_at}"
    _deletes.append(
        {key:{
            "author": author.name,
            "deleted_message":deleted_message.content, 
            }
    })
    await _save()

# 02/05/21
# Updated 03/05/21
# Snipe 

@data_locked 
async def snipe(message, items, target):
    channel = message.channel
    # sniped = []
    if target == "edits":
        if items <= len(_edits):
            # for i in n:
            #     sniped.append(_edits[i])
            # await message.channel.send(sniped)
            i = -1
            j = 0
            while j < items:
                await message.channel.send(_edits[i])
                # i will iterate through the list backward. 
                # j is just to break the loop. 

                i += -1
                j += 1
        else:
            await message.channel.send("tHere aren't that many edited messages.")
    else: 
        if items <= len(_deletes):
            # for i in n:
            #     sniped.append(_edits[i])
            # await message.channel.send(sniped)
            i = -1
            j = 0
            while i < items:
                await message.channel.send(_deletes[i])
                # i will iterate through the list backward. 
                # j is just to break the loop. 
                i += -1
                j += 1
        else:
            await message.channel.send("tHere aren't that many deleted messages.")



@data_locked
async def temp_ban(member: Member, duration: int):
    key: str = f"{member.guild.id}_{member.id}"
    await member.ban()
    if key not in _temp_bans:
        _temp_bans[key] = int(time.time()) + duration
        await _save()


@data_locked
async def unban(guild: Guild, user):
    key: str = f"{guild.id}_{user.id}"
    await guild.unban(user)
    if key in _temp_bans:
        del _temp_bans[key]
        await _save()


@data_locked
async def temp_mute(member: Member, mute_role: Role, duration: int):
    key: str = f"{member.guild.id}_{member.id}"
    await member.add_roles(mute_role)
    if key not in _temp_mutes:
        _temp_mutes[key] = int(time.time()) + duration
        await _save()


@data_locked
async def unmute(member: Member, mute_role: Role):
    key: str = f"{member.guild.id}_{member.id}"
    await member.remove_roles(mute_role)
    if key in _temp_mutes:
        del _temp_mutes[key]
        await _save()


@data_locked
async def check_temps():
    now: int = int(time.time())
    changed = False
    removing = []
    for key in _temp_bans:
        if _temp_bans[key] > now:
            key = key.split('_')
            guild: Guild = await client.fetch_guild(int(key[0]))
            user: User = await client.fetch_user(int(key[1]))
            await guild.unban(user)
            removing.append(key)
            changed = True
    for key in removing:
        del _temp_bans[key]
    removing.clear()
    for key in _temp_mutes:
        if _temp_mutes[key] < now:
            split_key = key.split('_')
            guild: Guild = await client.fetch_guild(int(split_key[0]))
            role: Role = guild.get_role(defs.mute_roles.get(int(split_key[0])))
            try:
                member: Member = await guild.fetch_member(int(split_key[1]))
                await member.remove_roles(role)
            except HTTPException:
                pass
            removing.append(key)
            changed = True
    for key in removing:
        del _temp_mutes[key]
    if changed:
        await _save()


@data_locked
async def warn(member: Member, warning: str, reason: str):
    # To get date and time
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    guild_id: str = str(member.guild.id)
    member_id: str = str(member.id)
    # print(guild_id in _warnings)
    if guild_id in _warnings:
        # print(member_id in _warnings[guild_id])
        if member_id in _warnings[guild_id]:
            # print(_warnings[guild_id][member_id])
            # print(warning)
            _warnings[guild_id][member_id].append(f'"Date and time" => {date_time},\n "Warning" => {warning},\n "Reason" => {reason}')

        else:
            _warnings[guild_id][member_id] = [f'"Date and time" => {date_time},\n "Warning" => {warning},\n "Reason" => {reason}']

    else:
        _warnings[guild_id] = {member_id: f'"Date and time" => {date_time},\n "Warning" => {warning},\n "Reason" => {reason}'}
    await _save()


@data_locked
async def clear_warnings(member: Member):
    guild_id: str = str(member.guild.id)
    member_id: str = str(member.id)
    #print( guild_id in _warnings and member_id in _warnings[guild_id])
    if guild_id in _warnings and member_id in _warnings[guild_id]:
        #print(_warnings[guild_id][member_id])
        del _warnings[guild_id][member_id]
        await _save()


@data_locked
async def list_guild_warnings(guild: Guild) -> Optional[Dict[str, int]]:
    guild_id: str = str(guild.id)
    if guild_id in _warnings:
        warning_counts: Dict[str, int] = {}
        warnings: Dict[str, List[str]] = _warnings[guild_id]
        for key, warning in warnings.items():
            warning_counts[key] = len(warning)
        return warning_counts
    else:
        return None


@data_locked
async def list_member_warnings(member: Member) -> Optional[List[str]]:  # For a specific member
    guild_id: str = str(member.guild.id)
    member_id: str = str(member.id)
    if guild_id in _warnings and member_id in _warnings[guild_id]:
        return _warnings[guild_id][member_id]
    else:
        return None


@data_locked
async def list_user_warnings(user_id: str) -> Dict[str, List[str]]:  # For a specific user, regardless of guild
    warnings: Dict[str, List[str]] = {}
    for key, guild_warnings in _warnings.items():
        if user_id in guild_warnings:
            warnings[key] = guild_warnings[user_id]
    return warnings


@data_locked
async def add_reaction_role(guild_id: str, emoji: str, role_id: str):
    if guild_id in _reaction_roles:
        _reaction_roles[guild_id][emoji] = role_id
    else:
        _reaction_roles[guild_id] = {emoji: role_id}
    await _save()


@data_locked
async def remove_reaction_role(guild_id: str, role_id: str):
    if guild_id in _reaction_roles:
        removing = []
        for emoji, role in _reaction_roles[guild_id].items():
            if role == role_id:
                removing.append(emoji)
        for emoji in removing:
            del _reaction_roles[guild_id][emoji]
            if not _reaction_roles[guild_id]:
                del _reaction_roles[guild_id]
        await _save()


async def list_all_reaction_roles() -> Dict[str, Dict[str, str]]:
    return _reaction_roles


async def list_reaction_roles(guild_id: str) -> Optional[Dict[str, str]]:
    return _reaction_roles.get(guild_id)


@data_locked
async def add_reaction_message(guild_id: str, channel_id: int, message_id: int):
    if guild_id in _reaction_messages:
        _reaction_messages[guild_id].append([channel_id, message_id])
    else:
        _reaction_messages[guild_id] = [[channel_id, message_id]]
    await _save()


@data_locked
async def remove_reaction_message(guild_id: str, channel_id: int, message_id: int):
    if guild_id in _reaction_messages and [channel_id, message_id] in _reaction_messages[guild_id]:
        _reaction_messages[guild_id].remove([channel_id, message_id])
        if not _reaction_messages[guild_id]:
            del _reaction_messages[guild_id]
        await _save()


async def should_update_reaction_messages(guild_id: str) -> bool:
    return guild_id in _reaction_messages


async def list_reaction_messages(guild_id: str) -> Optional[List[List[int]]]:
    return _reaction_messages.get(guild_id)


async def get_reaction_message(guild_id: str, channel_id: int, message_id: int, emoji: str) -> Optional[int]:
    messages = _reaction_messages.get(guild_id)
    print(messages, channel_id, message_id)
    if messages is None or [channel_id, message_id] not in messages:
        return None
    roles = _reaction_roles.get(guild_id)
    print(roles, guild_id)
    if roles is None:
        return None
    role = roles.get(emoji)
    print(role, emoji)
    if role is None:
        return None
    else:
        return int(role)


async def list_all_reaction_messages() -> Dict[str, List[List[int]]]:
    return _reaction_messages


@data_locked
async def load():
    global _temp_bans, _temp_mutes, _warnings, _reaction_roles, _reaction_messages, _edits, _deletes
    # global _queued
    with open('data.json', 'r') as f:
        data = json.load(f)
        if 'temp_bans' in data:
            _temp_bans = data['temp_bans']
        if '_temp_mutes' in data:
            _temp_mutes = data['_temp_mutes']
        if '_warnings' in data:
            _warnings = data['_warnings']
        if '_reaction_roles' in data:
            _reaction_roles = data['_reaction_roles']
        if '_reaction_messages' in data:
            _reaction_messages = data['_reaction_messages']
        if '_edits' in data: 
            _edits = data['_edits']
        if '_deletes' in data:
            _deletes = data['_deletes']
        # if '_queued' in data:
        #     _queued = data['_queued']


async def _save():
    with open('data.json', 'w') as f:
        json.dump({
            'temp_bans': _temp_bans,
            '_temp_mutes': _temp_mutes,
            '_warnings': _warnings,
            '_reaction_roles': _reaction_roles,
            '_reaction_messages': _reaction_messages,
            '_edits': _edits,
            '_deletes':_deletes

            # 021/21/21
            # '_queued':_queued
        }, f)
