import asyncio
from datetime import datetime
from datetime import timedelta
import re

import pytz

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
            print(recurring)

            if recurring[0] is None:
                print("not recurring - interval")
                await asyncio.sleep(seconds)
                await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
                #await ctx.send(embed=embed)
            else:
                while True: 
                    await asyncio.sleep(seconds)
                    await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" {counter} ago.")
                    #await ctx.send(embed=embed)


    else:
        # now = datetime.now()
        date = datetime.strptime(time, '%H:%M')
        # # %I is for 12 hour clock and %p is for AM/PM
        # day = date.strftime('%m/%d/%Y')
        hour = int(date.strftime('%H'))
        minute = int(date.strftime('%M'))
        # diff = date-now
        # seconds = diff.total_seconds()
        # print(seconds)

     # You could probably do this without localizing but I needed to
        # tz = pytz.timezone("US/Pacific")
        tz = pytz.timezone("US/Eastern")
        
        # get the current time
        current_time = tz.localize(datetime.now())
        print(current_time)

        # get the time you want
        execution_time = current_time.replace(hour=hour, minute=minute, second=0)
        #delayed = 0
        print(execution_time)

        # move the day to tomorrow if the current time is past the execution time
        if execution_time.time() < current_time.time():
            execution_time = execution_time + timedelta(days=1)
            # The delayed variable is to offset the bug later in the code. I need a way to ensure that only
            # reminders called on the same day will be offset so that they fire 24 hours after they were initially fired
            # e.g., if a command were set at 5:00 PM to fire at 5:10 PM, I'd need to wait 24 hours after firing, i.e.,
            # reset the seconds variable, to avoid being stuck at 10 minute intervals.
            
            # delayed += 1
            # print(delayed)

        # This is the total amount of seconds between what time it is right now and the next time we want to
        # execute the task
        seconds = (execution_time - current_time).total_seconds()
        # print(seconds)
        # print(recurring)
        # print(type(recurring))
        await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {hour}:{str(minute).zfill(2)} hours.")
        print(recurring)
        #for some reason recurring is now a tuple. so we have to index it.
        if recurring[0] is None:
            print("not recurring")
            await asyncio.sleep(seconds)
            await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {hour}:{str(minute).zfill(2)} hours.")
        else:

            i = 0
            seconds_day = 86400
            #print("am/pm recurring")
            while True:
                # if i == 1 and not delayed == 1:
                if i == 1:
                    seconds = seconds_day
                    print("i is 1")
                # 03/05/21
                # There's an interesting bug -- the bot will execute using the originally allotted numbers of seconds
                # So, add the equivalent of a day.
                # The bug is this: if it's 10:29 PM, and I set it to remind me at 10:30 PM, 
                # the bot will save that difference in seconds as the interval at which it should run for every reminder
                #rather than running at 10:30 PM every day. So, when the reminder runs, set the number of seconds
                # the bot should sleep to the number of seconds in 24 hours. I initially added the original number of 
                #seconds, but that was just a logic error. 

                await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {hour}:{str(minute).zfill(2)} hours.")

                print(seconds)
                await asyncio.sleep(seconds)
                i += 1
                print(i)
        

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

