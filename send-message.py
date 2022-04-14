from distutils.command.config import config
import discord
import tweepy
import asyncio
import json
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

def checkRequirements():
    # check requirements 
    print('Checking Requirements')
    dependencies = ['discord.py', 'tweepy']
    pkg_resources.require(dependencies)

# ------------------------------------------------------------------------------------

def main():    
    # Get message with confirmation
    message = getMessage()
    
    #  Read data from settings.json file
    settings = open('settings.json', 'r')
    settingsData = json.load(settings)
    
    # Activate Discord Messanger
    SendDiscordMessages(settingsData, message)
    
    # Activate Twitter Messanger
    SendTwitterMessage(settingsData, message)
    
# ------------------------------------------------------------------------------------   
 
def getMessage():
    ## Get message from user and display message
    message = input('Enter message:')
    print('')
    print('the message is: '  + str(message))
    print ('')
    
    # Get confirmation on the message from the user
    confirm = input('Are you happy with the message? (y/n): ')     
    print('')
    
    # If confirmation is not accepted, ask for message again
    if confirm.upper() == 'Y':
        return message
    else:
        return getMessage()
    
# ------------------------------------------------------------------------------------  

def SendDiscordMessages(settingsData, message):
    # Check if discord messanger is enabled
    if(settingsData['use-flags']['discord'] == True):
        # Run discordMessanger()
        discordMessanger(settingsData, message) 
    else:
        confirm = input('Discord messanger is disabled in settings, would you like to send a message to discord? (y/n): ')
        print('')
        
        if confirm.upper() == 'Y':
            discordMessanger(settingsData, message)
        else:
            print('Discord messanger is disabled')
            print('------------------------------------------------------------------------------------')
            print('')

# ------------------------------------------------------------------------------------  

def SendTwitterMessage(settingsData, message):
    # Check if twitter messanger is enabled
    if(settingsData['use-flags']['twitter'] == True):
        # Run twitterMessanger()
        twitterMessanger(settingsData, message)
    else:
        confirm = input('Twitter messanger is disabled in settings, would you like to send a message to twitter? (y/n): ')
        print('')
        if confirm.upper() == 'Y':
            twitterMessanger(settingsData, message)
        else:
            print('Twitter messanger is disabled')
            print('------------------------------------------------------------------------------------')
            print('')
 
# ------------------------------------------------------------------------------------  

def discordMessanger(settingsData, message):
    print('')
    print('Discord Messanger')
    print('-----------------')
    print('')
    
    try:
        # Read the data from channel-ids.txt
        channelIds = open('channel-ids.json', 'r')
        channelIdsData = json.load(channelIds)
        channelIdList = channelIdsData['channel-ids']

        # Create discord client
        client = discord.Client()

        # Async method to send message to channels in the list
        async def send(message):

            try:
                # Loop through every line in the channel id list
                for channelId in channelIdList:
                    if(channelId['active'] == True):
                        # Wait until client is ready
                        await client.wait_until_ready()

                        # Get channel using channelId
                        channel = client.get_channel(id=int(channelId['id']))

                        if channel is None:
                            raise Exception(f'Channel with id {channelId.strip()} not found')
                        
                        # Print out mesage and channel name to console
                        print(f'Sending message "{message}" to channel: "{channel}"')
                        print('')

                        # Send message to channel
                        await channel.send(f'{message}')

                # Close client
                await client.close()
            
            # Catch any errors
            except Exception as ex:
                print(ex)
                print('------------------------------------------------------------------------------------')
                print('')
                
                # close client
                await client.close()
                
                # Stop execution
                return
            
        # Event when client is ready
        @client.event
        async def on_ready():
            
            # Print username to console
            print(f'Logged in as {client.user.name}')
            print('-----------------------')
            print('')

        # Create async loop to send messages
        client.loop.create_task(send(message))

        # Run client using discord access token
        client.run(settingsData['access-tokens']['discord'], bot=False)

        # Close channel id list
        channelIds.close()

        # Print completed message to console
        print('Discord Sending Done')
        print('------------------------------------------------------------------------------------')
        print('')
        
    except Exception as e:
        
        # Print error to console
        print('')
        print(e)
        print("Discord Messanger Failed")
        print('------------------------------------------------------------------------------------')
        print('')
        
        # Stop execution
        return
    
# ------------------------------------------------------------------------------------
    
def twitterMessanger(settingsData, message):
    print('')
    print('Twitter Messanger')
    print('-----------------')
    print('')
    try:
        # Create tweepy API client
        client = tweepy.Client(consumer_key=settingsData['access-tokens']['twitter']['api-key'],
                       consumer_secret=settingsData['access-tokens']['twitter']['api-secret'],
                       access_token=settingsData['access-tokens']['twitter']['access-token'],
                       access_token_secret=settingsData['access-tokens']['twitter']['access-secret'],
                       bearer_token=settingsData['access-tokens']['twitter']['bearer-token'])

        # Replace the text with whatever you want to Tweet about
        print(f'Sending tweet: "{message}" to twitter')
        print('')
        
        # Send tweet
        response = client.create_tweet(text=message)
    
        # Print completed message to console
        print('')
        print('Twitter Posting Done')
        print('------------------------------------------------------------------------------------')
        print('')
        
    # Catch any errors
    except Exception as e:
        
        # Print error to console
        print('')
        print(e)
        print("Twitter Messanger Failed")
        print('------------------------------------------------------------------------------------')
        print('')
        # Stop execution
        return
    
# ------------------------------------------------------------------------------------
checkRequirements()
main()

print('')
print('Main Ending')