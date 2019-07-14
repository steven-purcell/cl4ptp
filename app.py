# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import bot
from flask import Flask, request, make_response, render_template

pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)


def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.
    Parameters
    ----------
    event_type : str
        type of event received from Slack
    slack_event : dict
        JSON response from a Slack reaction event
    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error
    """
    team_id = slack_event["team_id"]
    # ================ App Mention Events =============== #
    # When the user mentions the bot, the type of event will be app_mention
    if event_type == "app_mention":
        message = slack_event["event"]["text"]
        channel = slack_event["event"]["channel"]
        # Respond to mention
        pyBot.app_mention(message, channel)
        return make_response("Welcome Message Sent", 200,)

    # ============= Event Type Not Found! ==="test"========== #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    slack_event = request.get_json()
    print(slack_event)

    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    #       For more info: https://api.slack.com/events/url_verification
    # if "challenge" in slack_event:
    #     return make_response(slack_event["challenge"], 200, {"content_type":
    #                                                          "application/json"
    #                                                          })

    # # ============ Slack Token Verification =========== #
    # # We can verify the request is coming from Slack by checking that the
    # # verification token in the request matches our app's settings
    # if pyBot.verification != slack_event.get("token"):
    #     message = "Invalid Slack verification token: %s \npyBot has: \
    #                %s\n\n" % (slack_event["token"], pyBot.verification)
    #     # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
    #     # Slack's automatic retries during development.
    #     make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subscribed to
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)
    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(debug=True)