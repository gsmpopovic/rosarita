import asyncio

from discord import Guild, HTTPException, Forbidden, Role, PermissionOverwrite
from discord.abc import GuildChannel
import data
import defs

async def check_mute_roles():
    print("Checking mute roles...")
    guild_id: int
    for guild_id, role_id in defs.mute_roles.items():
        guild: Guild
        try:
            guild = await data.client.fetch_guild(guild_id)
        except Forbidden:
            print(f"Couln't get guild with ID {guild_id}. Bot doesn't have access to guild.")
            continue
        except HTTPException:
            print(f"Couln't get guild with ID {guild_id}. HTTPException.")
            continue
        role: Role = guild.get_role(role_id)
        if role is None:
            print(f"Couldn't find role with ID {role_id} from guild {guild} with ID {guild_id}.")
            continue
        if role.is_default():
            print(f"Ignoring role {role} with ID {role_id} from guild {guild} with ID {guild_id} "
                  f"because it's an @everyone role")
            continue
        channel: GuildChannel
        for channel in await guild.fetch_channels():
            overwrites: PermissionOverwrite = channel.overwrites_for(role)
            if overwrites.speak is not False or overwrites.send_messages is not False:
                try:
                    await channel.set_permissions(role, speak=False, send_messages=False)
                except Forbidden:
                    print(f"Not enough permissions to update role {role} "
                          f"from guild {guild} with ID {guild_id} "
                          f"on channel {channel}.")


def check_temp_stuff():
    async def wrapper():
        while True:
            await data.check_temps()
            await asyncio.sleep(defs.temp_check_delay)

    return wrapper


def check_creed():
    async def wrapper():
        while True:
            data.creed = max(0, data.creed - 1)
            await asyncio.sleep(defs.creed_cooldown_delay)

    return wrapper
