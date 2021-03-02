import asyncio
from typing import List, Dict

from discord import Message, Forbidden, Guild, Member, Role, User, NotFound, HTTPException, InvalidArgument, utils

#imported utils from discord 02/05/21

# 02/05/21
#import tasks from discord.ext 
# import checks

#02/17/21 
# imported commands 

from discord.ext import tasks, commands

import functions 
import checks 
import data
import defs
from interactions import time_ops, reaction_messages, str_ops
#from utils import message_ops

# 02/17/21
#imported get from utils
# imported FFmpegPCMAudio from discord
#imported youtube_dl 

# for FFmpegPCMAudio you need to download FFMPeg. 
# I use Windows, so:
# https://lame.buanzo.org/#lamewindl

from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

#02/25/21

import requests 

##########################################################################################################
##########################################################################################################

async def music(message: Message, split_content: List[str]):

    #voiceclient will either be a voiceclient object representing 
    # a particular voice connection, i.e., with attributes like "channel"
    # or, if the bot is already connected, an int being 0. 
    voiceclient = await functions.connect_to_voice(message, data.client) 

    print(type(voiceclient))

    if type(voiceclient) is int: 
        print("User isn't in a voice channel.")
        return

    if len(split_content) <= 4:
        target = split_content[2]
        # YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        # YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

        # FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

        if len(split_content)==4: 
            # try: 
            #     song = functions.search(url)
            #     print(song)
            #     functions.song_queue.append(song)
            # except: 
            #     # We're already playing a song. 
            #     print(" ")
            url = split_content[3]
            song = functions.search(url)
            print(song)
            functions.song_queue.append(song)

        if not voiceclient.is_playing():

            if target=="play":
                voiceclient.play(FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['source'], **FFMPEG_OPTIONS), after=lambda e: functions.play_next(voiceclient))
                voiceclient.is_playing()

            elif target=="resume":
                voiceclient.resume()
                print("Song resuming.")
                voiceclient.is_playing()

            
        else:

            if target=="pause":
                voiceclient.pause()
                voiceclient.is_playing()
                print("Song paused.")

            elif target == "stop":
                voiceclient.stop()
                voiceclient.is_playing()
                print("Song stopped.")
            return
                
##########################################################################################################
# TRIGGERS 
##########################################################################################################
exact = {
    "clear": clear,
    "unban": unban,
    "warn": warn,
    "owoify": owoify,

    # 02/05/21
    # Adding snipe trigger
    # Adding memberof trigger
    # Adding leaveguild trigger

    "snipe":snipe,
    "memberof":memberof,
    "leaveguild":leaveguild,

    #02/05/21 
    # Adding "music please" trigger
    # Adding remind trigger 
    "remind":remind, 
    "music":music
}