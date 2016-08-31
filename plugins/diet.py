""" Homer Simpson's greatest fear? """
from helpers import image


def setup():
    """ Registers the diet plugin. """
    return {'regex': "diet", 'act_on_event': 'message'}


def run(msg):
    """ Returns a scary image when talking about a diet. """
    diet_image = image.download('http://i.imgur.com/kZQDGNn.png')

    return ({'action': 'send_photo', 'payload': diet_image},)
