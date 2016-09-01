"""Retreive a 100% true fact about Canada."""

from helpers import twitter


def setup():
    """Register the statscanada plugin."""
    return {'regex': "stats canada", 'act_on_event': 'message'}


def run(msg):
    """Return a random tweet from statscanada."""
    # Do some twitter stuff
    result = twitter.randomtweet(701267743)
    if result:
        return ({'action': 'send_msg', 'payload': result},)
    else:
        return None
