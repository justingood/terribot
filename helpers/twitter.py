"""Provide helper methods for interacting with Twitter."""

import os
import random
import twitter

try:
    token = os.environ['TWITTER_TOKEN']
    token_secret = os.environ['TWITTER_TOKEN_SECRET']
    consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
    consumer_key = os.environ['TWITTER_CONSUMER_KEY']

    api = twitter.Twitter(auth=twitter.OAuth(token, token_secret, consumer_key, consumer_secret))
    twitter_enabled = True

except Exception:
    twitter_enabled = False


def randomtweet(user):
    """Return a random tweet from a given user."""
    if twitter_enabled:
        return random.choice(api.statuses.user_timeline(count=200, user_id=user))['text']
    else:
        return "Sorry, I wasn't given Twitter powers..."
