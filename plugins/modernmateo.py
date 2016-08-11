import os
from helpers import google_sheets

try:
    key = os.environ['GOOGLE_API_KEY']
    # MODERN_MATEO_ID should be a Google Sheets ID
    mateo_id = os.environ['MODERN_MATEO_ID']
    modern_mateo_enabled = True
except:
    modern_mateo_enabled = False


def setup():
    """ Registers the modern mateo plugin. """
    return {'regex': "^modern mateo", 'act_on_event': 'message'}


def run(msg):
    """ Returns the first image on google for a given search term. """
    if modern_mateo_enabled:
        awesome_mateo_plot = google_sheets.random_line(mateo_id)
        if awesome_mateo_plot:
            return ({'action': 'send_msg', 'payload': awesome_mateo_plot},)
        else:
            return None
    else:
        return ({'action': 'send_msg', 'payload': "Mateo is not enabled."},)
