""" An attempt to protect terribot from the inevitable abuse. """

from helpers import image

url = ['http://i.imgur.com/WvxdOOL.jpg',
       'http://i.imgur.com/cqC5Tpu.jpg',
       'http://i.imgur.com/tEGzyzZ.gif',
       'http://i.imgur.com/PpBCHaw.jpg',
       'http://i.imgur.com/GrwH5k7.jpg',
       'http://i.imgur.com/lhQtQ3P.jpg',
       'http://i.imgur.com/ZqNlQTc.jpg',
       'http://i.imgur.com/i64RTDP.jpg']


def setup():
    """ Registers the self defense plugin. """
    return {'regex': "fuck.*(off|you).*ED", 'act_on_event': 'message'}


def run(msg):
    """ Returns a random image when ED is insulted. """
    selfdefense_image = image.download(url)

    return ({'action': 'send_photo', 'payload': selfdefense_image},)
