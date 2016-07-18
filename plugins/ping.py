
''' ping: testing reachibility since 1983 '''

ping_pattern = r'''(?x) # verbose mode
^   # start of message
([bdfklmprstwyz]) # first character must be one of these letters
ing
\s* # ignore trailing whitespace
$   # end of message
'''

def setup():
    """ Registers the ping plugin. """
    return {'regex': ping_pattern, 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """ Returns a pong to a user's ping. """
    reply = re.sub(ping_pattern, r'\1ong', msg['text'], re.IGNORECASE)
    return ({'action': 'send_msg', 'payload': reply},)
