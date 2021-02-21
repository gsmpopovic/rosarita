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

    if len(client.voice_clients) == 0:
        return await channel.connect() 

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

                return voiceclient
                # return 0

            else:

                print("We're not already connected, so let's try to connect.")
                    
                #02/19/21
                #Get the VoiceClient to which the bot will be connecting. 
                # This was really annoying to figure out. 

                try: 

                    voiceclient = await channel.connect()

                    return voiceclient

                # I would have continued in this vein if I were aware of some 
                # means by which I can auto-connect a user to a voice channel. 
                # print(message.author.voice)
                # await message.author.move_to(channel)

                except:

                    print("Error upon trying to connect to VC. Either user isn't in a voice channel, or R is already in that voice channel.")

                    #This is just a general error

                    return 0

                    # voiceclient.disconnect()

    return