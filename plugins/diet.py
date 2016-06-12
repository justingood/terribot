import tempfile
import requests


def setup():
    """ Registers the diet plugin. """
    return {'regex': "diet", 'act_on_event': 'message'}


def run(msg):
    """ Returns a scary image when talking about a diet. """
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    response = requests.get('http://i.imgur.com/kZQDGNn.png')
    image.write(response.content)
    image.close()
    return ({'action': 'send_photo', 'payload': image.name},)
