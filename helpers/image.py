""" Provides helper functions for image operations """

import tempfile
import random
import requests


def download(url):
    """ This helper will download and return an image from a URL (or a random image if given a list of URLs). It will return the filename to be passed to tg-cli """
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    if isinstance(url, list):
        response = requests.get(random.choice(url))
    elif isinstance(url, str):
        response = requests.get(url)
    else:
        print("Error, I can't handle downloads of a " + type(url))
    image.write(response.content)
    image.close()
    return image.name
