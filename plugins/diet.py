"""Provide an opinion when diets are mentioned."""

from helpers import image


def setup():
    """Register the diet plugin."""
    return {'regex': "diet", 'act_on_event': 'message'}


def run(msg):
    """Return a scary image when talking about a diet."""
    diet_image = image.download('http://i.imgur.com/kZQDGNn.png')

    return ({'action': 'send_photo', 'payload': diet_image},)
