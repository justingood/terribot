"""Decipher the unknown with the help of Urban Dictionary."""

import requests


def setup():
    """Register the urbandictionary plugin."""
    return {'regex': "^define.*", 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    """Return the top definition from the urbandictionary."""
    if len(msg['text'].split()) > 1:
        try:
            searchterm = msg['text'].split(' ', 1)[1]
            searchurl = "http://api.urbandictionary.com/v0/define?term=" + searchterm

            response = requests.get(searchurl)
            result = response.json()

            word = result['list'][0]['word']
            definition = result['list'][0]['definition']
            example = result['list'][0]['example']

            definitionresult = word + ": " + definition
            exampleresult = "example: " + example

            definition_to_send = {'action': 'send_msg', 'payload': definitionresult}
            example_to_send = {'action': 'send_msg', 'payload': exampleresult}

            return (definition_to_send, example_to_send)
        except Exception:
            return ({'action': 'send_msg', 'payload': "Your guess is as good as mine..."},)
    else:
        return ()
