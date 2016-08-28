import requests
import re
from helpers import image


def setup():
    """ Registers frinkiac plugin. """
    return {'regex': "^simpsons\:.*", 'act_on_event': 'message'}


def run(msg):
    """ Returns an image from the frinkiac search engine. """
    message = re.match('^(simpsons\:) (.*)', msg['text'], re.IGNORECASE)
    searchterm = message.group(2)
    searchurl = "https://frinkiac.com/api/search?q=" + searchterm

    # Return first result...might want to make this configurable.
    searchresult = requests.get(searchurl).json()[0]
    print("SEARCHRESULT: ", searchresult)
    imageurl = "https://frinkiac.com/meme/" + searchresult['Episode'] + "/" + str(searchresult['Timestamp']) + ".jpg"

    print("Downloading & sending image: ", imageurl)
    print('')
    frinkiac_image = image.download(imageurl)

    # Initialize the first return value tuple with the image itself - we'll add the subtitles after
    results = ({'action': 'send_photo', 'payload': frinkiac_image},)

    # Grab the captions and append them to the tuple
    captionurl = "https://frinkiac.com/api/caption?e=" + searchresult['Episode'] + "&t=" + str(searchresult['Timestamp'])
    captions = requests.get(captionurl)
    for subtitle in captions.json()['Subtitles']:
        results = results + ({'action': 'send_msg', 'payload': subtitle['Content']},)

    # Return our image and the associated captions
    return results
