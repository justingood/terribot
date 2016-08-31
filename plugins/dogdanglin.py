"""Supply the appropriate Simpsons reference."""

from helpers import image


def setup():
    """Register the dogdanglin plugin."""
    return {'regex': "dog danglin", 'act_on_event': 'message'}


def run(msg):
    """Return an image appropriate for a dog danglin afternoon."""
    dogdanglin_image = image.download('http://i.imgur.com/KwVcdsL.png')

    return ({'action': 'send_photo', 'payload': dogdanglin_image},)
