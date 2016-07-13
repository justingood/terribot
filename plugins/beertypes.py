import random

beer_types= ['Altbier',
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

# We'll pad this with extra empty data so we only sporadically comment
while len(beer_types) < 200:
    beer_types.append('')

def setup():
    #Registers the beertypes plugin.
    return {'regex': "^.{0,75}", 'act_on_event': 'message', 'cooldown': 1}


def run(msg):
    #Chooses beer type
    beer_type = (random.choice(beer_types))
    #If beer type is blank option (sporadic comment logic)
    if beer_type == '':
        return ()
    else:
        #Responds with message plus beer name type
        answer = msg['text'] + ' ' + beer_type
    return ({'action': 'send_msg', 'payload': answer},)
