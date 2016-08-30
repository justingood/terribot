""" Searches sites on a cghmc site (Frinkiac/Morbotron) and returns images and quotes """

import requests
from helpers import image


def search(site, searchterm, number=1, animated=False):
    """ Searches frinkiac for a given search string and returns a dictionary including the image & captions """
    if site == 'frinkiac':
        siteurl = "https://frinkiac.com"
    elif site == 'morbotron':
        siteurl = "https://morbotron.com"
    else:
        print("CGHMC failed. You need to choose Frinkiac or Morbotron as the site")

    searchurl = siteurl + "/api/search?q=" + searchterm
    # Return specific result number (subract one because it's zero-indexed)
    result_number = int(number) - 1
    searchresult = requests.get(searchurl).json()[result_number]

    if animated:
        # Create & send a 2 second GIF
        imageurl = siteurl + "/gif/" + searchresult['Episode'] + "/" + str(searchresult['Timestamp']) + "/" + str(int(searchresult['Timestamp']) + 2000) + ".gif"
        frinkiac_image = image.download(imageurl, '.gif')
    elif not animated:
        imageurl = siteurl + "/meme/" + searchresult['Episode'] + "/" + str(searchresult['Timestamp']) + ".jpg"
        frinkiac_image = image.download(imageurl)

    # Grab the captions and append them to the tuple
    captionurl = siteurl + "/api/caption?e=" + searchresult['Episode'] + "&t=" + str(searchresult['Timestamp'])
    captions = requests.get(captionurl)

    # Create dictionary with results to return
    packed_result = {'image': frinkiac_image, 'captions': captions}

    return packed_result
