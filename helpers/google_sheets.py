""" Common methods for interacting with Google Sheets. """
import os
import requests
import random

try:
    api_key = os.environ['GOOGLE_API_KEY']
    sheets_enabled = True
except KeyError:
    sheets_enabled = False


def random_line(sheet_id):
    """ Returns a random line from a given Google Sheets ID. """
    if sheets_enabled:
        sheets_url = "https://sheets.googleapis.com/v4/spreadsheets/" + sheet_id + "/values/!A1:A500?key=" + api_key
        result = requests.get(sheets_url).json()

        return random.choice(result['values'])[0]
    else:
        return "Sorry, I wasn't given the power to view Google Sheets..."
