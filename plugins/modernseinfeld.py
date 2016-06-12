import helper_twitter


def setup():
    """ Registers the modernseinfeld plugin. """
    return {'regex': "modern seinfeld", 'act_on_event': 'message'}


def run(msg):
    """ Returns a random tweet from the modernseinfeld account. """
    # Do some twitter stuff
    result = helper_twitter.randomtweet(1000262514)
    if result:
        return ({'action': 'send_msg', 'payload': result},)
    else:
        return None
