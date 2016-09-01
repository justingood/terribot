"""Check if terribot is responding."""


def setup():
    """Register the ping plugin."""
    return {'regex': "^ping.*", 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """Return a pong to a user's ping."""
    return ({'action': 'send_msg', 'payload': "pong"},)
