"""Retreive a Modern Seinfeld tweet."""

from helpers import twitter


def setup():
    """Register the modernseinfeld plugin."""
    return {'regex': "modern seinfeld", 'act_on_event': 'message'}


def run(msg):
    """Return a random tweet from the modernseinfeld account."""
    # Do some twitter stuff
    result = twitter.randomtweet(1000262514)
    if result:
        return ({'action': 'send_msg', 'payload': result},)
    else:
        return None
