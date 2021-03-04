

        # current_hour = str(datetime.now().hour)
        # current_minute = str(datetime.now().minute)
        # mt = current_hour+current_minute
        # current_time = int(mt)
        # desired_time = int(time)
        # if desired_time < current_time:

        #     print(current_time)
        #     print(desired_time)
        #     diff = abs(current_time - 24)
        #     print(diff)
        # else: 
        #     diff = abs(current_time - desired_time)*60
        #     print(diff)

    # # If user enters military time (24:00) rather than a specific denomination of time.

    #     #Get the current hour and minute from LOCAL MACHINE
    #     current_hour = datetime.now().hour
    #     current_minute = datetime.now().minute

    #     #Get the time string, break into up nto hours and minutes
    #     # e.g, 22:00 --> 10:00 PM 
    #     split = time.split(":", 1)
    #     hours = int(split(0))
    #     minutes = int(split(1))

    #     # Special case if hours are zero, e.g., 00:15. 
    #     # or minutes, e.g., 22:00. 

    #     if minutes == 0 or hours == 0:
    #         # Get the difference of minutes from 60. e.g., from 21:55 -> 22:00 is 5 minutes. 
    #         if minutes == 0:
    #             # Get the difference of the hours and minutes, convert to seconds. 
    #             diff_hour = abs(current_hour-hours)*60*60
    #             diff_min = abs(current_minute-60)*60
    #             seconds = diff_min + diff_hour
    #             #Await, ibid. 
    #             print(seconds)

    #             await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {time} hours.")
    #             await asyncio.sleep(seconds)
    #             await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {time} hours.")


    #         else:
    #             # Get the difference of minutes from 60. e.g., from 21:55 -> 22:00 is 5 minutes. 
    #             diff_hour = abs(current_hour-24)*60*60
    #             # diff_hour = 0

    #             diff_min = abs(current_minute-minutes)*60
    #             seconds = diff_min + diff_hour
    #             print(seconds)
    #             await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {time} hours.")
    #             await asyncio.sleep(seconds)
    #             await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {time} hours.")



    #     else: 
    #         diff_hour = abs(current_hour-hours)*60*60
    #         diff_min = abs(current_minute-minutes)*60
    #         seconds = diff_min + diff_hour
    #         print(seconds)
    #         await message.channel.send(f"Alright, I will remind you that, and I quote, \"{reminder}\" at {time} hours.")
    #         await asyncio.sleep(seconds)
    #         await user.send(f"Hi, you asked me to remind you that, and I quote, \"{reminder}\" at {time} hours.")

