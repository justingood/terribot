"""Search for results on Frinkiac via the cghmc helper."""

import re
from helpers import cghmc


def setup():
    """Register frinkiac plugin."""
    return {'regex': '(^simpsons|^simpsons animated)\:', 'act_on_event': 'message'}


def run(msg):
    """Return an image from the frinkiac search engine."""
    simpsons_pattern = r'''(?ix)
    ^       # start of string
    (simpsons|simpsons\ animated):   # command, colon
    \s*     # optional space
    (.*?)   # search term (non-greedy match to allow for optional number)
    \s*     # optional space
    ([0-9]+)?   # optional number
    \s*     # optional space
    $       # end of string
    '''
    message = re.match(simpsons_pattern, msg['text'], re.IGNORECASE)
    searchtype = message.group(1)
    searchterm = message.group(2)
    result_num = message.group(3)
    if not result_num:
        result_num = 1

    # Get search results from cghmc helper
    if searchtype.lower() == 'simpsons':
        frink_result = cghmc.search('frinkiac', searchterm, result_num, False)
    elif searchtype.lower() == 'simpsons animated':
        frink_result = cghmc.search('frinkiac', searchterm, result_num, True)
    else:
        print("According to the gas chromatograph, the secret ingredient is...Love?! Who's been screwing with this thing?")

    # Initialize the first return value tuple with the image itself - we'll add the subtitles after
    results = ({'action': 'send_photo', 'payload': frink_result['image']},)

    for subtitle in frink_result['captions'].json()['Subtitles']:
        results = results + ({'action': 'send_msg', 'payload': subtitle['Content']},)

    # Return our image and the associated captions
    return results
