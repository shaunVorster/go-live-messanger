# go-live-messanger Setup

## Discord

To set up discord you will need your discord API key. To find your key, follow this guide below:
https://www.online-tech-tips.com/computer-tips/what-is-a-discord-token-and-how-to-get-one/

To find your channel id's, do the following:

How to enable Developer Mode in Discord
* Click on ‘User Settings’ (the gear icon next to your Discord avatar)
* In the left sidebar, click on ‘Advanced’ > Click on the ‘Developer Mode’ toggle to turn it on

How to find your channel Id
* To find the Channel ID, right-click on the required channel name in the left sidebar and click on ‘Copy ID’.
* Paste each channel id a new line in the channel-id

## Twitter

You will need to apply for a twitter deveopment account: https://developer.twitter.com

* Once you have signed up the development account. You will need to elevate your permission level.
* Click on the project name (Should be "Project 1") on your dashboard.
* Under the Access area, look for the "View Detailed features" link.
* Here you must apply for elevated access.

Then you can go back to the project and add an application. That will allow you to generate your keys.
Make sure to generate:
* Consumer Keys
* Authentication token
* Access token and secret

## Settings.json

* Rename the setting (Blank).json to settings.json
* Open the file in a text editor and provide all the required access tokens
* Enable in the use-flags section, the services you want to use by changing the value from "false" to "true"
* Save and close the file

## send-message.py
* Make sure that python is installed on your system
* Make sure that all dependencies are installed
  * discord.py (pip install discord.py)
  * tweepy (pip install tweepy)
* Call the script by opening a terminal in the folder and running "python3 send-message.p" and follow the promts

You should now see the message on your discord channels /  twitter feed.
If there are any errors, the terminal will show a failure message with an exception message.