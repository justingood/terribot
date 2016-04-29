import tempfile
import requests
import re

def setup():
    return {'regex': "^frinkiac.*", 'act_on_event': 'message'}


def run(msg):
    if image_search_enabled:
        image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        message = re.match('^(frinkiac) (.*)', msg['text'], re.IGNORECASE)
        searchterm = message.group(2)
        print("Image search for: ", searchterm)
        searchurl = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + engine_id + "&searchType=image&q=" + searchterm
        searchresults = requests.get(searchurl)
        imageurl = searchresults.json()['items'][0]['link']
        print("Downloading & sending image: ", imageurl)
        response = requests.get(imageurl)
        image.write(response.content)
        image.close()
        print('')
        return ({'action': 'send_photo', 'payload': image.name},)
    else:
        return ({'action': 'send_msg', 'payload': "Image search is not enabled."},)

def run(msg):
    image = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    message = re.match('^(frinkiac) (.*)', msg['text'], re.IGNORECASE)
    searchterm = message.group(2)
    searchurl = "https://frinkiac.com/api/search?q=" + searchterm
    searchresults = requests.get(searchurl)
    print searchresults
