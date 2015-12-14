import tempfile
import random
import requests

urls = ['https://i.imgur.com/TePrI2O.jpg',
        'http://i.imgur.com/LjdgV8V.png',
        'https://i.imgur.com/E4qTqtR.jpg',
        'https://i.imgur.com/osXT1yI.png']


def setup():
    return {'regex': ".*fuck this shit.*", 'act_on_event': 'message'}


def run(msg):
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    response = requests.get(random.choice(urls))
    image.write(response.content)
    image.close()
    return ({'action': 'send_photo', 'payload': image.name},)
