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

async def canceltask(message: Message, split_content: List[str]):
    # To cancel task user has to mention R in a channel and call the canceltask command.
    #e.g.,
    #@rosarita canceltask (Task-21)
    task = re.search( "\((.*)\)" ,message.content).group(1)

    # Gets all of the tasks in our event loop. All pending tasks, i.e.
    tasks = asyncio.all_tasks(data.client.loop)

    for elem in tasks: 
        if task == elem.get_name():
            elem.cancel()
            await message.author.send(f"Okay, I've cancelled {elem.get_name()} for you.")
            return 

async def remind(message: Message, split_content: List[str]):
    user = message.author
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
    recurring = re.search("\[(.*)\]", message.content)
    print(recurring)
    if recurring is not None: 
        print("recurring")
        
        if recurring.group(1) == "y":
            print("recurring")

            schedule_recurring = data.client.loop.create_task(sched_functions.schedule(message, reminder, time, recurring))
            print(dir(schedule_recurring))
            await user.send("To cancel this reminder, message me: @rosarita canceltask (task name)")
            await user.send(f"Here's the name of this task: {schedule_recurring.get_name()}")
    else: 
        print("not recurring")
        await sched_functions.schedule(message, reminder, time, recurring)

##########################################################################################################
# Snipe deleted or edited messages. 


async def snipe(message: Message, split_content: List[str]):
    #Command format:
    #@rosarita snipe 1 deletes

    max = 10
    items = int(split_content[2]) # The number of edits or deletes to snipe
    target = split_content[3].lower()

    if items > max:
        await message.channel.send("I can't snipe more than 10 edited/deleted messages at a time.")
        return

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

    # #02/05/21 
    #03/03/21
    # # Adding "music please" trigger
    # # Adding remind trigger 

    "music":music, 
    "remind":remind, 
    "canceltask":canceltask
}