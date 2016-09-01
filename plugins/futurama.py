"""Search for results on Morbotron via the cghmc helper."""

import re
from helpers import cghmc


def setup():
    """Register frinkiac plugin."""
    return {'regex': '(^futurama|^futurama animated)\:', 'act_on_event': 'message'}


def run(msg):
    """Return an image from the morbotron search engine."""
    futurama_pattern = r'''(?ix)
    ^       # start of string
    (futurama|futurama\ animated):   # command, colon
    \s*     # optional space
    (.*?)   # search term (non-greedy match to allow for optional number)
    \s*     # optional space
    ([0-9]+)?   # optional number
    \s*     # optional space
    $       # end of string
    '''
    message = re.match(futurama_pattern, msg['text'], re.IGNORECASE)
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
