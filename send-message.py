import discord
import tweepy
import praw
import asyncio
import json
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def checkRequirements():
    # check requirements
    print('Checking Requirements')
    dependencies = ['discord.py', 'tweepy', 'praw']
    pkg_resources.require(dependencies)

# ------------------------------------------------------------------------------------


def main():
    # Get message with confirmation
    message = getTextWithConfirmation("Enter message")

    #  Read data from settings.json file
    settings = open('settings.json', 'r')
    settingsData = json.load(settings)

    # Activate Discord Messanger
    SendDiscordMessages(settingsData, message)

    # Activate Twitter Messanger
    SendTwitterMessage(settingsData, message)

    # Activate Reddit Messanger
    SendRedditMessage(settingsData, message)

# ------------------------------------------------------------------------------------


def getTextWithConfirmation(inputMessage):
    # Get message from user and display message
    message = input(f'{inputMessage}: ')
    print('')
    print('the text is: ' + str(message))
    print('')

    # Get confirmation on the message from the user
    confirm = input('Are you happy with the text? (y/n): ')
    print('')

    # If confirmation is not accepted, ask for message again
    if confirm.upper() == 'Y':
        return message
    else:
        return getTextWithConfirmation(inputMessage)

# ------------------------------------------------------------------------------------


def SendDiscordMessages(settingsData, message):
    # Check if discord messanger is enabled
    if(settingsData['use-flags']['discord'] == True):
        # Run discordMessanger()
        discordMessanger(settingsData, message)
    else:
        confirm = input(
            'Discord messanger is disabled in settings, would you like to send a message to discord? (y/n): ')
        print('')

        if confirm.upper() == 'Y':
            discordMessanger(settingsData, message)
        else:
            print('Discord messanger is disabled')
            print(
                '------------------------------------------------------------------------------------')
            print('')

# ------------------------------------------------------------------------------------


def SendTwitterMessage(settingsData, message):
    # Check if twitter messanger is enabled
    if(settingsData['use-flags']['twitter'] == True):
        # Run twitterMessanger()
        twitterMessanger(settingsData, message)
    else:
        confirm = input(
            'Twitter messanger is disabled in settings, would you like to send a message to twitter? (y/n): ')
        print('')
        if confirm.upper() == 'Y':
            twitterMessanger(settingsData, message)
        else:
            print('Twitter messanger is disabled')
            print(
                '------------------------------------------------------------------------------------')
            print('')

# ------------------------------------------------------------------------------------


def SendRedditMessage(settingsData, message):
    # Check if reddit messanger is enabled
    if(settingsData['use-flags']['reddit'] == True):
        # Run redditMessanger()
        redditMessanger(settingsData, message)
    else:
        confirm = input(
            'Reddit messanger is disabled in settings, would you like to send a message to reddit? (y/n): ')
        print('')
        if confirm.upper() == 'Y':
            redditMessanger(settingsData, message)
        else:
            print('Reddit messanger is disabled')
            print(
                '------------------------------------------------------------------------------------')
            print('')

# ------------------------------------------------------------------------------------


def discordMessanger(settingsData, message):
    print('')
    print('Discord Messanger')
    print('-----------------')
    print('')

    try:
        # Read the discord channel ids from channel-ids.json
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
                            raise Exception(
                                f'Channel with id {channelId.strip()} not found')

                        # Print out mesage and channel name to console
                        print(
                            f'Sending message "{message}" to channel: "{channel}"')
                        print('')

                        # Send message to channel
                        await channel.send(f'{message}')

                # Close client
                await client.close()

            # Catch any errors
            except Exception as ex:
                print(ex)
                print(
                    '------------------------------------------------------------------------------------')
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
        client.run(settingsData['access-tokens']
                   ['discord']['api-key'], bot=False)

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


def redditMessanger(settingsData, message):
    print('')
    print('Reddit Messanger')
    print('-----------------')
    print('')

    try:
        # Read the reddit subreddits from channel-ids.json
        channelIds = open('channel-ids.json', 'r')
        subredditData = json.load(channelIds)
        subredditList = subredditData['subreddit-names']

        # Create reddit API client
        client = praw.Reddit(client_id=settingsData['access-tokens']['reddit']['client-id'],
                             client_secret=settingsData['access-tokens']['reddit']['client-secret'],
                             user_agent=settingsData['access-tokens']['reddit']['user-agent'],
                             redirect_uri=settingsData['access-tokens']['reddit']['redirect-uri'],
                             refresh_token=settingsData['access-tokens']['reddit']['refresh-token'])

        # Loop through every subreddit in the subreddit list
        for sub in subredditList:

            # Check if the subreddit is active
            if(sub['active'] == True):

                # Initialize the subreddit to a variable
                subreddit = client.subreddit(sub['name'])

                # Set flair-id to none
                flair_id = ''

                # If there is no saved flair-id in subreddit config
                if(sub['flair-id'] == ""):

                    # List all flairs in the subreddit
                    flairs = list(
                        subreddit.flair.link_templates.user_selectable())

                    # Loop through every flair in the list
                    for flair in flairs:

                        # Check if the flair_text is the same as the flair-text in subreddit config
                        if(flair['flair_text'] == sub['flair-text']):

                            # If they match, set the flair_id variable and exit
                            flair_id = flair['flair_template_id']
                            break
                else:
                    # Retrieve the saved flair-id from the subreddit config
                    flair_id = sub['flair-id']

                # Enter a title for the post
                title = getTextWithConfirmation("Enter a title for the post: ")

                # Set client validation on submit to true
                client.validate_on_submit = True

                # Check if the flair_id has been set
                if (flair_id == ""):

                    print(
                        f'Sending message "{message}" with title "{title}" to subreddit: "{sub["name"]}" without flair')
                    # If not, submit without the flair
                    subreddit.submit(title, selftext=message)
                else:
                    print(
                        f'Sending message "{message}" with title "{title}" to subreddit: "{sub["name"]}" with flair text "{sub["flair-text"]}" and flair id "{flair_id}"')
                    # If it has, submit with the flair
                    subreddit.submit(title, selftext=message,
                                     flair_id=flair_id)

        # Print completed message to console
        print('')
        print('Reddit Posting Done')
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
