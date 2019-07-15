# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the cl4p-tp app
"""
import subprocess
from slackclient import SlackClient
import requests
import json
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# ENV VAR test statement
# print(CLIENT_ID)
# print(CLIENT_SECRET)
# print(VERIFICATION_TOKEN)
# print(SLACK_BOT_TOKEN)

# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistent memory store.
authed_teams = {}


class Bot(object):
    """ Instantiates a Bot object to handle Slack onboarding interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.name = "cl4ptp"
        self.emoji = ":robot_face:"
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": CLIENT_ID,
                      "client_secret": CLIENT_SECRET,
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = VERIFICATION_TOKEN

        # NOTE: Python-slack requires a client connection to generate
        # an OAuth token. We can connect to the client without authenticating
        # by passing an empty string as a token and then reinstantiating the
        # client with a valid OAuth token once we have one.
        self.client = SlackClient(SLACK_BOT_TOKEN)
        # We'll use this dictionary to store the state of each message object.
        # In a production environment you'll likely want to store this more
        # persistently in  a database.
        self.messages = {}


    def app_mention(self, message, channel):
        if "joke" in str(message).lower():
            url     = 'https://icanhazdadjoke.com/slack'
            payload = {"Accept": "text/plain"}
            headers = {}
            res = requests.get(url, data=payload, headers=headers)
            joke = res.content
            joke = json.loads(joke.decode("utf-8"))
            joke = joke['attachments'][0]['fallback']
            

        self.client.api_call("chat.postMessage",
                            channel=channel,
                            text=str(joke))
