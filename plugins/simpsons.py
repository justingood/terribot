""" Searches for results on Frinkiac via the cghmc helper """

import re
from helpers import cghmc


def setup():
    """ Registers frinkiac plugin. """
    return {'regex': '(^simpsons|^simpsons animated)\:', 'act_on_event': 'message'}


def run(msg):
    """ Returns an image from the frinkiac search engine. """
    message = re.match('(^simpsons||^simpsons animated)\:(.*) ([0-9]*)', msg['text'], re.IGNORECASE)
    searchtype = message.group(1)
    searchterm = message.group(2)
    result_num = message.group(3)

    # Get search results from cghmc helper
    if searchtype.lower() == 'simpsons':
        cghmc_result = cghmc.search('frinkiac', searchterm, result_num, False)
    elif searchtype.lower() == 'simpsons anmiated':
        cghmc_result = cghmc.search('frinkiac', searchterm, result_num, True)
    else:
        print("Error, you shouldn't be here.")

    # Initialize the first return value tuple with the image itself - we'll add the subtitles after
    results = ({'action': 'send_photo', 'payload': cghmc_result['image']},)

    for subtitle in cghmc_result['captions'].json()['Subtitles']:
        results = results + ({'action': 'send_msg', 'payload': subtitle['Content']},)

    # Return our image and the associated captions
    return results
