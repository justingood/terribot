""" Searches for results on Frinkiac via the cghmc helper """

import re
from helpers import cghmc


def setup():
    """ Registers frinkiac plugin. """
    return {'regex': "^simpsons\:.*", 'act_on_event': 'message'}


def run(msg):
    """ Returns an image from the frinkiac search engine. """
    message = re.match('^(simpsons\:) (.*)', msg['text'], re.IGNORECASE)
    searchterm = message.group(2)

    # Get search results from cghmc helper
    frinkiac = cghmc.frinkiac(searchterm)

    # Initialize the first return value tuple with the image itself - we'll add the subtitles after
    results = ({'action': 'send_photo', 'payload': frinkiac['image']},)

    for subtitle in frinkiac['captions'].json()['Subtitles']:
        results = results + ({'action': 'send_msg', 'payload': subtitle['Content']},)

    # Return our image and the associated captions
    return results
