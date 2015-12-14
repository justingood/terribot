import helper_twitter


def setup():
    return {'regex': "modern seinfeld", 'act_on_event': 'message'}


def run(msg):
    # Do some twitter stuff
    result = helper_twitter.randomtweet(1000262514)
    if result:
        return ({'action': 'send_msg', 'payload': result},)
    else:
        return None
