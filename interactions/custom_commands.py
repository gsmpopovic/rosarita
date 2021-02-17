# @client.command(name="music")
# async def music(message: Message, split_content: List[str]):
    
#     # This would be to find a particular channel based on name. 
#     # channel = utils.find(lambda x: x.name == 'music', message.guild.channels)
#     # print(channel)

#     # This will raise the exception if our bot is already in a specific voice channel 
#     channel = message.author.voice.channel
#     print(message.author.voice.channel)

#     try:
#         await channel.connect()

#     except:
#         print("already connected")

#     # I would have continued in this vein if I were aware of some 
#     # means by which I can auto-connect a user to a voice channel. 
#     # print(message.author.voice)
#     # await message.author.move_to(channel)

#     YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
#     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#     # voice = get(data.client.voice_clients, guild=ctx.guild)
#     voice = data.client.voice_clients

#     if not voice.is_playing():
#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(video_link, download=False)
#         URL = info['formats'][0]['url']
#         voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#         voice.is_playing()
#     else:
#         await ctx.send("Already playing song")
#         return

