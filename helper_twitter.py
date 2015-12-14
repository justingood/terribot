import configparser
import twitter
import random

# Load configuration from file
config = configparser.ConfigParser()
config.read('config.ini')

try:
    token = config.get('twitter', 'token')
    token_key = config.get('twitter', 'token_key')
    consecret = config.get('twitter', 'consecret')
    consecretkey = config.get('twitter', 'consecretkey')

    api = twitter.Twitter(auth=twitter.OAuth(token, token_key, consecret, consecretkey))
    twitter_enabled = True

except:
    twitter_enabled = False


def randomtweet(user):
    if twitter_enabled:
        return random.choice(api.statuses.user_timeline(count=200, user_id=user))['text']
    else:
        return "Sorry, I wasn't given Twitter powers..."
