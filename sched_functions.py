import asyncio
from datetime import datetime
import re

async def schedule(message, reminder, time, *recurring):
    
    #Passing a set of curly braces inside the parentheses of the reminder will break the bot. 

    # Roberta, remind me ("something") in {Xm/h/d/s}
    # Roberta, remind me ("something") at { mm/dd/yy HH:MM}
    # To make a reminder recurring, you pass [y] at the end. 

    user = message.author

    if (time.lower().endswith("s") or
    time.lower().endswith("m") or 
    time.lower().endswith("h") or
    time.lower().endswith("d")):
        # embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        # embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
        seconds = 0
        if reminder is None or time is None:
            message.channel.send("Hey! You didn't set a reminder. Try again!")
            #embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
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
            if recurring is None: 
                await asyncio.sleep(seconds)
                await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
                #await ctx.send(embed=embed)
            else:
                await asyncio.sleep(seconds)
                await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
                    #await ctx.send(embed=embed)


    else:
        now = datetime.now()
        date = datetime.strptime(time, '%m/%d/%Y %H:%M')
        # %I is for 12 hour clock and %p is for AM/PM
        day = date.strftime('%m/%d/%Y')
        hour = date.strftime('%H:%M')
        diff = date-now
        seconds = diff.total_seconds()
        print(seconds)

        await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {hour} hours on {day}.")
        if recurring is None:
            await asyncio.sleep(seconds)
            await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {hour} hours on {day}.")
        else:
            await asyncio.sleep(seconds)
            await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {hour} hours on {day}.")
       

######################################################################################################################
# async def schedule_recurring(message, reminder, time, *recurring):
    
#     #Passing a set of curly braces inside the parentheses of the reminder will break the bot. 

#     # Roberta, remind me ("something") in {Xm/h/d/s}
#     # Roberta, remind me ("something") at { mm/dd/yy HH:MM}

#     user = message.author

#     if (time.lower().endswith("s") or
#     time.lower().endswith("m") or 
#     time.lower().endswith("h") or
#     time.lower().endswith("d")):
#         # embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
#         # embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url=f"{client.user.avatar_url}")
#         seconds = 0
#         if reminder is None or time is None:
#             message.channel.send("Hey! You didn't set a reminder. Try again!")
#             #embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
#         if time.lower().endswith("d"):
#             seconds += int(time[:-1]) * 60 * 60 * 24
#             counter = f"{seconds // 60 // 60 // 24} days"
#         if time.lower().endswith("h"):
#             seconds += int(time[:-1]) * 60 * 60
#             counter = f"{seconds // 60 // 60} hours"
#         elif time.lower().endswith("m"):
#             seconds += int(time[:-1]) * 60
#             counter = f"{seconds // 60} minutes"
#         elif time.lower().endswith("s"):
#             seconds += int(time[:-1])
#             counter = f"{seconds} seconds"
#         if seconds == 0:
#             pass
#             #embed.add_field(name='Warning',
#                             #value='Please specify a proper duration, send `reminder_help` for more information.')
#         # elif seconds < 300:
#         #     pass
#             # embed.add_field(name='Warning',
#             #                 value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
        
#         elif seconds > 7776000:
#             pass
#             # embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
#         else:
#             await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" in {counter}.")
#             while True: 
#                 await asyncio.sleep(seconds)
#                 await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
#         #await ctx.send(embed=embed)

#     else:
#         now = datetime.now()
#         date = datetime.strptime(time, '%m/%d/%Y %H:%M')
#         # %I is for 12 hour clock and %p is for AM/PM
#         day = date.strftime('%m/%d/%Y')
#         hour = date.strftime('%H:%M')
#         diff = date-now
#         seconds = diff.total_seconds()
#         print(seconds)

#         await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {hour} hours on {day}.")
#         while True: 
#             await asyncio.sleep(seconds)
#             await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {hour} hours on {day}.")

