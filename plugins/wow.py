""" Such cool. Much amaze. So sarcasm. Wow. """

from helpers import image

url = ['http://i.imgur.com/f07DJ1R.png',
       'http://i.imgur.com/yXAnrTi.jpg',
       'http://i.imgur.com/TitHeo5.jpg',
       'http://i.imgur.com/wNu8lSl.png',
       'http://i.imgur.com/5RQUwXF.gif',
       'http://i.imgur.com/2tH0Cb1.png',
       'http://i.imgur.com/XHk9NQw.jpg',
       'http://i.imgur.com/LNcbRn2.jpg',
       'http://i.imgur.com/wnvzgiW.jpg']


def setup():
    """ Registers the wow plugin. """
    return {'regex': "wow", 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """ Returns wow images. """
    wow_image = image.download(url)

    return ({'action': 'send_photo', 'payload': wow_image},)
