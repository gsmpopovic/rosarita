import asyncio
from typing import List, Dict

import re 

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
##########################################################################################################

# Remind me

#03/01/21

# @client.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
# @commands.bot_has_permissions(attach_files = True, embed_links = True)
# async def reminder(ctx, time, *, reminder):
async def remind(message: Message, split_content: List[str]):

    # reminder = split_content[3]
    # time = split_content[5]

    # 03/03/21

    #This regex will grab everything within parentheses and curly brackets respectively. 
    #It returns a list object, so we'll have to 
    # remind_subject = re.findall(r'\(.*?\)', message.content) 
    # time_subject = re.findall(r'\{.*?\}', message.content)

    #These will remove the parentheses and brackets via slicing. 
    # reminder = remind_subject[0][1:-1]
    # time = time_subject[0][1:-1]

    #This regex is more effective than the above as it'll grab everything within outermost
    #parentheses and brackets. So that's a win. 
    reminder = re.search( "\((.*)\)" ,message.content).group(1)
    time = re.search( "\{(.*)\}" ,message.content).group(1)

    #Passing a set of curly braces inside the parentheses of the reminder will break the bot. 



    #inter = split_content[6]
    #recurring = split_content[7] # yes or no

    # Roberta, remind me "something" in X (minutes, hours, days)
    # Roberta, remind me "something" at xx:xx AM/PM (timezone)
    
    if (time.lower().endswith("s") 
    or time.lower().endswith("m")
    or time.lower().endswith("h") 
    or time.lower().endswith("d")):
        user = message.author
        # embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        # embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
        seconds = 0
        if reminder is None or time is None:
            message.channel.send("Hey! You didn't set a reminder. Try again!")
            #embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
        if time is None: 
            message.channel.send("Hey! You didn't set a time. Try again!")
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            pass
            #embed.add_field(name='Warning',
                            #value='Please specify a proper duration, send `reminder_help` for more information.')
        # elif seconds < 300:
        #     pass
            # embed.add_field(name='Warning',
            #                 value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
        
        elif seconds > 7776000:
            pass
            # embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
        else:
            await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" in {counter}.")
            print(seconds)
            await asyncio.sleep(seconds)
            await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
            return
    #await ctx.send(embed=embed)
##########################################################################################################
# Snipe deleted or edited messages. 

async def snipe(message: Message, split_content: List[str]):
    items = int(split_content[2]) # The number of edits or deletes to snipe
    target = split_content[3]
    if target == "edits" or target == "deletes":
        await data.snipe(message, items, target)
##########################################################################################################
# TRIGGERS 
##########################################################################################################
exact = {
    # 02/05/21
    # Adding snipe trigger
    "snipe":snipe,
    # "memberof":memberof,
    # "leaveguild":leaveguild,

    # #02/05/21 
    #03/03/21
    # # Adding "music please" trigger
    # # Adding remind trigger 

    "music":music, 
    "remind":remind
}