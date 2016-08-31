""" https://www.youtube.com/watch?v=vRIbogQPKws """

from helpers import image


def setup():
    """ Registers the up yours plugin. """
    return {'regex': "up yours", 'act_on_event': 'message'}


def run(msg):
    """ Returns the upyours image. """
    upyours_image = image.download('http://i.imgur.com/am5PDx6.jpg')

    return ({'action': 'send_photo', 'payload': upyours_image},)
