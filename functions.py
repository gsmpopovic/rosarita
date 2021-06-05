
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

#02/19/21
# I had to create a function because I was getting an annoying scope error with try-except
# and did not want to create a global variable 
async def connect_to_voice(message, client):

    # This would be to find a particular channel based on name. 
    # channel = utils.find(lambda x: x.name == 'music', message.guild.channels)
    # print(channel)

    # This will raise the exception if our user isn't in a voice channel, 
    # i.e., if the type of our user's voiceclient is None

    none_type = isinstance(message.author.voice, type(None))
    if none_type: 
        await message.channel.send("You're not in a voice channel, so I can't do that! B-baka!")
        return 0

    channel = message.author.voice.channel

    # A list of the guild's voice channels
    voice_channel_list = message.guild.voice_channels

    # This is to handle the edge case (because you know someone is going to do it)
    # where a user asks the bot to leave despite the bot not being in a voice channel.
    if len(client.voice_clients) == 0 and message.content.split()[2]=="leave":
        await message.channel.send("I'm not in a voice channel, so I can't do that! B-baka!")
        return 0

    if len(client.voice_clients) == 0:
        return await channel.connect() 

    # for i in range(10):
    #         for voiceclient in client.voice_clients:
        
    #             for vc in voice_channel_list:
    #                 # print(voiceclient)
    #                 # print(vc)
    #                 print(f"this is a voice channel on the server: {vc}")
    #                 print(f" this is one of the bot's voice client {voiceclient.channel}")

    # A list of the bot's voiceclients. These are objects so we have to access their attributes. 
    for voiceclient in client.voice_clients:
        
        for vc in voice_channel_list:
            # print(voiceclient)
            # print(vc)
            # print(f"voice channel {vc}")
            # print(f"voice client {voiceclient.channel}")


            if channel == voiceclient.channel: 

                # Admittedly this statement will print whenever we try to connect to the voice channel (if already)
                # connected--but I need to check whether or not we're connected to perform any of the
                # functions. So this print statement is here for error handling. 

                print(f"I'm already connected to this voice channel, and the command was {message.content}")

                # If we want our bot to leave a voice channel, we pass the leave keyword. 
                # @r music leave 
                # Will only execute given user is connected to a voice channel, 
                # and bot as well. 

                if message.content.split()[2]=="leave":
                    await message.channel.send("Peace out, cub scout.")
                    print("Bot disconnecting from voice channel.")
                    await voiceclient.disconnect()
                    return 0

                return voiceclient
                # return 0

            else:

                print("We're not already connected, so let's try to connect.")
                    
                #02/19/21
                #Get the VoiceClient to which the bot will be connecting. 
                # This was really annoying to figure out. 

                try: 
                    
                    voiceclient = await channel.connect(reconnect=True)

                    return voiceclient

                # I would have continued in this vein if I were aware of some 
                # means by which I can auto-connect a user to a voice channel. 
                # print(message.author.voice)
                # await message.author.move_to(channel)

                except:

                    try: 
                        # The connection will fail if our bot's voice client already has a connection to that
                        #channel. So, if that is the case, we can just try to move to that channel. 
                        await voiceclient.move_to(channel)

                        return voiceclient

                    except: 
                        pass

                    print("Error upon trying to connect to VC. Either user isn't in a voice channel, or R is already in that voice channel.")

                    #This is just a general error

                    return 0

                    # voiceclient.disconnect()

    return
###########################################################
song_queue = []
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

#Search videos from key-words or links
def search(arg):
    try: requests.get("".join(arg))
    except: arg = "".join(arg)
    else: arg = "".join(arg)
    with YoutubeDL(YDL_OPTIONS ) as ydl:
        info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        # info = ydl.extract_info(url, download=False)

        
    return {'source': info['formats'][0]['url'], 'title': info['title']}

#Plays the next song in the queue
def play_next(voiceclient):
    if len(song_queue) > 1:
        print(len(song_queue))
        print(song_queue[0])
        del song_queue[0]
        #data.client.ffmpeg
        voiceclient.play(FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(voiceclient))
        # voiceclient.play(FFmpegPCMAudio(executable=client.ffmpeg, source=song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: play_next(voiceclient))

        voiceclient.is_playing()
###########################################################

# async def play_queued_songs(voiceclient, url): 

#     songs = asyncio.Queue()
#     play_next_song = asyncio.Event()

#     async def audio_player_task():
#         while True:
#             play_next_song.clear()
#             current = await songs.get()
#             current.start()
#             await play_next_song.wait()

# This doesn't work because the currrent v of the Discord.py library does not return an instance of player
#         player = await voiceclient.create_ytdl_Player(FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=url), after="toggle_next")

#         await songs.put(voiceclient)

#client.loop.create_task(audio_player_task())

# async def check_queue(data.client):
#     return len(data.client.queue) > 0


