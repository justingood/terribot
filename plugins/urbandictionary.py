import json
import requests


def setup():
    return {'regex': "^define.*", 'act_on_event': 'message', 'cooldown': 10}


def run(msg):
    if len(msg['text'].split()) > 1:
        try:
            searchterm = msg['text'].split(' ', 1)[1]
            searchurl = "http://api.urbandictionary.com/v0/define?term=" + searchterm

            response = requests.get(searchurl)
            result = response.json()

            word = json.dumps(result['list'][0]['word'])
            definition = json.dumps(result['list'][0]['definition'])
            example = json.dumps(result['list'][0]['example'])

            definitionresult = str(word) + ": " + str(definition)
            exampleresult = "example: " + str(example)

            definition_to_send = {'action': 'send_msg', 'payload': definitionresult}
            example_to_send = {'action': 'send_msg', 'payload': exampleresult}

            return (definition_to_send, example_to_send)
        except:
            return ({'action': 'send_msg', 'payload': "Your guess is as good as mine..."},)
    else:
        return ()
