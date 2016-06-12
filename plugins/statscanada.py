import helper_twitter


def setup():
    """ Registers the statscanada plugin. """
    return {'regex': "stats canada", 'act_on_event': 'message'}


def run(msg):
    """ Returns a random tweet from statscanada. """
    # Do some twitter stuff
    result = helper_twitter.randomtweet(701267743)
    if result:
        return ({'action': 'send_msg', 'payload': result},)
    else:
        return None
