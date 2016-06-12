import tempfile
import requests


def setup():
    """ Registers the dogdanglin plugin. """
    return {'regex': "dog danglin", 'act_on_event': 'message'}


def run(msg):
    """ Returns an image appropriate for a dog danglin afternoon. """
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    response = requests.get('http://i.imgur.com/KwVcdsL.png')
    image.write(response.content)
    image.close()
    return ({'action': 'send_photo', 'payload': image.name},)
