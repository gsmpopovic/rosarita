# import asyncio
# from typing import List, Optional

# import discord
# from discord import Message, AppInfo, Guild, Forbidden, Role, RawReactionActionEvent, Member

# # -2/20/21 
# # I tried to make it such that R would inherit from the bot provided by discord.ext, BotBase, but 
# # this proved very difficult and frustrating 

# # from discord.ext import commands
# # from discord.ext.commands import bot  

# # 02/17/21

# # The bot really should be using discord.ext.commands, but the previous dev didn't do that, 
# # so I'm left to continue where he left off. 
# # Quite interestingly, he parsed the commands himself

# import checks
# import data
# import defs
# import my_parser
# from interactions import exact, loose, bot_help, starts_with, admin_commands, lite_commands, str_ops, reaction_messages
# from utils import emoji_ops, message_ops

# #02/24/21
# from discord import FFmpegPCMAudio
# from youtube_dl import YoutubeDL

# class Playlist(asyncio.Queue):
#     async def next_song(self):
#         while True:
#             yield await self.get()

#     async def add_song(self, song):
#         await self.put(song)


# #class RosaritaClient(discord.Client, bot.BotBase):
# class RosaritaClient(discord.Client):
#     ready = False

#     async def on_ready(self):
        
#         if not self.ready:
#             app_info: AppInfo = await self.application_info()

#             data.owner = app_info.owner
#             data.self_user = self.user
#             data.self_mention = self.user.mention
#             data.client = self
#             await data.load()

#             # 02/24/21
#             #Playlist related 
#             self.playlist = Playlist()
#             self.isplaying = False

#             await reaction_messages.update_all_reaction_messages()

#             await checks.check_mute_roles()

#             asyncio.create_task(checks.check_temp_stuff()())
#             asyncio.create_task(checks.check_creed()())

#             # loop = asyncio.get_event_loop()
#             # loop.create_task(self.input_songs())
#             #loop.run()

#             self.ready = True
#             await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="@help"))

#             print("Ready!")

#         #First to execute
#     async def input_songs(self, url):
#         await self.add_songs(url)

#     #Second to execute
#     async def add_songs(self, song):
#         # for song in song:
#         #     if song != "play":
#         await self.playlist.add_song(song)
#         print("song {} added".format(song))
#         if self.playlist.qsize() == 1:
#             print("queue has one task, launching the play         function")
#             asyncio.gather(self.play(), self.input_songs(song))

#     #Third to execute 
#     async def play_song(self, song):
#         self.is_playing()
#         print('now playing:', song)
#         await asyncio.sleep(5)
#         print("{} has finished reproducing".format(song))
#         self.is_playing()
#         await self.play()

#     #Fourth to execute 
#     def is_playing(self):
#         self.isplaying = not self.isplaying

#     async def add_song(self, *args, **kwargs):
#         await self.playlist.add_song(*args, **kwargs)

#     #Fifth to execute
#     async def play(self):
#         if not self.isplaying:
#             async for song in self.playlist.next_song():
#                 asyncio.gather(self.play_song(song), await self.input_songs(song))
#         else:
#             print("waiting for the song to finish...")
  

#     async def on_message(self, message: Message):
#         if not self.ready or message.author.bot:
#             return

#         is_owner: bool = message.author == data.owner
#         if message.guild is not None:
#             content_lower: str = message.content.lower()
#             mentioned: bool = self.user in message.mentions
#             lite_mentioned: bool = defs.readable_bot_name in content_lower
#             guild: Guild = message.guild
#             is_guild_owner: bool = is_owner or message.author == guild.owner
#             if mentioned:
#                 split_content: List[str] = message.content.split()
#                 if len(split_content) >= 2:
#                     trigger: str = split_content[1].lower()
#                     if is_guild_owner:
#                         if trigger in admin_commands.exact:
#                             await admin_commands.exact[trigger](message, split_content,)
#                             return
#                         second_content_lower: str = content_lower[len(split_content[0]) + 1:]
#                         for trigger in admin_commands.starts_with:
#                             if second_content_lower.startswith(trigger):
#                                 await admin_commands.starts_with[trigger](message, split_content[1:])
#                                 return
#                     if trigger in lite_commands.exact:
#                         await lite_commands.exact[trigger](message)
#                         return
#                 if is_guild_owner:
#                     for trigger in admin_commands.loose:
#                         if trigger in content_lower:
#                             await admin_commands.loose[trigger](message)
#                             return
#             if mentioned or lite_mentioned:
#                 for trigger in loose.mentioned_interactions:
#                     if trigger in content_lower:
#                         await loose.mentioned_interactions[trigger](message)
#                         return
#             if content_lower in exact.interactions:
#                 await exact.interactions[content_lower](message)
#                 return
#             for trigger in starts_with.interactions:
#                 if content_lower.startswith(trigger):
#                     await starts_with.interactions[trigger](message)
#                     return
#             if await my_parser.all_parse(message, content_lower,
#                                          is_owner, is_guild_owner, False, mentioned):
#                 return
#             if await my_parser.parse(message, content_lower):
#                 return
#             for trigger in loose.interactions:
#                 if trigger in content_lower:
#                     await loose.interactions[trigger](message)
#                     return
#             split_content_lower: List[str] = content_lower.split()
#             for trigger in loose.word_interactions:
#                 if trigger in split_content_lower:
#                     await loose.word_interactions[trigger](message)
#                     return
#             if mentioned or lite_mentioned:
#                 await message.channel.send(defs.thats_me)
#                 return
#             if message.channel.id in data.owoified_channels:
#                 try:
#                     await message.delete()
#                     await message.channel.send(f"{message.author.mention}: {str_ops.owoify(message.content)}")
#                 except Forbidden:
#                     return
#         elif is_owner:
#             content_lower: str = message.content.lower()
#             mentioned: bool = self.user in message.mentions
#             if mentioned:
#                 split_content = content_lower.split()
#                 if len(split_content) >= 2:
#                     second_content_lower: str = content_lower[len(split_content[0]) + 1:]
#                     for trigger in admin_commands.private_starts_with:
#                         if second_content_lower.startswith(trigger):
#                             await admin_commands.private_starts_with[trigger](message, split_content[1:])
#                             return
#             if await my_parser.all_parse(message, content_lower,
#                                          True, True, True, mentioned):
#                 return
#             if mentioned:
#                 for trigger in admin_commands.private_loose:
#                     if trigger in content_lower:
#                         await admin_commands.private_loose[trigger](message)
#                         return

#     # 02/05/21
#     # On message delete
#     # Two positional arguments (because class), self and message object. 
#     async def on_message_delete(self, message: Message):

#         if not self.ready: 
#             return 

#         #await message.channel.send(f"{message.content} was deleted")

#         await data.record_deletes(message)

#     # 02/05/21
#     # On message edit
#     # Three positional arguments, self, message_before, message_after. 
#     async def on_message_edit(self, message_before, message_after):

#         if not self.ready: 
#             return 

#         #await message_after.channel.send(f"{message_before.content} was edited to say {message_after.content}")

#         await data.record_edits(message_before, message_after)

#     async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
#         if not self.ready:
#             return

#         is_owner: bool = payload.user_id == data.owner.id
#         if payload.guild_id is None and not is_owner:
#             return

#         user = payload.member
#         if user is None:
#             user = self.get_user(payload.user_id)
#             if user is None:
#                 user = await self.fetch_user(payload.user_id)
#         if user is None or user.bot:
#             return
#         message_id: int = payload.message_id

#         guild: Optional[Guild]
#         if payload.guild_id is None:
#             guild = None
#         else:
#             guild: Guild = self.get_guild(payload.guild_id)
#             if guild is None:
#                 guild = await self.fetch_guild(payload.guild_id)

#         if message_id in data.help_reactions and data.help_reactions[message_id] == payload.user_id:
#             channel = await self.fetch_channel(payload.channel_id)
#             message: Message = await channel.fetch_message(message_id)
#             emoji = payload.emoji.name
#             async with data.help_lock:
#                 if message_id in data.help_reactions:
#                     if emoji == defs.reaction_yes:
#                         await message.channel.send(message_ops.parse(defs.help_yes, user))
#                         for help_piece in bot_help.do_help(
#                                 is_owner, guild is not None and payload.user_id == guild.owner_id, guild is None):
#                             await message.channel.send(help_piece)
#                     elif emoji == defs.reaction_no:
#                         await message.channel.send(message_ops.parse(defs.help_no, user))
#                     del data.help_reactions[message_id]
#         if guild is None:
#             return
#         role_id: int = await data.get_reaction_message(
#             str(guild.id), payload.channel_id, message_id, emoji_ops.parse_emoji(payload.emoji))
#         if role_id is not None:
#             role: Role = guild.get_role(role_id)
#             if role is not None:
#                 if payload.member is None:
#                     await (await guild.fetch_member(payload.user_id)).add_roles(role)
#                 else:
#                     await payload.member.add_roles(role)

#     async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
#         if not self.ready or payload.guild_id is None:
#             return
#         message_id: int = payload.message_id
#         guild: Guild = self.get_guild(payload.guild_id)
#         if guild is None:
#             guild = await self.fetch_guild(payload.guild_id)
#         # For some reason, payload.member isn't defined on this event.
#         member: Member = await guild.fetch_member(payload.user_id)
#         if member.bot:
#             return

#         role_id: int = await data.get_reaction_message(
#             str(guild.id), payload.channel_id, message_id, emoji_ops.parse_emoji(payload.emoji))
#         if role_id is not None:
#             role: Role = guild.get_role(role_id)
#             if role is not None:
#                 await member.remove_roles(role)