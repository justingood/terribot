import random

beer_frequency = 0.02  # e.g. the percentage of matching messages turned into beer

beer_pattern = r'''(?x) # sets verbose flag
^       # match the beginning of the string
\s*     # ignore any leading whitespace
.{2,75} # match messages of 2 to 75 characters in length
\s*     # ignore any trailing whitespace
$       # match the end of the string
'''

beer_types = ['Altbier',
            'Düsseldorf Altbier',
            'Amber ale',
            'Barley wine',
            'American Barleywine',
            'Berliner weisse',
            'Bière de Garde',
            'Bitter',
            'Blonde Ale',
            'Bock',
            'Brown ale',
            'American Brown Ale',
            'California Common',
            'Cream Ale',
            'Dortmunder Export',
            'Doppelbock',
            'Dunkel',
            'Dunkelweizen',
            'Eisbock',
            'Flanders red ale',
            'Golden Ale',
            'Gose',
            'Gueuze',
            'Hefeweizen',
            'Helles',
            'India pale ale',
            'American IPA',
            'Imperial IPA',
            'Kölsch',
            'Lambic',
            'Light ale',
            'Maibock',
            'Malt liquor',
            'Mild',
            'Oktoberfestbier',
            'Old ale',
            'Oud bruin',
            'Pale ale',
            'Pilsener',
            'German-Style Pilsener',
            'Bohemian Pilsener',
            'Classic American Pilsner',
            'Porter',
            'Red ale',
            'Roggenbier',
            'Saison',
            'Scotch ale',
            'Peated Scotch Ale',
            'Stout',
            'Oatmeal Stout',
            'Schwarzbier',
            'Vienna lager',
            'Witbier',
            'Weissbier',
            'Weizenbock']


def setup():
    # Registers the beertypes plugin.
    return {'regex': beer_pattern, 'act_on_event': 'message', 'cooldown': 1}


def run(msg):
    if random.random() < beer_frequency:
        # Chooses beer type
        beer_type = (random.choice(beer_types))
        # Responds with message plus beer name type
        answer = msg['text'] + ' ' + beer_type
        return ({'action': 'send_msg', 'payload': answer},)
    else:
        # No beer this time
        return ()
