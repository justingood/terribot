""" Searches for results on Morbotron via the cghmc helper """

import re
from helpers import cghmc


def setup():
    """ Registers frinkiac plugin. """
    return {'regex': '(^futurama|^futurama animated)\:', 'act_on_event': 'message'}


def run(msg):
    """ Returns an image from the frinkiac search engine. """
    message = re.match('(^futurama|^futurama animated)\:(.*) ([0-9]*)', msg['text'], re.IGNORECASE)
    searchtype = message.group(1)
    searchterm = message.group(2)
    result_num = message.group(3)
    if not result_num:
        result_num = 1

    # Get search results from cghmc helper
    if searchtype.lower() == 'futurama':
        morbo_result = cghmc.search('morbotron', searchterm, result_num, False)
    elif searchtype.lower() == 'futurama animated':
        morbo_result = cghmc.search('morbotron', searchterm, result_num, True)
    else:
        print("Puny Earthling, you shouldn't be here!")

    # Initialize the first return value tuple with the image itself - we'll add the subtitles after
    results = ({'action': 'send_photo', 'payload': morbo_result['image']},)

    for subtitle in morbo_result['captions'].json()['Subtitles']:
        results = results + ({'action': 'send_msg', 'payload': subtitle['Content']},)

    # Return our image and the associated captions
    return results
