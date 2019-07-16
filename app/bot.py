# -*- coding: utf-8 -*-
"""
Python Slack Bot class for use with the cl4p-tp app
"""
import subprocess
# v2
import slack
import requests
import json
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

class Bot(object):
    """ Instantiates a Bot object to handle Slack interactions."""
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
        # v2
        self.client = slack.WebClient(token=SLACK_BOT_TOKEN)

    def app_mention(self, message, channel):
        if "joke" in str(message).lower():
            url     = 'https://icanhazdadjoke.com/slack'
            payload = {"Accept": "text/plain"}
            headers = {}
            res = requests.get(url, data=payload, headers=headers)
            joke = res.content
            joke = json.loads(joke.decode("utf-8"))
            joke = joke['attachments'][0]['fallback']

            self.client.chat_postMessage(channel=channel,
                                    text=str(joke))

        else:
            self.client.chat_postMessage(channel=channel,
                                    text="Huh? Wha?!")