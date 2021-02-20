#02/19/21
# I had to create a function because I was getting an annoying scope error with try-except
# and did not want to create a global variable 
async def connect_to_voice(message, client):

    # This would be to find a particular channel based on name. 
    # channel = utils.find(lambda x: x.name == 'music', message.guild.channels)
    # print(channel)

    # This will raise the exception if our bot is already in a specific voice channel 

    channel = message.author.voice.channel
    print(channel)
    #voiceclient = await voice_client.change_voice_state(channel)

    # A list of the guild's voice channels
    voice_channel_list = message.guild.voice_channels

    if len(client.voice_clients) == 0:
        return await channel.connect() 

    # A list of the bot's voiceclients. These are objects so we have to access their attributes. 
    for voiceclient in client.voice_clients:
        
        for vc in voice_channel_list:
            print(voiceclient)
            print(vc)
            # print(f"voice channel {vc}")
            # print(f"voice client {voiceclient.channel}")


            if channel == voiceclient.channel: 

                await message.channel.send("I'm already connected")

                return 0

            else:

                print("but the fucntions >>>>>>")
                    
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

                    return voiceclient

                    # voiceclient.disconnect()

    return