import tempfile
import requests
import re
from urimagic import percent_encode

def setup():
    """ Registers frinkiac plugin. """
    return {'regex': "^frink.*", 'act_on_event': 'message'}

def run(msg):
    """ Returns an image from the frinkiac search engine. """
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    message = re.match('^(frink) (.*)', msg['text'], re.IGNORECASE)
    searchterm = message.group(2)

    searchurl = "https://frinkiac.com/api/search?q=" + percent_encode(searchterm)
    # Return first result...might want to make this configurable.
    searchresult = requests.get(searchurl).json()[0]
    imageurl = "https://frinkiac.com/meme/" + searchresult['Episode'] + "/" + str(searchresult['Timestamp']) + ".jpg"

    print("Downloading & sending image: ", imageurl)
    response = requests.get(imageurl)
    image.write(response.content)
    image.close()
    print('')
    return ({'action': 'send_photo', 'payload': image.name},)
