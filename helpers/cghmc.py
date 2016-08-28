""" Searches sites on a cghmc site (Frinkiac/Morbotron) and returns images and quotes """

import requests
from helpers import image


def frinkiac(searchterm):
    """ Searches frinkiac for a given search string and returns a dictionary including the image & captions """

    searchurl = "https://frinkiac.com/api/search?q=" + searchterm
    # Return first result...might want to make this configurable.
    searchresult = requests.get(searchurl).json()[0]
    imageurl = "https://frinkiac.com/meme/" + searchresult['Episode'] + "/" + str(searchresult['Timestamp']) + ".jpg"
    frinkiac_static_image = image.download(imageurl)

    # Grab the captions and append them to the tuple
    captionurl = "https://frinkiac.com/api/caption?e=" + searchresult['Episode'] + "&t=" + str(searchresult['Timestamp'])
    captions = requests.get(captionurl)

    # Create dictionary with results to return
    packed_result = {'image': frinkiac_static_image, 'captions': captions}

    return packed_result
