from helpers import image

urls = ['https://i.imgur.com/TePrI2O.jpg',
        'http://i.imgur.com/LjdgV8V.png',
        'https://i.imgur.com/E4qTqtR.jpg',
        'https://i.imgur.com/osXT1yI.png']


def setup():
    """ Registers the fuckthisshit plugin. """
    return {'regex': ".*fuck this shit.*", 'act_on_event': 'message'}


def run(msg):
    """ Returns a random fuckthisshit image. """
    fuckthis_result = image.download(urls)

    return ({'action': 'send_photo', 'payload': fuckthis_result},)
