from typing import Dict, Set, List

from discord import Message, Role, Guild, TextChannel, NotFound, Forbidden, HTTPException

import data
import defs
from utils import emoji_ops


async def reaction_message_content(emoji_roles: Dict[str, str], guild: Guild) -> str:
    if emoji_roles is None or not emoji_roles:
        return f"{defs.reaction_role_message}\n" \
               f"No reaction roles configured for this guild!"
    else:
        content: str = defs.reaction_role_message
        for emoji, role_id in emoji_roles.items():
            role: Role = guild.get_role(int(role_id))
            if role is None:
                content += f"\n{emoji} **Role not found**"
            else:
                content += f"\n{emoji} {role.mention}"
        return content


async def update_all_reaction_messages():
    all_roles: Dict[str, Dict[str, str]] = await data.list_all_reaction_roles()
    if not all_roles:
        return
    all_messages: Dict[str, List[List[int]]] = await data.list_all_reaction_messages()
    if not all_messages:
        return
    for guild_id, emoji_roles in all_roles.items():
        messages: List[List[int]] = all_messages.get(guild_id)
        if messages is None or not messages:
            continue
        guild: Guild
        try:
            guild = await data.client.fetch_guild(int(guild_id))
        except Forbidden or HTTPException:
            continue
        await _update_reaction_messages(guild, emoji_roles, messages,
                                        await reaction_message_content(emoji_roles, guild))


async def update_reaction_messages(guild: Guild):
    messages: List[List[int]] = await data.list_reaction_messages(str(guild.id))
    if messages is None or not messages:
        return
    emoji_roles: Dict[str, str] = await data.list_reaction_roles(str(guild.id))
    await _update_reaction_messages(guild, emoji_roles, messages,
                                    await reaction_message_content(emoji_roles, guild))


async def _update_reaction_messages(guild: Guild,
                                    emoji_roles: Dict[str, str],
                                    messages: List[List[int]],
                                    content: str):
    removing_messages: List[List[int]] = []
    for channel_id, message_id in messages:
        channel: TextChannel = await data.client.fetch_channel(int(channel_id))
        if channel is None:
            continue
        message: Message
        try:
            message = await channel.fetch_message(int(message_id))
        except NotFound or Forbidden:
            print(channel_id, message_id)
            removing_messages.append([channel_id, message_id])
            continue
        except HTTPException:
            continue
        await update_reaction_message(message, emoji_roles, content)
    for target in removing_messages:
        await data.remove_reaction_message(str(guild.id), target[0], target[1])


async def update_single_reaction_message(message: Message):
    emoji_roles: Dict[str, str] = await data.list_reaction_roles(str(message.guild.id))
    if emoji_roles is None or not emoji_roles:
        await message.edit(content=f"{defs.reaction_role_message}\n"
                                   f"No reaction roles configured for this guild!")
        return
    return await update_reaction_message(
        message, emoji_roles,
        await reaction_message_content(emoji_roles, message.guild))


async def update_reaction_message(message: Message, emoji_roles: Dict[str, str], content: str):
    reactions: Set[str] = set()
    for reaction in message.reactions:
        reactions.add(emoji_ops.parse_emoji(reaction.emoji))
    if emoji_roles is None or not emoji_roles:
        try:
            await message.clear_reactions()
        except Forbidden or HTTPException:
            pass
    else:
        for emoji in emoji_roles:
            if emoji not in reactions:
                await message.add_reaction(emoji)
    await message.edit(content=content)
