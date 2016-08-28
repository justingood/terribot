from helpers import image


def setup():
    """ Registers the dogdanglin plugin. """
    return {'regex': "dog danglin", 'act_on_event': 'message'}


def run(msg):
    """ Returns an image appropriate for a dog danglin afternoon. """
    dogdanglin_image = image.download('http://i.imgur.com/KwVcdsL.png')

    return ({'action': 'send_photo', 'payload': dogdanglin_image},)
