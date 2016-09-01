"""Retreive a Google Image Search result."""

import os
import re
import requests
from helpers import image

try:
    key = os.environ['GOOGLE_API_KEY']
    engine_id = os.environ['GOOGLE_ENGINE_ID']
    image_search_enabled = True
except KeyError:
    image_search_enabled = False


def setup():
    """Register the google image search plugin."""
    return {'regex': "^image", 'act_on_event': 'message'}


def run(msg):
    """Return the first image on google for a given search term."""
    if image_search_enabled:
        message = re.match('^(image) (.*)', msg['text'], re.IGNORECASE)
        searchterm = message.group(2)
        print("Image search for: ", searchterm)
        searchurl = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + engine_id + "&searchType=image&q=" + searchterm
        searchresults = requests.get(searchurl)
        imageurl = searchresults.json()['items'][0]['link']
        print("Downloading & sending image: ", imageurl)
        print('')
        search_image = image.download(imageurl)

        return ({'action': 'send_photo', 'payload': search_image},)
    else:
        return ({'action': 'send_msg', 'payload': "Image search is not enabled."},)
