def setup():
    return {'regex': "^ping.*", 'act_on_event': 'message'}


def run(msg):
    return ({'action': 'send_msg', 'payload': "pong"},)
